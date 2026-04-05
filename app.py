"""
Splendor Online - Streamlit App
Multiplayer support with AI players
"""
import streamlit as st
import time
import uuid
import random

from data import GemColor, GEM_COLORS
from game import (
    GameState, Player, init_game, take_different_gems, take_same_gems,
    reserve_card, buy_card, get_available_actions, GamePhase
)

# Page config
st.set_page_config(
    page_title="Splendor Online",
    page_icon="💎",
    layout="wide"
)

# ===== STYLING =====
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap');
    
    h1, h2, h3 { font-family: 'Cinzel', serif !important; color: #ffd700 !important; }
    
    .gem { width: 44px; height: 44px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: bold; font-size: 16px; border: 2px solid #333; margin: 2px; }
    .gem-s { width: 32px; height: 32px; font-size: 12px; }
    
    .card { display: inline-block; width: 115px; height: 165px; background: linear-gradient(145deg, #2a2a4a, #1a1a3a); border-radius: 10px; padding: 8px; margin: 3px; text-align: center; color: white; position: relative; }
    .card-t1 { border-left: 5px solid #cd7f32; }
    .card-t2 { border-left: 5px solid #c0c0c0; }
    .card-t3 { border-left: 5px solid #ffd700; }
    .card-pts { position: absolute; top: 5px; right: 5px; background: #ffd700; color: #000; border-radius: 50%; width: 25px; height: 25px; font-size: 12px; font-weight: bold; display: flex; align-items: center; justify-content: center; }
    .card-gem { font-size: 28px; margin: 5px 0; }
    .card-cost { font-size: 10px; color: #aaa; }
    .card-bonus { font-size: 24px; margin: 3px 0; }
    
    .noble { display: inline-block; width: 120px; height: 90px; background: linear-gradient(135deg, #ffd700, #ff8c00); border-radius: 8px; padding: 8px; margin: 3px; text-align: center; color: #000; border: 2px solid #b8860b; }
    
    .player { background: linear-gradient(145deg, #1e3a5f, #0d2137); border-radius: 12px; padding: 12px; margin: 6px 0; border: 2px solid #2a4a6f; }
    .player-active { border: 3px solid #ffd700; box-shadow: 0 0 15px rgba(255,215,0,0.3); }
    .player-name { font-size: 16px; font-weight: bold; color: #fff; }
    .player-pts { font-size: 20px; color: #ffd700; font-weight: bold; }
    
    .turn-box { background: linear-gradient(135deg, #ffd700, #ff8c00); color: #000; padding: 10px 20px; border-radius: 25px; font-weight: bold; font-size: 16px; text-align: center; animation: pulse 2s infinite; }
    @keyframes pulse { 0%,100% { box-shadow: 0 0 10px rgba(255,215,0,0.5); } 50% { box-shadow: 0 0 20px rgba(255,215,0,0.8); } }
</style>
""", unsafe_allow_html=True)

# ===== SESSION STATE =====
if 'games' not in st.session_state:
    st.session_state.games = {}
if 'current_game_id' not in st.session_state:
    st.session_state.current_game_id = None

# ===== HELPERS =====
def gem(color, c, s=""): 
    c_hex = GEM_COLORS.get(color, "#888")
    tc = "white" if color in [GemColor.SAPPHIRE, GemColor.ONYX, GemColor.EMERALD] else "black"
    return f'<div class="gem {s}" style="background:{c_hex};color:{tc};">{c}</div>'

def card(c, t):
    b, bp = c.get("bonus"), c.get("points",0)
    bh = GEM_COLORS.get(b,"#888")
    cost = " ".join([gem(col,ct) for col,ct in c.get("cost",{}).items() if isinstance(col,GemColor)])
    gem_icons = {GemColor.EMERALD:"💚",GemColor.DIAMOND:"💎",GemColor.SAPPHIRE:"💙",GemColor.ONYX:"🖤",GemColor.RUBY:"❤️",GemColor.GOLD:"🪙"}
    return f'''<div class="card card-t{t}"><div class="card-pts">{bp}</div><div class="card-gem">{gem_icons.get(b,"💎")}</div><div class="card-cost">{cost}</div><div class="card-bonus" style="color:{bh};">●</div></div>'''

def noble(n):
    bs = " ".join([gem(cnt,cnt, "gem-s") for cnt,c in n.get("bonuses",{}).items() if isinstance(cnt,GemColor)])
    return f'''<div class="noble"><div style="font-size:24px;">👑</div><div style="font-size:10px;">{bs}</div><div style="font-weight:bold;">+3</div></div>'''

def player(p, cur):
    acts = "active" if cur else ""
    bons = p.get_bonuses()
    bs = " ".join([gem(c,c, "gem-s") for c,v in bons.items() if v>0 and isinstance(c,GemColor)]).strip() or "None"
    gs = " ".join([gem(c,v) for c,v in p.tokens.items() if v>0 and isinstance(c,GemColor)])
    return f'''<div class="player {acts}"><div class="player-name">{"⭐ " if cur else ""}{p.name}</div><div class="player-pts">⭐ {p.get_total_points()} pts</div><div>{gs}</div><div style="margin-top:5px;font-size:11px;color:#888;">Bonuses: {bs}</div><div style="font-size:11px;color:#888;">📇{len(p.purchased_cards)} 👑{len(p.nobles)} 📥{len(p.reserved_cards)}</div></div>'''

# ===== AI =====
def ai_move(game):
    p = game.players[game.current_player]
    if not p.name.startswith("AI "): return ""
    
    acts = get_available_actions(game)
    
    # Try buy
    for t in [3,2,1]:
        for a in acts.get("buy_faceup",[]):
            if a[0]==t: return buy_card(game,"faceup",t,a[1])
    
    # Try reserve
    if acts.get("reserve"):
        return reserve_card(game, random.choice([1,2,3]))
    
    # Take gems
    if acts.get("take_same"):
        return take_same_gems(game, random.choice(acts["take_same"]))
    avail = [c for c in GemColor if c!=GemColor.GOLD and game.bank.get(c,0)>0]
    if len(avail)>=3:
        return take_different_gems(game, random.sample(avail,3))
    
    return "AI passes."

# ===== SCREENS =====
def lobby():
    st.markdown("# 💎 Splendor Online")
    st.markdown("### A game of Renaissance merchants")
    
    c1, c2 = st.columns([1,1])
    
    with c1:
        st.markdown("## 🎮 Create Game")
        np = st.selectbox("Players", [2,3,4], key="np")
        
        names = []
        for i in range(np):
            names.append(st.text_input(f"P{i+1}", f"Player {i+1}", key=f"pn{i}"))
        
        ai_on = st.checkbox("Add AI Bots", value=True)
        ai_cnt = 0
        if ai_on:
            ai_cnt = st.slider("AI Bots", 1, 4-np, max(1, 4-np), key="aic")
        
        if st.button("✨ Create", use_container_width=True):
            final = names + [f"AI Bot {i+1}" for i in range(ai_cnt)]
            if all(final):
                gid = str(uuid.uuid4())[:8]
                g = init_game(final)
                g.phase = GamePhase.WAITING
                st.session_state.games[gid] = g
                st.session_state.current_game_id = gid
                st.rerun()
    
    with c2:
        st.markdown("## 🔗 Join")
        jid = st.text_input("Game ID", key="jid")
        if st.button("Join", use_container_width=True):
            if jid in st.session_state.games:
                st.session_state.current_game_id = jid
                st.rerun()
            else:
                st.error("Game not found!")
        
        if st.session_state.games:
            st.markdown("### Active")
            for gid,g in st.session_state.games.items():
                s = "Waiting" if g.phase==GamePhase.WAITING else "Playing" if g.phase==GamePhase.PLAY else "Done"
                st.markdown(f"**{gid}** - {s} ({len(g.players)}p)")

def waiting(gid):
    g = st.session_state.games[gid]
    
    st.markdown("# 💎 Splendor Online")
    st.markdown(f"### 📋 Waiting Room - ID: `{gid}`")
    
    st.markdown("#### Players:")
    for p in g.players:
        st.markdown(f"- **{p.name}** {'🤖' if p.name.startswith('AI ') else '👤'}")
    
    st.markdown(f"**{len(g.players)}/{len(g.players)} ready**")
    
    c1,c2 = st.columns(2)
    with c1:
        if st.button("▶️ Start", use_container_width=True):
            g.phase = GamePhase.PLAY
            g.message = f"{g.players[0].name} starts!"
            st.rerun()
    with c2:
        if st.button("❌ Cancel", use_container_width=True):
            del st.session_state.games[gid]
            st.session_state.current_game_id = None
            st.rerun()
    
    # Preview
    st.markdown("---")
    st.markdown("#### Preview")
    cl,cr = st.columns(2)
    with cl:
        st.markdown("**Bank:**")
        for c in [GemColor.EMERALD,GemColor.DIAMOND,GemColor.SAPPHIRE,GemColor.ONYX,GemColor.RUBY,GemColor.GOLD]:
            st.markdown(gem(c,g.bank.get(c,0)), unsafe_allow_html=True)
    with cr:
        st.markdown("**Nobles:**")
        for n in g.nobles: st.markdown(noble(n), unsafe_allow_html=True)

def game_ui(gid):
    g = st.session_state.games[gid]
    
    # AI move
    cp = g.players[g.current_player]
    if cp.name.startswith("AI ") and g.phase == GamePhase.PLAY:
        time.sleep(1)
        g.message = ai_move(g)
        st.rerun()
    
    # Header
    ch1, ch2 = st.columns([3,1])
    with ch1: st.markdown("# 💎 Splendor Online")
    with ch2:
        st.markdown(f"ID: `{gid}`")
        if st.button("🏠"): 
            st.session_state.current_game_id = None
            st.rerun()
    
    # Game over
    if g.phase == GamePhase.GAME_OVER:
        st.markdown(f"## 🏆 {g.winner} WINS!")
        if st.button("🔄 Again"):
            del st.session_state.games[gid]
            st.session_state.current_game_id = None
            st.rerun()
        return
    
    # Turn
    st.markdown(f'<div class="turn-box">🎯 {cp.name}\'s Turn</div>', unsafe_allow_html=True)
    st.markdown('<meta http-equiv="refresh" content="5">', unsafe_allow_html=True)
    
    # Layout
    cl, cc, cr = st.columns([1,2,1])
    
    with cl:
        st.markdown("#### 💰 Bank")
        for c in [GemColor.EMERALD,GemColor.DIAMOND,GemColor.SAPPHIRE,GemColor.ONYX,GemColor.RUBY,GemColor.GOLD]:
            st.markdown(gem(c,g.bank.get(c,0)), unsafe_allow_html=True)
        
        st.markdown("#### 👑 Nobles")
        for n in g.nobles: st.markdown(noble(n), unsafe_allow_html=True)
    
    with cc:
        st.markdown("#### 🃏 Cards")
        for tier,faceup in [(3,g.faceup3),(2,g.faceup2),(1,g.faceup1)]:
            st.markdown(f"**Tier {tier}**")
            cs = st.columns(4)
            for i,c in enumerate(faceup): cs[i%4].markdown(card(c,tier), unsafe_allow_html=True)
    
    with cr:
        st.markdown("#### 👥 Players")
        for i,p in enumerate(g.players):
            st.markdown(player(p, i==g.current_player), unsafe_allow_html=True)
    
    # Actions
    st.markdown("---")
    st.markdown("#### 🎯 Actions")
    
    acts = get_available_actions(g)
    ca1, ca2, ca3 = st.columns(3)
    
    with ca1:
        st.markdown("**💎 Gems**")
        with st.expander("Take 3 Different", expanded=True):
            av = [c for c in GemColor if c!=GemColor.GOLD and g.bank.get(c,0)>0]
            sel = st.multiselect("Select", av, key="sel3")
            if st.button("Take 3", key="bt3"):
                if len(sel)==3:
                    g.message = take_different_gems(g, sel)
                    st.rerun()
                else:
                    st.error("Select exactly 3!")
        
        with st.expander("Take 2 Same"):
            if acts["take_same"]:
                sc = st.selectbox("Color", acts["take_same"], key="sc2")
                if st.button("Take 2", key="bt2"):
                    g.message = take_same_gems(g, sc)
                    st.rerun()
            else:
                st.caption("Need 4+ gems available")
    
    with ca2:
        st.markdown("**📥 Reserve**")
        tr = st.radio("Tier", [1,2,3], horizontal=True, key="rt")
        rs = st.radio("From", ["Table","Deck"], horizontal=True, key="rf")
        
        if rs=="Table":
            fu = g.get_faceup(tr)
            if fu:
                opt = st.selectbox("Card", range(len(fu)), format_func=lambda i:f"Card {i+1} ({fu[i].get('points',0)}pts)", key="rc")
                if st.button("Reserve", key="bres"):
                    g.message = reserve_card(g, tr, opt)
                    st.rerun()
        else:
            if st.button("From Deck", key="bresd"):
                g.message = reserve_card(g, tr)
                st.rerun()
    
    with ca3:
        st.markdown("**🛒 Buy**")
        bs = st.radio("From", ["Table","Reserved"], horizontal=True, key="bf")
        
        if bs=="Table":
            bt = st.selectbox("Tier", [1,2,3], key="bt")
            fu = g.get_faceup(bt)
            if fu:
                opt = st.selectbox("Card", range(len(fu)), format_func=lambda i:f"Card {i+1} ({fu[i].get('points',0)}pts)", key="bc")
                if st.button("Buy", key="bbuy"):
                    g.message = buy_card(g, "faceup", bt, opt)
                    st.rerun()
        else:
            if cp.reserved_cards:
                opt = st.selectbox("Card", range(len(cp.reserved_cards)), format_func=lambda i:f"R{i+1} ({cp.reserved_cards[i].get('points',0)}pts)", key="brc")
                if st.button("Buy Reserved", key="bbuyr"):
                    from game import can_afford
                    if can_afford(cp, cp.reserved_cards[opt]):
                        g.message = buy_card(g, "reserved", reserved_index=opt)
                        st.rerun()
                    else:
                        st.error("Cannot afford!")
            else:
                st.caption("No reserved cards")

# ===== MAIN =====
def main():
    gid = st.session_state.current_game_id
    
    if gid and gid in st.session_state.games:
        g = st.session_state.games[gid]
        if g.phase == GamePhase.WAITING:
            waiting(gid)
        else:
            game_ui(gid)
    else:
        lobby()

if __name__ == "__main__":
    main()
