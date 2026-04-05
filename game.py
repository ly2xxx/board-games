"""
Splendor - Game State and Logic
"""
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import random

from data import (
    GemColor, NOBLES, create_deck, get_starting_tokens, 
    get_noble_count, GEM_COLORS
)

class GamePhase(Enum):
    SETUP = "setup"
    WAITING = "waiting"  # Waiting room
    PLAY = "play"
    GAME_OVER = "game_over"

@dataclass
class Player:
    name: str
    tokens: dict[GemColor, int] = field(default_factory=dict)
    reserved_cards: list = field(default_factory=list)
    purchased_cards: list = field(default_factory=list)
    nobles: list = field(default_factory=list)
    points: int = 0
    
    def __post_init__(self):
        if not self.tokens:
            self.tokens = {c: 0 for c in GemColor}
    
    def get_bonuses(self) -> dict[GemColor, int]:
        """Calculate bonus discounts from purchased cards."""
        bonuses = {c: 0 for c in GemColor if c != GemColor.GOLD}
        for card in self.purchased_cards:
            bonus = card.get("bonus")
            if bonus and bonus in bonuses:
                bonuses[bonus] += 1
        return bonuses
    
    def get_total_points(self) -> int:
        """Total points = purchased cards + nobles."""
        card_points = sum(c.get("points", 0) for c in self.purchased_cards)
        noble_points = sum(n.get("points", 0) for n in self.nobles)
        return card_points + noble_points
    
    def get_token_count(self) -> int:
        """Total tokens held."""
        return sum(self.tokens.values())

@dataclass
class GameState:
    players: list[Player] = field(default_factory=list)
    deck1: list = field(default_factory=list)
    deck2: list = field(default_factory=list)
    deck3: list = field(default_factory=list)
    faceup1: list = field(default_factory=list)
    faceup2: list = field(default_factory=list)
    faceup3: list = field(default_factory=list)
    nobles: list = field(default_factory=list)
    bank: dict[GemColor, int] = field(default_factory=dict)
    current_player: int = 0
    phase: GamePhase = GamePhase.SETUP
    winner: Optional[str] = None
    message: str = ""
    
    def get_deck(self, tier: int) -> list:
        if tier == 1:
            return self.deck1
        elif tier == 2:
            return self.deck2
        return self.deck3
    
    def get_faceup(self, tier: int) -> list:
        if tier == 1:
            return self.faceup1
        elif tier == 2:
            return self.faceup2
        return self.faceup3
    
    def set_faceup(self, tier: int, cards: list):
        if tier == 1:
            self.faceup1 = cards
        elif tier == 2:
            self.faceup2 = cards
        else:
            self.faceup3 = cards

def init_game(player_names: list[str]) -> GameState:
    """Initialize a new game."""
    game = GameState()
    
    # Create players
    game.players = [Player(name=name) for name in player_names]
    
    # Create decks
    game.deck1 = create_deck(1)
    game.deck2 = create_deck(2)
    game.deck3 = create_deck(3)
    
    # Deal face-up cards (4 of each tier)
    game.faceup1 = [game.deck1.pop() for _ in range(4)] if game.deck1 else []
    game.faceup2 = [game.deck2.pop() for _ in range(4)] if game.deck2 else []
    game.faceup3 = [game.deck3.pop() for _ in range(4)] if game.deck3 else []
    
    # Setup nobles
    all_nobles = NOBLES.copy()
    random.shuffle(all_nobles)
    num_nobles = get_noble_count(len(player_names))
    game.nobles = all_nobles[:num_nobles]
    
    # Setup bank tokens
    game.bank = get_starting_tokens(len(player_names))
    
    game.phase = GamePhase.PLAY
    game.current_player = 0
    game.message = f"Game started! {game.players[0].name}'s turn."
    
    return game

def get_card_cost(card: dict) -> dict[GemColor, int]:
    """Parse card cost to dict."""
    cost = {}
    for color, count in card.get("cost", {}).items():
        if isinstance(color, GemColor):
            cost[color] = count
    return cost

def can_afford(player: Player, card: dict) -> bool:
    """Check if player can afford a card (considering bonuses)."""
    cost = get_card_cost(card)
    bonuses = player.get_bonuses()
    
    # Calculate required tokens after discount
    required = {}
    for color, amount in cost.items():
        if color == GemColor.GOLD:
            required[color] = amount
        else:
            discount = bonuses.get(color, 0)
            needed = max(0, amount - discount)
            if needed > 0:
                required[color] = needed
    
    # Check if player has enough
    for color, amount in required.items():
        if player.tokens.get(color, 0) < amount:
            return False
    return True

def take_different_gems(game: GameState, colors: list[GemColor]) -> str:
    """Action: Take 3 different gems."""
    player = game.players[game.current_player]
    
    # Validate
    if len(colors) != 3:
        return "Must take exactly 3 gems."
    if len(set(colors)) != 3:
        return "Gems must be different colors."
    
    for color in colors:
        if game.bank.get(color, 0) < 1:
            return f"No {color.value} gems available."
    
    # Execute
    for color in colors:
        player.tokens[color] = player.tokens.get(color, 0) + 1
        game.bank[color] = game.bank.get(color, 0) - 1
    
    return next_turn(game, f"{player.name} took 3 gems.")

def take_same_gems(game: GameState, color: GemColor) -> str:
    """Action: Take 2 gems of the same color."""
    player = game.players[game.current_player]
    
    # Validate
    if game.bank.get(color, 0) < 4:
        return f"Not enough {color.value} gems available (need 4)."
    
    # Execute
    player.tokens[color] = player.tokens.get(color, 0) + 2
    game.bank[color] = game.bank.get(color, 0) - 2
    
    return next_turn(game, f"{player.name} took 2 {color.value} gems.")

def reserve_card(game: GameState, tier: int, faceup_index: int = None) -> str:
    """Action: Reserve a card and get a gold."""
    player = game.players[game.current_player]
    
    if len(player.reserved_cards) >= 3:
        return "Cannot reserve more than 3 cards."
    
    card = None
    
    if faceup_index is not None:
        # Reserve from face-up cards
        faceup = game.get_faceup(tier)
        if faceup_index >= len(faceup):
            return "Invalid card selection."
        card = faceup.pop(faceup_index)
        
        # Replace from deck
        deck = game.get_deck(tier)
        if deck:
            faceup.append(deck.pop())
    else:
        # Reserve from deck (face down)
        deck = game.get_deck(tier)
        if not deck:
            return "No cards left in deck."
        card = deck.pop()
    
    player.reserved_cards.append(card)
    
    # Get gold if available
    if game.bank.get(GemColor.GOLD, 0) > 0:
        player.tokens[GemColor.GOLD] = player.tokens.get(GemColor.GOLD, 0) + 1
        game.bank[GemColor.GOLD] -= 1
    
    return next_turn(game, f"{player.name} reserved a card and got gold.")

def buy_card(game: GameState, card_source: str, tier: int = None, faceup_index: int = None, reserved_index: int = None) -> str:
    """Action: Buy a development card."""
    player = game.players[game.current_player]
    
    card = None
    
    if card_source == "faceup":
        # Buy from face-up
        if tier is None or faceup_index is None:
            return "Invalid purchase: must specify tier and index."
        faceup = game.get_faceup(tier)
        if faceup_index >= len(faceup):
            return "Invalid card selection."
        card = faceup.pop(faceup_index)
        
        # Replace from deck
        deck = game.get_deck(tier)
        if deck:
            faceup.append(deck.pop())
    elif card_source == "reserved":
        # Buy from reserved cards
        if reserved_index is None:
            return "Please specify which reserved card to buy."
        if not player.reserved_cards or reserved_index >= len(player.reserved_cards):
            return "No reserved card at that index."
        card = player.reserved_cards.pop(reserved_index)
    else:
        return "Invalid card source."
    
    # Check if can afford
    if not can_afford(player, card):
        return "Cannot afford this card."
    
    # Calculate cost with bonuses
    cost = get_card_cost(card)
    bonuses = player.get_bonuses()
    
    # Spend tokens
    for color, amount in cost.items():
        if color == GemColor.GOLD:
            # Gold can replace any color
            gold_used = 0
            remaining = amount
            # Use gold first
            gold_available = player.tokens.get(GemColor.GOLD, 0)
            gold_used = min(gold_available, remaining)
            player.tokens[GemColor.GOLD] -= gold_used
            remaining -= gold_used
            
            # Then use color-specific tokens
            if remaining > 0:
                player.tokens[color] = player.tokens.get(color, 0) - remaining
                game.bank[color] = game.bank.get(color, 0) + remaining
        else:
            discount = bonuses.get(color, 0)
            actual_cost = max(0, amount - discount)
            if actual_cost > 0:
                player.tokens[color] = player.tokens.get(color, 0) - actual_cost
                game.bank[color] = game.bank.get(color, 0) + actual_cost
    
    # Add card to purchased
    player.purchased_cards.append(card)
    player.points = player.get_total_points()
    
    # Check for noble visit
    check_noble_visit(game, player)
    
    # Check win condition
    if player.points >= 15:
        game.phase = GamePhase.GAME_OVER
        game.winner = player.name
        return f"{player.name} wins with {player.points} points!"
    
    game.message = f"{player.name} bought a card for {card.get('points', 0)} points."
    return next_turn(game, game.message)

def check_noble_visit(game: GameState, player: Player):
    """Check if player qualifies for any noble visits."""
    bonuses = player.get_bonuses()
    
    for noble in game.nobles[:]:  # Copy list to modify during iteration
        required = noble.get("bonuses", {})
        qualifies = True
        
        for color, amount in required.items():
            if bonuses.get(color, 0) < amount:
                qualifies = False
                break
        
        if qualifies:
            player.nobles.append(noble)
            game.nobles.remove(noble)
            player.points = player.get_total_points()
            game.message = f"{player.name} was visited by a Noble! (+3 points)"

def next_turn(game: GameState, action_msg: str = "") -> str:
    """Move to next player's turn."""
    # Check token limit
    player = game.players[game.current_player]
    discarded = []
    
    while player.get_token_count() > 10:
        # Auto-discard for POC to avoid blocking
        available = [color for color, count in player.tokens.items() if count > 0]
        if available:
            to_discard = random.choice(available)
            player.tokens[to_discard] -= 1
            game.bank[to_discard] = game.bank.get(to_discard, 0) + 1
            discarded.append(to_discard.value)
        else:
            break
            
    # Next player
    game.current_player = (game.current_player + 1) % len(game.players)
    
    msg = action_msg
    if discarded:
        msg += f" (Auto-discarded: {', '.join(discarded)})"
        
    game.message = msg + f" {game.players[game.current_player].name}'s turn."
    
    return game.message

def get_available_actions(game: GameState) -> dict:
    """Get available actions for current player."""
    player = game.players[game.current_player]
    actions = {
        "take_different": True,
        "take_same": [],
        "reserve": True,
        "buy_faceup": [],
    }
    
    # Check which colors can be taken as same (need 4+)
    for color in [GemColor.EMERALD, GemColor.DIAMOND, GemColor.SAPPHIRE, 
                   GemColor.ONYX, GemColor.RUBY]:
        if game.bank.get(color, 0) >= 4:
            actions["take_same"].append(color)
    
    # Check which face-up cards can be bought
    for tier, faceup in [(1, game.faceup1), (2, game.faceup2), (3, game.faceup3)]:
        for idx, card in enumerate(faceup):
            if can_afford(player, card):
                actions["buy_faceup"].append((tier, idx, card))
    
    return actions
