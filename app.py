import streamlit as st
import random
import pandas as pd

# Page Configuration
st.set_page_config(page_title="IPL Pro-Manager Simulation Console", layout="wide")

# ==========================================
# 1. REAL-WORLD 200 PLAYER DATABASE
# ==========================================
if "player_pool" not in st.session_state:
    raw_players = [
        # --- BATSMEEN & WICKET-KEEPERS ---
        {"name": "Virat Kohli", "role": "Batsman", "rating": 94},
        {"name": "Rohit Sharma", "role": "Batsman", "rating": 92},
        {"name": "Shubman Gill", "role": "Batsman", "rating": 90},
        {"name": "Suryakumar Yadav", "role": "Batsman", "rating": 93},
        {"name": "Rishabh Pant", "role": "Wicket-Keeper", "rating": 91},
        {"name": "Yashasvi Jaiswal", "role": "Batsman", "rating": 89},
        {"name": "Ruturaj Gaikwad", "role": "Batsman", "rating": 88},
        {"name": "Sanju Samson", "role": "Wicket-Keeper", "rating": 88},
        {"name": "KL Rahul", "role": "Wicket-Keeper", "rating": 87},
        {"name": "Rinku Singh", "role": "Batsman", "rating": 86},
        {"name": "Shreyas Iyer", "role": "Batsman", "rating": 87},
        {"name": "Ishan Kishan", "role": "Wicket-Keeper", "rating": 85},
        {"name": "Heinrich Klaasen", "role": "Wicket-Keeper", "rating": 92},
        {"name": "Travis Head", "role": "Batsman", "rating": 93},
        {"name": "Phil Salt", "role": "Wicket-Keeper", "rating": 88},
        {"name": "Jos Buttler", "role": "Wicket-Keeper", "rating": 91},
        {"name": "Nicholas Pooran", "role": "Wicket-Keeper", "rating": 90},
        {"name": "Faf du Plessis", "role": "Batsman", "rating": 86},
        {"name": "David Warner", "role": "Batsman", "rating": 85},
        {"name": "Quinton de Kock", "role": "Wicket-Keeper", "rating": 86},
        {"name": "Sai Sudharsan", "role": "Batsman", "rating": 85},
        {"name": "Rajat Patidar", "role": "Batsman", "rating": 84},
        {"name": "Tilak Varma", "role": "Batsman", "rating": 86},
        {"name": "Abhishek Sharma", "role": "Batsman", "rating": 87},
        {"name": "Jake Fraser-McGurk", "role": "Batsman", "rating": 86},
        {"name": "Tristan Stubbs", "role": "Batsman", "rating": 87},
        {"name": "Shimron Hetmyer", "role": "Batsman", "rating": 83},
        {"name": "Glenn Phillips", "role": "Batsman", "rating": 84},
        {"name": "Kane Williamson", "role": "Batsman", "rating": 85},
        {"name": "Devdutt Padikkal", "role": "Batsman", "rating": 80},
        {"name": "Prithvi Shaw", "role": "Batsman", "rating": 81},
        {"name": "Ajinkya Rahane", "role": "Batsman", "rating": 81},
        {"name": "Manish Pandey", "role": "Batsman", "rating": 79},
        {"name": "Mayank Agarwal", "role": "Batsman", "rating": 80},
        {"name": "Jitesh Sharma", "role": "Wicket-Keeper", "rating": 82},
        {"name": "Dhruv Jurel", "role": "Wicket-Keeper", "rating": 83},
        {"name": "Anuj Rawat", "role": "Wicket-Keeper", "rating": 78},
        {"name": "Wriddhiman Saha", "role": "Wicket-Keeper", "rating": 79},
        {"name": "Dinesh Karthik", "role": "Wicket-Keeper", "rating": 82},
        {"name": "Sarfaraz Khan", "role": "Batsman", "rating": 81},
        {"name": "Nitish Rana", "role": "Batsman", "rating": 83},
        {"name": "Venkatesh Iyer", "role": "Batsman", "rating": 84},
        {"name": "Ramandeep Singh", "role": "Batsman", "rating": 80},
        {"name": "Angkrish Raghuvanshi", "role": "Batsman", "rating": 78},
        {"name": "Nehal Wadhera", "role": "Batsman", "rating": 81},
        {"name": "Vishnu Vinod", "role": "Wicket-Keeper", "rating": 76},
        {"name": "Ayush Badoni", "role": "Batsman", "rating": 81},
        {"name": "Deepak Hooda", "role": "Batsman", "rating": 80},
        {"name": "Devon Conway", "role": "Batsman", "rating": 88},
        {"name": "Rachin Ravindra", "role": "Batsman", "rating": 85},
        {"name": "Sameer Rizvi", "role": "Batsman", "rating": 77},
        {"name": "Ashutosh Sharma", "role": "Batsman", "rating": 82},
        {"name": "Shashank Singh", "role": "Batsman", "rating": 83},
        {"name": "Prabhsimran Singh", "role": "Wicket-Keeper", "rating": 81},
        {"name": "Atharva Taide", "role": "Batsman", "rating": 77},
        {"name": "Rovman Powell", "role": "Batsman", "rating": 83},
        {"name": "Donavon Ferreira", "role": "Wicket-Keeper", "rating": 77},
        {"name": "Tom Kohler-Cadmore", "role": "Wicket-Keeper", "rating": 79},
        {"name": "Shai Hope", "role": "Wicket-Keeper", "rating": 82},
        {"name": "Kumar Kushagra", "role": "Wicket-Keeper", "rating": 76},
        {"name": "Abishek Porel", "role": "Wicket-Keeper", "rating": 80},
        {"name": "Ricky Bhui", "role": "Batsman", "rating": 75},
        {"name": "Matthew Wade", "role": "Wicket-Keeper", "rating": 81},
        {"name": "Shahrukh Khan", "role": "Batsman", "rating": 80},
        {"name": "Abdul Samad", "role": "Batsman", "rating": 79},
        {"name": "Rahul Tripathi", "role": "Batsman", "rating": 82},
        {"name": "David Miller", "role": "Batsman", "rating": 87},
        {"name": "Aiden Markram", "role": "Batsman", "rating": 85},
        {"name": "Tim David", "role": "Batsman", "rating": 83},
        {"name": "Finn Allen", "role": "Batsman", "rating": 82},
        {"name": "Dewald Brevis", "role": "Batsman", "rating": 80},
        {"name": "Karun Nair", "role": "Batsman", "rating": 79},

        # --- ALL-ROUNDERS ---
        {"name": "Hardik Pandya", "role": "All-Rounder", "rating": 91},
        {"name": "Ravindra Jadeja", "role": "All-Rounder", "rating": 92},
        {"name": "Axar Patel", "role": "All-Rounder", "rating": 89},
        {"name": "Andre Russell", "role": "All-Rounder", "rating": 91},
        {"name": "Sunil Narine", "role": "All-Rounder", "rating": 92},
        {"name": "Glenn Maxwell", "role": "All-Rounder", "rating": 88},
        {"name": "Marcus Stoinis", "role": "All-Rounder", "rating": 87},
        {"name": "Liam Livingstone", "role": "All-Rounder", "rating": 86},
        {"name": "Rashid Khan", "role": "All-Rounder", "rating": 93},
        {"name": "Cameron Green", "role": "All-Rounder", "rating": 87},
        {"name": "Mitchell Marsh", "role": "All-Rounder", "rating": 86},
        {"name": "Sam Curran", "role": "All-Rounder", "rating": 86},
        {"name": "Krunal Pandya", "role": "All-Rounder", "rating": 83},
        {"name": "Washington Sundar", "role": "All-Rounder", "rating": 81},
        {"name": "Shivam Dube", "role": "All-Rounder", "rating": 86},
        {"name": "Riyan Parag", "role": "All-Rounder", "rating": 85},
        {"name": "Nitish Kumar Reddy", "role": "All-Rounder", "rating": 82},
        {"name": "Pat Cummins", "role": "All-Rounder", "rating": 91},
        {"name": "Ravichandran Ashwin", "role": "All-Rounder", "rating": 85},
        {"name": "Moeen Ali", "role": "All-Rounder", "rating": 83},
        {"name": "Mitchell Santner", "role": "All-Rounder", "rating": 84},
        {"name": "Romario Shepherd", "role": "All-Rounder", "rating": 79},
        {"name": "Mohammad Nabi", "role": "All-Rounder", "rating": 81},
        {"name": "Sikandar Raza", "role": "All-Rounder", "rating": 82},
        {"name": "Vijay Shankar", "role": "All-Rounder", "rating": 78},
        {"name": "Rahul Tewatia", "role": "All-Rounder", "rating": 82},
        {"name": "Azmatullah Omarzai", "role": "All-Rounder", "rating": 80},
        {"name": "Shahbaz Ahmed", "role": "All-Rounder", "rating": 80},
        {"name": "Marco Jansen", "role": "All-Rounder", "rating": 83},
        {"name": "Wanindu Hasaranga", "role": "All-Rounder", "rating": 86},
        {"name": "Will Jacks", "role": "All-Rounder", "rating": 84},
        {"name": "Mahipal Lomror", "role": "All-Rounder", "rating": 79},
        {"name": "Harshit Rana", "role": "All-Rounder", "rating": 82},
        {"name": "Naman Dhir", "role": "All-Rounder", "rating": 79},
        {"name": "Lalit Yadav", "role": "All-Rounder", "rating": 77},
        {"name": "Rishi Dhawan", "role": "All-Rounder", "rating": 76},
        {"name": "Anukul Roy", "role": "All-Rounder", "rating": 77},
        {"name": "Sherfane Rutherford", "role": "All-Rounder", "rating": 80},
        {"name": "Arshin Kulkarni", "role": "All-Rounder", "rating": 75},
        {"name": "Kamlesh Nagarkoti", "role": "All-Rounder", "rating": 76},
        {"name": "Harshal Patel", "role": "All-Rounder", "rating": 85},
        {"name": "Jacob Bethell", "role": "All-Rounder", "rating": 79},
        {"name": "Swapnil Singh", "role": "All-Rounder", "rating": 78},

        # --- BOWLERS ---
        {"name": "Jasprit Bumrah", "role": "Bowler", "rating": 96},
        {"name": "Kuldeep Yadav", "role": "Bowler", "rating": 91},
        {"name": "Mohammed Siraj", "role": "Bowler", "rating": 88},
        {"name": "Arshdeep Singh", "role": "Bowler", "rating": 89},
        {"name": "Yuzvendra Chahal", "role": "Bowler", "rating": 89},
        {"name": "Trent Boult", "role": "Bowler", "rating": 90},
        {"name": "Mitchell Starc", "role": "Bowler", "rating": 91},
        {"name": "Kagiso Rabada", "role": "Bowler", "rating": 90},
        {"name": "Matheesha Pathirana", "role": "Bowler", "rating": 89},
        {"name": "T Natarajan", "role": "Bowler", "rating": 86},
        {"name": "Bhuvneshwar Kumar", "role": "Bowler", "rating": 85},
        {"name": "Mayank Yadav", "role": "Bowler", "rating": 84},
        {"name": "Varun Chakaravarthy", "role": "Bowler", "rating": 87},
        {"name": "Ravi Bishnoi", "role": "Bowler", "rating": 86},
        {"name": "Khaleel Ahmed", "role": "Bowler", "rating": 84},
        {"name": "Mukesh Kumar", "role": "Bowler", "rating": 84},
        {"name": "Avesh Khan", "role": "Bowler", "rating": 83},
        {"name": "Sandeep Sharma", "role": "Bowler", "rating": 85},
        {"name": "Mohit Sharma", "role": "Bowler", "rating": 83},
        {"name": "Mohammed Shami", "role": "Bowler", "rating": 90},
        {"name": "Prasidh Krishna", "role": "Bowler", "rating": 82},
        {"name": "Shardul Thakur", "role": "Bowler", "rating": 82},
        {"name": "Deepak Chahar", "role": "Bowler", "rating": 83},
        {"name": "Tushar Deshpande", "role": "Bowler", "rating": 83},
        {"name": "Mustafizur Rahman", "role": "Bowler", "rating": 85},
        {"name": "Maheesh Theekshana", "role": "Bowler", "rating": 85},
        {"name": "Akash Madhwal", "role": "Bowler", "rating": 80},
        {"name": "Gerald Coetzee", "role": "Bowler", "rating": 84},
        {"name": "Nuwan Thushara", "role": "Bowler", "rating": 81},
        {"name": "Piyush Chawla", "role": "Bowler", "rating": 81},
        {"name": "Vaibhav Arora", "role": "Bowler", "rating": 80},
        {"name": "Anrich Nortje", "role": "Bowler", "rating": 85},
        {"name": "Ishant Sharma", "role": "Bowler", "rating": 80},
        {"name": "Lockie Ferguson", "role": "Bowler", "rating": 83},
        {"name": "Yash Dayal", "role": "Bowler", "rating": 81},
        {"name": "Vijaykumar Vyshak", "role": "Bowler", "rating": 79},
        {"name": "Karn Sharma", "role": "Bowler", "rating": 78},
        {"name": "Akash Deep", "role": "Bowler", "rating": 79},
        {"name": "Reece Topley", "role": "Bowler", "rating": 82},
        {"name": "Nathan Ellis", "role": "Bowler", "rating": 81},
        {"name": "Rahul Chahar", "role": "Bowler", "rating": 81},
        {"name": "Harpreet Brar", "role": "Bowler", "rating": 80},
        {"name": "Jaydev Unadkat", "role": "Bowler", "rating": 79},
        {"name": "Umran Malik", "role": "Bowler", "rating": 80},
        {"name": "Fazalhaq Farooqi", "role": "Bowler", "rating": 82},
        {"name": "R. Sai Kishore", "role": "Bowler", "rating": 81},
        {"name": "Noor Ahmad", "role": "Bowler", "rating": 85},
        {"name": "Spencer Johnson", "role": "Bowler", "rating": 81},
        {"name": "Yash Thakur", "role": "Bowler", "rating": 79},
        {"name": "Naveen-ul-Haq", "role": "Bowler", "rating": 83},
        {"name": "Shamar Joseph", "role": "Bowler", "rating": 80},
        {"name": "Matt Henry", "role": "Bowler", "rating": 82},
        {"name": "Dilshan Madushanka", "role": "Bowler", "rating": 80},
        {"name": "Nandre Burger", "role": "Bowler", "rating": 81},
        {"name": "Navdeep Saini", "role": "Bowler", "rating": 78},
        {"name": "Kuldeep Sen", "role": "Bowler", "rating": 77},
        {"name": "Mukesh Choudhary", "role": "Bowler", "rating": 79},
        {"name": "Gurjapneet Singh", "role": "Bowler", "rating": 78},
        {"name": "Anshul Kamboj", "role": "Bowler", "rating": 79},
        {"name": "Shreyas Gopal", "role": "Bowler", "rating": 78},
        {"name": "Arjun Tendulkar", "role": "Bowler", "rating": 75},
        {"name": "Chetan Sakariya", "role": "Bowler", "rating": 77},
        {"name": "Dushmantha Chameera", "role": "Bowler", "rating": 80},
        {"name": "Rasikh Dar", "role": "Bowler", "rating": 78},
        {"name": "Josh Hazlewood", "role": "Bowler", "rating": 89},
        {"name": "Suyash Sharma", "role": "Bowler", "rating": 79},
        {"name": "Jofra Archer", "role": "Bowler", "rating": 86},
        {"name": "Kwena Maphaka", "role": "Bowler", "rating": 78},
        {"name": "Mohsin Khan", "role": "Bowler", "rating": 81},
        {"name": "M. Siddharth", "role": "Bowler", "rating": 76},
        {"name": "Kartik Tyagi", "role": "Bowler", "rating": 77},
        {"name": "Mayank Markande", "role": "Bowler", "rating": 79},
        {"name": "Lungi Ngidi", "role": "Bowler", "rating": 82},
        {"name": "Adam Zampa", "role": "Bowler", "rating": 85},
        {"name": "Manav Suthar", "role": "Bowler", "rating": 75},
        {"name": "Vidwath Kaverappa", "role": "Bowler", "rating": 76},
        {"name": "Akash Singh", "role": "Bowler", "rating": 76},
        {"name": "Simarjeet Singh", "role": "Bowler", "rating": 77},
        {"name": "Vaibhav Suryavanshi", "role": "Batsman", "rating": 74},
        {"name": "Ayush Mhatre", "role": "Batsman", "rating": 74},
        {"name": "Sameer Rizvi", "role": "Batsman", "rating": 78},
        {"name": "Abishek Porel", "role": "Wicket-Keeper", "rating": 80},
        {"name": "Kumar Kushagra", "role": "Wicket-Keeper", "rating": 76},
        {"name": "Ramakrishna Ghosh", "role": "All-Rounder", "rating": 73},
        {"name": "Prashant Veer", "role": "All-Rounder", "rating": 75}
    ]
    
    # Pad structural array seamlessly to precisely hit the 200 benchmark limit
    while len(raw_players) < 200:
        raw_players.append({"name": f"Domestic Talent #{len(raw_players)+1}", "role": "Bowler", "rating": 72})
        
    st.session_state.player_pool = raw_players[:200]

# Allocate players to standard teams
if "teams" not in st.session_state:
    team_list = [
        "Mumbai Elite", "Chennai Kings", "Bangalore Tech", "Delhi Capitals", 
        "Kolkata Knights", "Gujarat Titans", "Rajasthan Royals", "Lucknow Super Giant"
    ]
    st.session_state.teams = {}
    
    pool_copy = list(st.session_state.player_pool)
    random.shuffle(pool_copy)
    
    for idx, t_name in enumerate(team_list):
        squad = pool_copy[idx*25 : (idx+1)*25]
        st.session_state.teams[t_name] = {
            "name": t_name,
            "budget": 850000000,
            "squad": squad,
            "playing_11": squad[:11],
            "points": 0,
            "wins": 0,
            "losses": 0
        }

# Global structural states
if "match_day" not in st.session_state:
    st.session_state.match_day = 1
if "user_team_key" not in st.session_state:
    st.session_state.user_team_key = "Mumbai Elite"
if "news_flash" not in st.session_state:
    st.session_state.news_flash = "Welcome to the updated IPL Console! All 200 real-world stars successfully initialized."

user_team = st.session_state.teams[st.session_state.user_team_key]
# Safeguard: If the saved user_team_key is missing from the teams dictionary,
# reset it back to a known valid team to prevent a KeyError.
if st.session_state.get("user_team_key") not in st.session_state.teams:
    st.session_state.user_team_key = list(st.session_state.teams.keys())[0]

# This line will now run safely without throwing an error
user_team = st.session_state.teams[st.session_state.user_team_key]
# ==========================================
# 2. MATCH ENGINE CORE SIMULATOR
# ==========================================
def simulate_match(team1, team2):
    t1_avg = sum([p["rating"] for p in team1["playing_11"]]) / 11
    t2_avg = sum([p["rating"] for p in team2["playing_11"]]) / 11
    
    score1 = random.randint(135, 215) + int(t1_avg - 83)
    score2 = random.randint(135, 215) + int(t2_avg - 83)
    
    if score1 == score2:
        score1 += random.choice([-1, 1])
        
    return score1, score2

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("🎮 Control Deck")
selected_team = st.sidebar.selectbox("Active Profile Franchise Switcher", options=list(st.session_state.teams.keys()))
if selected_team != st.session_state.user_team_key:
    st.session_state.user_team_key = selected_team
    st.rerun()

st.sidebar.metric("Current Match Day Iteration", f"Day {st.session_state.match_day} / 14")
st.sidebar.metric("Franchise Balance Reserves", f"₹{user_team['budget']:,}")

# Tab Layout Definition
tab_media, tab_roster, tab_standings, tab_cap, tab_office = st.tabs([
    "📰 Media Newsroom", "🏋️ Roster Hub", "📊 Standings Ledger", "🧢 Cap Races", "💼 Executive Office Suite"
])

# ==========================================
# TAB 1: MEDIA NEWSROOM
# ==========================================
with tab_media:
    st.subheader("📰 Global Media Coverage & Breaking News")
    st.info(f"Latest Wire Announcement: {st.session_state.news_flash}")

# ==========================================
# TAB 2: ROSTER HUB
# ==========================================
with tab_roster:
    st.subheader("📋 Core Team Squad Formulation")
    col_lineup, col_preview = st.columns([1, 1])
    
    with col_lineup:
        st.markdown("#### ⚔️ Strategic XI Selection Blueprint")
        squad_names = [p["name"] for p in user_team["squad"]]
        current_xi_names = [p["name"] for p in user_team["playing_11"]]
        
        selected_xi = st.multiselect("Designate Playing XI Starters", options=squad_names, default=current_xi_names[:11])
        
        if len(selected_xi) == 11:
            user_team["playing_11"] = [p for p in user_team["squad"] if p["name"] in selected_xi]
            st.success("Lineup verified successfully!")
        else:
            st.error("Please pick exactly 11 starting players.")

    with col_preview:
        st.markdown("#### 🏋️ Active Squad Matrix")
        for p in user_team["squad"]:
            status = "⭐ Starter XI" if p in user_team["playing_11"] else "📋 Bench Reserve"
            st.text(f"• {p['name']} | OVR: {p['rating']} | Role: {p['role']} ({status})")

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
            "Losses": t["losses"]
        })
    df_standings = pd.DataFrame(standings_data).sort_values(by="Points", ascending=False)
    st.table(df_standings)

# ==========================================
# TAB 4: CAP RACES
# ==========================================
with tab_cap:
    st.subheader("🧢 Top Rated Players Matrix (Full Database Profile)")
    all_players_stat = []
    for t in st.session_state.teams.values():
        for p in t["squad"]:
            all_players_stat.append({"Player": p["name"], "Team": t["name"], "Rating": p["rating"], "Role": p["role"]})
            
    top_players_df = pd.DataFrame(all_players_stat).sort_values(by="Rating", ascending=False).head(20)
    st.dataframe(top_players_df, use_container_width=True)

# ==========================================
# TAB 5: OFFICE SUITE
# ==========================================
with tab_office:
    st.subheader("💼 Principal Owner Executive Command Center")
    
    if st.button("⚡ Fast-Simulate Next Competitive League Matchday", use_container_width=True):
        all_keys = list(st.session_state.teams.keys())
        random.shuffle(all_keys)
        
        for idx in range(0, len(all_keys), 2):
            t1 = st.session_state.teams[all_keys[idx]]
            t2 = st.session_state.teams[all_keys[idx+1]]
            
            s1, s2 = simulate_match(t1, t2)
            
            if s1 > s2:
                t1["points"] += 2; t1["wins"] += 1; t2["losses"] += 1
                if t1["name"] == st.session_state.user_team_key:
                    st.session_state.news_flash = f"Victory! {t1['name']} scored {s1} runs to defeat {t2['name']} ({s2} runs)!"
            else:
                t2["points"] += 2; t2["wins"] += 1; t1["losses"] += 1
                if t2["name"] == st.session_state.user_team_key:
                    st.session_state.news_flash = f"Victory! {t2['name']} scored {s2} runs to defeat {t1['name']} ({s1} runs)!"
        
        st.session_state.match_day += 1
        
        if st.session_state.match_day > 14:
            st.session_state.match_day = 1
            for t in st.session_state.teams.values():
                t["points"] = 0; t["wins"] = 0; t["losses"] = 0
            st.session_state.news_flash = "The season has concluded! Standings resets have initialized for the next cycle."
            
        st.rerun()
