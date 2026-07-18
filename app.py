import streamlit as st
import random
import pandas as pd

# Set page configuration
st.set_page_config(page_title="IPL Pro-Manager Simulation Console", layout="wide")

# ==========================================
# MODULE 1: DATABASE GENERATOR & UPGRADER
# ==========================================
def initialize_advanced_player_attributes(player_list):
    """Ensures every player has traits, morale, and form history without overriding existing data."""
    traits_pool = ["Finisher", "Mystery Spinner", "Express Pace", "Anchor", "Slogger"]
    for p in player_list:
        if "form_history" not in p or not isinstance(p["form_history"], list):
            p["form_history"] = [6, 6, 6]  # Default neutral match ratings out of 10
        if "morale" not in p:
            p["morale"] = 80  # Scale of 0 to 100
        if "trait" not in p:
            # 40% chance to get a special trait, otherwise None
            p["trait"] = random.choice(traits_pool) if random.random() < 0.4 else "None"
        if "age" not in p:
            p["age"] = random.randint(18, 36)
        if "xp" not in p:
            p["xp"] = 0
        if "plan" not in p:
            p["plan"] = "Balanced Alignment"
        if "rating" not in p:
            p["rating"] = random.randint(70, 92)
        if "dyn_pot" not in p:
            p["dyn_pot"] = min(99, p["rating"] + random.randint(0, 10))
    return player_list

# Generate a mock pool of 200 players if not loaded
if "player_pool" not in st.session_state:
    first_names = ["Virat", "Rohit", "Jasprit", "Shubman", "Rishabh", "Hardik", "Suryakumar", "Ravindra", "Shreyas", "KL", "Yashasvi", "Rinku", "Sanju", "Ruturaj", "Ishan"]
    last_names = ["Kohli", "Sharma", "Bumrah", "Gill", "Pant", "Pandya", "Yadav", "Jadeja", "Iyer", "Rahul", "Jaiswal", "Singh", "Samson", "Gaikwad", "Kishan"]
    
    raw_players = []
    for i in range(200):
        name = f"{random.choice(first_names)} {random.choice(last_names)} ({i+1})"
        role = random.choice(["Batsman", "Bowler", "All-Rounder", "Wicket-Keeper"])
        rating = random.randint(70, 95)
        raw_players.append({
            "name": name,
            "role": role,
            "rating": rating,
            "dyn_pot": min(99, rating + random.randint(0, 8))
        })
    
    st.session_state.player_pool = initialize_advanced_player_attributes(raw_players)

# Initialize Franchise Teams
if "teams" not in st.session_state:
    team_names = ["Mumbai Elite", "Chennai Kings", "Bangalore Tech", "Delhi Capitals", "Kolkata Knights", "Gujarat Titans", "Rajasthan Royals", "Lucknow Super Giant"]
    st.session_state.teams = {}
    
    pool_copy = list(st.session_state.player_pool)
    random.shuffle(pool_copy)
    
    for i, t_name in enumerate(team_names):
        squad = pool_copy[i*25 : (i+1)*25]
        st.session_state.teams[t_name] = {
            "name": t_name,
            "budget": 85_00_00_000, # ₹85 Crore
            "squad": squad,
            "playing_11": squad[:11],
            "impact_player": squad[11],
            "points": 0,
            "nrr": 0.0,
            "wins": 0,
            "losses": 0
        }

# Global State Variables
if "match_day" not in st.session_state:
    st.session_state.match_day = 1
if "user_team_key" not in st.session_state:
    st.session_state.user_team_key = "Mumbai Elite"
if "xp_multiplier" not in st.session_state:
    st.session_state.xp_multiplier = 1.0
if "news_flash" not in st.session_state:
    st.session_state.news_flash = "Welcome to the new IPL Front-Office Season! Squad training metrics have initialized."

user_team = st.session_state.teams[st.session_state.user_team_key]

# ==========================================
# MODULE 2: SIMULATION ENGINE LOGIC
# ==========================================
def simulate_ball_by_ball(batting_team, bowling_team):
    """Simulates a highly detailed, trait-and-form-affected match innings."""
    innings_score = 0
    wickets = 0
    balls_bowled = 0
    
    batters = list(batting_team["playing_11"])
    bowlers = [p for p in bowling_team["playing_11"] if p.get("role") in ["Bowler", "All-Rounder"]]
    if not bowlers: 
        bowlers = bowling_team["playing_11"][-5:] # Fallback
        
    striker_idx = 0
    non_striker_idx = 1
    
    # Track stats for scorecard rendering
    for b in batters:
        b["match_runs"] = 0
        b["match_balls"] = 0
    for b in bowlers:
        b["match_overs"] = 0.0
        b["match_runs_conceded"] = 0
        b["match_wickets"] = 0

    current_innings = 1 # Simplified context assignment
    
    for current_over in range(1, 21):
        if wickets >= 10:
            break
            
        current_bowler = bowlers[(current_over - 1) % len(bowlers)]
        overs_balls = 0
        
        for ball in range(1, 7):
            if wickets >= 10:
                break
            
            balls_bowled += 1
            overs_balls += 1
            current_batsman = batters[striker_idx]
            
            # Update individual tracker properties safely
            if "balls_faced" not in current_batsman: current_batsman["balls_faced"] = 0
            current_batsman["balls_faced"] += 1
            
            # --- SIMULATION ENGINE DYNAMIC CALCULATION ---
            # 1. Fetch baseline attributes safely
            batsman_rating = current_batsman.get("rating", 80)
            bowler_rating = current_bowler.get("rating", 80)

            # 2. Add Form Factor (Average of last 3 matches compared to baseline of 6)
            bat_form_history = current_batsman.get("form_history", [6, 6, 6])
            b_form_history = current_bowler.get("form_history", [6, 6, 6])
            bat_form_avg = sum(bat_form_history) / len(bat_form_history)
            b_form_avg = sum(b_form_history) / len(b_form_history)

            batsman_rating += int((bat_form_avg - 6) * 2)
            bowler_rating += int((b_form_avg - 6) * 2)

            # 3. Add Morale Penalty (Low morale degrades performance)
            if current_batsman.get("morale", 80) < 50: batsman_rating -= 4
            if current_bowler.get("morale", 80) < 50: bowler_rating -= 4

            # 4. Trigger Situational Trait Architectures
            if current_batsman.get("trait") == "Finisher" and current_over >= 17:
                batsman_rating += 12
            if current_batsman.get("trait") == "Slogger" and current_over >= 16:
                batsman_rating += 8
            if current_bowler.get("trait") == "Express Pace":
                bowler_rating += 5
            if current_bowler.get("trait") == "Mystery Spinner" and current_batsman["balls_faced"] <= 3:
                bowler_rating += 10
                
            # Ball outcome math logic
            outcome_seed = random.randint(1, 100) + (batsman_rating - bowler_rating)
            
            if outcome_seed < 15: # Wicket
                wickets += 1
                current_bowler["match_wickets"] += 1
                striker_idx = max(striker_idx, non_striker_idx) + 1
                if striker_idx >= 11:
                    break
            elif outcome_seed < 45: # Dot ball
                current_bowler["match_runs_conceded"] += 0
            elif outcome_seed < 75: # Single/Twos
                runs = random.choice([1, 2])
                innings_score += runs
                current_batsman["match_runs"] += runs
                current_bowler["match_runs_conceded"] += runs
                if runs == 1: # Rotate Strike
                    striker_idx, non_striker_idx = non_striker_idx, striker_idx
            elif outcome_seed < 92: # Boundary Four
                innings_score += 4
                current_batsman["match_runs"] += 4
                current_bowler["match_runs_conceded"] += 4
            else: # Maximum Six
                innings_score += 6
                current_batsman["match_runs"] += 6
                current_bowler["match_runs_conceded"] += 6
                
        current_bowler["match_overs"] = round(current_bowler["match_overs"] + (overs_balls / 10), 1)
        # Rotate strike at over end
        striker_idx, non_striker_idx = non_striker_idx, striker_idx
        
    return innings_score, wickets

def process_seasonal_recalculations():
    """Applies seasonal aging, regression bounds, and potential adjustments."""
    for t_name, team in st.session_state.teams.items():
        for p in team["squad"]:
            p["age"] = p.get("age", 25) + 1
            # Age regression factor bounds
            if p["age"] > 32:
                p["rating"] = max(50, p.get("rating", 80) - random.randint(2, 5))
            else:
                # Potential boost mechanics
                if p.get("rating", 80) < p.get("dyn_pot", 85):
                    boost = random.randint(1, 4)
                    p["rating"] = min(p.get("dyn_pot", 85), p.get("rating", 80) + boost)


# ==========================================
# HEADER INTERFACE CONTROL PROFILE
# ==========================================
st.title("🏆 IPL Pro-Manager Simulation Console")
selected_profile = st.sidebar.selectbox("Active Profile Franchise Switcher", options=list(st.session_state.teams.keys()))
if selected_profile != st.session_state.user_team_key:
    st.session_state.user_team_key = selected_profile
    st.rerun()

st.sidebar.metric("Current Match Day Iteration", f"Day {st.session_state.match_day} / 14")
st.sidebar.metric("Franchise Balance Reserves", f"₹{user_team['budget']:,}")

tab_media, tab_roster, tab_standings, tab_cap, tab_office = st.tabs([
    "📰 Media Newsroom", "🏋️ Roster Hub", "📊 Standings Ledger", "🧢 Cap Races", "💼 Executive Office Suite"
])

# ==========================================
# TAB 1: MEDIA NEWSROOM (With Press Conf)
# ==========================================
with tab_media:
    st.subheader("📰 Global Media Coverage & Breaking News")
    st.info(f"Latest Wire Announcement: {st.session_state.news_flash}")
    
    # --- INTERACTIVE POST-MATCH PRESS CONFERENCE ---
    if st.session_state.match_day > 1:
        st.markdown("---")
        st.markdown("### 🎙️ Post-Match Press Conference Room")
        st.caption("The media is demanding a statement regarding your squad management choices.")
        
        conf_choice = st.radio(
            "Journalist Question: 'Your squad's consistency is being questioned. How do you respond?'",
            options=[
                "🗣️ Defend Squad (Boosts Morale +5 across team, adds Media Pressure)",
                "🏟️ Blame Pitch Conditions (Keeps Morale Stable, drops Fan Engagement slightly)",
                "⚠️ Publicly Reprimand Performance (Drops Star Morale -15, doubles Training XP gains for 1 iteration)"
            ],
            key="press_conf_radio"
        )
        
        if st.button("🎤 Submit Press Statement", use_container_width=True):
            if "Defend" in conf_choice:
                for p in user_team["squad"]:
                    p["morale"] = min(100, p.get("morale", 80) + 5)
                st.success("The dressing room respects your loyalty. Morale across the squad increased!")
            elif "Blame" in conf_choice:
                st.warning("The media calls it an excuse, but the team's internal chemistry remains stable.")
            elif "Reprimand" in conf_choice:
                star_player = max(user_team["squad"], key=lambda x: x.get("rating", 80))
                star_player["morale"] = max(0, star_player.get("morale", 80) - 15)
                st.error(f"{star_player['name']} took your comments personally! However, the squad's training intensity has doubled.")
                st.session_state["xp_multiplier"] = 2.0
                st.rerun()

# ==========================================
# TAB 2: ROSTER HUB LAYOUT (Upgraded Matrix)
# ==========================================
with tab_roster:
    st.subheader("📋 Core Team Squad Formulation & Academy Center")
    col_lineup, col_preview = st.columns([1, 1])
    
    with col_lineup:
        st.markdown("#### ⚔️ Strategic XI Selection Blueprint")
        all_member_names = [p["name"] for p in user_team["squad"]]
        
        current_xi_names = [p["name"] for p in user_team["playing_11"]]
        selected_xi = st.multiselect("Designate Playing XI Starters", options=all_member_names, default=current_xi_names[:11])
        
        if len(selected_xi) == 11:
            user_team["playing_11"] = [p for p in user_team["squad"] if p["name"] in selected_xi]
            st.success("Starter Lineup validation successfully initialized!")
        else:
            st.error("You must select exactly 11 players for your starting lineup.")
            
        impact_name = user_team["impact_player"]["name"] if user_team.get("impact_player") else all_member_names[11]
        selected_impact = st.selectbox("Assign Tactical Impact Substitute", options=all_member_names, index=all_member_names.index(impact_name))
        user_team["impact_player"] = next(p for p in user_team["squad"] if p["name"] == selected_impact)

    with col_preview:
        st.markdown("#### 🏋️ Active Squad Matrix & Performance Metrics")
        for p in user_team["squad"]:
            is_starter = "⭐ Starter XI" if p in user_team["playing_11"] else ("🔄 Impact Sub" if user_team.get("impact_player") and p["name"] == user_team["impact_player"]["name"] else "📋 Bench Reserve")
            
            # Safe parameters
            p_age = p.get("age", 25)
            p_rating = p.get("rating", 80)
            p_dyn_pot = p.get("dyn_pot", p_rating)
            p_xp = p.get("xp", 0)
            p_plan = p.get("plan", "Balanced Alignment")
            p_morale = p.get("morale", 80)
            p_trait = p.get("trait", "None")
            
            p_form_list = p.get("form_history", [6, 6, 6])
            p_form = round(sum(p_form_list) / len(p_form_list), 1)

            # Dynamic UX signals
            morale_emoji = "😊" if p_morale >= 75 else ("😐" if p_morale >= 45 else "😡")
            trait_badge = f" | ⚡ Trait: {p_trait}" if p_trait != "None" else ""

            with st.expander(f"{p['name']} (OVR {p_rating} | Form: {p_form}/10) — {is_starter}"):
                st.markdown(f"**Status Profile:** Age {p_age} | Morale: {p_morale}/100 {morale_emoji}{trait_badge}")
                
                p["plan"] = st.selectbox(
                    "Strategic Target Development Plan:", 
                    ["Balanced Alignment", "Focused Skill Burst", "Tactical IQ Training"], 
                    key=f"plan_sel_{p['name']}", 
                    index=["Balanced Alignment", "Focused Skill Burst", "Tactical IQ Training"].index(p_plan) if p_plan in ["Balanced Alignment", "Focused Skill Burst", "Tactical IQ Training"] else 0
                )
                st.progress(min(max(p_xp / 100, 0.0), 1.0))
                st.caption(f"XP Status: {p_xp}/100 | Hidden Potential Ceiling: {p_dyn_pot}")

# ==========================================
# TAB 3: STANDINGS LEDGER
# ==========================================
with tab_standings:
    st.subheader("📊 Dynamic League Standings Board")
    standings_data = []
    for t_key, t in st.session_state.teams.items():
        standings_data.append({
            "Team Franchise": t["name"],
            "Points": t["points"],
            "Wins": t["wins"],
            "Losses": t["losses"],
            "Net Run Rate (NRR)": round(t["nrr"], 3)
        })
    df_standings = pd.DataFrame(standings_data).sort_values(by=["Points", "Net Run Rate (NRR)"], ascending=False)
    st.table(df_standings)

# ==========================================
# TAB 4: CAP RACES
# ==========================================
with tab_cap:
    st.subheader("🧢 Statistics Leaderboard (Orange & Purple Cap Races)")
    
    all_players = []
    for t in st.session_state.teams.values():
        for p in t["squad"]:
            all_players.append(p)
            
    col_orange, col_purple = st.columns(2)
    with col_orange:
        st.markdown("### 🟠 Orange Cap Contenders")
        orange_df = pd.DataFrame([{
            "Player": p["name"], "Rating": p["rating"], "Trait": p.get("trait", "None")
        } for p in sorted(all_players, key=lambda x: x["rating"], reverse=True)[:5]])
        st.dataframe(orange_df, use_container_width=True)
        
    with col_purple:
        st.markdown("### 🟣 Purple Cap Contenders")
        purple_df = pd.DataFrame([{
            "Player": p["name"], "Ceiling Potential": p.get("dyn_pot", 90), "Trait": p.get("trait", "None")
        } for p in sorted(all_players, key=lambda x: x.get("dyn_pot", 0), reverse=True)[:5]])
        st.dataframe(purple_df, use_container_width=True)

# ==========================================
# TAB 5: OFFICE SUITE (Morale Activation & Trades)
# ==========================================
with tab_office:
    st.subheader("💼 Principal Owner Executive Command Center")
    
    if st.button("⚡ Fast-Simulate Next Competitive League Matchday", use_container_width=True):
        all_keys = list(st.session_state.teams.keys())
        random.shuffle(all_keys)
        
        # Matchmaking Pairs Loop
        for idx in range(0, len(all_keys), 2):
            t1 = st.session_state.teams[all_keys[idx]]
            t2 = st.session_state.teams[all_keys[idx+1]]
            
            # Execute Innings 
            s1, w1 = simulate_ball_by_ball(t1, t2)
            s2, w2 = simulate_ball_by_ball(t2, t1)
            
            # Form calculations score outputs bounded assignment logic
            for p in t1["playing_11"]:
                score = min(10, max(2, random.randint(4, 9) + (1 if s1 > s2 else -1)))
                p["form_history"] = (p.get("form_history", [6,6,6]) + [score])[-3:]
            for p in t2["playing_11"]:
                score = min(10, max(2, random.randint(4, 9) + (1 if s2 > s1 else -1)))
                p["form_history"] = (p.get("form_history", [6,6,6]) + [score])[-3:]
            
            # Determine Winner Matrix 
            if s1 > s2:
                t1["points"] += 2; t1["wins"] += 1; t1["nrr"] += 0.45
                t2["losses"] += 1; t2["nrr"] -= 0.45
                if t1["name"] == st.session_state.user_team_key:
                    st.session_state.news_flash = f"Victory! {t1['name']} scored {s1}/{w1} beating {t2['name']} ({s2}/{w2})!"
            else:
                t2["points"] += 2; t2["wins"] += 1; t2["nrr"] += 0.45
                t1["losses"] += 1; t1["nrr"] -= 0.45
                if t2["name"] == st.session_state.user_team_key:
                    st.session_state.news_flash = f"Victory! {t2['name']} scored {s2}/{w2} beating {t1['name']} ({s1}/{w1})!"
                    
        # Apply XP development steps across user roster profiles
        xp_gain = int(15 * st.session_state.xp_multiplier)
        for p in user_team["squad"]:
            p["xp"] += xp_gain
            if p["xp"] >= 100:
                p["xp"] = 0
                p["rating"] = min(p.get("dyn_pot", 99), p["rating"] + 1)
                
        # Reset multiplier baseline
        st.session_state.xp_multiplier = 1.0
        st.session_state.match_day += 1
        
        # Season review cutoff threshold
        if st.session_state.match_day > 14:
            process_seasonal_recalculations()
            st.session_state.match_day = 1
            st.session_state.news_flash = "Season Concluded! Biological development cycles, age regressions, and dynamic thresholds have re-synchronized."
            
        st.rerun()

    st.markdown("---")
    st.markdown("### 🏛 *Principal Owner Corporate Operations*")
    col_actions1, col_actions2 = st.columns(2)
    
    with col_actions1:
        st.markdown("#### 📣 Team Morale Activation")
        st.caption("Invest franchise liquid reserves back into team happiness.")
        pep_cost = 15_00_000  # ₹15 Lakhs
        
        if st.button(f"💵 Host Corporate Luxury Dinner (Cost: ₹15L)", use_container_width=True):
            if user_team.get("budget", 0) >= pep_cost:
                user_team["budget"] -= pep_cost
                for p in user_team["squad"]:
                    p["morale"] = min(100, p.get("morale", 80) + 20)
                st.success("The atmosphere is electric! Morale surged across the franchise roster.")
                st.rerun()
            else:
                st.error("Insufficient liquidity pools available in team reserves.")
                
    with col_actions2:
        st.markdown("#### 🤝 Mid-Season Trade Market")
        current_day = st.session_state.match_day
        
        # Restrict window accessibility to mid-season marks
        if 6 <= current_day <= 8:
            st.warning("🚨 The Mid-Season Trade Window is Open!")
            trade_away = st.selectbox("Select Player to Trade Out:", options=[p["name"] for p in user_team["squad"]])
            
            if st.button("Consummate Exchange Deal", use_container_width=True):
                st.success(f"Successfully processed transactional trading parameters for {trade_away}!")
        else:
            st.info("The trade window opens exclusively between Match Days 6 and 8.")
