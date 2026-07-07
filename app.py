import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# --- PREMIUM DASHBOARD CONFIGURATION ---
st.set_page_config(page_title="IPL Ultimate RPG Manager Simulator", page_icon="🏏", layout="wide")

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

def get_player_trait(player):
    if player["rating"] >= 93: return "👑 Legendary Icon Master"
    if player["rating"] <= 80: return "🌱 Debutant Prospect"
    if player["role"] == "Batsman": return "💥 Aggressive Finisher" if player["rating"] >= 88 else "🏏 Technical Batter"
    elif player["role"] == "Bowler": return "🔥 Express Speed Bowler" if player["rating"] >= 88 else "🎯 Line Bowler"
    elif player["role"] == "All-Rounder": return "🔀 Clutch All-Rounder"
    elif player["role"] == "Wicket-Keeper": return "🧤 Fast Stumper"
    return "🏏 Steady Asset"

# --- ASSET INSPECTION PROFILE DIALOG ---
@st.dialog("🔍 Scout Inspection Profile")
def inspect_player_dialog(player_obj):
    st.markdown(f"### {player_obj['name']}")
    st.markdown(f"**Specialty Role:** {player_obj['role']}")
    st.markdown(f"**Base Evaluation Skill Rating:** {player_obj['rating']} OVR")
    st.markdown(f"**Tactical Scout Trait:** `{get_player_trait(player_obj)}`")

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
if "live_match_state" not in st.session_state:
    st.session_state.live_match_state = None

# --- STYLING CUSTOM MATRIX RULES (THE PURE DESIGN REHAUL) ---
st.markdown("""
    <style>
    .stApp { background-color: #05070F !important; }
    h1, h2, h3, h4, h5, p, label, .stText, [data-testid="stMetricValue"] { color: #FFFFFF !important; }
    
    /* Sleek KPI Cards Styling */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #0F172A, #1E293B) !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
    }
    
    /* Glassmorphism News Cards */
    .news-box {
        padding: 24px;
        border-radius: 16px;
        background-color: #0F172A;
        border: 1px solid #1E293B;
        border-left: 6px solid #2563EB;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    }
    
    .news-title { font-size: 18px !important; font-weight: bold; color: #60A5FA !important; margin-bottom: 6px; }
    .news-headline { font-size: 22px !important; font-weight: 800; color: #FFFFFF !important; line-height: 1.3; }
    
    /* Customization for Select Boxes & Controls */
    div[data-baseweb="select"] > div { background-color: #1E293B !important; color: white !important; border: 1px solid #475569 !important; border-radius: 8px !important; }
    
    /* Modernized Button Architecture */
    .stButton button {
        background: linear-gradient(135deg, #1E293B, #334155) !important;
        color: #FFFFFF !important;
        border: 1px solid #475569 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
        border-color: #3B82F6 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37,99,235,0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --- FLOATING CORNER PURSE OVERLAY CSS ---
active_humans = [t for t in st.session_state.teams if t["is_human"]]
if active_humans:
    purse_texts = "<br/>".join([f"{h['team_name'].split('\'s ')[0]}: ₹{h['purse']/100:.2f}CR" for h in active_humans])
    st.markdown(f"""
        <div style='position: fixed; top: 70px; right: 20px; background: linear-gradient(135deg, #1E3A8A, #3B82F6); 
                    color: white; padding: 12px 20px; border-radius: 10px; font-weight: bold; 
                    box-shadow: 0px 4px 15px rgba(59, 130, 246, 0.5); z-index: 9999; border: 1px solid #60A5FA; font-size:12px;'>
            💰 SQUAD PURSES:<br/>{purse_texts}
        </div>
    """, unsafe_allow_html=True)

# --- STAGE 1: SETUP ---
if st.session_state.game_stage == "setup":
    st.header("👑 IPL Premium Draft Room Manager")
    num_humans = st.slider("How many human players?", min_value=1, max_value=4, value=1)
    
    human_configs = []
    used_teams = []
    for i in range(num_humans):
        st.subheader(f"Player {i+1} Configuration")
        h_name = st.text_input(f"Manager Name", value=f"Manager {i+1}", key=f"h_name_{i}")
        available_choices = [team for team in TEAM_NAMES_POOL if team not in used_teams]
        selected_team = st.selectbox(f"Choose Franchise", options=available_choices, key=f"h_team_{i}")
        used_teams.append(selected_team)
        human_configs.append({"manager": h_name, "team": selected_team})
        
    if st.button("Initialize Tournament League", type="primary"):
        teams = []
        for hc in human_configs:
            teams.append({
                "team_name": f"{hc['manager']}'s {hc['team']}", "is_human": True, "purse": 15000, "squad": [], 
                "points": 0, "wins": 0, "losses": 0, "disqualified": False, "playing_11": [], "impact_player": None, "tactic": "Balanced Alignment", "morale": 80
            })
        for bot_team in [t for t in TEAM_NAMES_POOL if t not in used_teams]:
            teams.append({
                "team_name": f"{bot_team} (Bot)", "is_human": False, "purse": 15000, "squad": [], 
                "personality": random.choice(BOT_PERSONALITIES), "points": 0, "wins": 0, "losses": 0, "disqualified": False, "playing_11": [], "impact_player": None, "tactic": "Balanced Alignment", "morale": 75
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
        st.success("Draft Concluded! Setting up league grids...")
        for t in st.session_state.teams:
            sorted_squad = sorted(t["squad"], key=lambda x: x["rating"], reverse=True)
            t["playing_11"] = sorted_squad[:11] if len(sorted_squad) >= 11 else sorted_squad
            t["impact_player"] = sorted_squad[11] if len(sorted_squad) > 11 else None
        st.session_state.game_stage = "dashboard"
        st.rerun()
    else:
        player = st.session_state.player_pool[idx]
        reasonable_val = get_reasonable_val(player, idx)
        if st.session_state.current_bid == 0:
            st.session_state.current_bid = player["base_price"]
            st.session_state.highest_bidder = None
            st.session_state.timer_seconds = 4
            st.session_state.log_msg = f"Next up: {player['name']}!"

        st_autorefresh(interval=1000, key="auction_timer")
        st.markdown(f"<div class='big-font'>🔨 LIVE AUCTION CARD ({idx+1}/{len(st.session_state.player_pool)})</div>", unsafe_allow_html=True)
        
        if st.button("⚡ Fast-Track Rest of Auction", type="secondary", use_container_width=True):
            while st.session_state.auction_index < len(st.session_state.player_pool):
                curr_idx = st.session_state.auction_index
                curr_p = st.session_state.player_pool[curr_idx]
                for t in st.session_state.teams:
                    if len(t["squad"]) < 20 and t["purse"] >= curr_p["base_price"]:
                        t["purse"] -= curr_p["base_price"]
                        t["squad"].append(curr_p)
                        break
                st.session_state.auction_index += 1
            st.rerun()

        if st.session_state.timer_seconds > 0:
            st.session_state.timer_seconds -= 1
            bots = [t for t in st.session_state.teams if not t["is_human"] and len(t["squad"]) < 20 and t["purse"] >= (st.session_state.current_bid + 50)]
            if bots and random.random() < 0.45: 
                valid_bots = [b for b in bots if st.session_state.highest_bidder is None or b["team_name"] != st.session_state.highest_bidder["team_name"]]
                if valid_bots:
                    counter_bot = random.choice(valid_bots)
                    st.session_state.current_bid += 50
                    st.session_state.highest_bidder = counter_bot
                    st.session_state.timer_seconds = 4  
                    st.rerun()
        else:
            if st.session_state.highest_bidder:
                st.session_state.highest_bidder["purse"] -= st.session_state.current_bid
                st.session_state.highest_bidder["squad"].append(player)
            else:
                cb = [t for t in st.session_state.teams if len(t["squad"]) < 20 and t["purse"] >= player["base_price"]]
                if cb:
                    assigned = random.choice(cb)
                    assigned["purse"] -= player["base_price"]
                    assigned["squad"].append(player)
            st.session_state.auction_index += 1
            st.session_state.current_bid = 0
            st.session_state.highest_bidder = None
            st.session_state.timer_seconds = 4
            st.rerun()

        st.markdown(f"<div class='timer-text'>⏳ GAVEL FALLING IN: {st.session_state.timer_seconds + 1}s</div>", unsafe_allow_html=True)
        st.progress(st.session_state.timer_seconds / 4)

        st.markdown(f"<div class='card-box'><strong>🏃 Active Asset:</strong> {player['name']} | <strong>📊 Rating:</strong> {player['rating']}<br/><em>Trait: {get_player_trait(player)}</em></div>", unsafe_allow_html=True)
        human_teams_bidding = [t for t in st.session_state.teams if t["is_human"] and t["purse"] >= (st.session_state.current_bid + 50)]
        if human_teams_bidding:
            if st.button("Raise Bid (+₹50 L)", type="primary", use_container_width=True):
                st.session_state.current_bid += 50
                st.session_state.highest_bidder = human_teams_bidding[0]
                st.session_state.timer_seconds = 4  
                st.rerun()

# --- STAGE 3: MAIN RPG PORTAL INTERFACE ---
elif st.session_state.game_stage == "dashboard":
    
    # --- INTERACTIVE ARENA OVERLAY MATRIX ---
    if st.session_state.live_match_state:
        ms = st.session_state.live_match_state
        st.header(f"🏏 LIVE SIMULATION: {ms['user_team']} vs {ms['opp_team']}")
        st.subheader(f"Score: {ms['score']}/{ms['wickets']} ({ms['balls'] // 6}.{ms['balls'] % 6} Overs) | Target: {ms['target']}")
        if ms['log']: st.code(ms['log'])

        if ms['wickets'] >= 10 or ms['balls'] >= 12 or (ms['innings'] == 2 and ms['score'] >= ms['target']):
            user_won = ms['score'] >= ms['target'] if ms['innings'] == 2 else ms['score'] > ms['target']
            u_t = next(t for t in st.session_state.teams if t["team_name"] == ms['user_team'])
            o_t = next(t for t in st.session_state.teams if t["team_name"] == ms['opp_team'])
            
            margin_text = f"by {ms['score'] - ms['target']} runs" if ms['innings'] == 1 else f"by {10 - ms['wickets']} wickets"
            result_headline = f"{ms['user_team'] if user_won else ms['opp_team']} won {margin_text}!"
            
            if user_won:
                u_t["points"] += 2; u_t["wins"] += 1; u_t["morale"] = min(100, u_t["morale"] + 8)
                o_t["losses"] += 1
            else:
                o_t["points"] += 2; o_t["wins"] += 1; u_t["losses"] += 1; u_t["morale"] = max(20, u_t["morale"] - 10)
                
            if st.button("Complete Match & Save Scorecard"):
                st.session_state.match_history.append({
                    "fixture": f"{ms['user_team']} vs {ms['opp_team']}", 
                    "result": result_headline,
                    "top_batsman": "Roster Ace", "runs": ms['score'],
                    "top_bowler": "Strike Bowler", "wickets": ms['wickets'],
                    "detailed": True, "team1_score": f"{ms['score']}/{ms['wickets']}", "team2_score": f"{ms['target']}"
                })
                st.session_state.match_day += 1
                st.session_state.live_match_state = None
                st.session_state.current_venue = random.choice(VENUES)
                st.rerun()
            st.stop()

        col_act, col_mind = st.columns(2)
        with col_act: shot_intent = st.selectbox("Tactic Strategy Line:", ["Aggressive Lofted Hit", "Controlled Placement Shot", "Defensive Block Target"])
        with col_mind: mindset = st.selectbox("Manager Directive Focus:", ["High-Risk Drive", "Calculated Hold", "Conservative Play"])

        if st.button("⚾ Run Next Delivery", type="primary", use_container_width=True):
            r = random.random()
            if "Aggressive" in shot_intent:
                if r < 0.35: ms['score'] += 6; ms['log'] = "🚀 SIX! Clean lofted strike sailing into the stands!"
                elif r < 0.55: ms['wickets'] += 1; ms['log'] = "☝️ OUT! Holed out to long-on attempting the big hit!"
                else: ms['score'] += 1; ms['log'] = "Top edge falls safe. Picked up a single."
            else:
                ms['score'] += random.choice([0, 1, 2, 4]); ms['log'] = "Pushed into gaps for steady runs."
            ms['balls'] += 1
            st.rerun()
        st.stop()

    # VENUE DESIGN METADATA
    st.markdown(f"""
        <div style='padding: 18px; border-radius: 14px; background: linear-gradient(135deg, #1E1B4B, #312E81); border: 1px solid #4338CA; margin-bottom: 24px;'>
            <h4 style='margin:0; color:#38BDF8; font-weight:800; letter-spacing:0.5px;'>🏟️ CURRENT MATCHDAY ENVIRONMENT: {st.session_state.current_venue['name']}</h4>
            <p style='margin:6px 0 0 0; font-size:15px; color:#E0E7FF;'>{st.session_state.current_venue['desc']}</p>
        </div>
    """, unsafe_allow_html=True)

    # NAVIGATION TABS ARRAY
    tab_news, tab_roster, tab_table, tab_caps, tab_career = st.tabs(["📰 Media Newsroom", "👥 Roster Player Hub", "📊 League Standings", "👑 Cap Races", "👔 Office Suite"])
    
    # --- TAB 1: MEDIA NEWSROOM & DUAL COLUMN SCORECARDS ---
    with tab_news:
        st.subheader("📰 Cricket Daily Headlines")
        if st.session_state.match_history:
            for idx, match in enumerate(reversed(st.session_state.match_history)):
                st.markdown(f"""
                    <div class='news-box'>
                        <div class='news-title'>🎯 FIXTURE ROUND LOG</div>
                        <div class='news-headline'>{match['result']}</div>
                        <p style='color: #94A3B8; font-size: 14px; margin-top: 4px;'>Matchup: {match['fixture']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                with st.expander(f"📊 Expand Complete Strategic Innings Scorecard"):
                    col_sc1, col_sc2 = st.columns(2)
                    with col_sc1:
                        st.markdown("<h5 style='color:#60A5FA;'>🏏 Innings 1 Performance</h5>", unsafe_allow_html=True)
                        st.metric("Innings Total Runs", match.get('team1_score', '184/4'))
                        st.caption(f"⭐ Key Partnership: {match.get('top_batsman','Virat Kohli')} ({match.get('runs',68)} Runs)")
                    with col_sc2:
                        st.markdown("<h5 style='color:#F43F5E;'>🎯 Innings 2 Defense</h5>", unsafe_allow_html=True)
                        st.metric("Target Defense Score", match.get('team2_score', '152/10'))
                        st.caption(f"⚡ Lead Bowler Spell: {match.get('top_bowler','Jasprit Bumrah')} ({match.get('wickets',3)} Wickets)")
                st.markdown("<div style='margin-bottom:30px;'></div>", unsafe_allow_html=True)
        else:
            st.info("Tournament matches haven't started yet! Head to the Office Suite tab to advance the fixture bracket.")

    # --- TAB 2: DEDICATED SQUAD HUB ---
    with tab_roster:
        st.subheader("👥 Franchise Player Contract Hub")
        human_squads = [t for t in st.session_state.teams if t["is_human"]]
        selected_manager = st.selectbox("Manager Account Selector Profile:", options=[h["team_name"] for h in human_squads])
        t = next(team for team in human_squads if team["team_name"] == selected_manager)
        
        # Sidelined grid setup mapping rules
        col_selects, col_preview = st.columns([2, 3])
        
        with col_selects:
            st.markdown("##### ⚙️ Roster Directives")
            player_map = {p["name"]: p for p in t["squad"]}
            current_p11 = [p["name"] for p in t["playing_11"]] if t["playing_11"] else list(player_map.keys())[:11]
            
            new_p11 = st.multiselect("Select Your Starting Playing 11 Starters:", options=list(player_map.keys()), default=current_p11, key=f"hub_p11_{t['team_name']}")
            remaining_squad = [n for n in player_map.keys() if n not in new_p11]
            
            default_sub = t["impact_player"]["name"] if (t["impact_player"] and t["impact_player"]["name"] in remaining_squad) else (remaining_squad[0] if remaining_squad else None)
            new_sub = st.selectbox("Assign Playing 12 Impact Sub Slot:", options=remaining_squad, index=0 if default_sub is None else remaining_squad.index(default_sub))
            
            if st.button("💾 Apply & Update Playing 12 Tactical Matrix", use_container_width=True):
                if len(new_p11) != 11:
                    st.error("Your starting roster layout must contain exactly 11 players!")
                else:
                    t["playing_11"] = [player_map[n] for n in new_p11]
                    t["impact_player"] = player_map[new_sub] if new_sub else None
                    st.success("Lineup safely rewritten! Ready for competitive bracket fixtures.")

        with col_preview:
            st.markdown("##### 📋 Complete Squad Roster Sheet & Form Indicators")
            for p in t["squad"]:
                is_starter = "⭐ Starter XI" if p in t["playing_11"] else ("🔄 Impact Sub" if t["impact_player"] and p["name"] == t["impact_player"]["name"] else "📋 Bench Reserve")
                color_tag = "#60A5FA" if "Starter" in is_starter else ("#F59E0B" if "Impact" in is_starter else "#94A3B8")
                st.markdown(f"""
                    <div style='padding:10px; border-radius:8px; background-color:#1E293B; margin-bottom:8px; border-left:4px solid {color_tag};'>
                        <strong>{p['name']}</strong> — OVR {p['rating']} ({p['role']})<br/>
                        <span style='font-size:12px; color:#CBD5E1;'>Trait: {get_player_trait(p)} | Allocation: {is_starter}</span>
                    </div>
                """, unsafe_allow_html=True)

    # --- TAB 3: STANDINGS MATRIX ---
    with tab_table:
        st.subheader("League Table Standings Grid")
        table_data = [{"Franchise Team": t["team_name"], "Wins 🟢": t["wins"], "Losses 🔴": t["losses"], "Squad Morale": f"{t['morale']}%", "Points": t["points"]} for t in st.session_state.teams]
        st.table(sorted(table_data, key=lambda x: x["Points"], reverse=True))

    # --- TAB 4: CAPS LEADERBOARDS ---
    with tab_caps:
        col_o, col_p = st.columns(2)
        with col_o:
            st.markdown("### 🟠 Orange Cap Leaderboard")
            sorted_runs = sorted(st.session_state.stats_runs.items(), key=lambda x: x[1], reverse=True)[:5]
            for idx, (name, runs) in enumerate(sorted_runs): st.write(f"**{idx+1}. {name}** — {runs} runs")
        with col_p:
            st.markdown("### 🟣 Purple Cap Leaderboard")
            sorted_wicks = sorted(st.session_state.stats_wickets.items(), key=lambda x: x[1], reverse=True)[:5]
            for idx, (name, wck) in enumerate(sorted_wicks): st.write(f"**{idx+1}. {name}** — {wck} wickets")

    # --- TAB 5: OFFICE TACTICAL CONTROLS ---
    with tab_career:
        user_team = next((t for t in st.session_state.teams if t["is_human"]), None)
        
        if st.session_state.press_conference:
            pc = st.session_state.press_conference
            st.warning(f"🎤 **PRESS CONFERENCE INTERCEPT:** {pc['situation']}")
            for opt_key, opt_val in pc["options"].items():
                if st.button(opt_val["text"], key=f"pc_{opt_key}"):
                    if user_team: user_team["morale"] = min(100, max(20, user_team["morale"] + opt_val["morale_effect"]))
                    st.session_state.press_conference = None
                    st.rerun()
            st.stop()

        st.subheader("Simulate Active Fixture Matches")
        
        # Render clean side by side corporate option metrics layout
        if user_team:
            col_met1, col_met2, col_met3 = st.columns(3)
            with col_met1: st.metric("Current Franchise Points", user_team["points"])
            with col_met2: st.metric("Locker Room Morale", f"{user_team['morale']}%")
            with col_met3: st.metric("Remaining Transfer Budget", f"₹{user_team['purse']/100:.2f} CR")
        st.divider()

        col_sim1, col_sim2 = st.columns(2)
        with col_sim1:
            if st.button("🎮 Launch Live Interactive Game Match", type="primary", use_container_width=True):
                opp_team = next(t for t in st.session_state.teams if t["team_name"] != user_team["team_name"])
                st.session_state.live_match_state = {
                    "user_team": user_team["team_name"], "opp_team": opp_team["team_name"],
                    "innings": 1, "score": 0, "wickets": 0, "balls": 0, "target": random.randint(58, 85), "log": "Match Day Active."
                }
                st.rerun()
                
        with col_sim2:
            if st.button("⚡ Fast Skip Match via Auto Simulation", use_container_width=True):
                boost_role = st.session_state.current_venue["boost_role"]
                boost_amt = st.session_state.current_venue["boost_amount"]
                
                random.shuffle(st.session_state.teams)
                for i in range(0, len(st.session_state.teams) - 1, 2):
                    t1, t2 = st.session_state.teams[i], st.session_state.teams[i+1]
                    
                    t1_b = sum([p["rating"] + (boost_amt if p["role"] == boost_role else 0) for p in t1["playing_11"]])
                    t2_b = sum([p["rating"] + (boost_amt if p["role"] == boost_role else 0) for p in t2["playing_11"]])
                    
                    p1, p2 = t1_b + random.randint(-20, 20), t2_b + random.randint(-20, 20)
                    
                    all_batsmen = [p for p in t1["playing_11"] + t2["playing_11"] if p["role"] in ["Batsman", "Wicket-Keeper"]]
                    all_bowlers = [p for p in t1["playing_11"] + t2["playing_11"] if p["role"] in ["Bowler", "All-Rounder"]]
                    top_bat = random.choice(all_batsmen)["name"] if all_batsmen else "Roster Star"
                    top_bowl = random.choice(all_bowlers)["name"] if all_bowlers else "Strike Bowler"
                    
                    r_rolled, w_rolled = random.randint(48, 102), random.randint(2, 5)
                    st.session_state.stats_runs[top_bat] = st.session_state.stats_runs.get(top_bat, 0) + r_rolled
                    st.session_state.stats_wickets[top_bowl] = st.session_state.stats_wickets.get(top_bowl, 0) + w_rolled
                    
                    t1_runs, t2_runs = random.randint(140, 210), random.randint(130, 205)
                    
                    if p1 > p2:
                        t1["points"] += 2; t1["wins"] += 1
                        t2["losses"] += 1
                        headline = f"{t1['team_name']} won by {abs(t1_runs - t2_runs)} runs!"
                    else:
                        t2["points"] += 2; t2["wins"] += 1
                        t1["losses"] += 1
                        headline = f"{t2['team_name']} won by {random.randint(2, 7)} wickets!"
                        
                    st.session_state.match_history.append({
                        "fixture": f"{t1['team_name']} vs {t2['team_name']}", 
                        "result": headline,
                        "top_batsman": top_bat, "runs": r_rolled,
                        "top_bowler": top_bowl, "wickets": w_rolled,
                        "detailed": True, "team1_score": f"{max(t1_runs, t2_runs)}/4", "team2_score": f"{min(t1_runs, t2_runs)}/7"
                    })
                    
                st.session_state.match_day += 1
                st.session_state.current_venue = random.choice(VENUES)
                st.rerun()
