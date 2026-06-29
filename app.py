import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# --- STYLES & CONFIG ---
st.set_page_config(page_title="IPL RPG Manager Simulator", page_icon="🏏", layout="centered")

# --- DATA POOLS ---
TEAM_NAMES_POOL = [
    "Mumbai Mavericks", "Chennai Kings", "Bangalore Blasters", 
    "Delhi Dynamos", "Kolkata Knights", "Gujarat Giants", 
    "Punjab Panthers", "Rajasthan Royals", "Lucknow Lions", "Hyderabad Heroes"
]

BOT_PERSONALITIES = ["Batting-Heavy", "Bowling-Heavy", "Youth-Focus", "Balanced"]

VENUES = [
    {"name": "M. Chinnaswamy Stadium (Bengaluru)", "desc": "💥 Flat Track Paradise! Batsmen get a massive +10 rating boost. Bowlers suffer.", "boost_role": "Batsman", "boost_amount": 10},
    {"name": "M. A. Chidambaram Stadium (Chepauk)", "desc": "🌀 Dry, Dusty Spin Turner! Spinners and clever bowlers get a +10 tactical edge.", "boost_role": "Bowler", "boost_amount": 10},
    {"name": "Wankhede Stadium (Mumbai)", "desc": "🌊 True Bounce & Sea Breeze! All-Rounders thrive under pressure here with a +8 boost.", "boost_role": "All-Rounder", "boost_amount": 8},
    {"name": "Narendra Modi Stadium (Ahmedabad)", "desc": "⚖️ Balanced Coliseum! Symmetrical boundaries favor a steady, disciplined game layout.", "boost_role": "Balanced", "boost_amount": 0}
]

# --- MASTER 200 REAL-WORLD PLAYER EXPLICIT DATABASE ---
if "player_pool" not in st.session_state:
    st.session_state.player_pool = [
        # === PURE BATSMEN (1 - 60) ===
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
        {"name": "David Miller", "role": "Batsman", "rating": 87, "base_price": 100},
        {"name": "Steve Smith", "role": "Batsman", "rating": 83, "base_price": 200},
        {"name": "Marnus Labuschagne", "role": "Batsman", "rating": 80, "base_price": 100},
        {"name": "Harry Brook", "role": "Batsman", "rating": 86, "base_price": 150},
        {"name": "Dawid Malan", "role": "Batsman", "rating": 82, "base_price": 75},
        {"name": "Rilee Rossouw", "role": "Batsman", "rating": 83, "base_price": 75},
        {"name": "Reeza Hendricks", "role": "Batsman", "rating": 81, "base_price": 50},
        {"name": "Finn Allen", "role": "Batsman", "rating": 84, "base_price": 75},
        {"name": "Glenn Phillips", "role": "Batsman", "rating": 85, "base_price": 50},
        {"name": "Alex Hales", "role": "Batsman", "rating": 83, "base_price": 75},
        {"name": "Chris Lynn", "role": "Batsman", "rating": 79, "base_price": 50},
        {"name": "Evain Lewis", "role": "Batsman", "rating": 80, "base_price": 50},
        {"name": "Brandon King", "role": "Batsman", "rating": 81, "base_price": 30},
        {"name": "Johnson Charles", "role": "Batsman", "rating": 79, "base_price": 30},
        {"name": "Pathum Nissanka", "role": "Batsman", "rating": 83, "base_price": 50},
        {"name": "Charith Asalanka", "role": "Batsman", "rating": 84, "base_price": 50},
        {"name": "Litton Das", "role": "Batsman", "rating": 78, "base_price": 50},
        {"name": "Najmul Hossain Shanto", "role": "Batsman", "rating": 79, "base_price": 30},
        {"name": "Ibrahim Zadran", "role": "Batsman", "rating": 82, "base_price": 50},
        {"name": "Najibullah Zadran", "role": "Batsman", "rating": 80, "base_price": 50},
        {"name": "Paul Stirling", "role": "Batsman", "rating": 78, "base_price": 50},
        {"name": "Harry Tector", "role": "Batsman", "rating": 81, "base_price": 30},
        {"name": "Karun Nair", "role": "Batsman", "rating": 79, "base_price": 30},
        {"name": "Anmolpreet Singh", "role": "Batsman", "rating": 76, "base_price": 20},
        {"name": "Subhranshu Senapati", "role": "Batsman", "rating": 75, "base_price": 20},
        {"name": "Atharva Taide", "role": "Batsman", "rating": 77, "base_price": 20},
        {"name": "Sameer Rizvi", "role": "Batsman", "rating": 81, "base_price": 30},
        {"name": "Kumar Kushagra", "role": "Batsman", "rating": 78, "base_price": 20},
        {"name": "Swastik Chikara", "role": "Batsman", "rating": 75, "base_price": 20},
        {"name": "Angkrish Raghuvanshi", "role": "Batsman", "rating": 80, "base_price": 20},

        # === PURE BOWLERS (61 - 120) ===
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
        {"name": "Josh Hazlewood", "role": "Bowler", "rating": 89, "base_price": 200},
        {"name": "Tim Southee", "role": "Bowler", "rating": 84, "base_price": 75},
        {"name": "Matt Henry", "role": "Bowler", "rating": 83, "base_price": 75},
        {"name": "Ish Sodhi", "role": "Bowler", "rating": 81, "base_price": 50},
        {"name": "Adil Rashid", "role": "Bowler", "rating": 85, "base_price": 75},
        {"name": "Reece Topley", "role": "Bowler", "rating": 83, "base_price": 75},
        {"name": "Mark Wood", "role": "Bowler", "rating": 86, "base_price": 150},
        {"name": "Gus Atkinson", "role": "Bowler", "rating": 82, "base_price": 100},
        {"name": "Tabraiz Shamsi", "role": "Bowler", "rating": 82, "base_price": 50},
        {"name": "Lungi Ngidi", "role": "Bowler", "rating": 83, "base_price": 75},
        {"name": "Gerald Coetzee", "role": "Bowler", "rating": 85, "base_price": 50},
        {"name": "Marco Jansen", "role": "Bowler", "rating": 86, "base_price": 75},
        {"name": "Alzarri Joseph", "role": "Bowler", "rating": 82, "base_price": 100},
        {"name": "Shamar Joseph", "role": "Bowler", "rating": 83, "base_price": 50},
        {"name": "Akeal Hosein", "role": "Bowler", "rating": 82, "base_price": 50},
        {"name": "Mujeeb Ur Rahman", "role": "Bowler", "rating": 84, "base_price": 100},
        {"name": "Naveen-ul-Haq", "role": "Bowler", "rating": 83, "base_price": 50},
        {"name": "Fazalhaq Farooqi", "role": "Bowler", "rating": 84, "base_price": 50},
        {"name": "Mustafizur Rahman", "role": "Bowler", "rating": 85, "base_price": 200},
        {"name": "Taskin Ahmed", "role": "Bowler", "rating": 81, "base_price": 75},
        {"name": "Dushmantha Chameera", "role": "Bowler", "rating": 79, "base_price": 50},
        {"name": "Dilshan Madushanka", "role": "Bowler", "rating": 82, "base_price": 50},
        {"name": "Nuwan Thushara", "role": "Bowler", "rating": 81, "base_price": 50},
        {"name": "Sandeep Warrier", "role": "Bowler", "rating": 77, "base_price": 20},
        {"name": "Chetan Sakariya", "role": "Bowler", "rating": 78, "base_price": 30},

        # === ALL-ROUNDERS (121 - 170) ===
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
        {"name": "Shakib Al Hasan", "role": "All-Rounder", "rating": 87, "base_price": 100},
        {"name": "Ben Stokes", "role": "All-Rounder", "rating": 88, "base_price": 200},
        {"name": "Chris Woakes", "role": "All-Rounder", "rating": 83, "base_price": 100},
        {"name": "Daryl Mitchell", "role": "All-Rounder", "rating": 87, "base_price": 100},
        {"name": "Rachin Ravindra", "role": "All-Rounder", "rating": 86, "base_price": 50},
        {"name": "Jimmy Neesham", "role": "All-Rounder", "rating": 81, "base_price": 75},
        {"name": "Mitchell Santner", "role": "All-Rounder", "rating": 84, "base_price": 50},
        {"name": "Wanindu Hasaranga", "role": "All-Rounder", "rating": 89, "base_price": 150},
        {"name": "Angelo Mathews", "role": "All-Rounder", "rating": 80, "base_price": 50},
        {"name": "Dasun Shanaka", "role": "All-Rounder", "rating": 79, "base_price": 50},
        {"name": "Dunith Wellalage", "role": "All-Rounder", "rating": 81, "base_price": 30},
        {"name": "Mohammad Nabi", "role": "All-Rounder", "rating": 83, "base_price": 75},
        {"name": "Azmatullah Omarzai", "role": "All-Rounder", "rating": 84, "base_price": 50},
        {"name": "Gulbadin Naib", "role": "All-Rounder", "rating": 81, "base_price": 50},
        {"name": "Jason Holder", "role": "All-Rounder", "rating": 82, "base_price": 100},
        {"name": "Kyle Mayers", "role": "All-Rounder", "rating": 83, "base_price": 75},
        {"name": "Roston Chase", "role": "All-Rounder", "rating": 80, "base_price": 50},
        {"name": "Mehidy Hasan Miraz", "role": "All-Rounder", "rating": 82, "base_price": 50},
        {"name": "Sikandar Raza", "role": "All-Rounder", "rating": 84, "base_price": 50},
        {"name": "Sean Williams", "role": "All-Rounder", "rating": 80, "base_price": 50},
        {"name": "Rishi Dhawan", "role": "All-Rounder", "rating": 77, "base_price": 30},
        {"name": "Shahbaz Ahmed", "role": "All-Rounder", "rating": 82, "base_price": 30},
        {"name": "Lalit Yadav", "role": "All-Rounder", "rating": 78, "base_price": 20},
        {"name": "Mahipal Lomror", "role": "All-Rounder", "rating": 81, "base_price": 20},
        {"name": "Ramandeep Singh", "role": "All-Rounder", "rating": 82, "base_price": 20},
        {"name": "Prerak Mankad", "role": "All-Rounder", "rating": 76, "base_price": 20},
        {"name": "Atharva Ankolekar", "role": "All-Rounder", "rating": 74, "base_price": 20},
        {"name": "Shams Mulani", "role": "All-Rounder", "rating": 78, "base_price": 20},
        {"name": "Raj Angad Bawa", "role": "All-Rounder", "rating": 76, "base_price": 20},
        {"name": "Nishant Sindhu", "role": "All-Rounder", "rating": 77, "base_price": 20},
        {"name": "Kamlesh Nagarkoti", "role": "All-Rounder", "rating": 76, "base_price": 30},

        # === WICKET-KEEPERS (171 - 200) ===
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
        {"name": "Wriddhiman Saha", "role": "Wicket-Keeper", "rating": 79, "base_price": 30},
        {"name": "Jonny Bairstow", "role": "Wicket-Keeper", "rating": 87, "base_price": 150},
        {"name": "Sam Billings", "role": "Wicket-Keeper", "rating": 82, "base_price": 100},
        {"name": "Tom Latham", "role": "Wicket-Keeper", "rating": 81, "base_price": 75},
        {"name": "Heinrich Klaasen", "role": "Wicket-Keeper", "rating": 93, "base_price": 150},
        {"name": "Ryan Rickelton", "role": "Wicket-Keeper", "rating": 82, "base_price": 50},
        {"name": "Rahmanullah Gurbaz", "role": "Wicket-Keeper", "rating": 85, "base_price": 50},
        {"name": "Kusal Mendis", "role": "Wicket-Keeper", "rating": 83, "base_price": 50},
        {"name": "Sadeera Samarawickrama", "role": "Wicket-Keeper", "rating": 81, "base_price": 30},
        {"name": "Mushfiqur Rahim", "role": "Wicket-Keeper", "rating": 80, "base_price": 50},
        {"name": "Shai Hope", "role": "Wicket-Keeper", "rating": 82, "base_price": 75},
        {"name": "Sarfaraz Khan", "role": "Wicket-Keeper", "rating": 81, "base_price": 30},
        {"name": "Narayan Jagadeesan", "role": "Wicket-Keeper", "rating": 79, "base_price": 20},
        {"name": "Sheldon Jackson", "role": "Wicket-Keeper", "rating": 78, "base_price": 20},
        {"name": "Baba Indrajith", "role": "Wicket-Keeper", "rating": 80, "base_price": 20},
        {"name": "Upul Tharanga", "role": "Wicket-Keeper", "rating": 81, "base_price": 50}
    ]
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
if "match_day" not in st.session_state:
    st.session_state.match_day = 1
if "current_venue" not in st.session_state:
    st.session_state.current_venue = random.choice(VENUES)
if "stats_runs" not in st.session_state:
    st.session_state.stats_runs = {}
if "stats_wickets" not in st.session_state:
    st.session_state.stats_wickets = {}
if "press_conference" not in st.session_state:
    st.session_state.press_conference = None

# --- FLOATING CORNER PURSE OVERLAY CSS ---
user_team = next((t for t in st.session_state.teams if t["is_human"]), None)
if user_team:
    st.markdown(f"""
        <div style='position: fixed; top: 70px; right: 20px; background: linear-gradient(135deg, #1E3A8A, #3B82F6); 
                    color: white; padding: 12px 20px; border-radius: 10px; font-weight: bold; 
                    box-shadow: 0px 4px 15px rgba(59, 130, 246, 0.5); z-index: 9999; border: 1px solid #60A5FA;'>
            💰 PURSE: ₹{user_team['purse']/100:.2f} CR
        </div>
    """, unsafe_allow_html=True)

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
                "tactic": "Balanced Alignment", "morale": 80
            })
        remaining_bot_names = [team for team in TEAM_NAMES_POOL if team not in used_teams]
        for bot_team in remaining_bot_names:
            teams.append({
                "team_name": f"{bot_team} (Bot)", "is_human": False,
                "purse": 15000, "squad": [], "personality": random.choice(BOT_PERSONALITIES), 
                "points": 0, "wins": 0, "losses": 0, "disqualified": False, 
                "targets": [], "playing_11": [], "impact_player": None,
                "tactic": "Balanced Alignment", "morale": 75
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
        st.success("All players indexed! Evaluating precise composition checks...")
        for t in st.session_state.teams:
            b_count = len([p for p in t["squad"] if p["role"] == "Batsman"])
            wk_count = len([p for p in t["squad"] if p["role"] == "Wicket-Keeper"])
            ar_count = len([p for p in t["squad"] if p["role"] == "All-Rounder"])
            bowl_count = len([p for p in t["squad"] if p["role"] == "Bowler"])
            
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
                    
                    b_count = len([p for p in t["squad"] if p["role"] == "Batsman"])
                    wk_count = len([p for p in t["squad"] if p["role"] == "Wicket-Keeper"])
                    ar_count = len([p for p in t["squad"] if p["role"] == "All-Rounder"])
                    bowl_count = len([p for p in t["squad"] if p["role"] == "Bowler"])
                    
                    if curr_p["role"] == "Batsman" and b_count >= 6: continue
                    if curr_p["role"] == "Wicket-Keeper" and wk_count >= 3: continue
                    if curr_p["role"] == "All-Rounder" and ar_count >= 4: continue
                    if curr_p["role"] == "Bowler" and bowl_count >= 6: continue
                    
                    is_target = curr_p["name"] in t.get("targets", [])
                    mult = 1.10
                    
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
    st.header(f"🏆 IPL Franchise Operations Hub — Day {st.session_state.match_day}/14")
    
    # Render current venue conditions
    st.markdown(f"""
        <div style='padding: 15px; border-radius: 8px; background-color: #1E1B4B; border: 1px solid #4338CA; margin-bottom: 20px;'>
            <h4 style='margin:0; color:#60A5FA;'>🏟️ NEXT VENUE: {st.session_state.current_venue['name']}</h4>
            <p style='margin:5px 0 0 0; font-size:14px; color:#E0E7FF;'>{st.session_state.current_venue['desc']}</p>
        </div>
    """, unsafe_allow_html=True)

    tab_table, tab_stats, tab_caps, tab_career = st.tabs(["📊 Tournament Standings Table", "🏏 Roster Performance Stats", "👑 Orange & Purple Caps", "👔 Manager Career Room"])
    
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
                    st.write(f"🌟 **Top Scorer:** {match['top_batsman']} ({match['runs']} runs)")
                with col_wck:
                    st.write(f"🎯 **Top Bowler:** {match['top_bowler']} ({match['wickets']} wickets)")
                st.divider()
        else:
            st.caption("No matches simulated yet. Head over to the Career Room to kick off match days!")

    # --- TAB 3: CAP RACE LEADERBOARDS ---
    with tab_caps:
        col_orange, col_purple = st.columns(2)
        with col_orange:
            st.markdown("### 🟠 Orange Cap Leaderboard")
            sorted_runs = sorted(st.session_state.stats_runs.items(), key=lambda x: x[1], reverse=True)[:5]
            if sorted_runs:
                for idx, (name, runs) in enumerate(sorted_runs):
                    st.write(f"**{idx+1}. {name}** — {runs} runs")
            else: st.caption("Awaiting first innings totals.")
        with col_purple:
            st.markdown("### 🟣 Purple Cap Leaderboard")
            sorted_wicks = sorted(st.session_state.stats_wickets.items(), key=lambda x: x[1], reverse=True)[:5]
            if sorted_wicks:
                for idx, (name, wck) in enumerate(sorted_wicks):
                    st.write(f"**{idx+1}. {name}** — {wck} wickets")
            else: st.caption("Awaiting first match spell wickets.")

    # --- TAB 4: MANAGER CAREER SUITE & TRADES ---
    with tab_career:
        user_team = next((t for t in st.session_state.teams if t["is_human"] and not t["disqualified"]), None)
        
        # Post Match Press Conferences Interceptor UI
        if st.session_state.press_conference:
            pc = st.session_state.press_conference
            st.warning(f"🎤 **CRITICAL PRESS CONFERENCE CONSOLE:** {pc['situation']}")
            for opt_key, opt_val in pc["options"].items():
                if st.button(opt_val["text"], key=f"pc_{opt_key}"):
                    user_team["morale"] = min(100, max(20, user_team["morale"] + opt_val["morale_effect"]))
                    st.success(opt_val["outcome"])
                    st.session_state.press_conference = None
                    st.rerun()
            st.stop()

        st.subheader("Operational Tactical Controls")
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

        # Mid-Season Trade Logic Injection (Locks active between day 4 and day 8)
        if 4 <= st.session_state.match_day <= 8:
            st.markdown("""
                <div style='padding:12px; background-color:#065F46; border:1px solid #047857; border-radius:6px; margin: 10px 0;'>
                    🤝 <strong>MID-SEASON TRANSFER WINDOW ACTIVE:</strong> Negotiate contracts using available purse liquidity.
                </div>
            """, unsafe_allow_html=True)
            
            ai_teams = [t for t in st.session_state.teams if not t["is_human"]]
            trade_team = ai_teams[st.session_state.match_day % len(ai_teams)]
            if trade_team["squad"]:
                target_p = trade_team["squad"][0]
                trade_cost = target_p["base_price"] * 2
                
                col_tr1, col_tr2 = st.columns([2, 1])
                with col_tr1:
                    st.write(f"Offer from **{trade_team['team_name']}**: Buy **{target_p['name']}** (OVR: {target_p['rating']}, {target_p['role']})")
                    st.write(f"Required Investment: ₹{trade_cost/100:.2f} CR")
                with col_tr2:
                    if user_team and user_team["purse"] >= trade_cost:
                        if st.button("🤝 Accept Trade Deal"):
                            user_team["purse"] -= trade_cost
                            trade_team["purse"] += trade_cost
                            trade_team["squad"].remove(target_p)
                            user_team["squad"].append(target_p)
                            st.success(f"Successfully signed {target_p['name']}!")
                            st.rerun()
                    else:
                        st.caption("Insufficient Pursc Liquility")
        
        st.divider()
        st.subheader("Simulate League Actions")
        active_squads = st.session_state.teams
        
        if len(active_squads) >= 2:
            if st.button("⚡ Simulate Next Match Fixtures", type="primary", use_container_width=True):
                twist_roll = random.random()
                if twist_roll < 0.25: 
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

                # Compute rock-paper-scissors tactic modifiers and pitch criteria boosts
                boost_role = st.session_state.current_venue["boost_role"]
                boost_amt = st.session_state.current_venue["boost_amount"]

                random.shuffle(active_squads)
                for i in range(0, len(active_squads) - 1, 2):
                    t1, t2 = active_squads[i], active_squads[i+1]
                    
                    t1_mod = 1.05 if t1["tactic"] == "Ultra-Aggressive Attack" and t2["tactic"] == "Balanced Alignment" else 1.0
                    t2_mod = 1.05 if t2["tactic"] == "Ultra-Aggressive Attack" and t1["tactic"] == "Balanced Alignment" else 1.0
                    if t1["tactic"] == "Defensive Anchor" and t2["tactic"] == "Ultra-Aggressive Attack": t1_mod = 1.05
                    if t2["tactic"] == "Defensive Anchor" and t1["tactic"] == "Ultra-Aggressive Attack": t2_mod = 1.05
                    
                    t1_base = sum([p["rating"] + (boost_amt if p["role"] == boost_role else 0) for p in t1["playing_11"]])
                    t2_base = sum([p["rating"] + (boost_amt if p["role"] == boost_role else 0) for p in t2["playing_11"]])

                    t1_power = t1_base * (t1["morale"] / 100) * t1_mod + random.randint(-40, 40)
                    t2_power = t2_base * (t2["morale"] / 100) * t2_mod + random.randint(-40, 40)
                    
                    all_batsmen = [p for p in t1["playing_11"] + t2["playing_11"] if p["role"] in ["Batsman", "Wicket-Keeper"]]
                    all_bowlers = [p for p in t1["playing_11"] + t2["playing_11"] if p["role"] in ["Bowler", "All-Rounder"]]
                    
                    top_bat = random.choice(all_batsmen)["name"] if all_batsmen else "Unknown Player"
                    top_bowl = random.choice(all_bowlers)["name"] if all_bowlers else "Unknown Player"
                    
                    runs_rolled = random.randint(45, 98)
                    wicks_rolled = random.randint(3, 5)

                    st.session_state.stats_runs[top_bat] = st.session_state.stats_runs.get(top_bat, 0) + runs_rolled
                    st.session_state.stats_wickets[top_bowl] = st.session_state.stats_wickets.get(top_bowl, 0) + wicks_rolled

                    if t1_power > t2_power:
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
                        "runs": runs_rolled,
                        "top_bowler": top_bowl,
                        "wickets": wicks_rolled
                    })

                # Setup Press Conference if Human Manager Lost
                user_check = next(t for t in st.session_state.teams if t["is_human"])
                last_match = st.session_state.match_history[-1]
                if user_check["team_name"] in last_match["fixture"] and "won" not in last_match["result"]:
                    st.session_state.press_conference = {
                        "situation": "Your squad suffered an embarrassing tactical loss today. Fans are demanding immediate accountability in front of the cameras!",
                        "options": {
                            "A": {"text": "🎙️ Blame the roster work ethic (-10% Morale, increases aggression)", "morale_effect": -10, "outcome": "Locker room atmosphere grew icy."},
                            "B": {"text": "🎙️ Absorb full blame yourself to protect players (+15% Morale)", "morale_effect": 15, "outcome": "Players respect your loyalty! Team morale boosted."}
                        }
                    }

                st.session_state.match_day += 1
                st.session_state.current_venue = random.choice(VENUES)
                st.rerun()
        else:
            st.error("Not enough qualified squads to run management fixtures.")

        if st.session_state.career_event:
            st.warning(st.session_state.career_event)
