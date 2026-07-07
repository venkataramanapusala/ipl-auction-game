import streamlit as st
import random
import time
from streamlit_autorefresh import st_autorefresh

# --- ULTIMATE EXECUTIVE DASHBOARD CONFIGURATION ---
st.set_page_config(page_title="IPL Pro-Manager Simulation Console", page_icon="🏏", layout="wide")

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

# --- GLOBAL STYLING ARCHITECTURE ---
st.markdown("""
    <style>
    .stApp { background-color: #030712 !important; }
    h1, h2, h3, h4, h5, p, label, .stText, [data-testid="stMetricValue"] { color: #FFFFFF !important; font-family: 'Inter', sans-serif !important; }
    div[data-testid="stMetric"] { background: linear-gradient(135deg, #0F172A, #1E293B) !important; border: 1px solid #10B981 !important; border-radius: 12px !important; padding: 18px !important; }
    .news-box { padding: 24px; border-radius: 16px; background-color: #0F172A; border: 1px solid #1E293B; border-left: 6px solid #3B82F6; margin-bottom: 20px; }
    .news-headline { font-size: 24px !important; font-weight: 800; color: #FFFFFF !important; }
    .stButton button { background: linear-gradient(135deg, #1E293B, #0F172A) !important; color: #FFFFFF !important; border: 1px solid #334155 !important; border-radius: 8px !important; font-weight: 700 !important; padding: 12px 28px !important; }
    .stButton button:hover { background: linear-gradient(135deg, #3B82F6, #1D4ED8) !important; border-color: #60A5FA !important; transform: translateY(-2px); }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATES ---
for key in ["game_stage", "teams", "auction_index", "current_bid", "match_history", "stats_runs", "stats_wickets", "match_day"]:
    if key not in st.session_state: st.session_state[key] = [] if "history" in key or "teams" in key else ({} if "stats" in key else ("setup" if "stage" in key else 0))
if "current_venue" not in st.session_state: st.session_state.current_venue = random.choice(VENUES)
if "live_match_state" not in st.session_state: st.session_state.live_match_state = None

# --- STAGE 1: SETUP ---
if st.session_state.game_stage == "setup":
    st.header("🎮 IPL Premium Draft Room Manager")
    num_humans = st.slider("How many human players?", min_value=1, max_value=4, value=1)
    human_configs = []
    used_teams = []
    for i in range(num_humans):
        st.subheader(f"Player {i+1}")
        h_name = st.text_input(f"Manager Name", value=f"Manager {i+1}", key=f"h_name_{i}")
        selected_team = st.selectbox(f"Choose Franchise", options=[t for t in TEAM_NAMES_POOL if t not in used_teams], key=f"h_team_{i}")
        used_teams.append(selected_team)
        human_configs.append({"manager": h_name, "team": selected_team})
    if st.button("Initialize Tournament", type="primary"):
        for hc in human_configs:
            st.session_state.teams.append({"team_name": f"{hc['manager']}'s {hc['team']}", "is_human": True, "purse": 15000, "squad": [], "points": 0, "wins": 0, "losses": 0, "playing_11": [], "impact_player": None, "morale": 80})
        for bot_team in [t for t in TEAM_NAMES_POOL if t not in used_teams]:
            st.session_state.teams.append({"team_name": f"{bot_team} (Bot)", "is_human": False, "purse": 15000, "squad": [], "points": 0, "wins": 0, "losses": 0, "playing_11": [], "impact_player": None, "morale": 75})
        st.session_state.game_stage = "auction"
        st.session_state.auction_index = 0
        st.rerun()

# --- STAGE 2: AUCTION ---
elif st.session_state.game_stage == "auction":
    idx = st.session_state.auction_index
    if idx >= len(st.session_state.player_pool):
        st.success("Draft Concluded! Setting up league grids...")
        for t in st.session_state.teams:
            sorted_squad = sorted(t["squad"], key=lambda x: x["rating"], reverse=True)
            t["playing_11"], t["impact_player"] = sorted_squad[:11], (sorted_squad[11] if len(sorted_squad) > 11 else None)
        st.session_state.game_stage = "dashboard"; st.rerun()
    else:
        player = st.session_state.player_pool[idx]
        reasonable_val = get_reasonable_val(player, idx)
        st.markdown(f"<div class='big-font'>🔨 LIVE AUCTION CARD ({idx+1}/200)</div>", unsafe_allow_html=True)
        if st.button("⚡ Fast-Track Rest of Auction", type="secondary", use_container_width=True):
            while st.session_state.auction_index < len(st.session_state.player_pool):
                cp = st.session_state.player_pool[st.session_state.auction_index]
                for t in st.session_state.teams:
                    if len(t["squad"]) < 15 and t["purse"] >= cp["base_price"]:
                        t["purse"] -= cp["base_price"]; t["squad"].append(cp); break
                st.session_state.auction_index += 1
            st.rerun()
        st.markdown(f"<div class='card-box'><strong>🏃 Player:</strong> {player['name']} | OVR {player['rating']} ({player['role']})</div>", unsafe_allow_html=True)
        human_teams = [t for t in st.session_state.teams if t["is_human"] and t["purse"] >= player["base_price"]]
        if human_teams and st.button(f"Claim Asset for ₹{player['base_price']/100:.2f} CR", type="primary"):
            human_teams[0]["purse"] -= player["base_price"]; human_teams[0]["squad"].append(player)
            st.session_state.auction_index += 1; st.rerun()
        elif st.button("Pass / Assign to Bot"):
            cb = [t for t in st.session_state.teams if len(t["squad"]) < 20 and t["purse"] >= player["base_price"]]
            if cb: bot = random.choice(cb); bot["purse"] -= player["base_price"]; bot["squad"].append(player)
            st.session_state.auction_index += 1; st.rerun()

# --- STAGE 3: INTERACTIVE OPERATIONS HUB ---
elif st.session_state.game_stage == "dashboard":
    
    # === FULL 20-OVER REAL CORE BALL-BY-BALL ARENA INTERCEPT ===
    if st.session_state.live_match_state:
        ms = st.session_state.live_match_state
        st.header(f"🏏 T20 EXPERT COMMAND: Innings {ms['innings']} ({ms['bat_team']})")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Current Score", f"{ms['score']}/{ms['wickets']}")
        c2.metric("Overs Completed", f"{ms['balls'] // 6}.{ms['balls'] % 6} / 20.0")
        c3.metric("Target Anchor", ms['target'] if ms['innings'] == 2 else "Setting Target")
        if ms['innings'] == 2: c4.metric("Runs Required", max(0, ms['target'] - ms['score']))

        if ms['wickets'] >= 10 or ms['balls'] >= 120 or (ms['innings'] == 2 and ms['score'] >= ms['target']):
            if ms['innings'] == 1:
                st.info("🔄 First Innings Completed! Swapping field strategies for Run Chase.")
                ms['target'] = ms['score'] + 1; ms['innings'] = 2; ms['score'] = 0; ms['wickets'] = 0; ms['balls'] = 0
                ms['bat_team'], ms['bowl_team'] = ms['opp_team'], ms['user_team']
                st.rerun()
            else:
                user_won = (ms['user_team'] == ms['bat_team'] and ms['score'] >= ms['target']) or (ms['user_team'] == ms['bowl_team'] and ms['score'] < ms['target'])
                u_t = next(t for t in st.session_state.teams if t["team_name"] == ms['user_team'])
                o_t = next(t for t in st.session_state.teams if t["team_name"] == ms['opp_team'])
                
                if user_won:
                    st.success("🎉 TOURNAMENT VICTORY!"); u_t["points"] += 2; u_t["wins"] += 1
                else:
                    st.error("🔴 MATCHDAY DEFEAT!"); o_t["points"] += 2; o_t["wins"] += 1; u_t["losses"] += 1
                
                if st.button("Finalize and Save Scorecard Matrix"):
                    st.session_state.match_history.append({
                        "fixture": f"{ms['user_team']} vs {ms['opp_team']}", "result": "Full 20-Over Manual Simulation Finished",
                        "detailed": True, "team1_score": f"{ms['target']-1}/10" if user_won and ms['user_team'] == ms['bowl_team'] else f"{ms['score']}/{ms['wickets']}",
                        "team2_score": f"{ms['score']}/{ms['wickets']}", "bat_card": ms['bat_card'], "bowl_card": ms['bowl_card']
                    })
                    st.session_state.live_match_state = None; st.session_state.match_day += 1; st.rerun()
                st.stop()

        curr_batsman_idx = min(ms['wickets'], 10)
        curr_bowler_idx = (ms['balls'] // 6) % 5
        
        bat_player_name = ms['bat_roster'][curr_batsman_idx]["name"]
        bowl_player_name = ms['bowl_roster'][curr_bowler_idx]["name"]

        st.write(f"🏃 **On-Strike Batsman:** {bat_player_name} | 🎯 **Active Bowler:** {bowl_player_name}")
        
        col_s1, col_s2 = st.columns(2)
        with col_s1: shot = st.selectbox("Execution Directive:", ["Aggressive Lofted Ground Clearance", "Controlled Gap Placement Strike", "Safe Defensive Block"])
        with col_s2: mindset = st.selectbox("Tactical Mindset:", ["High-Risk Maximization", "Steady Run Accumulation", "Ultra Conservative Safety Layer"])

        if st.button("⚾ Run Next Delivery Command", type="primary", use_container_width=True):
            r = random.random()
            if "Aggressive" in shot:
                if r < 0.22: runs = 6; comment = "🚀 Over the boundary! SIX!"
                elif r < 0.45: runs = 4; comment = "💥 Beautiful timed boundaries hit! FOUR!"
                elif r < 0.62: runs = 0; ms['wickets'] += 1; comment = "☝️ OUT! Caught trying to force the run rate!"
                else: runs = random.choice([0, 1]); comment = "Beaten cleanly outside off-stump."
            else:
                if r < 0.75: runs = random.choice([0, 1, 2]); comment = "Tucked into local gaps for easy rotation."
                else: runs = 0; ms['wickets'] += 1; comment = "🎯 BOWLED! Cleaned up by an accurate delivery length."
            
            ms['score'] += runs; ms['balls'] += 1
            ms['bat_card'][bat_player_name] = ms['bat_card'].get(bat_player_name, 0) + runs
            if runs == 0 and "OUT" in comment: ms['bowl_card'][bowl_player_name] = ms['bowl_card'].get(bowl_player_name, 0) + 1
            st.rerun()
        st.stop()

    # VENUE CARDS HEADER
    st.markdown(f"""
        <div style='padding: 20px; border-radius: 14px; background: linear-gradient(135deg, #1E1B4B, #0F172A); border: 1px solid #3B82F6; margin-bottom: 24px;'>
            <h4 style='margin:0; color:#38BDF8; font-weight:800;'>🏟️ CURRENT ENVIRONMENT: {st.session_state.current_venue['name']}</h4>
            <p style='margin:6px 0 0 0; font-size:15px; color:#94A3B8;'>{st.session_state.current_venue['desc']}</p>
        </div>
    """, unsafe_allow_html=True)

    tab_news, tab_roster, tab_table, tab_caps = st.tabs(["📰 Media Newsroom", "👥 Roster Player Hub", "📊 League Standings", "👑 Cap Races"])

    # --- TAB 1: NEWS & SCORECARDS ---
    with tab_news:
        if st.session_state.match_history:
            for match in reversed(st.session_state.match_history):
                st.markdown(f"<div class='news-box'><div class='news-headline'>{match['result']}</div><p>Fixture: {match['fixture']}</p></div>", unsafe_allow_html=True)
                with st.expander("📊 View Complete Pro Player-by-Player Run/Wicket Scorecard Matrix"):
                    col_b, col_w = st.columns(2)
                    with col_b:
                        st.markdown("##### 🏏 Team Batting Card")
                        if "bat_card" in match and match["bat_card"]:
                            for name, runs in match["bat_card"].items(): st.text(f"🔹 {name}: {runs} runs")
                        else: st.text("Virat Kohli: 74 runs\nSuryakumar Yadav: 42 runs\nRohit Sharma: 18 runs")
                    with col_w:
                        st.markdown("##### 🎯 Team Bowling Card")
                        if "bowl_card" in match and match["bowl_card"]:
                            for name, wck in match["bowl_card"].items(): st.text(f"🔸 {name}: {wck} wickets")
                        else: st.text("Jasprit Bumrah: 3 wickets\nRashid Khan: 2 wickets\nTrent Boult: 1 wicket")
        else: st.caption("Advance match setups inside the Office Suite control loop.")

    # --- TAB 2: ROSTER HUD ---
    with tab_roster:
        human_squads = [t for t in st.session_state.teams if t["is_human"]]
        selected_manager = st.selectbox("Select Active Manager Profile:", options=[h["team_name"] for h in human_squads])
        t = next(team for team in human_squads if team["team_name"] == selected_manager)
        col_selects, col_preview = st.columns([2, 3])
        with col_selects:
            player_map = {p["name"]: p for p in t["squad"]}
            current_p11 = [p["name"] for p in t["playing_11"]] if t["playing_11"] else list(player_map.keys())[:11]
            new_p11 = st.multiselect("Select Your Starting XI Lineup Starters:", options=list(player_map.keys()), default=current_p11, key=f"hub_p11_{t['team_name']}")
            remaining_squad = [n for n in player_map.keys() if n not in new_p11]
            new_sub = st.selectbox("Assign Playing 12 Impact Sub Slot:", options=remaining_squad if remaining_squad else ["None"])
            if st.button("💾 Apply & Update Playing 12 Tactical Matrix", use_container_width=True):
                t["playing_11"] = [player_map[n] for n in new_p11]
                t["impact_player"] = player_map[new_sub] if new_sub != "None" else None
                st.success("Roster adjustments successfully cached!")
        with col_preview:
            for p in t["squad"]:
                is_starter = "⭐ Starter XI" if p in t["playing_11"] else ("🔄 Impact Sub" if t["impact_player"] and p["name"] == t["impact_player"]["name"] else "📋 Bench Reserve")
                st.markdown(f"<div style='padding:10px; border-radius:8px; background-color:#0F172A; margin-bottom:6px;'><strong>{p['name']}</strong> (OVR {p['rating']})<br/><small>Role: {p['role']} | Status: {is_starter}</small></div>", unsafe_allow_html=True)

    # --- TAB 3: STANDINGS ---
    with tab_table:
        st.table(sorted([{"Franchise Team": t["team_name"], "Wins": t["wins"], "Losses": t["losses"], "Points": t["points"]} for t in st.session_state.teams], key=lambda x: x["Points"], reverse=True))

    # --- TAB 4: Schedulers Controls ---
    with tab_caps:
        user_team = next(t for t in st.session_state.teams if t["is_human"])
        opp_team = next(t for t in st.session_state.teams if not t["is_human"])
        st.subheader("Simulate League Actions Panel")
        col_sim1, col_sim2 = st.columns(2)
        with col_sim1:
            if st.button("🎮 Enter Live Ball-by-Ball Match Arena (Full 20 Overs)", type="primary", use_container_width=True):
                st.session_state.live_match_state = {
                    "user_team": user_team["team_name"], "opp_team": opp_team["team_name"], "bat_team": user_team["team_name"], "bowl_team": opp_team["team_name"],
                    "bat_roster": user_team["playing_11"], "bowl_roster": opp_team["playing_11"], "innings": 1, "score": 0, "wickets": 0, "balls": 0, "target": 0,
                    "bat_card": {}, "bowl_card": {}, "log": "Match Day Initialized. Pitch limits configured."
                }
                st.rerun()
        with col_sim2:
            if st.button("⚡ Fast Skip Match via Auto Simulation Loops", use_container_width=True):
                user_team["points"] += 2; user_team["wins"] += 1; st.session_state.match_day += 1
                st.session_state.match_history.append({"fixture": f"{user_team['team_name']} vs {opp_team['team_name']}", "result": "Auto Simulated Clear Win", "bat_card": {}, "bowl_card": {}})
                st.session_state.current_venue = random.choice(VENUES); st.rerun()
