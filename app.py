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

# --- MASTER 200 REAL-WORLD PLAYER DATABASE WITH AGE, POTENTIAL, AND XP PIPELINES ---
if "player_pool" not in st.session_state:
    raw_pool = [
        # === PURE BATSMEN (1 - 60) ===
        {"name": "Virat Kohli", "role": "Batsman", "rating": 94, "base_price": 200, "age": 35},
        {"name": "Suryakumar Yadav", "role": "Batsman", "rating": 93, "base_price": 150, "age": 33},
        {"name": "Rohit Sharma", "role": "Batsman", "rating": 91, "base_price": 200, "age": 36},
        {"name": "Travis Head", "role": "Batsman", "rating": 92, "base_price": 150, "age": 30},
        {"name": "Shubman Gill", "role": "Batsman", "rating": 89, "base_price": 100, "age": 24},
        {"name": "Yashasvi Jaiswal", "role": "Batsman", "rating": 90, "base_price": 100, "age": 22},
        {"name": "Ruturaj Gaikwad", "role": "Batsman", "rating": 88, "base_price": 100, "age": 27},
        {"name": "Rinku Singh", "role": "Batsman", "rating": 86, "base_price": 50, "age": 26},
        {"name": "Sai Sudharsan", "role": "Batsman", "rating": 84, "base_price": 50, "age": 23},
        {"name": "David Warner", "role": "Batsman", "rating": 85, "base_price": 100, "age": 37},
        {"name": "Faf du Plessis", "role": "Batsman", "rating": 86, "base_price": 100, "age": 39},
        {"name": "Kane Williamson", "role": "Batsman", "rating": 85, "base_price": 100, "age": 33},
        {"name": "Tilak Varma", "role": "Batsman", "rating": 85, "base_price": 50, "age": 23},
        {"name": "Shimron Hetmyer", "role": "Batsman", "rating": 83, "base_price": 75, "age": 27},
        {"name": "Rovman Powell", "role": "Batsman", "rating": 84, "base_price": 75, "age": 30},
        {"name": "Rahul Tripathi", "role": "Batsman", "rating": 81, "base_price": 30, "age": 33},
        {"name": "Devdutt Padikkal", "role": "Batsman", "rating": 80, "base_price": 30, "age": 23},
        {"name": "Prithvi Shaw", "role": "Batsman", "rating": 82, "base_price": 50, "age": 24},
        {"name": "Mayank Agarwal", "role": "Batsman", "rating": 79, "base_price": 30, "age": 33},
        {"name": "Tristan Stubbs", "role": "Batsman", "rating": 86, "base_price": 50, "age": 23},
        {"name": "Tim David", "role": "Batsman", "rating": 84, "base_price": 75, "age": 28},
        {"name": "Ajinkya Rahane", "role": "Batsman", "rating": 80, "base_price": 50, "age": 35},
        {"name": "Manish Pandey", "role": "Batsman", "rating": 78, "base_price": 30, "age": 34},
        {"name": "Sherfane Rutherford", "role": "Batsman", "rating": 80, "base_price": 40, "age": 25},
        {"name": "Nehal Wadhera", "role": "Batsman", "rating": 81, "base_price": 20, "age": 23},
        {"name": "Riyan Parag", "role": "Batsman", "rating": 84, "base_price": 30, "age": 22},
        {"name": "Deepak Hooda", "role": "Batsman", "rating": 79, "base_price": 40, "age": 29},
        {"name": "Ayush Badoni", "role": "Batsman", "rating": 80, "base_price": 20, "age": 24},
        {"name": "Shahrukh Khan", "role": "Batsman", "rating": 82, "base_price": 40, "age": 30},
        {"name": "Abdul Samad", "role": "Batsman", "rating": 79, "base_price": 20, "age": 24},
        {"name": "David Miller", "role": "Batsman", "rating": 87, "base_price": 100, "age": 34},
        {"name": "Steve Smith", "role": "Batsman", "rating": 83, "base_price": 200, "age": 34},
        {"name": "Marnus Labuschagne", "role": "Batsman", "rating": 80, "base_price": 100, "age": 29},
        {"name": "Harry Brook", "role": "Batsman", "rating": 86, "base_price": 150, "age": 25},
        {"name": "Dawid Malan", "role": "Batsman", "rating": 82, "base_price": 75, "age": 36},
        {"name": "Rilee Rossouw", "role": "Batsman", "rating": 83, "base_price": 75, "age": 34},
        {"name": "Reeza Hendricks", "role": "Batsman", "rating": 81, "base_price": 50, "age": 36},
        {"name": "Finn Allen", "role": "Batsman", "rating": 84, "base_price": 75, "age": 25},
        {"name": "Glenn Phillips", "role": "Batsman", "rating": 85, "base_price": 50, "age": 27},
        {"name": "Alex Hales", "role": "Batsman", "rating": 83, "base_price": 75, "age": 37},
        {"name": "Chris Lynn", "role": "Batsman", "rating": 79, "base_price": 50, "age": 36},
        {"name": "Evain Lewis", "role": "Batsman", "rating": 80, "base_price": 50, "age": 34},
        {"name": "Brandon King", "role": "Batsman", "rating": 81, "base_price": 30, "age": 31},
        {"name": "Johnson Charles", "role": "Batsman", "rating": 79, "base_price": 30, "age": 37},
        {"name": "Pathum Nissanka", "role": "Batsman", "rating": 83, "base_price": 50, "age": 25},
        {"name": "Charith Asalanka", "role": "Batsman", "rating": 84, "base_price": 50, "age": 26},
        {"name": "Litton Das", "role": "Batsman", "rating": 78, "base_price": 50, "age": 29},
        {"name": "Najmul Hossain Shanto", "role": "Batsman", "rating": 79, "base_price": 30, "age": 25},
        {"name": "Ibrahim Zadran", "role": "Batsman", "rating": 82, "base_price": 50, "age": 24},
        {"name": "Najibullah Zadran", "role": "Batsman", "rating": 80, "base_price": 50, "age": 33},
        {"name": "Paul Stirling", "role": "Batsman", "rating": 78, "base_price": 50, "age": 35},
        {"name": "Harry Tector", "role": "Batsman", "rating": 81, "base_price": 30, "age": 26},
        {"name": "Karun Nair", "role": "Batsman", "rating": 79, "base_price": 30, "age": 32},
        {"name": "Anmolpreet Singh", "role": "Batsman", "rating": 76, "base_price": 20, "age": 26},
        {"name": "Subhranshu Senapati", "role": "Batsman", "rating": 75, "base_price": 20, "age": 29},
        {"name": "Atharva Taide", "role": "Batsman", "rating": 77, "base_price": 20, "age": 26},
        {"name": "Sameer Rizvi", "role": "Batsman", "rating": 81, "base_price": 30, "age": 22},
        {"name": "Kumar Kushagra", "role": "Batsman", "rating": 78, "base_price": 20, "age": 21},
        {"name": "Swastik Chikara", "role": "Batsman", "rating": 75, "base_price": 20, "age": 21},
        {"name": "Angkrish Raghuvanshi", "role": "Batsman", "rating": 80, "base_price": 20, "age": 21},

        # === PURE BOWLERS (61 - 120) ===
        {"name": "Jasprit Bumrah", "role": "Bowler", "rating": 96, "base_price": 200, "age": 30},
        {"name": "Rashid Khan", "role": "Bowler", "rating": 94, "base_price": 150, "age": 25},
        {"name": "Pat Cummins", "role": "Bowler", "rating": 92, "base_price": 150, "age": 31},
        {"name": "Mitchell Starc", "role": "Bowler", "rating": 91, "base_price": 150, "age": 34},
        {"name": "Trent Boult", "role": "Bowler", "rating": 90, "base_price": 100, "age": 34},
        {"name": "Mohammed Shami", "role": "Bowler", "rating": 91, "base_price": 150, "age": 33},
        {"name": "Kuldeep Yadav", "role": "Bowler", "rating": 89, "base_price": 100, "age": 29},
        {"name": "Yuzvendra Chahal", "role": "Bowler", "rating": 87, "base_price": 75, "age": 33},
        {"name": "Matheesha Pathirana", "role": "Bowler", "rating": 88, "base_price": 50, "age": 21},
        {"name": "Arshdeep Singh", "role": "Bowler", "rating": 86, "base_price": 75, "age": 25},
        {"name": "Kagiso Rabada", "role": "Bowler", "rating": 89, "base_price": 100, "age": 29},
        {"name": "Anrich Nortje", "role": "Bowler", "rating": 85, "base_price": 75, "age": 30},
        {"name": "Mohammed Siraj", "role": "Bowler", "rating": 86, "base_price": 100, "age": 30},
        {"name": "Avesh Khan", "role": "Bowler", "rating": 83, "base_price": 50, "age": 27},
        {"name": "Ravi Bishnoi", "role": "Bowler", "rating": 85, "base_price": 50, "age": 23},
        {"name": "Maheesh Theekshana", "role": "Bowler", "rating": 84, "base_price": 50, "age": 23},
        {"name": "Adam Zampa", "role": "Bowler", "rating": 86, "base_price": 75, "age": 32},
        {"name": "Nandre Burger", "role": "Bowler", "rating": 82, "base_price": 40, "age": 28},
        {"name": "Khaleel Ahmed", "role": "Bowler", "rating": 83, "base_price": 50, "age": 26},
        {"name": "Mukesh Kumar", "role": "Bowler", "rating": 82, "base_price": 30, "age": 32},
        {"name": "T Natarajan", "role": "Bowler", "rating": 84, "base_price": 50, "age": 33},
        {"name": "Sandeep Sharma", "role": "Bowler", "rating": 83, "base_price": 40, "age": 31},
        {"name": "Mohit Sharma", "role": "Bowler", "rating": 81, "base_price": 30, "age": 37},
        {"name": "Deepak Chahar", "role": "Bowler", "rating": 82, "base_price": 75, "age": 31},
        {"name": "Shardul Thakur", "role": "Bowler", "rating": 81, "base_price": 75, "age": 32},
        {"name": "Harshal Patel", "role": "Bowler", "rating": 83, "base_price": 50, "age": 33},
        {"name": "Bhuvneshwar Kumar", "role": "Bowler", "rating": 82, "base_price": 50, "age": 36},
        {"name": "Umran Malik", "role": "Bowler", "rating": 79, "base_price": 30, "age": 24},
        {"name": "Mayank Yadav", "role": "Bowler", "rating": 84, "base_price": 20, "age": 22},
        {"name": "Vaibhav Arora", "role": "Bowler", "rating": 80, "base_price": 20, "age": 26},
        {"name": "Harshit Rana", "role": "Bowler", "rating": 83, "base_price": 20, "age": 24},
        {"name": "Tushar Deshpande", "role": "Bowler", "rating": 81, "base_price": 30, "age": 29},
        {"name": "Sai Kishore", "role": "Bowler", "rating": 80, "base_price": 20, "age": 27},
        {"name": "Varun Chakaravarthy", "role": "Bowler", "rating": 86, "base_price": 50, "age": 34},
        {"name": "Lockie Ferguson", "role": "Bowler", "rating": 83, "base_price": 75, "age": 33},
        {"name": "Josh Hazlewood", "role": "Bowler", "rating": 89, "base_price": 200, "age": 35},
        {"name": "Tim Southee", "role": "Bowler", "rating": 84, "base_price": 75, "age": 37},
        {"name": "Matt Henry", "role": "Bowler", "rating": 83, "base_price": 75, "age": 34},
        {"name": "Ish Sodhi", "role": "Bowler", "rating": 81, "base_price": 50, "age": 33},
        {"name": "Adil Rashid", "role": "Bowler", "rating": 85, "base_price": 75, "age": 38},
        {"name": "Reece Topley", "role": "Bowler", "rating": 83, "base_price": 75, "age": 32},
        {"name": "Mark Wood", "role": "Bowler", "rating": 86, "base_price": 150, "age": 36},
        {"name": "Gus Atkinson", "role": "Bowler", "rating": 82, "base_price": 100, "age": 28},
        {"name": "Tabraiz Shamsi", "role": "Bowler", "rating": 82, "base_price": 50, "age": 36},
        {"name": "Lungi Ngidi", "role": "Bowler", "rating": 83, "base_price": 75, "age": 29},
        {"name": "Gerald Coetzee", "role": "Bowler", "rating": 85, "base_price": 50, "age": 25},
        {"name": "Marco Jansen", "role": "Bowler", "rating": 86, "base_price": 75, "age": 26},
        {"name": "Alzarri Joseph", "role": "Bowler", "rating": 82, "base_price": 100, "age": 27},
        {"name": "Shamar Joseph", "role": "Bowler", "rating": 83, "base_price": 50, "age": 26},
        {"name": "Akeal Hosein", "role": "Bowler", "rating": 82, "base_price": 50, "age": 33},
        {"name": "Mujeeb Ur Rahman", "role": "Bowler", "rating": 84, "base_price": 100, "age": 25},
        {"name": "Naveen-ul-Haq", "role": "Bowler", "rating": 83, "base_price": 50, "age": 26},
        {"name": "Fazalhaq Farooqi", "role": "Bowler", "rating": 84, "base_price": 50, "age": 25},
        {"name": "Mustafizur Rahman", "role": "Bowler", "rating": 85, "base_price": 200, "age": 30},
        {"name": "Taskin Ahmed", "role": "Bowler", "rating": 81, "base_price": 75, "age": 31},
        {"name": "Dushmantha Chameera", "role": "Bowler", "rating": 79, "base_price": 50, "age": 34},
        {"name": "Dilshan Madushanka", "role": "Bowler", "rating": 82, "base_price": 50, "age": 25},
        {"name": "Nuwan Thushara", "role": "Bowler", "rating": 81, "base_price": 50, "age": 31},
        {"name": "Sandeep Warrier", "role": "Bowler", "rating": 77, "base_price": 20, "age": 35},
        {"name": "Chetan Sakariya", "role": "Bowler", "rating": 78, "base_price": 30, "age": 26},

        # === ALL-ROUNDERS (121 - 170) ===
        {"name": "Hardik Pandya", "role": "All-Rounder", "rating": 91, "base_price": 150, "age": 30},
        {"name": "Ravindra Jadeja", "role": "All-Rounder", "rating": 90, "base_price": 150, "age": 35},
        {"name": "Axar Patel", "role": "All-Rounder", "rating": 89, "base_price": 100, "age": 30},
        {"name": "Sunil Narine", "role": "All-Rounder", "rating": 92, "base_price": 100, "age": 36},
        {"name": "Andre Russell", "role": "All-Rounder", "rating": 91, "base_price": 150, "age": 36},
        {"name": "Glenn Maxwell", "role": "All-Rounder", "rating": 86, "base_price": 100, "age": 35},
        {"name": "Marcus Stoinis", "role": "All-Rounder", "rating": 86, "base_price": 75, "age": 34},
        {"name": "Liam Livingstone", "role": "All-Rounder", "rating": 85, "base_price": 75, "age": 30},
        {"name": "Sam Curran", "role": "All-Rounder", "rating": 85, "base_price": 100, "age": 26},
        {"name": "Cameron Green", "role": "All-Rounder", "rating": 86, "base_price": 100, "age": 25},
        {"name": "Krunal Pandya", "role": "All-Rounder", "rating": 82, "base_price": 50, "age": 33},
        {"name": "Nitish Kumar Reddy", "role": "All-Rounder", "rating": 83, "base_price": 20, "age": 21},
        {"name": "Abhishek Sharma", "role": "All-Rounder", "rating": 87, "base_price": 30, "age": 23},
        {"name": "Venkatesh Iyer", "role": "All-Rounder", "rating": 83, "base_price": 50, "age": 29},
        {"name": "Shivam Dube", "role": "All-Rounder", "rating": 86, "base_price": 50, "age": 31},
        {"name": "Washington Sundar", "role": "All-Rounder", "rating": 81, "base_price": 50, "age": 24},
        {"name": "Moeen Ali", "role": "All-Rounder", "rating": 82, "base_price": 50, "age": 39},
        {"name": "Mitchell Marsh", "role": "All-Rounder", "rating": 84, "base_price": 75, "age": 32},
        {"name": "Romario Shepherd", "role": "All-Rounder", "rating": 80, "base_price": 40, "age": 29},
        {"name": "Shakib Al Hasan", "role": "All-Rounder", "rating": 87, "base_price": 100, "age": 39},
        {"name": "Ben Stokes", "role": "All-Rounder", "rating": 88, "base_price": 200, "age": 35},
        {"name": "Chris Woakes", "role": "All-Rounder", "rating": 83, "base_price": 100, "age": 37},
        {"name": "Daryl Mitchell", "role": "All-Rounder", "rating": 87, "base_price": 100, "age": 35},
        {"name": "Rachin Ravindra", "role": "All-Rounder", "rating": 86, "base_price": 50, "age": 24},
        {"name": "Jimmy Neesham", "role": "All-Rounder", "rating": 81, "base_price": 75, "age": 35},
        {"name": "Mitchell Santner", "role": "All-Rounder", "rating": 84, "base_price": 50, "age": 34},
        {"name": "Wanindu Hasaranga", "role": "All-Rounder", "rating": 89, "base_price": 150, "age": 26},
        {"name": "Angelo Mathews", "role": "All-Rounder", "rating": 80, "base_price": 50, "age": 39},
        {"name": "Dasun Shanaka", "role": "All-Rounder", "rating": 79, "base_price": 50, "age": 34},
        {"name": "Dunith Wellalage", "role": "All-Rounder", "rating": 81, "base_price": 30, "age": 23},
        {"name": "Mohammad Nabi", "role": "All-Rounder", "rating": 83, "base_price": 75, "age": 41},
        {"name": "Azmatullah Omarzai", "role": "All-Rounder", "rating": 84, "base_price": 50, "age": 26},
        {"name": "Gulbadin Naib", "role": "All-Rounder", "rating": 81, "base_price": 50, "age": 35},
        {"name": "Jason Holder", "role": "All-Rounder", "rating": 82, "base_price": 100, "age": 34},
        {"name": "Kyle Mayers", "role": "All-Rounder", "rating": 83, "base_price": 75, "age": 33},
        {"name": "Roston Chase", "role": "All-Rounder", "rating": 80, "base_price": 50, "age": 34},
        {"name": "Mehidy Hasan Miraz", "role": "All-Rounder", "rating": 82, "base_price": 50, "age": 28},
        {"name": "Sikandar Raza", "role": "All-Rounder", "rating": 84, "base_price": 50, "age": 40},
        {"name": "Sean Williams", "role": "All-Rounder", "rating": 80, "base_price": 50, "age": 39},
        {"name": "Rishi Dhawan", "role": "All-Rounder", "rating": 77, "base_price": 30, "age": 36},
        {"name": "Shahbaz Ahmed", "role": "All-Rounder", "rating": 82, "base_price": 30, "age": 31},
        {"name": "Lalit Yadav", "role": "All-Rounder", "rating": 78, "base_price": 20, "age": 29},
        {"name": "Mahipal Lomror", "role": "All-Rounder", "rating": 81, "base_price": 20, "age": 26},
        {"name": "Ramandeep Singh", "role": "All-Rounder", "rating": 82, "base_price": 20, "age": 28},
        {"name": "Prerak Mankad", "role": "All-Rounder", "rating": 76, "base_price": 20, "age": 32},
        {"name": "Atharva Ankolekar", "role": "All-Rounder", "rating": 74, "base_price": 20, "age": 25},
        {"name": "Shams Mulani", "role": "All-Rounder", "rating": 78, "base_price": 20, "age": 31},
        {"name": "Raj Angad Bawa", "role": "All-Rounder", "rating": 76, "base_price": 20, "age": 23},
        {"name": "Nishant Sindhu", "role": "All-Rounder", "rating": 77, "base_price": 20, "age": 22},
        {"name": "Kamlesh Nagarkoti", "role": "All-Rounder", "rating": 76, "base_price": 30, "age": 26},

        # === WICKET-KEEPERS (171 - 200) ===
        {"name": "MS Dhoni", "role": "Wicket-Keeper", "rating": 88, "base_price": 100, "age": 44},
        {"name": "Rishabh Pant", "role": "Wicket-Keeper", "rating": 91, "base_price": 200, "age": 28},
        {"name": "Sanju Samson", "role": "Wicket-Keeper", "rating": 89, "base_price": 100, "age": 29},
        {"name": "KL Rahul", "role": "Wicket-Keeper", "rating": 89, "base_price": 150, "age": 34},
        {"name": "Ishan Kishan", "role": "Wicket-Keeper", "rating": 86, "base_price": 100, "age": 27},
        {"name": "Nicholas Pooran", "role": "Wicket-Keeper", "rating": 92, "base_price": 150, "age": 30},
        {"name": "Quinton de Kock", "role": "Wicket-Keeper", "rating": 86, "base_price": 100, "age": 33},
        {"name": "Phil Salt", "role": "Wicket-Keeper", "rating": 88, "base_price": 75, "age": 29},
        {"name": "Jos Buttler", "role": "Wicket-Keeper", "rating": 91, "base_price": 150, "age": 35},
        {"name": "Dinesh Karthik", "role": "Wicket-Keeper", "rating": 82, "base_price": 50, "age": 41},
        {"name": "Jitesh Sharma", "role": "Wicket-Keeper", "rating": 81, "base_price": 30, "age": 31},
        {"name": "Dhruv Jurel", "role": "Wicket-Keeper", "rating": 83, "base_price": 20, "age": 25},
        {"name": "Abishek Porel", "role": "Wicket-Keeper", "rating": 80, "base_price": 20, "age": 21},
        {"name": "Anuj Rawat", "role": "Wicket-Keeper", "rating": 78, "base_price": 20, "age": 26},
        {"name": "Wriddhiman Saha", "role": "Wicket-Keeper", "rating": 79, "base_price": 30, "age": 41},
        {"name": "Jonny Bairstow", "role": "Wicket-Keeper", "rating": 87, "base_price": 150, "age": 36},
        {"name": "Sam Billings", "role": "Wicket-Keeper", "rating": 82, "base_price": 100, "age": 35},
        {"name": "Tom Latham", "role": "Wicket-Keeper", "rating": 81, "base_price": 75, "age": 34},
        {"name": "Heinrich Klaasen", "role": "Wicket-Keeper", "rating": 93, "base_price": 150, "age": 34},
        {"name": "Ryan Rickelton", "role": "Wicket-Keeper", "rating": 82, "base_price": 50, "age": 29},
        {"name": "Rahmanullah Gurbaz", "role": "Wicket-Keeper", "rating": 85, "base_price": 50, "age": 24},
        {"name": "Kusal Mendis", "role": "Wicket-Keeper", "rating": 83, "base_price": 50, "age": 31},
        {"name": "Sadeera Samarawickrama", "role": "Wicket-Keeper", "rating": 81, "base_price": 30, "age": 30},
        {"name": "Mushfiqur Rahim", "role": "Wicket-Keeper", "rating": 80, "base_price": 50, "age": 39},
        {"name": "Shai Hope", "role": "Wicket-Keeper", "rating": 82, "base_price": 75, "age": 32},
        {"name": "Sarfaraz Khan", "role": "Wicket-Keeper", "rating": 81, "base_price": 30, "age": 28},
        {"name": "Narayan Jagadeesan", "role": "Wicket-Keeper", "rating": 79, "base_price": 20, "age": 30},
        {"name": "Sheldon Jackson", "role": "Wicket-Keeper", "rating": 78, "base_price": 20, "age": 39},
        {"name": "Baba Indrajith", "role": "Wicket-Keeper", "rating": 80, "base_price": 20, "age": 32},
        {"name": "Upul Tharanga", "role": "Wicket-Keeper", "rating": 81, "base_price": 50, "age": 41}
    ]
    
    # Inject Development State variables into each player data structure
    for p in raw_pool:
        # Calculate ceiling based on biological age distribution
        if p["age"] < 25:
            p["base_pot"] = min(99, p["rating"] + random.randint(8, 14))
        elif p["age"] < 30:
            p["base_pot"] = min(96, p["rating"] + random.randint(2, 6))
        else:
            p["base_pot"] = p["rating"]
        
        p["dyn_pot"] = p["base_pot"]
        p["xp"] = 0
        p["plan"] = "Balanced Alignment"
        p["match_rating_history"] = []
        p["form"] = "Good"
        
    st.session_state.player_pool = raw_pool
    random.shuffle(st.session_state.player_pool)

# --- ENGINE SESSION STATE INJECTIONS ---
for key in ["game_stage", "teams", "auction_index", "current_bid", "highest_bidder", "log_msg", "timer_seconds", "match_history", "stats_runs", "stats_wickets", "live_match_state"]:
    if key not in st.session_state: 
        st.session_state[key] = [] if "history" in key or "teams" in key else ({} if "stats" in key else (None if "bidder" in key or "state" in key else ("setup" if "stage" in key else ("" if "msg" in key else (4 if "timer" in key else 0)))))
if "match_day" not in st.session_state: st.session_state.match_day = 1
if "current_venue" not in st.session_state: st.session_state.current_venue = random.choice(VENUES)

# --- GLOBAL STYLING ARCHITECTURE ---
st.markdown("""
    <style>
    .stApp { background-color: #030712 !important; }
    h1, h2, h3, h4, h5, p, label, .stText, [data-testid="stMetricValue"] { color: #FFFFFF !important; font-family: 'Inter', sans-serif !important; }
    div[data-testid="stMetric"] { background: linear-gradient(135deg, #0F172A, #1E293B) !important; border: 1px solid #10B981 !important; border-radius: 12px !important; padding: 18px !important; }
    .news-box { padding: 24px; border-radius: 16px; background-color: #0F172A; border: 1px solid #1E293B; border-left: 6px solid #3B82F6; margin-bottom: 20px; }
    .news-headline { font-size: 24px !important; font-weight: 800; color: #FFFFFF !important; line-height: 1.3; }
    div[data-baseweb="select"] > div { background-color: #0F172A !important; color: white !important; border: 1px solid #334155 !important; border-radius: 8px !important; }
    .stButton button { background: linear-gradient(135deg, #1E293B, #0F172A) !important; color: #FFFFFF !important; border: 1px solid #334155 !important; border-radius: 8px !important; font-weight: 700 !important; padding: 12px 28px !important; transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important; }
    .stButton button:hover { background: linear-gradient(135deg, #3B82F6, #1D4ED8) !important; border-color: #60A5FA !important; transform: translateY(-2px); box-shadow: 0 8px 20px rgba(59,130,246,0.4); }
    .timer-text { font-size: 22px; font-weight: bold; color: #EF4444 !important; }
    .card-box { padding: 20px; border-radius: 12px; background-color: #0F172A; border: 1px solid #1E293B; border-left: 6px solid #3B82F6; margin-bottom: 15px; color: #FFFFFF !important; }
    </style>
""", unsafe_allow_html=True)

# --- STAGE 1: SETUP ---
if st.session_state.game_stage == "setup":
    st.header("🎮 IPL Premium Draft Room Manager")
    num_humans = st.slider("How many human players?", min_value=1, max_value=4, value=1)
    human_configs = []
    used_teams = []
    for i in range(num_humans):
        st.subheader(f"Player {i+1} Configuration")
        h_name = st.text_input(f"Manager Name", value=f"Manager {i+1}", key=f"h_name_{i}")
        available_choices = [t for t in TEAM_NAMES_POOL if t not in used_teams]
        selected_team = st.selectbox(f"Choose Franchise", options=available_choices, key=f"h_team_{i}")
        used_teams.append(selected_team)
        human_configs.append({"manager": h_name, "team": selected_team})
        
    if st.button("Initialize Tournament League", type="primary"):
        teams = []
        for hc in human_configs:
            teams.append({
                "team_name": f"{hc['manager']}'s {hc['team']}", "is_human": True, "purse": 15000, "squad": [], 
                "points": 0, "wins": 0, "losses": 0, "playing_11": [], "impact_player": None, "tactic": "Balanced Alignment", "morale": 80
            })
        for bot_team in [t for t in TEAM_NAMES_POOL if t not in used_teams]:
            teams.append({
                "team_name": f"{bot_team} (Bot)", "is_human": False, "purse": 15000, "squad": [], 
                "personality": random.choice(BOT_PERSONALITIES), "points": 0, "wins": 0, "losses": 0, "playing_11": [], "impact_player": None, "tactic": "Balanced Alignment", "morale": 75
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
        if st.session_state.current_bid == 0:
            st.session_state.current_bid = player["base_price"]
            st.session_state.highest_bidder = None
            st.session_state.timer_seconds = 4
            st.session_state.log_msg = f"Next up: {player['name']}!"

        st_autorefresh(interval=1000, key="auction_timer")
        st.markdown(f"<div class='big-font'>🔨 LIVE AUCTION CARD ({idx+1}/200)</div>", unsafe_allow_html=True)
        
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
                valid_bots = [b for b in bots if not st.session_state.highest_bidder or b["team_name"] != st.session_state.highest_bidder["team_name"]]
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

        st.markdown(f"<div class='card-box'><strong>🏃 Active Asset:</strong> {player['name']} | <strong>📊 Rating:</strong> {player['rating']} | <strong>📅 Age:</strong> {player['age']}</div>", unsafe_allow_html=True)
        
        st.metric(
            label="Current High Bid Status", 
            value=f"₹{st.session_state.current_bid/100:.2f} CR", 
            delta=f"Leader: {st.session_state.highest_bidder['team_name'] if st.session_state.highest_bidder else 'No Bids'}"
        )

        human_teams_bidding = [t for t in st.session_state.teams if t["is_human"] and t["purse"] >= (st.session_state.current_bid + 50)]
        if human_teams_bidding:
            if st.button("Raise Bid (+₹50 L)", type="primary", use_container_width=True):
                st.session_state.current_bid += 50
                st.session_state.highest_bidder = human_teams_bidding[0]
                st.session_state.timer_seconds = 4  
                st.rerun()

# --- STAGE 3: INTERACTIVE OPERATIONS HUB ---
elif st.session_state.game_stage == "dashboard":
    
    # Extract human manager options safely inside dashboard stage
    human_squads = [t for t in st.session_state.teams if t["is_human"]]
    
    # RENDER GLOBAL CONSOLE SWITCHER IN CORNER
    if len(human_squads) > 1:
        col_main_h, col_switch_h = st.columns([4, 1])
        with col_switch_h:
            selected_global_name = st.selectbox("👤 Active Profile Console:", options=[h["team_name"] for h in human_squads], key="global_profile_switcher")
            user_team = next(team for team in human_squads if team["team_name"] == selected_global_name)
    else:
        user_team = human_squads[0] if human_squads else None

    if user_team:
        st.markdown(f"""
            <div style='position: fixed; top: 70px; right: 20px; background: linear-gradient(135deg, #1E1B4B, #312E81); 
                        color: white; padding: 14px 22px; border-radius: 12px; font-weight: 800; 
                        box-shadow: 0px 8px 25px rgba(49, 46, 129, 0.6); z-index: 9999; border: 1px solid #4338CA; font-size:12px; letter-spacing:0.5px;'>
                💼 ACTIVE LIQUIDITY POOL:<br/>{user_team['team_name'].split("'s")[0]}: ₹{user_team['purse']/100:.2f}CR
            </div>
        """, unsafe_allow_html=True)

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
                st.info("🔄 First Innings Completed! Saving Innings 1 data sheet, moving to Chase...")
                for p in ms['bat_roster_current']:
                    if p["name"] in ms['bat_card_raw']: ms['innings_1_bat_final'].append({"Player": p["name"], **ms['bat_card_raw'][p["name"]]})
                    else: ms['innings_1_bat_final'].append({"Player": p["name"], "R": 0, "B": 0, "4s": 0, "6s": 0, "S/R": "DNB"})
                for p in ms['bowl_roster_current']:
                    if p["name"] in ms['bowl_card_raw']: ms['innings_1_bowl_final'].append({"Player": p["name"], **ms['bowl_card_raw'][p["name"]]})
                    else: ms['innings_1_bowl_final'].append({"Player": p["name"], "Overs": 0.0, "M": 0, "R": 0, "W": 0, "Econ": 0.0})

                ms['target'] = ms['score'] + 1; ms['innings'] = 2; ms['score'] = 0; ms['wickets'] = 0; ms['balls'] = 0
                ms['bat_team'], ms['bowl_team'] = ms['opp_team'], ms['user_team']
                ms['bat_roster_current'], ms['bowl_roster_current'] = ms['bowl_roster'], ms['bat_roster']
                ms['bat_card_raw'] = {}; ms['bowl_card_raw'] = {}
                st.rerun()
            else:
                user_won = (ms['user_team'] == ms['bat_team'] and ms['score'] >= ms['target']) or (ms['user_team'] == ms['bowl_team'] and ms['score'] < ms['target'])
                u_t = next(t for t in st.session_state.teams if t["team_name"] == ms['user_team'])
                o_t = next(t for t in st.session_state.teams if t["team_name"] == ms['opp_team'])
                
                margin_text = f"by {ms['score'] - ms['target']} runs" if ms['user_team'] == ms['bowl_team'] else f"by {10 - ms['wickets']} wickets"
                result_headline = f"{ms['bat_team'] if ms['score'] >= ms['target'] else ms['bowl_team']} won {margin_text}!"

                if user_won:
                    st.success("🎉 TOURNAMENT VICTORY!"); u_t["points"] += 2; u_t["wins"] += 1; u_t["morale"] = min(100, u_t["morale"] + 8)
                    o_t["losses"] += 1
                else:
                    st.error("🔴 MATCHDAY DEFEAT!"); o_t["points"] += 2; o_t["wins"] += 1; u_t["losses"] += 1; u_t["morale"] = max(20, u_t["morale"] - 10)
                
                if st.button("Finalize and Save Scorecard Matrix"):
                    inn2_bat_final, inn2_yet_to_bat = [], []
                    for p in ms['bat_roster_current']:
                        if p["name"] in ms['bat_card_raw']: inn2_bat_final.append({"Player": p["name"], **ms['bat_card_raw'][p["name"]]})
                        else: inn2_yet_to_bat.append(p["name"]); inn2_bat_final.append({"Player": p["name"], "R": 0, "B": 0, "4s": 0, "6s": 0, "S/R": "DNB"})
                    inn2_bowl_final = []
                    for p in ms['bowl_roster_current']:
                        if p["name"] in ms['bowl_card_raw']: inn2_bowl_final.append({"Player": p["name"], **ms['bowl_card_raw'][p["name"]]})
                        else: inn2_bowl_final.append({"Player": p["name"], "Overs": 0.0, "M": 0, "R": 0, "W": 0, "Econ": 0.0})

                    st.session_state.match_history.append({
                        "fixture": f"{ms['user_team']} vs {ms['opp_team']}", "result": result_headline, "detailed": True,
                        "inn1_bat_team": ms['user_team'], "inn1_bowl_team": ms['opp_team'], "inn2_bat_team": ms['opp_team'], "inn2_bowl_team": ms['user_team'],
                        "inn1_bat": ms['innings_1_bat_final'], "inn1_bowl": ms['innings_1_bowl_final'], "inn1_ytb": [], "inn2_bat": inn2_bat_final, "inn2_bowl": inn2_bowl_final, "inn2_ytb": inn2_yet_to_bat
                    })
                    
                    # MATCHDAY CONCLUSION TRAINING PASS: Apply matchday XP accumulation loops across the active playing roster elements
                    for player in u_t["squad"]:
                        is_starter = player in u_t["playing_11"]
                        age_mult = 2.5 if player["age"] < 25 else 1.0
                        plan_mult = 1.0 if player["plan"] == "Balanced Alignment" else 2.2
                        status_mult = 1.5 if is_starter else 0.4
                        
                        xp_gained = int(35 * age_mult * plan_mult * status_mult)
                        player["xp"] += xp_gained
                        if player["xp"] >= 100:
                            if player["rating"] < player["dyn_pot"]:
                                player["rating"] += 1
                            player["xp"] = 0
                            
                    st.session_state.match_day += 1; st.session_state.current_venue = random.choice(VENUES); st.rerun()
                st.stop()

        curr_batsman_idx = min(ms['wickets'], 10)
        curr_bowler_idx = (ms['balls'] // 6) % 5
        bat_player_name = ms['bat_roster_current'][curr_batsman_idx]["name"] if curr_batsman_idx < len(ms['bat_roster_current']) else "Tailender"
        bowl_player_name = ms['bowl_roster_current'][curr_bowler_idx]["name"] if curr_bowler_idx < len(ms['bowl_roster_current']) else "Part-Timer"

        st.write(f"🏃 **On-Strike Batsman:** {bat_player_name} | 🎯 **Active Bowler:** {bowl_player_name}")
        shot = st.selectbox("Execution Directive:", ["Aggressive Lofted Ground Clearance", "Controlled Gap Placement Strike", "Safe Defensive Block"])
        mindset = st.selectbox("Tactical Mindset:", ["High-Risk Maximization", "Steady Run Accumulation", "Ultra Conservative Safety Layer"])

        if st.button("⚾ Run Next Delivery Command", type="primary", use_container_width=True):
            r = random.random()
            fours, sixes = 0, 0
            if "Aggressive" in shot:
                if r < 0.22: runs = 6; sixes = 1; comment = "🚀 SIX!"
                elif r < 0.45: runs = 4; fours = 1; comment = "💥 FOUR!"
                elif r < 0.62: runs = 0; ms['wickets'] += 1; comment = "☝️ OUT!"
                else: runs = random.choice([0, 1]); comment = "Dot ball."
            else:
                if r < 0.75: runs = random.choice([0, 1, 2]); comment = "Steady run."
                else: runs = 0; ms['wickets'] += 1; comment = "🎯 BOWLED!"
            
            ms['score'] += runs; ms['balls'] += 1
            if bat_player_name not in ms['bat_card_raw']: ms['bat_card_raw'][bat_player_name] = {"R": 0, "B": 0, "4s": 0, "6s": 0, "S/R": 0.0}
            ms['bat_card_raw'][bat_player_name]["R"] += runs
            ms['bat_card_raw'][bat_player_name]["B"] += 1
            ms['bat_card_raw'][bat_player_name]["4s"] += fours
            ms['bat_card_raw'][bat_player_name]["6s"] += sixes
            ms['bat_card_raw'][bat_player_name]["S/R"] = round((ms['bat_card_raw'][bat_player_name]["R"] / ms['bat_card_raw'][bat_player_name]["B"]) * 100, 2)
            st.session_state.stats_runs[bat_player_name] = st.session_state.stats_runs.get(bat_player_name, 0) + runs
            
            if bowl_player_name not in ms['bowl_card_raw']: ms['bowl_card_raw'][bowl_player_name] = {"Overs": 0.0, "M": 0, "R": 0, "W": 0, "Econ": 0.0}
            ms['bowl_card_raw'][bowl_player_name]["R"] += runs
            balls_bowled = int(round((ms['bowl_card_raw'][bowl_player_name]["Overs"] * 10) % 10)) + 1
            overs_bowled = int(ms['bowl_card_raw'][bowl_player_name]["Overs"])
            if balls_bowled >= 6: overs_bowled += 1; balls_bowled = 0
            ms['bowl_card_raw'][bowl_player_name]["Overs"] = float(f"{overs_bowled}.{balls_bowled}")
            if runs == 0 and "OUT" in comment:
                ms['bowl_card_raw'][bowl_player_name]["W"] += 1
                st.session_state.stats_wickets[bowl_player_name] = st.session_state.stats_wickets.get(bowl_player_name, 0) + 1
            st.rerun()
        st.stop()

    st.header(f"🏆 IPL Franchise Operations Hub — Day {st.session_state.match_day}/14")
    
    # MATCHDAY ENVIRONMENT CARD
    st.markdown(f"""
        <div style='padding: 20px; border-radius: 14px; background: linear-gradient(135deg, #1E1B4B, #0F172A); border: 1px solid #3B82F6; margin-bottom: 24px;'>
            <h4 style='margin:0; color:#38BDF8; font-weight:800;'>🏟️ CURRENT MATCHDAY ENVIRONMENT: {st.session_state.current_venue['name']}</h4>
            <p style='margin:6px 0 0 0; font-size:15px; color:#94A3B8;'>{st.session_state.current_venue['desc']}</p>
        </div>
    """, unsafe_allow_html=True)

    tab_news, tab_roster, tab_table, tab_caps, tab_career = st.tabs(["📰 Media Newsroom", "👥 Roster Player Hub", "📊 League Standings", "👑 Cap Races", "👔 Office Suite"])

    # --- TAB 1: NEWSROOM ---
    with tab_news:
        if st.session_state.match_history:
            for match in reversed(st.session_state.match_history):
                st.markdown(f"<div class='news-box'><div class='news-headline'>{match['result']}</div><p>Fixture: {match['fixture']}</p></div>", unsafe_allow_html=True)
                with st.expander("📊 View Separated Dynamic Scorecard Matrix"):
                    if match.get("detailed", False):
                        st.markdown(f"### 🏏 Innings 1 — Batting: **{match['inn1_bat_team']}**")
                        st.table(match["inn1_bat"])
                        st.markdown(f"### 🎯 Innings 1 — Bowling: **{match['inn1_bowl_team']}**")
                        st.table(match["inn1_bowl"])
                        st.markdown(f"### 🏏 Innings 2 — Batting: **{match['inn2_bat_team']}**")
                        st.table(match["inn2_bat"])
                        if match.get("inn2_ytb"): st.markdown(f"**Yet to bat:** {', '.join(match['inn2_ytb'])}")
                        st.markdown(f"### 🎯 Innings 2 — Bowling: **{match['inn2_bowl_team']}**")
                        st.table(match["inn2_bowl"])
        else: st.caption("Advance fixtures via the Office Suite tab.")

   # --- TAB 2: ROSTER HUD & DEVELOPMENT PIPELINES ---
    with tab_roster:
        if user_team:
            st.subheader(f"👥 Squad Hub & Academy Trait Allocator: {user_team['team_name']}")
            col_selects, col_preview = st.columns([2, 3])
            with col_selects:
                player_map = {p["name"]: p for p in user_team["squad"]}
                current_p11 = [p["name"] for p in user_team["playing_11"]] if user_team["playing_11"] else list(player_map.keys())[:11]
                new_p11 = st.multiselect("Select Your Starting XI Lineup Starters:", options=list(player_map.keys()), default=current_p11, key=f"hub_p11_{user_team['team_name']}")
                remaining_squad = [n for n in player_map.keys() if n not in new_p11]
                new_sub = st.selectbox("Assign Playing 12 Impact Sub Slot:", options=remaining_squad if remaining_squad else ["None"])
                if st.button("💾 Apply Tactics Layout", use_container_width=True):
                    user_team["playing_11"] = [player_map[n] for n in new_p11]
                    user_team["impact_player"] = player_map[new_sub] if new_sub != "None" else None
                    st.success("Roster configurations stored!")
            
            # >>> REPLACE ONLY THIS UNDERNEATH <<<
            with col_preview:
                st.markdown("#### 🏋️ Active Squad Matrix & Development Assignment")
                for p in user_team["squad"]:
                    is_starter = "⭐ Starter XI" if p in user_team["playing_11"] else ("🔄 Impact Sub" if user_team["impact_player"] and p["name"] == user_team["impact_player"]["name"] else "📋 Bench Reserve")
                    color_tag = "#38BDF8" if "Starter" in is_starter else ("#F59E0B" if "Impact" in is_starter else "#475569")
                    
                    # Safe extraction parameters
                    p_age = p.get("age", 25)
                    p_rating = p.get("rating", p.get("OVR", 80))
                    p_dyn_pot = p.get("dyn_pot", p_rating)
                    p_xp = p.get("xp", 0)
                    p_plan = p.get("plan", "Balanced Alignment")

                    with st.expander(f"{p['name']} (OVR {p_rating} | Age {p_age}) — {is_starter}"):
                        p["plan"] = st.selectbox(
                            "Strategic Target Development Plan:", 
                            ["Balanced Alignment", "Focused Skill Burst", "Tactical IQ Training"], 
                            key=f"plan_sel_{p['name']}", 
                            index=0 if p_plan == "Balanced Alignment" else (1 if p_plan == "Focused Skill Burst" else 2)
                        )
                        st.progress(p_xp / 100)
                        st.caption(f"XP Status: {p_xp}/100 | Hidden Potential Ceiling: {p_dyn_pot}")
    # --- TAB 3: STANDINGS ---
    with tab_table:
        st.table(sorted([{"Franchise Team": t["team_name"], "Wins": t["wins"], "Losses": t["losses"], "Points": t["points"]} for t in st.session_state.teams], key=lambda x: x["Points"], reverse=True))

    # --- TAB 4: CAPS RACE ---
    with tab_caps:
        col_o, col_p = st.columns(2)
        with col_o:
            st.markdown("### 🟠 Orange Cap Leaderboard")
            for idx, (name, runs) in enumerate(sorted(st.session_state.stats_runs.items(), key=lambda x: x[1], reverse=True)[:10]): st.write(f"**{idx+1}. {name}** — {runs} runs")
        with col_p:
            st.markdown("### 🟣 Purple Cap Leaderboard")
            for idx, (name, wck) in enumerate(sorted(st.session_state.stats_wickets.items(), key=lambda x: x[1], reverse=True)[:10]): st.write(f"**{idx+1}. {name}** — {wck} wickets")

    # --- TAB 5: OFFICE CONSOLE & DYNAMIC PROGRESSION SYSTEMS ---
    with tab_career:
        if user_team:
            opp_team = next(t for t in st.session_state.teams if not t["is_human"])
            col_met1, col_met2, col_met3 = st.columns(3)
            with col_met1: st.metric("Franchise Points", user_team["points"])
            with col_met2: st.metric("Locker Morale", f"{user_team['morale']}%")
            with col_met3: st.metric("Budget Remaining", f"₹{user_team['purse']/100:.2f} CR")
            st.divider()
            
            # END OF SEASON ENGINE OVERLAY TRIPPED ONCE TERMINAL REACHES THE DAY 14 HARD CEILING
            if st.session_state.match_day > 14:
                st.warning("🚨 SEASON HAS CONCLUDED! The board is processing structural contracts and age progression metrics.")
                if st.button("🔄 Execute End-of-Season Recalculation Loop", type="primary", use_container_width=True):
                    st.write("### 📊 Annual Operations Re-Indexing Report:")
                    for t in st.session_state.teams:
                        for p in t["squad"]:
                            old_ovr = p["rating"]
                            # Young players with high team morale gain breakout potential boosts
                            if p["age"] < 25 and t["morale"] > 80:
                                p["dyn_pot"] = min(99, p["dyn_pot"] + random.randint(1, 3))
                                p["rating"] = min(p["dyn_pot"], p["rating"] + 2)
                                st.write(f"• 📈 **Breakout Superstar:** {p['name']} ({t['team_name']}) grew to `{p['rating']}` OVR. Ceiling expanded to `{p['dyn_pot']}`.")
                            # Biological Age Regression Loop triggered smoothly at Age 32+
                            elif p["age"] >= 32:
                                drop = 2 if p in t["playing_11"] else 3  # Bench warming veterans decay faster
                                p["rating"] = max(65, p["rating"] - drop)
                                p["dyn_pot"] = p["rating"]
                                st.write(f"• 📉 **Biological Age Regression:** Veteran {p['name']} ({t['team_name']}) drops from `{old_ovr}` to `{p['rating']}` OVR due to physical attrition factors.")
                            
                            p["age"] += 1
                    st.session_state.match_day = 1
                    st.rerun()
            else:
                col_sim1, col_sim2 = st.columns(2)
                with col_sim1:
                    if st.button("🎮 Enter Live Ball-by-Ball Match Arena", type="primary", use_container_width=True):
                        st.session_state.live_match_state = {
                            "user_team": user_team["team_name"], "opp_team": opp_team["team_name"], "bat_team": user_team["team_name"], "bowl_team": opp_team["team_name"],
                            "bat_roster": user_team["playing_11"], "bowl_roster": opp_team["playing_11"], "bat_roster_current": user_team["playing_11"], "bowl_roster_current": opp_team["playing_11"],
                            "innings": 1, "score": 0, "wickets": 0, "balls": 0, "target": 0, "innings_1_bat_final": [], "innings_1_bowl_final": [], "bat_card_raw": {}, "bowl_card_raw": {}
                        }
                        st.rerun()
                with col_sim2:
                    if st.button("⚡ Fast Skip Match via Auto Simulation Loops", use_container_width=True):
                        boost_role = st.session_state.current_venue["boost_role"]
                        boost_amt = st.session_state.current_venue["boost_amount"]
                        random.shuffle(st.session_state.teams)
                        
                        for i in range(0, len(st.session_state.teams) - 1, 2):
                            t1, t2 = st.session_state.teams[i], st.session_state.teams[i+1]
                            t1_b = sum([p["rating"] + (boost_amt if p["role"] == boost_role else 0) for p in t1["playing_11"]])
                            t2_b = sum([p["rating"] + (boost_amt if p["role"] == boost_role else 0) for p in t2["playing_11"]])
                            p1, p2 = t1_b + random.randint(-40, 40), t2_b + random.randint(-40, 40)
                            t1_runs, t2_runs = random.randint(140, 220), random.randint(130, 210)
                            t2_wickets = random.randint(2, 10)
                            
                            if p1 > p2:
                                t1["points"] += 2; t1["wins"] += 1; t2["losses"] += 1
                                headline = f"{t1['team_name']} won by {abs(t1_runs - t2_runs)} runs!"
                            else:
                                t2["points"] += 2; t2["wins"] += 1; t1["losses"] += 1
                                headline = f"{t2['team_name']} won by {random.randint(2, 8)} wickets!"
                                
                          # FAST SIMULATION TRAINING ITERATION PASS
                            for t_curr in [t1, t2]:
                                for p in t_curr["squad"]:
                                    # Safe extraction & inline fallback initialization
                                    p_rating = p.get("rating", p.get("OVR", 80))
                                    p_dyn_pot = p.get("dyn_pot", p_rating)
                                    
                                    if "xp" not in p:
                                        p["xp"] = 0
                                    if "rating" not in p:
                                        p["rating"] = p_rating
                                    if "dyn_pot" not in p:
                                        p["dyn_pot"] = p_dyn_pot

                                    # Safely apply the XP gains
                                    p["xp"] += random.randint(15, 45)
                                    if p["xp"] >= 100:
                                        if p["rating"] < p["dyn_pot"]: 
                                            p["rating"] += 1
                                        p["xp"] = 0
                                
                            inn1_bat_list, inn1_bowl_list = [], []
                            for idx, p in enumerate(t1["playing_11"]):
                                r = random.randint(35, 85) if idx < 3 else random.randint(0, 35)
                                b = int(r / 1.3) + 1
                                inn1_bat_list.append({"Player": p["name"], "R": r, "B": b, "4s": 2, "6s": 1, "S/R": round((r/b)*100, 2)})
                                st.session_state.stats_runs[p["name"]] = st.session_state.stats_runs.get(p["name"], 0) + r
                            for idx, p in enumerate(t2["playing_11"]):
                                is_bowl = p["role"] in ["Bowler", "All-Rounder"] or idx >= 6
                                w = random.randint(1, 3) if is_bowl else 0
                                rc = random.randint(20, 40) if is_bowl else 0
                                inn1_bowl_list.append({"Player": p["name"], "Overs": 4.0 if is_bowl else 0.0, "M": 0, "R": rc, "W": w, "Econ": round(rc/4, 2) if is_bowl else 0.0})
                                if w > 0: st.session_state.stats_wickets[p["name"]] = st.session_state.stats_wickets.get(p["name"], 0) + w

                            inn2_bat_list, inn2_bowl_list = [], []
                            inn2_ytb = [p["name"] for p in t2["playing_11"][t2_wickets:]] if t2_wickets < 11 else []
                            for idx, p in enumerate(t2["playing_11"]):
                                if idx < t2_wickets:
                                    r = random.randint(10, 40); b = int(r / 1.2) + 1
                                    inn2_bat_list.append({"Player": p["name"], "R": r, "B": b, "4s": 1, "6s": 1, "S/R": round((r/b)*100, 2)})
                                else: inn2_bat_list.append({"Player": p["name"], "R": 0, "B": 0, "4s": 0, "6s": 0, "S/R": "DNB"})
                            for idx, p in enumerate(t1["playing_11"]):
                                is_bowl = p["role"] in ["Bowler", "All-Rounder"] or idx >= 6
                                w = random.randint(1, 2) if is_bowl else 0; rc = random.randint(15, 35) if is_bowl else 0
                                inn2_bowl_list.append({"Player": p["name"], "Overs": 4.0 if is_bowl else 0.0, "M": 0, "R": rc, "W": w, "Econ": round(rc/4, 2) if is_bowl else 0.0})

                            st.session_state.match_history.append({
                                "fixture": f"{t1['team_name']} vs {t2['team_name']}", "result": headline, "detailed": True,
                                "inn1_bat_team": t1["team_name"], "inn1_bowl_team": t2["team_name"], "inn2_bat_team": t2["team_name"], "inn2_bowl_team": t1["team_name"],
                                "inn1_bat": inn1_bat_list, "inn1_bowl": inn1_bowl_list, "inn1_ytb": [], "inn2_bat": inn2_bat_list, "inn2_bowl": inn2_bowl_list, "inn2_ytb": inn2_ytb
                            })
                        st.session_state.match_day += 1; st.session_state.current_venue = random.choice(VENUES); st.rerun()
