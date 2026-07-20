import streamlit as st
import random
import time
import pandas as pd
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
    {"name": "M. Chinnaswamy Stadium (Bengaluru)", "desc": "💥 Flat Track Paradise! Batsmen get a massive +10 rating boost. Bowlers suffer.", "boost_role": "Batsman", "boost_amount": 10, "short": "M. Chinnaswamy"},
    {"name": "M. A. Chidambaram Stadium (Chepauk)", "desc": "🌀 Dry, Dusty Spin Turner! Spinners and clever bowlers get a +10 tactical edge.", "boost_role": "Bowler", "boost_amount": 10, "short": "Chepauk Stadium"},
    {"name": "Wankhede Stadium (Mumbai)", "desc": "🌊 True Bounce & Sea Breeze! All-Rounders thrive under pressure here with a +8 boost.", "boost_role": "All-Rounder", "boost_amount": 8, "short": "Wankhede Stadium"},
    {"name": "Narendra Modi Stadium (Ahmedabad)", "desc": "⚖️ Balanced Coliseum! Symmetrical boundaries favor a steady, disciplined game layout.", "boost_role": "Balanced", "boost_amount": 0, "short": "Narendra Modi"}
]

# --- MASTER 200 REAL-WORLD PLAYER DATABASE ---
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
        {"name": "Nicholas Pooran", "wicket-keeper": True, "role": "Wicket-Keeper", "rating": 92, "base_price": 150, "age": 30},
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
    
    while len(raw_pool) < 200:
        raw_pool.append({"name": f"Domestic Prospect #{len(raw_pool)+1}", "role": "Bowler", "rating": 75, "base_price": 20, "age": 22})

    for p in raw_pool:
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
        p["form"] = random.choice(["Steady", "Good", "Red-Hot"])
        
    st.session_state.player_pool = raw_pool
    random.shuffle(st.session_state.player_pool)

# --- SYSTEM INJECTIONS ---
for key in ["game_stage", "teams", "auction_index", "current_bid", "highest_bidder", "log_msg", "timer_seconds", "match_history", "stats_runs", "stats_wickets", "live_match_state", "current_tab", "selected_headline_idx"]:
    if key not in st.session_state: 
        if key == "current_tab": st.session_state[key] = "Home"
        elif key == "selected_headline_idx": st.session_state[key] = 0
        else: st.session_state[key] = [] if "history" in key or "teams" in key else ({} if "stats" in key else (None if "bidder" in key or "state" in key else ("setup" if "stage" in key else ("" if "msg" in key else (4 if "timer" in key else 0)))))

if "match_day" not in st.session_state: st.session_state.match_day = 1
if "current_venue" not in st.session_state: st.session_state.current_venue = random.choice(VENUES)

# --- DEFENSIVE DATA MIGRATION OVERLAY (CRASH SHIELD) ---
if "teams" in st.session_state and isinstance(st.session_state.teams, list):
    for team in st.session_state.teams:
        if "manager" not in team:
            team["manager"] = "Franchise Owner"
        if "nrr" not in team:
            team["nrr"] = 0.00

# --- ULTRALUX DARK DESIGN SYSTEM ENGINE ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14 !important; }
    [data-testid="stSidebar"] { background-color: #11141b !important; border-right: 1px solid #1c202a !important; min-width: 260px !important; }
    .top-badge-date { background-color: #16221f !important; border: 1px solid #1b4d3e !important; border-radius: 8px; padding: 8px 16px; color: #52d69b !important; font-weight: 700; font-family: 'Inter', sans-serif; display: flex; align-items: center; gap: 8px; }
    
    /* Sim & Play Match Control Header Actions Layout Checkpoints */
    .sim-match-btn button { background: #1f242e !important; color: #ffffff !important; border: 1px solid #2d3748 !important; font-weight: 700 !important; border-radius: 8px !important; padding: 10px 20px !important; transition: all 0.2s; }
    .sim-match-btn button:hover { background: #2d3748 !important; }
    .play-match-btn button { background: #10b981 !important; color: #000000 !important; border: none !important; font-weight: 800 !important; border-radius: 8px !important; padding: 10px 24px !important; transition: all 0.2s; }
    .play-match-btn button:hover { background: #34d399 !important; box-shadow: 0 0 15px rgba(16,185,129,0.3); }
    
    .dashboard-panel-card { background-color: #11141b; border: 1px solid #1c202a; border-radius: 12px; padding: 20px; height: 100%; min-height: 140px; position: relative; }
    .panel-header-text { color: #8892b0 !important; font-size: 13px !important; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px; }
    .logo-square-icon { width: 50px; height: 50px; background: linear-gradient(135deg, #ea580c, #f97316); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 18px; color: #ffffff; }
    .opponent-badge-icon { width: 44px; height: 44px; background: #ea580c; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 15px; color: #ffffff; }
    .sidebar-nav-item { padding: 12px 16px; border-radius: 8px; margin-bottom: 4px; font-weight: 700; font-size: 15px; color: #a0aec0; cursor: pointer; display: flex; align-items: center; gap: 12px; transition: all 0.15s ease; }
    .sidebar-nav-item:hover { background-color: #1c202a; color: #ffffff; }
    .sidebar-nav-item.active { background-color: #242936; color: #ffffff; border-left: 4px solid #10b981; }
    .headline-stream-card { padding: 14px; border-radius: 8px; background-color: #11141b; border: 1px solid #1c202a; margin-bottom: 8px; cursor: pointer; transition: all 0.2s ease; }
    .headline-stream-card:hover { border-color: #2d3748; background-color: #161b24; }
    .headline-stream-card.active { border-color: #10b981 !important; background-color: #121e1a !important; }
    .stat-hero-ovr { font-size: 36px; font-weight: 800; color: #ffffff; line-height: 1; }
    .stat-hero-delta-red { color: #f87171 !important; font-weight: 700; font-size: 16px; }
    .stat-hero-delta-green { color: #34d399 !important; font-weight: 700; font-size: 16px; }
    h1, h2, h3, h4, h5, p, span, div { font-family: 'Inter', sans-serif !important; }
    </style>
""", unsafe_allow_html=True)

# --- HELPERS FOR SYSTEM ARCHITECTURE ---
def get_form_offset(form_string):
    mapping = {"Slumping": -4, "Steady": 0, "Good": 2, "Red-Hot": 5}
    return mapping.get(form_string, 0)

def trigger_form_roulette():
    for t in st.session_state.teams:
        for p in t["squad"]:
            p["form"] = random.choice(["Slumping", "Steady", "Good", "Red-Hot"])

def simulate_matchday_loop():
    st.session_state.current_tab = "Home"
    boost_role = st.session_state.current_venue["boost_role"]
    boost_amt = st.session_state.current_venue["boost_amount"]
    random.shuffle(st.session_state.teams)
    
    for i in range(0, len(st.session_state.teams) - 1, 2):
        t1, t2 = st.session_state.teams[i], st.session_state.teams[i+1]
        t1_b = sum([p["rating"] + get_form_offset(p["form"]) for p in t1["playing_11"]])
        t2_b = sum([p["rating"] + get_form_offset(p["form"]) for p in t2["playing_11"]])
        
        p1, p2 = t1_b + random.randint(-40, 40), t2_b + random.randint(-40, 40)
        t1_runs, t2_runs = random.randint(145, 215), random.randint(140, 210)
        
        if p1 > p2:
            t1["points"] += 2; t1["wins"] += 1; t1["morale"] = min(100, t1.get("morale", 75) + 8)
            t2["losses"] += 1; t2["morale"] = max(20, t2.get("morale", 75) - 10)
            t1["nrr"] = t1.get("nrr", 0.0) + 0.45
            t2["nrr"] = t2.get("nrr", 0.0) - 0.45
            headline = f"{t1['team_name']} cruise to victory over {t2['team_name']}"
            body_text = f"The chase was completed successfully by the batting order assets. Performance multipliers applied securely."
        else:
            t2["points"] += 2; t2["wins"] += 1; t2["morale"] = min(100, t2.get("morale", 75) + 8)
            t1["losses"] += 1; t1["morale"] = max(20, t1.get("morale", 75) - 10)
            t2["nrr"] = t2.get("nrr", 0.0) + 0.52
            t1["nrr"] = t1.get("nrr", 0.0) - 0.52
            headline = f"{t2['team_name']} record emphatic win over {t1['team_name']}"
            body_text = f"Rival line-up elements structured clean defenses and constrained the runs effectively on this surface tier."
        
        st.session_state.match_history.append({
            "type": "MATCH REPORT", "date": f"Mar {22 + st.session_state.match_day}, 2026", "headline": headline,
            "body": body_text, "detailed": False, "t1": t1["team_name"], "t2": t2["team_name"]
        })
    
    st.session_state.match_day += 1
    trigger_form_roulette()

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
                "team_name": hc['team'], "manager": hc['manager'], "is_human": True, "purse": 15000, "squad": [], 
                "points": 0, "wins": 0, "losses": 0, "playing_11": [], "impact_player": None, "tactic": "Balanced Alignment", "morale": 80, "nrr": 0.00
            })
        for bot_team in [t for t in TEAM_NAMES_POOL if t not in used_teams]:
            teams.append({
                "team_name": bot_team, "manager": "AI Bot Executive", "is_human": False, "purse": 15000, "squad": [], 
                "personality": random.choice(BOT_PERSONALITIES), "points": 0, "wins": 0, "losses": 0, "playing_11": [], "impact_player": None, "tactic": "Balanced Alignment", "morale": 75, "nrr": 0.00
            })
        st.session_state.teams = teams
        st.session_state.game_stage = "auction"
        st.session_state.auction_index = 0
        st.session_state.timer_seconds = 4
        
        st.session_state.match_history.append({
            "type": "WELCOME", "date": "Mar 22, 2026", "headline": "New era begins: Managers take charge of team selections",
            "body": "The front offices are open. Pre-season draft analytics declare massive roster space available for young assets.", "detailed": False
        })
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
        st.markdown(f"<h3>🔨 LIVE AUCTION CARD ({idx+1}/200)</h3>", unsafe_allow_html=True)
        
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
        
        high_bidder_label = st.session_state.highest_bidder["team_name"] if st.session_state.highest_bidder is not None else 'No Bids'
        st.metric(
            label="Current High Bid Status", 
            value=f"₹{st.session_state.current_bid/100:.2f} CR", 
            delta=f"Leader: {high_bidder_label}"
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
    
    human_squads = [t for t in st.session_state.teams if t["is_human"]]
    
    if "selected_human_idx" not in st.session_state:
        st.session_state.selected_human_idx = 0
        
    user_team = human_squads[st.session_state.selected_human_idx] if human_squads else None
    
    # =========================================================
    # SIDEBAR PLATFORM DESIGN ARCHITECTURE
    # =========================================================
    with st.sidebar:
        st.markdown("<br/>", unsafe_allow_html=True)
        if user_team:
            team_short = user_team["team_name"][:3].upper()
            st.markdown(f"""
                <div style='display: flex; align-items: center; gap: 14px; padding: 10px 8px;'>
                    <div class='logo-square-icon'>{team_short}</div>
                    <div>
                        <div style='font-size: 18px; font-weight: 800; color: #ffffff;'>{user_team['team_name']}</div>
                        <div style='font-size: 13px; color: #718096; font-weight:600;'>{user_team.get('manager', 'Franchise Owner')}</div>
                    </div>
                </div>
                <br/>
            """, unsafe_allow_html=True)
            
        tabs_list = ["Home", "Squad", "Schedule", "Table", "Stats"]
        for tab in tabs_list:
            is_active_class = "active" if st.session_state.current_tab == tab else ""
            
            # Use direct sidebar native components to trigger tab switches instead of plain text leaks
            if st.sidebar.button(tab, key=f"nav_btn_{tab}", use_container_width=True):
                st.session_state.current_tab = tab
                st.rerun()
                
        st.markdown("<br/><br/><br/>", unsafe_allow_html=True)
        st.markdown("<div style='padding-left:16px; font-weight:700; color:#718096; font-size:14px;'>💛 Support</div>", unsafe_allow_html=True)
        if st.sidebar.button("🚪 Reset Console Session", key="exit_game_system"):
            st.session_state.clear()
            st.rerun()

    # =========================================================
    # TOP HEADER OPERATIONS BAR (PHOTO ONE DUAL BUTTONS)
    # =========================================================
    top_col_left, top_col_mid, top_col_right = st.columns([3, 1, 1])
    with top_col_left:
        st.markdown(f"""
            <div style='display: flex; align-items: center; gap: 12px; margin-top:4px;'>
                <div class='top-badge-date'>📅 Wed, Mar {22 + st.session_state.match_day}</div>
                <div style='color: #718096; font-size: 14px; font-weight: 600;'>Simulation Console Active</div>
            </div>
        """, unsafe_allow_html=True)
    with top_col_mid:
        st.markdown("<div class='sim-match-btn'>", unsafe_allow_html=True)
        if st.button("⏩ Sim Match", key="global_sim_match_action"):
            simulate_matchday_loop()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with top_col_right:
        st.markdown("<div class='play-match-btn'>", unsafe_allow_html=True)
        if st.button("▷ Play Match", key="global_play_match_action"):
            simulate_matchday_loop()
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # =========================================================
    # TAB ROUTING 1: HOME VIEW (CLEAN PACKED COMPACT CARDS)
    # =========================================================
    if st.session_state.current_tab == "Home":
        met_col1, met_col2, met_col3 = st.columns(3)
        
        with met_col1:
            bot_teams_pool = [t for t in st.session_state.teams if not t["is_human"]]
            next_opp = bot_teams_pool[0]["team_name"] if bot_teams_pool else "Rival Franchise"
            opp_short = next_opp[:3].upper()
            
            # Content is completely packed into the card, no overflow leakage
            st.markdown(f"""
                <div class='dashboard-panel-card'>
                    <div class='panel-header-text'>🔮 Next Match</div>
                    <div style='display: flex; align-items: center; gap: 16px; margin-top: 12px;'>
                        <div class='opponent-badge-icon'>{opp_short}</div>
                        <div>
                            <div style='font-size: 18px; font-weight: 800; color: #ffffff;'>vs {next_opp}</div>
                            <div style='font-size: 13px; color: #718096; font-weight: 600; margin-top:2px;'>Today • Away • {st.session_state.current_venue['short']}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with met_col2:
            sorted_teams = sorted(st.session_state.teams, key=lambda x: x["points"], reverse=True)
            my_pos = sorted_teams.index(user_team) + 1 if user_team in sorted_teams else 3
            nrr_value = user_team.get("nrr", 1.16) if user_team else 1.16
            nrr_class = "stat-hero-delta-green" if nrr_value >= 0 else "stat-hero-delta-red"
            
            st.markdown(f"""
                <div class='dashboard-panel-card'>
                    <div class='panel-header-text'>🏆 League Position</div>
                    <div style='display: flex; justify-content: space-between; align-items: flex-end; margin-top: 10px;'>
                        <div>
                            <div class='stat-hero-ovr'>#{my_pos}</div>
                            <div style='font-size: 13px; color: #718096; font-weight:600; margin-top: 6px;'>{user_team['points'] if user_team else 2} pts accumulated</div>
                        </div>
                        <div style='text-align: right;'>
                            <div class='{nrr_class}'>{nrr_value:+.2f}</div>
                            <div style='font-size: 11px; color: #718096; font-weight:700; margin-top:2px;'>NET RUN RATE</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with met_col3:
            wins_count = user_team["wins"] if user_team else 1
            loss_count = user_team["losses"] if user_team else 0
            
            st.markdown(f"""
                <div class='dashboard-panel-card'>
                    <div class='panel-header-text'>📈 Recent Form</div>
                    <div style='display: flex; justify-content: space-between; align-items: center; margin-top: 10px;'>
                        <div>
                            <div style='display: flex; gap: 6px; align-items: center;'>
                                <div style='width: 10px; height: 10px; background-color: #10b981; border-radius: 50%;'></div>
                                <div style='width: 10px; height: 10px; background-color: #718096; border-radius: 50%;'></div>
                                <div style='width: 10px; height: 10px; background-color: #718096; border-radius: 50%;'></div>
                            </div>
                            <div style='font-size: 13px; color: #718096; font-weight:600; margin-top: 16px;'>Locker Morale: {user_team['morale'] if user_team else 80}%</div>
                        </div>
                        <div style='text-align: right;'>
                            <div style='font-size: 20px; font-weight: 800; color: #10b981;'>{wins_count}W <span style='color:#ef4444;'>- {loss_count}L</span></div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br/><h4 style='color: #8892b0; font-size:14px; font-weight:700; text-transform:uppercase;'>📰 Operations Wire & Central Newsroom</h4>", unsafe_allow_html=True)
        
        news_stream_col, news_view_col = st.columns([2, 3])
        
        with news_stream_col:
            st.markdown("<div style='max-height: 480px; overflow-y: auto;'>", unsafe_allow_html=True)
            reversed_history = list(enumerate(st.session_state.match_history))[::-1]
            if not reversed_history:
                st.caption("No historical briefings indexed.")
            else:
                for idx, history_item in reversed_history:
                    is_selected = "active" if st.session_state.selected_headline_idx == idx else ""
                    item_type = history_item.get("type", "REPORT")
                    
                    st.markdown(f"""
                        <div class='headline-stream-card {is_selected}'>
                            <div style='font-size: 11px; font-weight: 700; color: #10b981; text-transform: uppercase;'>🟢 {item_type} • {history_item['date']}</div>
                            <div style='font-size: 15px; font-weight: 700; color: #ffffff; margin-top: 4px;'>{history_item['headline']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Read Article", key=f"read_wire_{idx}", use_container_width=True):
                        st.session_state.selected_headline_idx = idx
                        st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
            
        with news_view_col:
            active_idx = st.session_state.selected_headline_idx
            if active_idx < len(st.session_state.match_history):
                article = st.session_state.match_history[active_idx]
                st.markdown(f"""
                    <div style='background-color: #11141b; border: 1px solid #1c202a; border-radius: 12px; padding: 30px; min-height: 320px;'>
                        <div style='font-size: 13px; font-weight: 700; color: #8892b0; text-transform: uppercase;'>{article.get('type', 'NEWS WIRE')} • {article['date']}</div>
                        <h2 style='color: #ffffff; font-weight: 800; margin-top: 10px; font-size: 28px;'>{article['headline']}</h2>
                        <p style='color: #a0aec0; font-size: 16px; margin-top: 20px; line-height: 1.6;'>{article['body']}</p>
                        <p style='color: #718096; font-size: 14px; margin-top: 15px;'>Roster evaluations, dynamic multipliers, and training pipelines are running silently under management alignment plans.</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("📊 View Complete League Standings Grid", use_container_width=True):
                    st.session_state.current_tab = "Table"
                    st.rerun()

    # =========================================================
    # TAB ROUTING 2: ROSTER HUD VIEW
    # =========================================================
    elif st.session_state.current_tab == "Squad":
        if user_team:
            st.subheader(f"👥 Squad Hub & Development Matrix: {user_team['team_name']}")
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
            with col_preview:
                st.markdown("#### 🏋️ Active Squad Matrix & Assignment")
                for p in user_team["squad"]:
                    is_starter = "⭐ Starter XI" if p in user_team["playing_11"] else ("🔄 Impact Sub" if user_team["impact_player"] and p["name"] == user_team["impact_player"]["name"] else "📋 Bench Reserve")
                    form_color = "red" if p["form"] == "Slumping" else ("orange" if p["form"] == "Steady" else "green")
                    with st.expander(f"{p['name']} (OVR {p['rating']} | Age {p['age']}) — {is_starter}"):
                        st.markdown(f"**Current Player Condition:** :{form_color}[{p['form']}] (OVR Impact: {get_form_offset(p['form']):+})")
                        p["plan"] = st.selectbox("Strategic Target Plan:", ["Balanced Alignment", "Focused Skill Burst", "Tactical IQ Training"], key=f"plan_sel_{p['name']}", index=0 if p["plan"] == "Balanced Alignment" else (1 if p["plan"] == "Focused Skill Burst" else 2))
                        st.progress(p["xp"] / 100)
                        st.caption(f"XP Status: {p['xp']}/100 | Hidden Potential Ceiling: {p['dyn_pot']}")

    # =========================================================
    # TAB ROUTING 3: SCHEDULE METRIC DATA TABLES
    # =========================================================
    elif st.session_state.current_tab == "Schedule":
        st.subheader("🗓️ Complete Tournament League Fixtures")
        schedule_data = []
        for match in st.session_state.match_history:
            if match.get("type") == "MATCH REPORT":
                schedule_data.append({"Date": match["date"], "Fixture Briefing": match["headline"]})
        if schedule_data:
            st.dataframe(pd.DataFrame(schedule_data), use_container_width=True, hide_index=True)
        else:
            st.info("No corporate fixtures auto-simulated yet. Click 'Sim Match' to run iterations.")

    # =========================================================
    # TAB ROUTING 4: STANDINGS BOARD VIEW
    # =========================================================
    elif st.session_state.current_tab == "Table":
        st.subheader("📊 Dynamic League Standings Leaderboard")
        standings_board = sorted([
            {
                "Franchise Team": t["team_name"], 
                "Wins": t["wins"], 
                "Losses": t["losses"], 
                "Points": t["points"], 
                "Net Run Rate": f"{t.get('nrr', 0.00):+.2f}",
                "Morale": f"{t.get('morale', 75)}%"
            } for t in st.session_state.teams
        ], key=lambda x: int(x["Points"]), reverse=True)
        
        st.table(pd.DataFrame(standings_board))

    # =========================================================
    # TAB ROUTING 5: STATS CAPS RACE OVERLAYS
    # =========================================================
    elif st.session_state.current_tab == "Stats":
        st.subheader("👑 Global League Leader Cap Race Standings")
        col_o, col_p = st.columns(2)
        with col_o:
            st.markdown("### 🟠 Orange Cap Leaderboard (Top Batsmen)")
            if st.session_state.stats_runs:
                for idx, (name, runs) in enumerate(sorted(st.session_state.stats_runs.items(), key=lambda x: x[1], reverse=True)[:10]): 
                    st.write(f"**{idx+1}. {name}** — {runs} runs accumulated")
            else:
                st.caption("No batsman data compiled yet.")
        with col_p:
            st.markdown("### 🟣 Purple Cap Leaderboard (Top Bowlers)")
            if st.session_state.stats_wickets:
                for idx, (name, wck) in enumerate(sorted(st.session_state.stats_wickets.items(), key=lambda x: x[1], reverse=True)[:10]): 
                    st.write(f"**{idx+1}. {name}** — {wck} wickets claimed")
            else:
                st.caption("No bowler data compiled yet.")
