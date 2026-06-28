import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# --- STYLES & CONFIG ---
st.set_page_config(page_title="IPL Auction Manager", page_icon="🏏", layout="centered")

# --- DATA POOLS ---
TEAM_NAMES_POOL = [
    "Mumbai Mavericks", "Chennai Kings", "Bangalore Blasters", 
    "Delhi Dynamos", "Kolkata Knights", "Gujarat Giants", 
    "Punjab Panthers", "Rajasthan Royals", "Lucknow Lions", "Hyderabad Heroes"
]

BOT_PERSONALITIES = ["Batting-Heavy", "Bowling-Heavy", "Youth-Focus", "Balanced"]

# --- 100 PLAYER DATABASE ---
if "player_pool" not in st.session_state:
    st.session_state.player_pool = [
        # --- BATSMEN ---
        {"name": "Virat Kohli", "role": "Batsman", "rating": 94, "base_price": 200},
        {"name": "Suryakumar Yadav", "role": "Batsman", "rating": 93, "base_price": 150},
        {"name": "Rohit Sharma", "role": "Batsman", "rating": 91, "base_price": 200},
        {"name": "Travis Head", "role": "Batsman", "rating": 92, "base_price": 150},
        {"name": "Shubman Gill", "role": "Batsman", "rating": 89, "base_price": 100},
        {"name": "Yashasvi Jaiswal", "role": "Batsman", "rating": 90, "base_price": 100},
        {"name": "Ruturaj Gaikwad", "role": "Batsman", "rating": 88, "base_price": 100},
        {"name": "Rinku Singh", "role": "Batsman", "rating": 86, "base_price": 50},
        {"name": "Sai Sudharsan", "role": "Batsman", "rating": 84, "base_price": 50},
        {"name": "David Warner", "role": "Batsman", "rating": 85, "base_price": 100},
        {"name": "Faf du Plessis", "role": "Batsman", "rating": 86, "base_price": 100},
        {"name": "Kane Williamson", "role": "Batsman", "rating": 85, "base_price": 100},
        {"name": "Tilak Varma", "role": "Batsman", "rating": 85, "base_price": 50},
        {"name": "Shimron Hetmyer", "role": "Batsman", "rating": 83, "base_price": 75},
        {"name": "Rovman Powell", "role": "Batsman", "rating": 84, "base_price": 75},
        {"name": "Rahul Tripathi", "role": "Batsman", "rating": 81, "base_price": 30},
        {"name": "Devdutt Padikkal", "role": "Batsman", "rating": 80, "base_price": 30},
        {"name": "Prithvi Shaw", "role": "Batsman", "rating": 82, "base_price": 50},
        {"name": "Mayank Agarwal", "role": "Batsman", "rating": 79, "base_price": 30},
        {"name": "Tristan Stubbs", "role": "Batsman", "rating": 86, "base_price": 50},
        {"name": "Tim David", "role": "Batsman", "rating": 84, "base_price": 75},
        {"name": "Ajinkya Rahane", "role": "Batsman", "rating": 80, "base_price": 50},
        {"name": "Manish Pandey", "role": "Batsman", "rating": 78, "base_price": 30},
        {"name": "Sherfane Rutherford", "role": "Batsman", "rating": 80, "base_price": 40},
        {"name": "Nehal Wadhera", "role": "Batsman", "rating": 81, "base_price": 20},
        {"name": "Riyan Parag", "role": "Batsman", "rating": 84, "base_price": 30},
        {"name": "Deepak Hooda", "role": "Batsman", "rating": 79, "base_price": 40},
        {"name": "Ayush Badoni", "role": "Batsman", "rating": 80, "base_price": 20},
        {"name": "Shahrukh Khan", "role": "Batsman", "rating": 82, "base_price": 40},
        {"name": "Abdul Samad", "role": "Batsman", "rating": 79, "base_price": 20},

        # --- BOWLERS ---
        {"name": "Jasprit Bumrah", "role": "Bowler", "rating": 96, "base_price": 200},
        {"name": "Rashid Khan", "role": "Bowler", "rating": 94, "base_price": 150},
        {"name": "Pat Cummins", "role": "Bowler", "rating": 92, "base_price": 150},
        {"name": "Mitchell Starc", "role": "Bowler", "rating": 91, "base_price": 150},
        {"name": "Trent Boult", "role": "Bowler", "rating": 90, "base_price": 100},
        {"name": "Mohammed Shami", "role": "Bowler", "rating": 91, "base_price": 150},
        {"name": "Kuldeep Yadav", "role": "Bowler", "rating": 89, "base_price": 100},
        {"name": "Yuzvendra Chahal", "role": "Bowler", "rating": 87, "base_price": 75},
        {"name": "Matheesha Pathirana", "role": "Bowler", "rating": 88, "base_price": 50},
        {"name": "Arshdeep Singh", "role": "Bowler", "rating": 86, "base_price": 75},
        {"name": "Kagiso Rabada", "role": "Bowler", "rating": 89, "base_price": 100},
        {"name": "Anrich Nortje", "role": "Bowler", "rating": 85, "base_price": 75},
        {"name": "Mohammed Siraj", "role": "Bowler", "rating": 86, "base_price": 100},
        {"name": "Avesh Khan", "role": "Bowler", "rating": 83, "base_price": 50},
        {"name": "Ravi Bishnoi", "role": "Bowler", "rating": 85, "base_price": 50},
        {"name": "Maheesh Theekshana", "role": "Bowler", "rating": 84, "base_price": 50},
        {"name": "Adam Zampa", "role": "Bowler", "rating": 86, "base_price": 75},
        {"name": "Nandre Burger", "role": "Bowler", "rating": 82, "base_price": 40},
        {"name": "Khaleel Ahmed", "role": "Bowler", "rating": 83, "base_price": 50},
        {"name": "Mukesh Kumar", "role": "Bowler", "rating": 82, "base_price": 30},
        {"name": "T Natarajan", "role": "Bowler", "rating": 84, "base_price": 50},
        {"name": "Sandeep Sharma", "role": "Bowler", "rating": 83, "base_price": 40},
        {"name": "Mohit Sharma", "role": "Bowler", "rating": 81, "base_price": 30},
        {"name": "Deepak Chahar", "role": "Bowler", "rating": 82, "base_price": 75},
        {"name": "Shardul Thakur", "role": "Bowler", "rating": 81, "base_price": 75},
        {"name": "Harshal Patel", "role": "Bowler", "rating": 83, "base_price": 50},
        {"name": "Bhuvneshwar Kumar", "role": "Bowler", "rating": 82, "base_price": 50},
        {"name": "Umran Malik", "role": "Bowler", "rating": 79, "base_price": 30},
        {"name": "Mayank Yadav", "role": "Bowler", "rating": 84, "base_price": 20},
        {"name": "Vaibhav Arora", "role": "Bowler", "rating": 80, "base_price": 20},
        {"name": "Harshit Rana", "role": "Bowler", "rating": 83, "base_price": 20},
        {"name": "Tushar Deshpande", "role": "Bowler", "rating": 81, "base_price": 30},
        {"name": "Sai Kishore", "role": "Bowler", "rating": 80, "base_price": 20},
        {"name": "Varun Chakaravarthy", "role": "Bowler", "rating": 86, "base_price": 50},
        {"name": "Lockie Ferguson", "role": "Bowler", "rating": 83, "base_price": 75},

        # --- ALL-ROUNDERS ---
        {"name": "Hardik Pandya", "role": "All-Rounder", "rating": 91, "base_price": 150},
        {"name": "Ravindra Jadeja", "role": "All-Rounder", "rating": 90, "base_price": 150},
        {"name": "Axar Patel", "role": "All-Rounder", "rating": 89, "base_price": 100},
        {"name": "Sunil Narine", "role": "All-Rounder", "rating": 92, "base_price": 100},
        {"name": "Andre Russell", "role": "All-Rounder", "rating": 91, "base_price": 150},
        {"name": "Glenn Maxwell", "role": "All-Rounder", "rating": 86, "base_price": 100},
        {"name": "Marcus Stoinis", "role": "All-Rounder", "rating": 86, "base_price": 75},
        {"name": "Liam Livingstone", "role": "All-Rounder", "rating": 85, "base_price": 75},
        {"name": "Sam Curran", "role": "All-Rounder", "rating": 85, "base_price": 100},
        {"name": "Cameron Green", "role": "All-Rounder", "rating": 86, "base_price": 100},
        {"name": "Krunal Pandya", "role": "All-Rounder", "rating": 82, "base_price": 50},
        {"name": "Nitish Kumar Reddy", "role": "All-Rounder", "rating": 83, "base_price": 20},
        {"name": "Abhishek Sharma", "role": "All-Rounder", "rating": 87, "base_price": 30},
        {"name": "Venkatesh Iyer", "role": "All-Rounder", "rating": 83, "base_price": 50},
        {"name": "Shivam Dube", "role": "All-Rounder", "rating": 86, "base_price": 50},
        {"name": "Washington Sundar", "role": "All-Rounder", "rating": 81, "base_price": 50},
        {"name": "Moeen Ali", "role": "All-Rounder", "rating": 82, "base_price": 50},
        {"name": "Mitchell Marsh", "role": "All-Rounder", "rating": 84, "base_price": 75},
        {"name": "Romario Shepherd", "role": "All-Rounder", "rating": 80, "base_price": 40},

        # --- WICKET-KEEPERS ---
        {"name": "MS Dhoni", "role": "Wicket-Keeper", "rating": 88, "base_price": 100},
        {"name": "Rishabh Pant", "role": "Wicket-Keeper", "rating": 91, "base_price": 200},
        {"name": "Sanju Samson", "role": "Wicket-Keeper", "rating": 89, "base_price": 100},
        {"name": "KL Rahul", "role": "Wicket-Keeper", "rating": 89, "base_price": 150},
        {"name": "Ishan Kishan", "role": "Wicket-Keeper", "rating": 86, "base_price": 100},
        {"name": "Nicholas Pooran", "role": "Wicket-Keeper", "rating": 92, "base_price": 150},
        {"name": "Quinton de Kock", "role": "Wicket-Keeper", "rating": 86, "base_price": 100},
        {"name": "Phil Salt", "role": "Wicket-Keeper", "rating": 88, "base_price": 75},
        {"name": "Jos Buttler", "role": "Wicket-Keeper", "rating": 91, "base_price": 150},
        {"name": "Dinesh Karthik", "role": "Wicket-Keeper", "rating": 82, "base_price": 50},
        {"name": "Jitesh Sharma", "role": "Wicket-Keeper", "rating": 81, "base_price": 30},
        {"name": "Dhruv Jurel", "role": "Wicket-Keeper", "rating": 83, "base_price": 20},
        {"name": "Abishek Porel", "role": "Wicket-Keeper", "rating": 80, "base_price": 20},
        {"name": "Anuj Rawat", "role": "Wicket-Keeper", "rating": 78, "base_price": 20},
        {"name": "Wriddhiman Saha", "role": "Wicket-Keeper", "rating": 79, "base_price": 30}
    ]
    random.shuffle(st.session_state.player_pool)

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
    st.session_state.timer_seconds = 10

# --- APP HEADER ---
st.title("🏏 IPL 100-Player Live Clock Auction")
st.markdown("Choose your team, start with **₹150.00 CR**, and bid before the **10-second timer** hits zero!")
st.divider()

# --- STAGE 1: SETUP & TEAM SELECTION ---
if st.session_state.game_stage == "setup":
    st.header("👥 League Setup & Team Selection")
    num_humans = st.slider("How many human players?", min_value=1, max_value=4, value=1)
    
    human_configs = []
    used_teams = []
    for i in range(num_humans):
        st.subheader(f"Player {i+1}")
        h_name = st.text_input(f"Manager Name", value=f"Manager {i+1}", key=f"h_name_{i}")
        available_choices = [team for team in TEAM_NAMES_POOL if team not in used_teams]
        selected_team = st.selectbox(f"Choose Franchise", options=available_choices, key=f"h_team_{i}")
        used_teams.append(selected_team)
        human_configs.append({"manager": h_name, "team": selected_team})
        
    if st.button("Initialize ₹150 CR League", type="primary"):
        teams = []
        for hc in human_configs:
            teams.append({
                "team_name": f"{hc['manager']}'s {hc['team']}", "is_human": True,
                "purse": 15000, "squad": [], "personality": "User", "points": 0
            })
        remaining_bot_names = [team for team in TEAM_NAMES_POOL if team not in used_teams]
        for bot_team in remaining_bot_names:
            teams.append({
                "team_name": f"{bot_team} (Bot)", "is_human": False,
                "purse": 15000, "squad": [], "personality": random.choice(BOT_PERSONALITIES), "points": 0
            })
        st.session_state.teams = teams
        st.session_state.game_stage = "auction"
        st.session_state.auction_index = 0
        st.session_state.timer_seconds = 10
        st.rerun()

# --- STAGE 2: LIVE AUCTION ROOM WITH TIMER ---
elif st.session_state.game_stage == "auction":
    idx = st.session_state.auction_index
    if idx >= len(st.session_state.player_pool):
        st.success("All players finished! Ready for the tournament dashboard?")
        if st.button("Proceed to Dashboard"):
            st.session_state.game_stage = "dashboard"
            st.rerun()
    else:
        player = st.session_state.player_pool[idx]
        
        if st.session_state.current_bid == 0:
            st.session_state.current_bid = player["base_price"]
            st.session_state.highest_bidder = None
            st.session_state.timer_seconds = 10
            st.session_state.log_msg = f"Next up: {player['name']}! Base price set at ₹{player['base_price']/100:.2f} CR."

        # --- TIMER ENGINE ---
        # Forces the browser tab to refresh every 1000 milliseconds (1 second)
        st_autorefresh(interval=1000, key="auction_timer")
        
        st.header("🔨 Live Auction Room")
        
        # Display the countdown clock visually
        if st.session_state.timer_seconds > 0:
            st.session_state.timer_seconds -= 1
            st.warning(f"⏳ Time Remaining: **{st.session_state.timer_seconds + 1} seconds**")
            st.progress(st.session_state.timer_seconds / 10)
        else:
            # TIME HAS RUN OUT! Auto-sell player to the current leader
            if st.session_state.highest_bidder:
                hb = st.session_state.highest_bidder
                for t in st.session_state.teams:
                    if t["team_name"] == hb["team_name"]:
                        t["purse"] -= st.session_state.current_bid
                        t["squad"].append(player)
                st.error(f"🔴 GONE! Hammer falls! {player['name']} SOLD to {hb['team_name']} for ₹{st.session_state.current_bid/100:.2f} CR!")
            else:
                st.error(f"🔴 UNSOLD! Time ran out and no one bid for {player['name']}.")
            
            # Reset clock variables for next player card
            time.sleep(2) # Give users a brief moment to read the sale alert banner
            st.session_state.auction_index += 1
            st.session_state.current_bid = 0
            st.session_state.highest_bidder = None
            st.session_state.timer_seconds = 10
            st.rerun()

        # Display Player Info & Price Metrics
        st.info(f"**Player ({idx+1}/100):** {player['name']} | **Role:** {player['role']} | **Skill OVR:** {player['rating']}")
        st.metric(label="Current High Bid", value=f"₹{st.session_state.current_bid/100:.2f} CR", 
                  delta=f"Held by: {st.session_state.highest_bidder['team_name'] if st.session_state.highest_bidder else 'None'}")
        
        st.caption(st.session_state.log_msg)
        
        # Bidding Buttons Interactivity
        human_teams = [t for t in st.session_state.teams if t["is_human"] and t["purse"] >= (st.session_state.current_bid + 50)]
        human_options = [t["team_name"] for t in human_teams]
        
        col1, col2 = st.columns(2)
        with col1:
            if human_options:
                bidding_manager = st.selectbox("Select Bidding Manager:", options=human_options)
                if st.button("Raise Bid (+₹50 L)", type="primary", use_container_width=True):
                    st.session_state.current_bid += 50
                    st.session_state.highest_bidder = next(t for t in st.session_state.teams if t["team_name"] == bidding_manager)
                    st.session_state.timer_seconds = 10  # RESET TIMER!
                    st.session_state.log_msg = f"{bidding_manager} raised bid to ₹{st.session_state.current_bid/100:.2f} CR!"
                    
                    # Bot counter mechanics check
                    bots = [t for t in st.session_state.teams if not t["is_human"] and t["purse"] >= (st.session_state.current_bid + 50)]
                    if bots and random.random() > 0.35:
                        counter_bot = random.choice(bots)
                        st.session_state.current_bid += 50
                        st.session_state.highest_bidder = counter_bot
                        st.session_state.timer_seconds = 10  # RESET TIMER AGAIN!
                        st.session_state.log_msg = f"🤖 {counter_bot['team_name']} instantly countered with ₹{st.session_state.current_bid/100:.2f} CR!"
                    st.rerun()
            else:
                st.write("No humans can afford this player.")
                
        with col2:
            st.write("---")
            if st.button("Skip / Let Bots Battle Out", type="secondary", use_container_width=True):
                # Immediate bot-vs-bot simulation step to speed up passing cards
                if st.session_state.highest_bidder is None:
                    bots = [t for t in st.session_state.teams if not t["is_human"] and t["purse"] >= st.session_state.current_bid]
                    for _ in range(random.randint(1, 6)):
                        if bots and random.random() > 0.3:
                            counter_bot = random.choice(bots)
                            st.session_state.current_bid += 50
                            st.session_state.highest_bidder = counter_bot
                            bots = [t for t in bots if t["purse"] >= (st.session_state.current_bid + 50)]
                        else: break
                st.session_state.timer_seconds = 0 # Forces immediate checkout settlement on loop run
                st.rerun()

# --- STAGE 3: DASHBOARD & SEASON SIMULATION ---
elif st.session_state.game_stage == "dashboard":
    st.header("📋 Tournament Leaderboard")
    
    if random.random() < 0.20:
        st.warning("🚨 **UNEXPECTED SEASON TWIST!**")
        twist_type = random.choice(["injury", "morale"])
        human_team = [t for t in st.session_state.teams if t["is_human"]][0]
        if twist_type == "injury" and human_team["squad"]:
            injured_p = random.choice(human_team["squad"])
            st.error(f"Medical Report: {injured_p['name']} is injured in training! Form rating dropped.")
        else:
            st.info("Management Update: Traveling fatigue caused a dip in recovery fitness. Morale shifts!")
            
    sorted_teams = sorted(st.session_state.teams, key=lambda x: x["points"], reverse=True)
    for t in sorted_teams:
        col_t, col_p, col_w = st.columns([2, 1, 1])
        with col_t: st.markdown(f"**{t['team_name']}** ({len(t['squad'])} players)")
        with col_p: st.markdown(f"🏆 {t['points']} Pts")
        with col_w: st.caption(f"Wallet: ₹{t['purse']/100:.2f} CR")
            
    st.divider()
    if st.button("Simulate Next Match Day 🏏", type="primary", use_container_width=True):
        random.shuffle(st.session_state.teams)
        for i in range(0, len(st.session_state.teams), 2):
            t1, t2 = st.session_state.teams[i], st.session_state.teams[i+1]
            p1_score = sum([p["rating"] for p in t1["squad"]]) + random.randint(-40, 40)
            p2_score = sum([p["rating"] for p in t2["squad"]]) + random.randint(-40, 40)
            if p1_score > p2_score: t1["points"] += 2
            elif p2_score > p1_score: t2["points"] += 2
            else:
                t1["points"] += 1
                t2["points"] += 1
        st.rerun()

    if st.button("Reset Tournament", type="secondary"):
        st.session_state.game_stage = "setup"
        st.session_state.teams = []
        st.rerun()
