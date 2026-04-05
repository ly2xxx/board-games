"""
Splendor - Core Game Data
90 Development Cards + 10 Nobles
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional
import random

class GemColor(Enum):
    EMERALD = "emerald"      # Green
    DIAMOND = "diamond"      # White
    SAPPHIRE = "sapphire"    # Blue
    ONYX = "onyx"            # Black
    RUBY = "ruby"            # Red
    GOLD = "gold"            # Yellow (joker)

# Noble tiles (10 total, each worth 3 points)
NOBLES = [
    {"bonuses": {GemColor.EMERALD: 4, GemColor.DIAMOND: 4}, "points": 3},
    {"bonuses": {GemColor.SAPPHIRE: 4, GemColor.ONYX: 4}, "points": 3},
    {"bonuses": {GemColor.RUBY: 4, GemColor.EMERALD: 4}, "points": 3},
    {"bonuses": {GemColor.DIAMOND: 4, GemColor.SAPPHIRE: 4}, "points": 3},
    {"bonuses": {GemColor.ONYX: 3, GemColor.RUBY: 3, GemColor.DIAMOND: 3}, "points": 3},
    {"bonuses": {GemColor.SAPPHIRE: 3, GemColor.EMERALD: 3, GemColor.RUBY: 3}, "points": 3},
    {"bonuses": {GemColor.EMERALD: 3, GemColor.SAPPHIRE: 3, GemColor.ONYX: 3}, "points": 3},
    {"bonuses": {GemColor.DIAMOND: 3, GemColor.ONYX: 3, GemColor.RUBY: 3}, "points": 3},
    {"bonuses": {GemColor.DIAMOND: 5, GemColor.SAPPHIRE: 5}, "points": 3},
    {"bonuses": {GemColor.EMERALD: 5, GemColor.RUBY: 5}, "points": 3},
]

# Development cards: (tier, cost: {color: count}, bonus, points)
# Tier 1 (beginner) - 40 cards
TIER1_CARDS = [
    # 0-4 points cards
    {"cost": {GemColor.DIAMOND: 1}, "bonus": GemColor.DIAMOND, "points": 0},
    {"cost": {GemColor.DIAMOND: 1}, "bonus": GemColor.DIAMOND, "points": 0},
    {"cost": {GemColor.DIAMOND: 1}, "bonus": GemColor.DIAMOND, "points": 0},
    {"cost": {GemColor.SAPPHIRE: 1}, "bonus": GemColor.SAPPHIRE, "points": 0},
    {"cost": {GemColor.SAPPHIRE: 1}, "bonus": GemColor.SAPPHIRE, "points": 0},
    {"cost": {GemColor.SAPPHIRE: 1}, "bonus": GemColor.SAPPHIRE, "points": 0},
    {"cost": {GemColor.EMERALD: 1}, "bonus": GemColor.EMERALD, "points": 0},
    {"cost": {GemColor.EMERALD: 1}, "bonus": GemColor.EMERALD, "points": 0},
    {"cost": {GemColor.EMERALD: 1}, "bonus": GemColor.EMERALD, "points": 0},
    {"cost": {GemColor.RUBY: 1}, "bonus": GemColor.RUBY, "points": 0},
    {"cost": {GemColor.RUBY: 1}, "bonus": GemColor.RUBY, "points": 0},
    {"cost": {GemColor.RUBY: 1}, "bonus": GemColor.RUBY, "points": 0},
    {"cost": {GemColor.ONYX: 1}, "bonus": GemColor.ONYX, "points": 0},
    {"cost": {GemColor.ONYX: 1}, "bonus": GemColor.ONYX, "points": 0},
    {"cost": {GemColor.ONYX: 1}, "bonus": GemColor.ONYX, "points": 0},
    # 1 point cards
    {"cost": {GemColor.DIAMOND: 2, GemColor.SAPPHIRE: 1}, "bonus": GemColor.DIAMOND, "points": 1},
    {"cost": {GemColor.SAPPHIRE: 2, GemColor.EMERALD: 1}, "bonus": GemColor.SAPPHIRE, "points": 1},
    {"cost": {GemColor.EMERALD: 2, GemColor.RUBY: 1}, "bonus": GemColor.EMERALD, "points": 1},
    {"cost": {GemColor.RUBY: 2, GemColor.ONYX: 1}, "bonus": GemColor.RUBY, "points": 1},
    {"cost": {GemColor.ONYX: 2, GemColor.DIAMOND: 1}, "bonus": GemColor.ONYX, "points": 1},
    {"cost": {GemColor.DIAMOND: 2, GemColor.EMERALD: 1}, "bonus": GemColor.EMERALD, "points": 1},
    {"cost": {GemColor.SAPPHIRE: 2, GemColor.RUBY: 1}, "bonus": GemColor.RUBY, "points": 1},
    {"cost": {GemColor.EMERALD: 2, GemColor.ONYX: 1}, "bonus": GemColor.ONYX, "points": 1},
    {"cost": {GemColor.RUBY: 2, GemColor.DIAMOND: 1}, "bonus": GemColor.DIAMOND, "points": 1},
    {"cost": {GemColor.ONYX: 2, GemColor.SAPPHIRE: 1}, "bonus": GemColor.SAPPHIRE, "points": 1},
    # 2 point cards
    {"cost": {GemColor.DIAMOND: 3, GemColor.SAPPHIRE: 2}, "bonus": GemColor.ONYX, "points": 2},
    {"cost": {GemColor.SAPPHIRE: 3, GemColor.EMERALD: 2}, "bonus": GemColor.EMERALD, "points": 2},
    {"cost": {GemColor.EMERALD: 3, GemColor.RUBY: 2}, "bonus": GemColor.RUBY, "points": 2},
    {"cost": {GemColor.RUBY: 3, GemColor.ONYX: 2}, "bonus": GemColor.SAPPHIRE, "points": 2},
    {"cost": {GemColor.ONYX: 3, GemColor.DIAMOND: 2}, "bonus": GemColor.DIAMOND, "points": 2},
    {"cost": {GemColor.DIAMOND: 2, GemColor.SAPPHIRE: 2, GemColor.EMERALD: 1}, "bonus": GemColor.ONYX, "points": 2},
    {"cost": {GemColor.SAPPHIRE: 2, GemColor.EMERALD: 2, GemColor.RUBY: 1}, "bonus": GemColor.DIAMOND, "points": 2},
    {"cost": {GemColor.EMERALD: 2, GemColor.RUBY: 2, GemColor.ONYX: 1}, "bonus": GemColor.SAPPHIRE, "points": 2},
    {"cost": {GemColor.RUBY: 2, GemColor.ONYX: 2, GemColor.DIAMOND: 1}, "bonus": GemColor.EMERALD, "points": 2},
    {"cost": {GemColor.ONYX: 2, GemColor.DIAMOND: 2, GemColor.SAPPHIRE: 1}, "bonus": GemColor.RUBY, "points": 2},
    # 3 point cards
    {"cost": {GemColor.DIAMOND: 3, GemColor.SAPPHIRE: 3}, "bonus": GemColor.DIAMOND, "points": 3},
    {"cost": {GemColor.SAPPHIRE: 3, GemColor.EMERALD: 3}, "bonus": GemColor.SAPPHIRE, "points": 3},
    {"cost": {GemColor.EMERALD: 3, GemColor.RUBY: 3}, "bonus": GemColor.EMERALD, "points": 3},
    {"cost": {GemColor.RUBY: 3, GemColor.ONYX: 3}, "bonus": GemColor.RUBY, "points": 3},
    {"cost": {GemColor.ONYX: 3, GemColor.DIAMOND: 3}, "bonus": GemColor.ONYX, "points": 3},
]

# Tier 2 (intermediate) - 30 cards
TIER2_CARDS = [
    # 2-3 point cards
    {"cost": {GemColor.DIAMOND: 3, GemColor.SAPPHIRE: 2}, "bonus": GemColor.SAPPHIRE, "points": 2},
    {"cost": {GemColor.SAPPHIRE: 3, GemColor.EMERALD: 2}, "bonus": GemColor.EMERALD, "points": 2},
    {"cost": {GemColor.EMERALD: 3, GemColor.RUBY: 2}, "bonus": GemColor.RUBY, "points": 2},
    {"cost": {GemColor.RUBY: 3, GemColor.ONYX: 2}, "bonus": GemColor.ONYX, "points": 2},
    {"cost": {GemColor.ONYX: 3, GemColor.DIAMOND: 2}, "bonus": GemColor.DIAMOND, "points": 2},
    {"cost": {GemColor.DIAMOND: 4, GemColor.SAPPHIRE: 1}, "bonus": GemColor.SAPPHIRE, "points": 3},
    {"cost": {GemColor.SAPPHIRE: 4, GemColor.EMERALD: 1}, "bonus": GemColor.EMERALD, "points": 3},
    {"cost": {GemColor.EMERALD: 4, GemColor.RUBY: 1}, "bonus": GemColor.RUBY, "points": 3},
    {"cost": {GemColor.RUBY: 4, GemColor.ONYX: 1}, "bonus": GemColor.ONYX, "points": 3},
    {"cost": {GemColor.ONYX: 4, GemColor.DIAMOND: 1}, "bonus": GemColor.DIAMOND, "points": 3},
    # 4-5 point cards
    {"cost": {GemColor.DIAMOND: 4, GemColor.SAPPHIRE: 3}, "bonus": GemColor.ONYX, "points": 4},
    {"cost": {GemColor.SAPPHIRE: 4, GemColor.EMERALD: 3}, "bonus": GemColor.DIAMOND, "points": 4},
    {"cost": {GemColor.EMERALD: 4, GemColor.RUBY: 3}, "bonus": GemColor.SAPPHIRE, "points": 4},
    {"cost": {GemColor.RUBY: 4, GemColor.ONYX: 3}, "bonus": GemColor.EMERALD, "points": 4},
    {"cost": {GemColor.ONYX: 4, GemColor.DIAMOND: 3}, "bonus": GemColor.RUBY, "points": 4},
    {"cost": {GemColor.DIAMOND: 5, GemColor.SAPPHIRE: 2}, "bonus": GemColor.EMERALD, "points": 5},
    {"cost": {GemColor.SAPPHIRE: 5, GemColor.EMERALD: 2}, "bonus": GemColor.ONYX, "points": 5},
    {"cost": {GemColor.EMERALD: 5, GemColor.RUBY: 2}, "bonus": GemColor.DIAMOND, "points": 5},
    {"cost": {GemColor.RUBY: 5, GemColor.ONYX: 2}, "bonus": GemColor.SAPPHIRE, "points": 5},
    {"cost": {GemColor.ONYX: 5, GemColor.DIAMOND: 2}, "bonus": GemColor.EMERALD, "points": 5},
    # More varied
    {"cost": {GemColor.DIAMOND: 3, GemColor.SAPPHIRE: 3, GemColor.EMERALD: 1}, "bonus": GemColor.DIAMOND, "points": 3},
    {"cost": {GemColor.SAPPHIRE: 3, GemColor.EMERALD: 3, GemColor.RUBY: 1}, "bonus": GemColor.SAPPHIRE, "points": 3},
    {"cost": {GemColor.EMERALD: 3, GemColor.RUBY: 3, GemColor.ONYX: 1}, "bonus": GemColor.EMERALD, "points": 3},
    {"cost": {GemColor.RUBY: 3, GemColor.ONYX: 3, GemColor.DIAMOND: 1}, "bonus": GemColor.RUBY, "points": 3},
    {"cost": {GemColor.ONYX: 3, GemColor.DIAMOND: 3, GemColor.SAPPHIRE: 1}, "bonus": GemColor.ONYX, "points": 3},
    {"cost": {GemColor.DIAMOND: 4, GemColor.EMERALD: 4}, "bonus": GemColor.RUBY, "points": 4},
    {"cost": {GemColor.SAPPHIRE: 4, GemColor.RUBY: 4}, "bonus": GemColor.EMERALD, "points": 4},
    {"cost": {GemColor.EMERALD: 4, GemColor.ONYX: 4}, "bonus": GemColor.SAPPHIRE, "points": 4},
    {"cost": {GemColor.RUBY: 4, GemColor.DIAMOND: 4}, "bonus": GemColor.ONYX, "points": 4},
    {"cost": {GemColor.ONYX: 4, GemColor.SAPPHIRE: 4}, "bonus": GemColor.DIAMOND, "points": 4},
]

# Tier 3 (advanced) - 20 cards
TIER3_CARDS = [
    # 3-4 point cards
    {"cost": {GemColor.DIAMOND: 4, GemColor.SAPPHIRE: 4}, "bonus": GemColor.EMERALD, "points": 3},
    {"cost": {GemColor.SAPPHIRE: 4, GemColor.EMERALD: 4}, "bonus": GemColor.RUBY, "points": 3},
    {"cost": {GemColor.EMERALD: 4, GemColor.RUBY: 4}, "bonus": GemColor.ONYX, "points": 3},
    {"cost": {GemColor.RUBY: 4, GemColor.ONYX: 4}, "bonus": GemColor.DIAMOND, "points": 3},
    {"cost": {GemColor.ONYX: 4, GemColor.DIAMOND: 4}, "bonus": GemColor.SAPPHIRE, "points": 3},
    # 5 point cards
    {"cost": {GemColor.DIAMOND: 5, GemColor.SAPPHIRE: 3, GemColor.EMERALD: 2}, "bonus": GemColor.RUBY, "points": 5},
    {"cost": {GemColor.SAPPHIRE: 5, GemColor.EMERALD: 3, GemColor.RUBY: 2}, "bonus": GemColor.ONYX, "points": 5},
    {"cost": {GemColor.EMERALD: 5, GemColor.RUBY: 3, GemColor.ONYX: 2}, "bonus": GemColor.DIAMOND, "points": 5},
    {"cost": {GemColor.RUBY: 5, GemColor.ONYX: 3, GemColor.DIAMOND: 2}, "bonus": GemColor.SAPPHIRE, "points": 5},
    {"cost": {GemColor.ONYX: 5, GemColor.DIAMOND: 3, GemColor.SAPPHIRE: 2}, "bonus": GemColor.EMERALD, "points": 5},
    # 7-8 point cards
    {"cost": {GemColor.DIAMOND: 6, GemColor.SAPPHIRE: 6}, "bonus": GemColor.ONYX, "points": 7},
    {"cost": {GemColor.SAPPHIRE: 6, GemColor.EMERALD: 6}, "bonus": GemColor.DIAMOND, "points": 7},
    {"cost": {GemColor.EMERALD: 6, GemColor.RUBY: 6}, "bonus": GemColor.SAPPHIRE, "points": 7},
    {"cost": {GemColor.RUBY: 6, GemColor.ONYX: 6}, "bonus": GemColor.EMERALD, "points": 7},
    {"cost": {GemColor.ONYX: 6, GemColor.DIAMOND: 6}, "bonus": GemColor.RUBY, "points": 7},
    # 3-4 point with gold
    {"cost": {GemColor.GOLD: 3, GemColor.DIAMOND: 3, GemColor.SAPPHIRE: 3}, "bonus": GemColor.EMERALD, "points": 4},
    {"cost": {GemColor.GOLD: 3, GemColor.SAPPHIRE: 3, GemColor.EMERALD: 3}, "bonus": GemColor.RUBY, "points": 4},
    {"cost": {GemColor.GOLD: 3, GemColor.EMERALD: 3, GemColor.RUBY: 3}, "bonus": GemColor.ONYX, "points": 4},
    {"cost": {GemColor.GOLD: 3, GemColor.RUBY: 3, GemColor.ONYX: 3}, "bonus": GemColor.DIAMOND, "points": 4},
    {"cost": {GemColor.GOLD: 3, GemColor.ONYX: 3, GemColor.DIAMOND: 3}, "bonus": GemColor.SAPPHIRE, "points": 4},
]

def create_deck(tier: int) -> list[dict]:
    """Create a shuffled deck for a given tier."""
    if tier == 1:
        cards = TIER1_CARDS.copy()
    elif tier == 2:
        cards = TIER2_CARDS.copy()
    elif tier == 3:
        cards = TIER3_CARDS.copy()
    else:
        return []
    
    random.shuffle(cards)
    return cards

def get_starting_tokens(num_players: int) -> dict[GemColor, int]:
    """Get starting token counts based on player count."""
    base = 7
    if num_players == 2:
        return {
            GemColor.EMERALD: 4,
            GemColor.DIAMOND: 4,
            GemColor.SAPPHIRE: 4,
            GemColor.ONYX: 4,
            GemColor.RUBY: 4,
            GemColor.GOLD: 5,
        }
    elif num_players == 3:
        return {
            GemColor.EMERALD: 5,
            GemColor.DIAMOND: 5,
            GemColor.SAPPHIRE: 5,
            GemColor.ONYX: 5,
            GemColor.RUBY: 5,
            GemColor.GOLD: 5,
        }
    else:  # 4 players
        return {
            GemColor.EMERALD: 7,
            GemColor.DIAMOND: 7,
            GemColor.SAPPHIRE: 7,
            GemColor.ONYX: 7,
            GemColor.RUBY: 7,
            GemColor.GOLD: 5,
        }

def get_noble_count(num_players: int) -> int:
    """Get number of nobles to reveal."""
    return num_players + 1

# Colors for UI
GEM_COLORS = {
    GemColor.EMERALD: "#50C878",   # Green
    GemColor.DIAMOND: "#B9F2FF",   # White/light blue
    GemColor.SAPPHIRE: "#0F52BA",   # Blue
    GemColor.ONYX: "#1A1A1A",      # Black
    GemColor.RUBY: "#E0115F",      # Red
    GemColor.GOLD: "#FFD700",      # Gold
}
