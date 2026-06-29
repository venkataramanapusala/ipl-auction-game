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

def get_player_trait(player):
    if player["rating"] >= 93: return "👑 Legendary Icon Master"
    if player["rating"] <= 80: return f"🌱 Debutant Prospect"
    if player["role"] == "Batsman": return "💥 Aggressive Finisher" if player["rating"] >= 88 else "🏏 Technical Batter"
    elif player["role"] == "Bowler": return "🔥 Express Speed Bowler" if player["rating"] >= 88 else "🎯 Line Bowler"
    elif player["role"] == "All-Rounder": return "🔀 Clutch All-Rounder"
    elif player["role"] == "Wicket-Keeper": return "🧤 Fast Stumper"
    return "🏏 Steady Asset"

# --- INTERACTIVE MINI-GAME STATE ---
if "live_match_state" not in st.session_state:
    st.session_state.live_match_state = None

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

# --- GLOBAL STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    h1, h2, h3, p, label, .stText { color: #FFFFFF !important; }
    .big-font { font-size: 26px !important; font-weight: bold; color: #3B82F6 !important; text-shadow: 0px 0px 8px rgba(59, 130, 246, 0.4); }
    .timer-text { font-size: 22px; font-weight: bold; color: #EF4444 !important; }
    .card-box { padding: 20px; border-radius: 12px; background-color: #0F172A; border: 1px solid #1E293B; border-left: 6px solid #3B82F6; margin-bottom: 15px; color: #FFFFFF !important; }
    .stButton button { background-color: #1F2937 !important; color: #FFFFFF !important; border: 1px solid #4B5563 !important; border-radius: 8px !important; }
    .stButton button:hover { background-color: #374151 !important; border-color: #3B82F6 !important; color: #3B82F6 !important; }
    </style>
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
        st.rerun()

# --- STAGE 2: AUCTION ---
elif st.session_state.game_stage == "auction":
    idx = st.session_state.auction_index
    if idx >= len(st.session_state.player_pool):
        st.success("Draft Concluded!")
        for t in st.session_state.teams: t["disqualified"] = False
        st.session_state.game_stage = "lineup"
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
        
        if st.button("⚡ Fast-Track Auction", type="secondary", use_container_width=True):
            while st.session_state.auction_index < len(st.session_state.player_pool):
                curr_idx = st.session_state.auction_index
                curr_p = st.session_state.player_pool[curr_idx]
                val = get_reasonable_val(curr_p, curr_idx)
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
                counter_bot = random.choice(bots)
                st.session_state.current_bid += 50
                st.session_state.highest_bidder = counter_bot
                st.session_state.timer_seconds = 4
                st.session_state.log_msg = f"🤖 {counter_bot['team_name']} bids ₹{st.session_state.current_bid/100:.2f} CR."
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
            st.rerun()

        st.markdown(f"<div class='card-box'><strong>🏃 Player:</strong> {player['name']} | <strong>🎯 Role:</strong> {player['role']} | <strong>📊 OVR:</strong> {player['rating']}<br/><em>Trait: {get_player_trait(player)}</em></div>", unsafe_allow_html=True)
        human_teams = [t for t in st.session_state.teams if t["is_human"] and t["purse"] >= (st.session_state.current_bid + 50)]
        if human_teams:
            if st.button("Raise Bid (+₹50 L)", type="primary", use_container_width=True):
                st.session_state.current_bid += 50
                st.session_state.highest_bidder = human_teams[0]
                st.session_state.timer_seconds = 4
                st.rerun()

# --- STAGE 2.5: LINEUP LOCK IN (WITH MULTI-HUMAN DROPDOWN + PROFILE PREVIEW) ---
elif st.session_state.game_stage == "lineup":
    st.header("🏏 Match Lineup Selector Room")
    
    # Enable bots to auto-build lines
    for t in st.session_state.teams:
        if not t["is_human"]:
            sorted_squad = sorted(t["squad"], key=lambda x: x["rating"], reverse=True)
            t["playing_11"] = sorted_squad[:11]
            t["impact_player"] = sorted_squad[11] if len(sorted_squad) > 11 else None

    # Multi-Human Team Switcher Toggle Selector
    human_teams = [t for t in st.session_state.teams if t["is_human"]]
    selected_human_name = st.selectbox("Switch Between Active Human Rosters:", options=[t["team_name"] for t in human_teams])
    t = next(team for team in human_teams if team["team_name"] == selected_human_name)
    
    st.subheader(f"Configure Strategy Matrix: {t['team_name']}")
    player_map = {p["name"]: p for p in t["squad"]}
    
    p12_names = st.multiselect(f"Select Playing 12 (11 Starters + 1 Impact Sub):", options=list(player_map.keys()), default=list(player_map.keys())[:12] if len(t["squad"]) >= 12 else list(player_map.keys()), key=f"p12_{t['team_name']}")
    
    # Skill and Trait Inspector Profile Panel
    if p12_names:
        inspect_name = st.selectbox("🔍 Select Player to Inspect Skills & Traits:", options=p12_names, key=f"inspect_{t['team_name']}")
        target_p = player_map[inspect_name]
        st.info(f"📋 **{target_p['name']}** — OVR: {target_p['rating']} | Role: {target_p['role']} | Trait: `{get_player_trait(target_p)}`")

    if st.button(f"Save Tactical 12 Roster Setup for {t['team_name']}", type="secondary"):
        if len(p12_names) < 11 or len(p12_names) > 12: st.error("Roster counts must match exactly 11 or 12 structural players!")
        else:
            t["playing_11"] = [player_map[n] for n in p12_names[:11]]
            t["impact_player"] = player_map[p12_names[12]] if len(p12_names) == 12 else None
            st.success("Squad composition metrics locked in successfully!")

    st.divider()
    if st.button("Launch Management Hub Operations", type="primary", use_container_width=True):
        for h in human_teams:
            if not h["playing_11"]:
                s = sorted(h["squad"], key=lambda x: x["rating"], reverse=True)
                h["playing_11"] = s[:11]
                h["impact_player"] = s[11] if len(s) > 11 else None
        st.session_state.game_stage = "dashboard"
        st.rerun()

# --- STAGE 3: MANAGEMENT OPERATIONS HUB & LIVE INTERACTIVE GAMEPLAY ---
elif st.session_state.game_stage == "dashboard":
    # IF INTERACTIVE BALL-BY-BALL MINI-GAME MODAL IS LAUNCHED
    if st.session_state.live_match_state:
        ms = st.session_state.live_match_state
        st.header(f"🏏 LIVE SIMULATION: {ms['user_team']} vs {ms['opp_team']}")
        st.subheader(f"Innings: {ms['innings']} | Score: {ms['score']}/{ms['wickets']} ({ms['balls'] // 6}.{ms['balls'] % 6} Overs)")
        st.info(f"🎯 Target to Win: {ms['target']} runs")
        
        if ms['log']: st.code(ms['log'])

        if ms['wickets'] >= 10 or ms['balls'] >= 12 or (ms['innings'] == 2 and ms['score'] >= ms['target']):
            # Match Finished Evaluation End Block
            st.subheader("🏁 Match Day Concluded!")
            user_won = False
            if ms['innings'] == 1:
                st.write("First innings finished. AI failed to chase standard simulated totals.")
                user_won = True
            else:
                user_won = ms['score'] >= ms['target']
                
            u_t = next(t for t in st.session_state.teams if t["team_name"] == ms['user_team'])
            o_t = next(t for t in st.session_state.teams if t["team_name"] == ms['opp_team'])
            
            if user_won:
                st.success("🎉 VICTORY! Your strategic ball selections outplayed the opposition.")
                u_t["points"] += 2; u_t["wins"] += 1; u_t["morale"] = min(100, u_t["morale"] + 8)
                o_t["losses"] += 1
            else:
                st.error("🔴 DEFEAT! The AI decoded your tactics down the stretch.")
                o_t["points"] += 2; o_t["wins"] += 1; u_t["losses"] += 1; u_t["morale"] = max(20, u_t["morale"] - 10)
                
            if st.button("Exit Interactive Arena & Save Match Data"):
                st.session_state.match_history.append({"fixture": f"{ms['user_team']} vs {ms['opp_team']}", "result": "Interactive Manual Finish", "top_batsman": "User Roster Star", "runs": random.randint(40, 75), "top_bowler": "User Bullet Bowler", "wickets": random.randint(2, 4)})
                st.session_state.match_day += 1
                st.session_state.live_match_state = None
                st.rerun()
            st.stop()

        # BALL CONTROL GAME OPTIONS ACTIONS
        st.markdown("### 👔 Direct Ball Action Tactics")
        col_m1, col_m2 = st.columns(2)
        with col_m1: shot_intent = st.selectbox("Set Batter Action / Bowl Delivery Target Line:", ["Aggressive Lofted Drive / Yorker Target Length", "Controlled Placement Placement / Sharp Cutting Bouncer", "Defensive Safe Block / Subversive Off-Spinner Target"])
        with col_m2: mindset = st.selectbox("Manager Directive Mindset Setting:", ["High-Risk Heroics", "Calculated Calibration", "Ultra Conservative Safety Block"])

        if st.button("⚾ Deliver / Face Next Ball", type="primary", use_container_width=True):
            roll = random.random()
            if ms['innings'] == 1: # USER BATTING SIM
                if "Lofted" in shot_intent and "Heroics" in mindset:
                    if roll < 0.35: ms['score'] += 6; ms['log'] = "🚀 CRACK! Outstanding Lofted Drive clearing the boundary rope! SIX!"
                    elif roll < 0.60: ms['wickets'] += 1; ms['log'] = "☝️ OUT! Caught in the deep attempting an aggressive boundary clearing drive!"
                    else: ms['score'] += 1; ms['log'] = "Single down to long-on."
                else:
                    if roll < 0.75: ms['score'] += random.choice([1, 2, 4]); ms['log'] = "Controlled shot finding open space inside the inner field ring."
                    else: ms['wickets'] += 1; ms['log'] = "🎯 BOWLED! Beaten by pace trying to defend."
            else: # USER BOWLING SIM
                if "Yorker" in shot_intent and "Heroics" in mindset:
                    if roll < 0.45: ms['wickets'] += 1; ms['log'] = "🎯 CRACK! Perfect block-hole Yorker smashing the base of middle stump!"
                    else: ms['score'] += random.choice([4, 6]); ms['log'] = "Missed length slightly, whipped over mid-wicket for a boundary."
                else:
                    ms['score'] += random.choice([0, 1, 2]); ms['log'] = "Good economical defensive length keeping the batsman checked."
                    
            ms['balls'] += 1
            st.rerun()
        st.stop()

    # STANDARD FRANCHISE OPERATIONS SUITE DESIGN
    st.header(f"🏆 IPL Operations Suite Panel — Day {st.session_state.match_day}/14")
    tab_table, tab_stats, tab_career = st.tabs(["📊 Standings Table", "🏏 Log History Charts", "👔 Active Manager Room"])

    with tab_table:
        st.subheader("League Table Standings")
        t_data = [{"Team": t["team_name"], "Wins": t["wins"], "Losses": t["losses"], "Morale": f"{t['morale']}%", "Points": t["points"]} for t in st.session_state.teams]
        st.table(sorted(t_data, key=lambda x: x["Points"], reverse=True))

    with tab_stats:
        if st.session_state.match_history:
            for m in reversed(st.session_state.match_history[-6:]):
                st.write(f"**🏏 {m['fixture']}** — {m['result']}")
        else: st.caption("No historical match day loops recorded yet.")

    with tab_career:
        user = next(t for t in st.session_state.teams if t["is_human"])
        opp = next(t for t in st.session_state.teams if not t["is_human"])
        
        st.subheader("Simulate League Actions Panel")
        col_b1, col_b2 = st.columns(2)
        
        with col_b1:
            if st.button("🎮 Enter Live Ball-by-Ball Match Arena", type="primary", use_container_width=True):
                st.session_state.live_match_state = {
                    "user_team": user["team_name"], "opp_team": opp["team_name"],
                    "innings": 1, "score": 0, "wickets": 0, "balls": 0, "target": random.randint(45, 80), "log": "Match initiated. Grab your gloves manager!"
                }
                st.rerun()
                
        with col_b2:
            if st.button("⚡ Fast Skip Match Day via Auto Simulation", use_container_width=True):
                user["points"] += 2; user["wins"] += 1; st.session_state.match_day += 1
                st.session_state.match_history.append({"fixture": f"{user['team_name']} vs {opp['team_name']}", "result": "Auto-Simulates Finish"})
                st.rerun()
