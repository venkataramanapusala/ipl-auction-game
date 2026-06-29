import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# --- STYLES & CONFIG ---
st.set_page_config(page_title="IPL Live Draft Room", page_icon="🏏", layout="centered")

# --- CUSTOM CSS FOR SLICK DESIGN ---
st.markdown("""
    <style>
    /* Global Background Fix */
    .stApp {
        background-color: #000000 !important;
    }
    
    /* Typography & Headers */
    h1, h2, h3, p, label, .stText {
        color: #FFFFFF !important;
    }
    .big-font { 
        font-size: 26px !important; 
        font-weight: bold; 
        color: #3B82F6 !important; 
        text-shadow: 0px 0px 8px rgba(59, 130, 246, 0.4);
    }
    .timer-text { 
        font-size: 22px; 
        font-weight: bold; 
        color: #EF4444 !important; 
    }
    
    /* Player Asset Card Box */
    .card-box { 
        padding: 20px; 
        border-radius: 12px; 
        background-color: #0F172A; 
        border: 1px solid #1E293B;
        border-left: 6px solid #3B82F6; 
        margin-bottom: 15px; 
        color: #FFFFFF !important; 
    }
    
    /* Target Override Streamlit Info Alert Box */
    div[data-testid="stNotification"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
    }
    div[data-testid="stNotification"] p {
        color: #3B82F6 !important;
        font-weight: bold !important;
    }
    
    /* Customization for Select Boxes / Inputs */
    div[data-baseweb="select"] > div {
        background-color: #1F2937 !important;
        color: white !important;
        border: 1px solid #4B5563 !important;
    }

    /* FIX FOR THE WHITE BUTTONS MATRIX */
    .stButton button {
        background-color: #1F2937 !important;
        color: #FFFFFF !important;
        border: 1px solid #4B5563 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease-in-out;
    }
    
    .stButton button:hover {
        background-color: #374151 !important;
        border-color: #3B82F6 !important;
        color: #3B82F6 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- LARGE SQUAD POOL GENERATOR ---
if "player_pool" not in st.session_state:
    pool = []
    for i in range(1, 61):
        pool.append({"name": f"Batsman Elite {i}", "role": "Batsman", "rating": random.randint(78, 95), "base_price": random.choice([50, 100, 150, 200])})
    for i in range(1, 61):
        pool.append({"name": f"Pace Star {i}", "role": "Bowler", "rating": random.randint(78, 96), "base_price": random.choice([50, 100, 150, 200])})
    for i in range(1, 51):
        pool.append({"name": f"AllRound Dynamo {i}", "role": "All-Rounder", "rating": random.randint(78, 93), "base_price": random.choice([50, 100, 150])})
    for i in range(1, 31):
        pool.append({"name": f"Gloveman Pro {i}", "role": "Wicket-Keeper", "rating": random.randint(78, 94), "base_price": random.choice([50, 100, 150, 200])})
    
    st.session_state.player_pool = pool
    random.shuffle(st.session_state.player_pool)

# --- VALUATION HELPER ---
def get_reasonable_val(player, current_index):
    random.seed(current_index + 1000)
    if player["rating"] >= 93: val = random.randint(1350, 1650)
    elif player["rating"] >= 90: val = random.randint(950, 1300)
    elif player["rating"] >= 86: val = random.randint(450, 950)
    else: val = random.randint(80, 400)
    random.seed() 
    return val

# --- LIVE ROSTER VIEW DIALOG POPUP ---
@st.dialog("📋 Current Roster & Budget Review", width="medium")
def view_teams_dialog():
    st.write("Review team spending status and compositional category balance:")
    for t in st.session_state.teams:
        batsmen = len([p for p in t["squad"] if p["role"] == "Batsman"])
        keepers = len([p for p in t["squad"] if p["role"] == "Wicket-Keeper"])
        all_rounders = len([p for p in t["squad"] if p["role"] == "All-Rounder"])
        bowlers = len([p for p in t["squad"] if p["role"] == "Bowler"])
        
        status_text = "⚠️ SQUAD MISMATCH" if (batsmen < 5 or keepers < 2 or all_rounders < 3 or bowlers < 5) else "✅ VALID"
        if len(t["squad"]) > 20: status_text = "⚠️ OVER SIGNED"
            
        with st.expander(f"{t['team_name']} — Purse: ₹{t['purse']/100:.2f} CR ({status_text})"):
            st.write(f"**Total Squad Count:** {len(t['squad'])} / 20 Players")
            st.write(f"🏏 Bat: {batsmen}/5 | 🧤 WK: {keepers}/2 | 🔀 AR: {all_rounders}/3 | 🎯 Bowl: {bowlers}/5")

# --- SESSION STATE INITIALIZATION ---
if "game_stage" not in st.session_state:
    st.session_state.game_stage = "setup"
if "teams" not in st.session_state:
    st.session_state.teams = []
if "auction_index" not in st.session_state:
    st.session_state.auction_index = 0
if "current_bid" not in st.session_state:
    st.session_state.current_bid = 0
if "highest_bidder" not in st.session_state:
    st.session_state.highest_bidder = None
if "log_msg" not in st.session_state:
    st.session_state.log_msg = ""
if "timer_seconds" not in st.session_state:
    st.session_state.timer_seconds = 4
if "scouted_count" not in st.session_state:
    st.session_state.scouted_count = 0
if "scouted_players" not in st.session_state:
    st.session_state.scouted_players = set()
if "match_history" not in st.session_state:
    st.session_state.match_history = []
if "career_event" not in st.session_state:
    st.session_state.career_event = None

# --- STAGE 1: SETUP ---
if st.session_state.game_stage == "setup":
    st.header("👑 IPL Premium Draft Room Manager")
    num_humans = st.slider("How many human players?", min_value=1, max_value=4, value=1)
    
    human_configs = []
    used_teams = []
    sorted_names = sorted([p["name"] for p in st.session_state.player_pool])
    
    for i in range(num_humans):
        st.subheader(f"Player {i+1} Configuration")
        h_name = st.text_input(f"Manager Name", value=f"Manager {i+1}", key=f"h_name_{i}")
        available_choices = [team for team in TEAM_NAMES_POOL if team not in used_teams]
        selected_team = st.selectbox(f"Choose Franchise", options=available_choices, key=f"h_team_{i}")
        used_teams.append(selected_team)
        
        targets = st.multiselect(f"🎯 Choose up to 5 Target Players for your Auto-Proxy Strategy:", 
                                 options=sorted_names, max_selections=5, key=f"h_targets_{i}")
        human_configs.append({"manager": h_name, "team": selected_team, "targets": targets})
        
    if st.button("Initialize ₹150 CR Tournament League", type="primary"):
        teams = []
        for hc in human_configs:
            teams.append({
                "team_name": f"{hc['manager']}'s {hc['team']}", "is_human": True,
                "purse": 15000, "squad": [], "personality": "User", 
                "points": 0, "wins": 0, "losses": 0, "disqualified": False, 
                "targets": hc["targets"], "playing_11": [], "impact_player": None,
                "tactic": "Balanced", "morale": 80
            })
        remaining_bot_names = [team for team in TEAM_NAMES_POOL if team not in used_teams]
        for bot_team in remaining_bot_names:
            teams.append({
                "team_name": f"{bot_team} (Bot)", "is_human": False,
                "purse": 15000, "squad": [], "personality": random.choice(BOT_PERSONALITIES), 
                "points": 0, "wins": 0, "losses": 0, "disqualified": False, 
                "targets": [], "playing_11": [], "impact_player": None,
                "tactic": "Balanced", "morale": 75
            })
        st.session_state.teams = teams
        st.session_state.game_stage = "auction"
        st.session_state.auction_index = 0
        st.session_state.timer_seconds = 4
        st.rerun()

# --- STAGE 2: LIVE AUCTION ROOM ---
elif st.session_state.game_stage == "auction":
    idx = st.session_state.auction_index
    if idx >= len(st.session_state.player_pool):
        st.success("All players indexed! Evaluating precise composition rule checks...")
        for t in st.session_state.teams:
            b_count = len([p for p in t["squad"] if p["role"] == "Batsman"])
            wk_count = len([p for p in t["squad"] if p["role"] == "Wicket-Keeper"])
            ar_count = len([p for p in t["squad"] if p["role"] == "All-Rounder"])
            bowl_count = len([p for p in t["squad"] if p["role"] == "Bowler"])
            
            # Global Evaluation Check Block
            if (len(t["squad"]) < 15 or len(t["squad"]) > 20 or 
                b_count < 5 or wk_count < 2 or ar_count < 3 or bowl_count < 5):
                t["disqualified"] = True
                t["points"] = -99  
            else:
                t["disqualified"] = False
        if st.button("Proceed to Lineup Selection", type="primary", use_container_width=True):
            st.session_state.game_stage = "lineup"
            st.rerun()
    else:
        player = st.session_state.player_pool[idx]
        reasonable_val = get_reasonable_val(player, idx)

        if st.session_state.current_bid == 0:
            st.session_state.current_bid = player["base_price"]
            st.session_state.highest_bidder = None
            st.session_state.timer_seconds = 4
            st.session_state.log_msg = f"Next up: {player['name']}! Base price set at ₹{player['base_price']/100:.2f} CR."

        st_autorefresh(interval=1000, key="auction_timer")
        st.markdown(f"<div class='big-font'>🔨 LIVE AUCTION CARD ({idx+1}/{len(st.session_state.player_pool)})</div>", unsafe_allow_html=True)
        
        # --- FAST-TRACK SIMULATION WITH SMART DRAFT AI ---
        if st.button("⚡ Fast-Track/Simulate Rest of Auction", type="secondary", use_container_width=True):
            while st.session_state.auction_index < len(st.session_state.player_pool):
                curr_idx = st.session_state.auction_index
                curr_p = st.session_state.player_pool[curr_idx]
                val = get_reasonable_val(curr_p, curr_idx)
                
                bidders = []
                for t in st.session_state.teams:
                    if len(t["squad"]) >= 20: continue
                    
                    # Core Category Counting Rules
                    b_count = len([p for p in t["squad"] if p["role"] == "Batsman"])
                    wk_count = len([p for p in t["squad"] if p["role"] == "Wicket-Keeper"])
                    ar_count = len([p for p in t["squad"] if p["role"] == "All-Rounder"])
                    bowl_count = len([p for p in t["squad"] if p["role"] == "Bowler"])
                    
                    # BLOCK bidding if this category is already perfectly full (stops bots from hoarding)
                    if curr_p["role"] == "Batsman" and b_count >= 6: continue
                    if curr_p["role"] == "Wicket-Keeper" and wk_count >= 3: continue
                    if curr_p["role"] == "All-Rounder" and ar_count >= 4: continue
                    if curr_p["role"] == "Bowler" and bowl_count >= 6: continue
                    
                    is_target = curr_p["name"] in t.get("targets", [])
                    mult = 1.10
                    
                    # FORCE critical bidding if missing a slot entirely
                    if curr_p["role"] == "Batsman" and b_count < 5: mult = 1.40
                    elif curr_p["role"] == "Wicket-Keeper" and wk_count < 2: mult = 1.50
                    elif curr_p["role"] == "All-Rounder" and ar_count < 3: mult = 1.40
                    elif curr_p["role"] == "Bowler" and bowl_count < 5: mult = 1.40
                    
                    if t["is_human"]:
                        max_limit = int(val * 1.15) if is_target else (int(val * mult) if mult > 1.10 else 0)
                    else:
                        max_limit = int(val * mult)
                        
                    if t["purse"] >= curr_p["base_price"] and max_limit >= curr_p["base_price"]:
                        bidders.append((t, max_limit))
                
                if bidders:
                    winner_tuple = max(bidders, key=lambda item: item[1])
                    winner_team = winner_tuple[0]
                    final_price = random.randint(curr_p["base_price"], min(winner_tuple[1], winner_team["purse"]))
                    final_price = max(curr_p["base_price"], (final_price // 50) * 50)
                    winner_team["purse"] -= final_price
                    winner_team["squad"].append(curr_p)
                else:
                    capable_bots = [t for t in st.session_state.teams if not t["is_human"] and len(t["squad"]) < 20 and t["purse"] >= curr_p["base_price"]]
                    if capable_bots:
                        bot = random.choice(capable_bots)
                        bot["purse"] -= curr_p["base_price"]
                        bot["squad"].append(curr_p)
                st.session_state.auction_index += 1
            st.session_state.current_bid = 0
            st.session_state.highest_bidder = None
            st.rerun()

        # Live clock counters
        if st.session_state.timer_seconds > 0:
            st.session_state.timer_seconds -= 1
            bots = [t for t in st.session_state.teams if not t["is_human"] and len(t["squad"]) < 20 and t["purse"] >= (st.session_state.current_bid + 50)]
            if bots and random.random() < 0.45: 
                valid_bots = [b for b in bots if st.session_state.highest_bidder is None or b["team_name"] != st.session_state.highest_bidder["team_name"]]
                smart_bidding_bots = []
                for b in valid_bots:
                    b_c = len([p for p in b["squad"] if p["role"] == "Batsman"])
                    wk_c = len([p for p in b["squad"] if p["role"] == "Wicket-Keeper"])
                    ar_c = len([p for p in b["squad"] if p["role"] == "All-Rounder"])
                    bowl_c = len([p for p in b["squad"] if p["role"] == "Bowler"])
                    
                    if player["role"] == "Batsman" and b_c >= 6: continue
                    if player["role"] == "Wicket-Keeper" and wk_c >= 3: continue
                    if player["role"] == "All-Rounder" and ar_c >= 4: continue
                    if player["role"] == "Bowler" and bowl_c >= 6: continue
                    
                    multiplier = 1.10
                    if player["role"] == "Batsman" and b_c < 5: multiplier = 1.40
                    elif player["role"] == "Wicket-Keeper" and wk_c < 2: multiplier = 1.50
                    elif player["role"] == "All-Rounder" and ar_c < 3: multiplier = 1.40
                    elif player["role"] == "Bowler" and bowl_c < 5: multiplier = 1.40
                    
                    if (st.session_state.current_bid + 50) <= int(reasonable_val * multiplier):
                        smart_bidding_bots.append(b)
                if smart_bidding_bots:
                    counter_bot = random.choice(smart_bidding_bots)
                    st.session_state.current_bid += 50
                    st.session_state.highest_bidder = counter_bot
                    st.session_state.timer_seconds = 4  
                    st.session_state.log_msg = f"🤖 {counter_bot['team_name']} bids ₹{st.session_state.current_bid/100:.2f} CR."
                    st.rerun()
        else:
            if st.session_state.highest_bidder:
                hb = st.session_state.highest_bidder
                for t in st.session_state.teams:
                    if t["team_name"] == hb["team_name"]:
                        t["purse"] -= st.session_state.current_bid
                        t["squad"].append(player)
            else:
                capable_bots = [t for t in st.session_state.teams if not t["is_human"] and len(t["squad"]) < 20 and t["purse"] >= player["base_price"]]
                if capable_bots:
                    assigned_bot = random.choice(capable_bots)
                    assigned_bot["purse"] -= player["base_price"]
                    assigned_bot["squad"].append(player)
            st.session_state.auction_index += 1
            st.session_state.current_bid = 0
            st.session_state.highest_bidder = None
            st.session_state.timer_seconds = 4
            st.rerun()

        st.markdown(f"<div class='timer-text'>⏳ GAVEL FALLING IN: {st.session_state.timer_seconds + 1}s</div>", unsafe_allow_html=True)
        st.progress(st.session_state.timer_seconds / 4)

        st.markdown(f"""
            <div class='card-box'>
                <strong>🏃 Active Asset:</strong> {player['name']}<br/>
                <strong>🎯 Specialty Category:</strong> {player['role']}<br/>
                <strong>📊 Skill OVR Rating:</strong> {player['rating']}
            </div>
        """, unsafe_allow_html=True)
        
        col_scout, col_view_btn = st.columns([2, 1])
        with col_scout:
            if player["name"] in st.session_state.scouted_players:
                st.success(f"📊 Scouting Valuation Guide: ₹{reasonable_val/100:.2f} CR")
            elif st.session_state.scouted_count < 30:
                if st.button(f"🔍 Scan Fair Limit ({30 - st.session_state.scouted_count} Left)", use_container_width=True):
                    st.session_state.scouted_players.add(player["name"])
                    st.session_state.scouted_count += 1
                    st.rerun()
        with col_view_btn:
            if st.button("📋 View Rosters", use_container_width=True): view_teams_dialog()

        st.metric(label="Current High Bid", value=f"₹{st.session_state.current_bid/100:.2f} CR", 
                  delta=f"Leader: {st.session_state.highest_bidder['team_name'] if st.session_state.highest_bidder else 'None'}")
        st.info(st.session_state.log_msg)
        
        human_teams = [t for t in st.session_state.teams if t["is_human"] and len(t["squad"]) < 20 and t["purse"] >= (st.session_state.current_bid + 50)]
        human_options = [t["team_name"] for t in human_teams]
        
        col1, col2 = st.columns(2)
        with col1:
            if human_options:
                bidding_manager = st.selectbox("Select Bidding Manager:", options=human_options)
                if st.button("Raise Bid (+₹50 L)", type="primary", use_container_width=True):
                    st.session_state.current_bid += 50
                    st.session_state.highest_bidder = next(t for t in st.session_state.teams if t["team_name"] == bidding_manager)
                    st.session_state.timer_seconds = 4  
                    st.session_state.log_msg = f"{bidding_manager} raised bid to ₹{st.session_state.current_bid/100:.2f} CR!"
                    st.rerun()
        with col2:
            if st.button("Pass / Drop Hammer Immediately", type="secondary", use_container_width=True):
                st.session_state.timer_seconds = 0
                st.rerun()

# --- STAGE 2.5: LINEUP LOCK IN ---
elif st.session_state.game_stage == "lineup":
    st.header("🏏 Match Lineup Selector Room")
    
    for t in st.session_state.teams:
        if not t["is_human"] and not t["disqualified"]:
            sorted_squad = sorted(t["squad"], key=lambda x: x["rating"], reverse=True)
            t["playing_11"] = sorted_squad[:11]
            t["impact_player"] = sorted_squad[11] if len(sorted_squad) > 11 else sorted_squad[0]

    active_humans = [t for t in st.session_state.teams if t["is_human"] and not t["disqualified"]]
    if active_humans:
        for t in active_humans:
            st.subheader(f"Configure {t['team_name']}")
            player_names = [p["name"] for p in t["squad"]]
            p11_names = st.multiselect(f"Select XI Starters:", options=player_names, key=f"p11_{t['team_name']}")
            remaining_options = [name for name in player_names if name not in p11_names]
            impact_name = st.selectbox(f"Select Impact Sub:", options=remaining_options, key=f"imp_{t['team_name']}")
            
            if st.button(f"Lock Lineup for {t['team_name']}"):
                if len(p11_names) != 11: st.error("Roster counts must hit exactly 11 players!")
                else:
                    t["playing_11"] = [p for p in t["squad"] if p["name"] in p11_names]
                    t["impact_player"] = next((p for p in t["squad"] if p["name"] == impact_name), None)
                    st.success("Lineup safely registered!")
                    
        if st.button("Proceed to Operations Dashboard", type="primary", use_container_width=True):
            st.session_state.game_stage = "dashboard"
            st.rerun()
    else:
        st.error("⚠️ Some rosters missed exact structural totals, but the Smart AI balanced things out.")
        if st.button("Enter Management Hub", type="primary", use_container_width=True):
            for t in st.session_state.teams:
                t["disqualified"] = False 
                sorted_squad = sorted(t["squad"], key=lambda x: x["rating"], reverse=True)
                t["playing_11"] = sorted_squad[:11] if len(sorted_squad) >= 11 else sorted_squad
                t["impact_player"] = sorted_squad[11] if len(sorted_squad) > 11 else None
            st.session_state.game_stage = "dashboard"
            st.rerun()

# --- STAGE 3: INTERACTIVE OPERATIONS HUB ---
elif st.session_state.game_stage == "dashboard":
    st.header("🏆 IPL Franchise Operations Hub")
    
    tab_table, tab_stats, tab_career = st.tabs(["📊 Tournament Standings Table", "🏏 Roster Performance Stats", "👔 Manager Career Room"])
    
    # --- TAB 1: STANDINGS TABLE ---
    with tab_table:
        st.subheader("League Table Standings")
        table_data = []
        for t in st.session_state.teams:
            if not t["disqualified"]:
                table_data.append({
                    "Franchise Team": t["team_name"],
                    "Wins 🟢": t["wins"],
                    "Losses 🔴": t["losses"],
                    "Squad Morale": f"{t['morale']}%",
                    "Points": t["points"]
                })
        if table_data:
            sorted_table = sorted(table_data, key=lambda x: x["Points"], reverse=True)
            st.table(sorted_table)
            
    # --- TAB 2: PERFORMANCE STATS ---
    with tab_stats:
        st.subheader("Live Performance Match Log")
        if st.session_state.match_history:
            for match in reversed(st.session_state.match_history[-8:]):
                st.markdown(f"**🏏 {match['fixture']}**")
                st.caption(f"Outcome: {match['result']}")
                col_runs, col_wck = st.columns(2)
                with col_runs:
                    st.write(f"🌟 **Top Scorer:** {match['top_batsman']} ({match['runs_scored']} runs)")
                with col_wck:
                    st.write(f"🎯 **Top Bowler:** {match['top_bowler']} ({match['wickets_taken']} wickets)")
                st.divider()
        else:
            st.caption("No matches simulated yet. Head over to the Career Room to kick off match days!")

    # --- TAB 3: MANAGER CAREER SUITE ---
    with tab_career:
        st.subheader("Operational Tactical Controls")
        
        user_team = next((t for t in st.session_state.teams if t["is_human"] and not t["disqualified"]), None)
        if user_team:
            col_tactic, col_morale = st.columns(2)
            with col_tactic:
                user_team["tactic"] = st.selectbox("Current Team Match Tactic:", ["Defensive Anchor", "Balanced Alignment", "Ultra-Aggressive Attack"], index=1)
            with col_morale:
                st.metric("Team Satisfaction Morale Indicator", f"{user_team['morale']}%")
                
            if st.button("🎉 Host Team Bond Dinner (+10% Morale, Costs ₹50 L)", use_container_width=True):
                if user_team["purse"] >= 50:
                    user_team["purse"] -= 50
                    user_team["morale"] = min(100, user_team["morale"] + 10)
                    st.success("Morale boosted!")
                    st.rerun()
        
        st.divider()
        st.subheader("Simulate League Actions")
        active_squads = [t for t in st.session_state.teams if not t["disqualified"]]
        
        if len(active_squads) >= 2:
            if st.button("⚡ Simulate Next Match Fixtures", type="primary", use_container_width=True):
                twist_roll = random.random()
                if twist_roll < 0.30: 
                    affected_team = random.choice(active_squads)
                    twist_type = random.choice(["injury", "unrest"])
                    
                    if twist_type == "injury" and affected_team["playing_11"]:
                        injured_p = random.choice(affected_team["playing_11"])
                        injured_p["rating"] -= 8 
                        st.session_state.career_event = f"🚨 TWIST: {affected_team['team_name']}'s key player **{injured_p['name']}** suffered an injury! Skill rating down by -8 points."
                        affected_team["morale"] = max(30, affected_team["morale"] - 15)
                    elif twist_type == "unrest":
                        st.session_state.career_event = f"⚠️ TWIST: Locker room unrest detected at **{affected_team['team_name']}**! Morale dropped by -20%."
                        affected_team["morale"] = max(20, affected_team["morale"] - 20)
                else:
                    st.session_state.career_event = None

                random.shuffle(active_squads)
                for i in range(0, len(active_squads) - 1, 2):
                    t1, t2 = active_squads[i], active_squads[i+1]
                    
                    t1_mod = 1.05 if t1["tactic"] == "Ultra-Aggressive Attack" else 1.0
                    t2_mod = 1.05 if t2["tactic"] == "Ultra-Aggressive Attack" else 1.0
                    
                    t1_power = (sum([p["rating"] for p in t1["playing_11"]]) + (t1["impact_player"]["rating"] if t1["impact_player"] else 0)) * (t1["morale"] / 100) * t1_mod
                    t2_power = (sum([p["rating"] for p in t2["playing_11"]]) + (t2["impact_player"]["rating"] if t2["impact_player"] else 0)) * (t2["morale"] / 100) * t2_mod
                    
                    p1_score = t1_power + random.randint(-40, 40)
                    p2_score = t2_power + random.randint(-40, 40)
                    
                    all_batsmen = [p for p in t1["playing_11"] + t2["playing_11"] if p["role"] in ["Batsman", "Wicket-Keeper"]]
                    all_bowlers = [p for p in t1["playing_11"] + t2["playing_11"] if p["role"] in ["Bowler", "All-Rounder"]]
                    
                    top_bat = random.choice(all_batsmen)["name"] if all_batsmen else "Unknown Player"
                    top_bowl = random.choice(all_bowlers)["name"] if all_bowlers else "Unknown Player"
                    
                    if p1_score > p2_score:
                        t1["points"] += 2; t1["wins"] += 1; t1["morale"] = min(100, t1["morale"] + 4)
                        t2["losses"] += 1; t2["morale"] = max(30, t2["morale"] - 5)
                        res = f"{t1['team_name']} won!"
                    else:
                        t2["points"] += 2; t2["wins"] += 1; t2["morale"] = min(100, t2["morale"] + 4)
                        t1["losses"] += 1; t1["morale"] = max(30, t1["morale"] - 5)
                        res = f"{t2['team_name']} won!"
                        
                    st.session_state.match_history.append({
                        "fixture": f"{t1['team_name']} vs {t2['team_name']}",
                        "result": res,
                        "top_batsman": top_bat,
                        "runs_scored": random.randint(45, 98),
                        "top_bowler": top_bowl,
                        "wickets_taken": random.randint(3, 5)
                    })
                st.rerun()

        if st.session_state.career_event:
            st.warning(st.session_state.career_event)
