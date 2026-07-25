import random
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# --- ULTIMATE EXECUTIVE DASHBOARD CONFIGURATION ---
st.set_page_config(
    page_title="IPL Pro-Manager Simulation Console",
    page_icon="🏏",
    layout="wide",
)

# --- DATA POOLS ---
TEAM_NAMES_POOL = [
    "Mumbai Indians",
    "Chennai Super Kings",
    "Royal Challengers Bengaluru",
    "Delhi Capitals",
    "Kolkata Knight Riders",
    "Gujarat Titans",
    "Punjab Kings",
    "Rajasthan Royals",
    "Lucknow Super Giants",
    "Sunrisers Hyderabad",
]

BOT_PERSONALITIES = ["Batting-Heavy", "Bowling-Heavy", "Youth-Focus", "Balanced"]

VENUES = [
    {
        "name": "M. Chinnaswamy Stadium (Bengaluru)",
        "desc": "💥 Flat Track Paradise! Batsmen get a massive boost. Bowlers suffer.",
        "boost_role": "Batsman",
        "boost_amount": 10,
        "short": "M. Chinnaswamy",
    },
    {
        "name": "M. A. Chidambaram Stadium (Chepauk)",
        "desc": "🌀 Dry, Dusty Spin Turner! Spinners get a +10 tactical edge.",
        "boost_role": "Bowler",
        "boost_amount": 10,
        "short": "Chepauk Stadium",
    },
    {
        "name": "Wankhede Stadium (Mumbai)",
        "desc": (
            "🌊 True Bounce & Sea Breeze! All-Rounders thrive under pressure."
        ),
        "boost_role": "All-Rounder",
        "boost_amount": 8,
        "short": "Wankhede Stadium",
    },
    {
        "name": "Narendra Modi Stadium (Ahmedabad)",
        "desc": (
            "⚖️ Balanced Coliseum! Symmetrical boundaries favor steady"
            " gameplay."
        ),
        "boost_role": "Balanced",
        "boost_amount": 0,
        "short": "Narendra Modi",
    },
]

MASTER_200_REAL_PLAYERS = [
    # ==================== BATSMEN (1 - 60) ====================
    {"name": "Virat Kohli", "role": "Batsman", "batting_rating": 96, "bowling_rating": 20, "base_price": 200, "age": 35},
    {"name": "Suryakumar Yadav", "role": "Batsman", "batting_rating": 93, "bowling_rating": 15, "base_price": 150, "age": 33},
    {"name": "Rohit Sharma", "role": "Batsman", "batting_rating": 95, "bowling_rating": 25, "base_price": 200, "age": 36},
    {"name": "Travis Head", "role": "Batsman", "batting_rating": 92, "bowling_rating": 35, "base_price": 150, "age": 30},
    {"name": "Shubman Gill", "role": "Batsman", "batting_rating": 89, "bowling_rating": 10, "base_price": 100, "age": 24},
    {"name": "Yashasvi Jaiswal", "role": "Batsman", "batting_rating": 90, "bowling_rating": 20, "base_price": 100, "age": 22},
    {"name": "Ruturaj Gaikwad", "role": "Batsman", "batting_rating": 88, "bowling_rating": 10, "base_price": 100, "age": 27},
    {"name": "Rinku Singh", "role": "Batsman", "batting_rating": 86, "bowling_rating": 15, "base_price": 50, "age": 26},
    {"name": "Sai Sudharsan", "role": "Batsman", "batting_rating": 84, "bowling_rating": 10, "base_price": 50, "age": 23},
    {"name": "David Warner", "role": "Batsman", "batting_rating": 85, "bowling_rating": 10, "base_price": 100, "age": 37},
    {"name": "Faf du Plessis", "role": "Batsman", "batting_rating": 86, "bowling_rating": 10, "base_price": 100, "age": 39},
    {"name": "Kane Williamson", "role": "Batsman", "batting_rating": 85, "bowling_rating": 20, "base_price": 100, "age": 33},
    {"name": "Tilak Varma", "role": "Batsman", "batting_rating": 85, "bowling_rating": 30, "base_price": 50, "age": 23},
    {"name": "David Miller", "role": "Batsman", "batting_rating": 87, "bowling_rating": 10, "base_price": 100, "age": 34},
    {"name": "Shimron Hetmyer", "role": "Batsman", "batting_rating": 83, "bowling_rating": 10, "base_price": 75, "age": 27},
    {"name": "Rovman Powell", "role": "Batsman", "batting_rating": 84, "bowling_rating": 25, "base_price": 75, "age": 30},
    {"name": "Rahul Tripathi", "role": "Batsman", "batting_rating": 81, "bowling_rating": 10, "base_price": 30, "age": 33},
    {"name": "Devdutt Padikkal", "role": "Batsman", "batting_rating": 80, "bowling_rating": 10, "base_price": 30, "age": 23},
    {"name": "Prithvi Shaw", "role": "Batsman", "batting_rating": 82, "bowling_rating": 10, "base_price": 50, "age": 24},
    {"name": "Tristan Stubbs", "role": "Batsman", "batting_rating": 86, "bowling_rating": 25, "base_price": 50, "age": 23},
    {"name": "Tim David", "role": "Batsman", "batting_rating": 84, "bowling_rating": 15, "base_price": 75, "age": 28},
    {"name": "Ajinkya Rahane", "role": "Batsman", "batting_rating": 80, "bowling_rating": 10, "base_price": 50, "age": 35},
    {"name": "Riyan Parag", "role": "Batsman", "batting_rating": 84, "bowling_rating": 35, "base_price": 30, "age": 22},
    {"name": "Steve Smith", "role": "Batsman", "batting_rating": 83, "bowling_rating": 20, "base_price": 200, "age": 34},
    {"name": "Harry Brook", "role": "Batsman", "batting_rating": 86, "bowling_rating": 10, "base_price": 150, "age": 25},
    {"name": "Rajat Patidar", "role": "Batsman", "batting_rating": 85, "bowling_rating": 10, "base_price": 50, "age": 30},
    {"name": "Shreyas Iyer", "role": "Batsman", "batting_rating": 87, "bowling_rating": 15, "base_price": 150, "age": 29},
    {"name": "Nehal Wadhera", "role": "Batsman", "batting_rating": 81, "bowling_rating": 10, "base_price": 20, "age": 23},
    {"name": "Ayush Badoni", "role": "Batsman", "batting_rating": 80, "bowling_rating": 20, "base_price": 20, "age": 24},
    {"name": "Vaibhav Sooryavanshi", "role": "Batsman", "batting_rating": 94, "bowling_rating": 10, "base_price": 150, "age": 15},
    {"name": "Devon Conway", "role": "Batsman", "batting_rating": 87, "bowling_rating": 10, "base_price": 100, "age": 32},
    {"name": "Aiden Markram", "role": "Batsman", "batting_rating": 84, "bowling_rating": 45, "base_price": 100, "age": 29},
    {"name": "Jake Fraser-McGurk", "role": "Batsman", "batting_rating": 88, "bowling_rating": 10, "base_price": 50, "age": 22},
    {"name": "Will Jacks", "role": "Batsman", "batting_rating": 85, "bowling_rating": 40, "base_price": 75, "age": 25},
    {"name": "Angkrish Raghuvanshi", "role": "Batsman", "batting_rating": 81, "bowling_rating": 10, "base_price": 20, "age": 19},
    {"name": "Finn Allen", "role": "Batsman", "batting_rating": 85, "bowling_rating": 10, "base_price": 75, "age": 25},
    {"name": "Dewald Brevis", "role": "Batsman", "batting_rating": 82, "bowling_rating": 20, "base_price": 30, "age": 21},
    {"name": "Priyansh Arya", "role": "Batsman", "batting_rating": 81, "bowling_rating": 10, "base_price": 20, "age": 23},
    {"name": "Sherfane Rutherford", "role": "Batsman", "batting_rating": 82, "bowling_rating": 30, "base_price": 50, "age": 25},
    {"name": "Manish Pandey", "role": "Batsman", "batting_rating": 78, "bowling_rating": 10, "base_price": 30, "age": 34},
    {"name": "Karun Nair", "role": "Batsman", "batting_rating": 77, "bowling_rating": 10, "base_price": 20, "age": 32},
    {"name": "Abhinav Manohar", "role": "Batsman", "batting_rating": 79, "bowling_rating": 10, "base_price": 20, "age": 29},
    {"name": "Atharva Taide", "role": "Batsman", "batting_rating": 78, "bowling_rating": 10, "base_price": 20, "age": 24},
    {"name": "Yash Dhull", "role": "Batsman", "batting_rating": 77, "bowling_rating": 10, "base_price": 20, "age": 21},
    {"name": "Anmolpreet Singh", "role": "Batsman", "batting_rating": 76, "bowling_rating": 10, "base_price": 20, "age": 26},
    {"name": "Sameer Rizvi", "role": "Batsman", "batting_rating": 80, "bowling_rating": 10, "base_price": 30, "age": 20},
    {"name": "Cooper Connolly", "role": "Batsman", "batting_rating": 82, "bowling_rating": 35, "base_price": 30, "age": 20},
    {"name": "Ryan Rickelton", "role": "Batsman", "batting_rating": 84, "bowling_rating": 5, "base_price": 50, "age": 27},
    {"name": "Shikhar Dhawan", "role": "Batsman", "batting_rating": 83, "bowling_rating": 10, "base_price": 100, "age": 38},
    {"name": "Mayank Agarwal", "role": "Batsman", "batting_rating": 78, "bowling_rating": 10, "base_price": 50, "age": 33},
    {"name": "Mandeep Singh", "role": "Batsman", "batting_rating": 75, "bowling_rating": 10, "base_price": 20, "age": 32},
    {"name": "Sachin Baby", "role": "Batsman", "batting_rating": 74, "bowling_rating": 15, "base_price": 20, "age": 35},
    {"name": "Himmat Singh", "role": "Batsman", "batting_rating": 74, "bowling_rating": 10, "base_price": 20, "age": 27},
    {"name": "Shashank Singh", "role": "Batsman", "batting_rating": 83, "bowling_rating": 30, "base_price": 30, "age": 32},
    {"name": "Ashutosh Sharma", "role": "Batsman", "batting_rating": 82, "bowling_rating": 10, "base_price": 30, "age": 25},
    {"name": "Swastik Chikara", "role": "Batsman", "batting_rating": 75, "bowling_rating": 10, "base_price": 20, "age": 19},
    {"name": "Rohan Kunnummal", "role": "Batsman", "batting_rating": 75, "bowling_rating": 10, "base_price": 20, "age": 25},
    {"name": "Priyam Garg", "role": "Batsman", "batting_rating": 76, "bowling_rating": 10, "base_price": 20, "age": 23},
    {"name": "Subhranshu Senapati", "role": "Batsman", "batting_rating": 74, "bowling_rating": 10, "base_price": 20, "age": 27},
    {"name": "Aniket Verma", "role": "Batsman", "batting_rating": 75, "bowling_rating": 10, "base_price": 20, "age": 22},

    # ==================== BOWLERS (61 - 120) ====================
    {"name": "Jasprit Bumrah", "role": "Bowler", "batting_rating": 25, "bowling_rating": 96, "base_price": 200, "age": 30},
    {"name": "Rashid Khan", "role": "Bowler", "batting_rating": 55, "bowling_rating": 94, "base_price": 150, "age": 25},
    {"name": "Pat Cummins", "role": "Bowler", "batting_rating": 60, "bowling_rating": 92, "base_price": 150, "age": 31},
    {"name": "Mitchell Starc", "role": "Bowler", "batting_rating": 35, "bowling_rating": 91, "base_price": 150, "age": 34},
    {"name": "Trent Boult", "role": "Bowler", "batting_rating": 20, "bowling_rating": 90, "base_price": 100, "age": 34},
    {"name": "Mohammed Shami", "role": "Bowler", "batting_rating": 20, "bowling_rating": 91, "base_price": 150, "age": 33},
    {"name": "Kuldeep Yadav", "role": "Bowler", "batting_rating": 30, "bowling_rating": 89, "base_price": 100, "age": 29},
    {"name": "Yuzvendra Chahal", "role": "Bowler", "batting_rating": 15, "bowling_rating": 87, "base_price": 75, "age": 33},
    {"name": "Matheesha Pathirana", "role": "Bowler", "batting_rating": 10, "bowling_rating": 88, "base_price": 50, "age": 21},
    {"name": "Arshdeep Singh", "role": "Bowler", "batting_rating": 20, "bowling_rating": 86, "base_price": 75, "age": 25},
    {"name": "Kagiso Rabada", "role": "Bowler", "batting_rating": 30, "bowling_rating": 89, "base_price": 100, "age": 29},
    {"name": "Mohammed Siraj", "role": "Bowler", "batting_rating": 20, "bowling_rating": 86, "base_price": 100, "age": 30},
    {"name": "Avesh Khan", "role": "Bowler", "batting_rating": 15, "bowling_rating": 83, "base_price": 50, "age": 27},
    {"name": "Ravi Bishnoi", "role": "Bowler", "batting_rating": 20, "bowling_rating": 85, "base_price": 50, "age": 23},
    {"name": "Adam Zampa", "role": "Bowler", "batting_rating": 15, "bowling_rating": 86, "base_price": 75, "age": 32},
    {"name": "T Natarajan", "role": "Bowler", "batting_rating": 10, "bowling_rating": 84, "base_price": 50, "age": 33},
    {"name": "Sandeep Sharma", "role": "Bowler", "batting_rating": 20, "bowling_rating": 83, "base_price": 40, "age": 31},
    {"name": "Deepak Chahar", "role": "Bowler", "batting_rating": 45, "bowling_rating": 82, "base_price": 75, "age": 31},
    {"name": "Shardul Thakur", "role": "Bowler", "batting_rating": 55, "bowling_rating": 81, "base_price": 75, "age": 32},
    {"name": "Harshal Patel", "role": "Bowler", "batting_rating": 35, "bowling_rating": 83, "base_price": 50, "age": 33},
    {"name": "Bhuvneshwar Kumar", "role": "Bowler", "batting_rating": 35, "bowling_rating": 82, "base_price": 50, "age": 36},
    {"name": "Mayank Yadav", "role": "Bowler", "batting_rating": 15, "bowling_rating": 84, "base_price": 20, "age": 22},
    {"name": "Varun Chakaravarthy", "role": "Bowler", "batting_rating": 10, "bowling_rating": 86, "base_price": 50, "age": 34},
    {"name": "Josh Hazlewood", "role": "Bowler", "batting_rating": 15, "bowling_rating": 89, "base_price": 200, "age": 35},
    {"name": "Anrich Nortje", "role": "Bowler", "batting_rating": 20, "bowling_rating": 85, "base_price": 75, "age": 30},
    {"name": "Lockie Ferguson", "role": "Bowler", "batting_rating": 20, "bowling_rating": 83, "base_price": 75, "age": 33},
    {"name": "Harshit Rana", "role": "Bowler", "batting_rating": 40, "bowling_rating": 83, "base_price": 20, "age": 24},
    {"name": "Khaleel Ahmed", "role": "Bowler", "batting_rating": 10, "bowling_rating": 83, "base_price": 50, "age": 26},
    {"name": "Mukesh Kumar", "role": "Bowler", "batting_rating": 15, "bowling_rating": 82, "base_price": 30, "age": 32},
    {"name": "Mustafizur Rahman", "role": "Bowler", "batting_rating": 10, "bowling_rating": 85, "base_price": 200, "age": 30},
    {"name": "Mohsin Khan", "role": "Bowler", "batting_rating": 15, "bowling_rating": 83, "base_price": 30, "age": 25},
    {"name": "Prasidh Krishna", "role": "Bowler", "batting_rating": 15, "bowling_rating": 84, "base_price": 50, "age": 28},
    {"name": "Jofra Archer", "role": "Bowler", "batting_rating": 30, "bowling_rating": 88, "base_price": 150, "age": 29},
    {"name": "Noor Ahmad", "role": "Bowler", "batting_rating": 10, "bowling_rating": 85, "base_price": 50, "age": 19},
    {"name": "Maheesh Theekshana", "role": "Bowler", "batting_rating": 15, "bowling_rating": 83, "base_price": 50, "age": 23},
    {"name": "Rahul Chahar", "role": "Bowler", "batting_rating": 20, "bowling_rating": 80, "base_price": 30, "age": 24},
    {"name": "Vaibhav Arora", "role": "Bowler", "batting_rating": 15, "bowling_rating": 81, "base_price": 20, "age": 26},
    {"name": "Yash Dayal", "role": "Bowler", "batting_rating": 10, "bowling_rating": 82, "base_price": 30, "age": 26},
    {"name": "Akash Deep", "role": "Bowler", "batting_rating": 25, "bowling_rating": 81, "base_price": 20, "age": 27},
    {"name": "Rasikh Salam", "role": "Bowler", "batting_rating": 15, "bowling_rating": 82, "base_price": 20, "age": 24},
    {"name": "Spencer Johnson", "role": "Bowler", "batting_rating": 15, "bowling_rating": 82, "base_price": 50, "age": 28},
    {"name": "Naveen-ul-Haq", "role": "Bowler", "batting_rating": 15, "bowling_rating": 82, "base_price": 50, "age": 24},
    {"name": "Umran Malik", "role": "Bowler", "batting_rating": 10, "bowling_rating": 81, "base_price": 30, "age": 24},
    {"name": "Ishant Sharma", "role": "Bowler", "batting_rating": 10, "bowling_rating": 78, "base_price": 30, "age": 35},
    {"name": "Umesh Yadav", "role": "Bowler", "batting_rating": 25, "bowling_rating": 79, "base_price": 50, "age": 36},
    {"name": "Jaydev Unadkat", "role": "Bowler", "batting_rating": 20, "bowling_rating": 78, "base_price": 30, "age": 32},
    {"name": "Dushmantha Chameera", "role": "Bowler", "batting_rating": 10, "bowling_rating": 80, "base_price": 30, "age": 32},
    {"name": "Lungi Ngidi", "role": "Bowler", "batting_rating": 10, "bowling_rating": 81, "base_price": 50, "age": 28},
    {"name": "Fazalhaq Farooqi", "role": "Bowler", "batting_rating": 10, "bowling_rating": 81, "base_price": 30, "age": 23},
    {"name": "Alzarri Joseph", "role": "Bowler", "batting_rating": 25, "bowling_rating": 80, "base_price": 50, "age": 27},
    {"name": "Reece Topley", "role": "Bowler", "batting_rating": 10, "bowling_rating": 81, "base_price": 50, "age": 30},
    {"name": "Nathan Ellis", "role": "Bowler", "batting_rating": 15, "bowling_rating": 82, "base_price": 50, "age": 29},
    {"name": "Gerald Coetzee", "role": "Bowler", "batting_rating": 30, "bowling_rating": 83, "base_price": 50, "age": 23},
    {"name": "Nuwan Thushara", "role": "Bowler", "batting_rating": 10, "bowling_rating": 82, "base_price": 30, "age": 29},
    {"name": "Karn Sharma", "role": "Bowler", "batting_rating": 20, "bowling_rating": 77, "base_price": 20, "age": 36},
    {"name": "Shreyas Gopal", "role": "Bowler", "batting_rating": 30, "bowling_rating": 76, "base_price": 20, "age": 30},
    {"name": "Piyush Chawla", "role": "Bowler", "batting_rating": 20, "bowling_rating": 78, "base_price": 30, "age": 35},
    {"name": "Manimaran Siddharth", "role": "Bowler", "batting_rating": 10, "bowling_rating": 77, "base_price": 20, "age": 25},
    {"name": "Suyash Sharma", "role": "Bowler", "batting_rating": 10, "bowling_rating": 80, "base_price": 20, "age": 21},
    {"name": "Kartik Tyagi", "role": "Bowler", "batting_rating": 10, "bowling_rating": 78, "base_price": 20, "age": 23},

    # ==================== ALL-ROUNDERS (121 - 160) ====================
    {"name": "Hardik Pandya", "role": "All-Rounder", "batting_rating": 88, "bowling_rating": 85, "base_price": 150, "age": 30},
    {"name": "Ravindra Jadeja", "role": "All-Rounder", "batting_rating": 84, "bowling_rating": 89, "base_price": 150, "age": 35},
    {"name": "Axar Patel", "role": "All-Rounder", "batting_rating": 82, "bowling_rating": 86, "base_price": 100, "age": 30},
    {"name": "Sunil Narine", "role": "All-Rounder", "batting_rating": 85, "bowling_rating": 90, "base_price": 100, "age": 36},
    {"name": "Andre Russell", "role": "All-Rounder", "batting_rating": 90, "bowling_rating": 84, "base_price": 150, "age": 36},
    {"name": "Glenn Maxwell", "role": "All-Rounder", "batting_rating": 87, "bowling_rating": 78, "base_price": 100, "age": 35},
    {"name": "Marcus Stoinis", "role": "All-Rounder", "batting_rating": 85, "bowling_rating": 76, "base_price": 75, "age": 34},
    {"name": "Liam Livingstone", "role": "All-Rounder", "batting_rating": 85, "bowling_rating": 74, "base_price": 75, "age": 30},
    {"name": "Sam Curran", "role": "All-Rounder", "batting_rating": 80, "bowling_rating": 85, "base_price": 100, "age": 26},
    {"name": "Cameron Green", "role": "All-Rounder", "batting_rating": 86, "bowling_rating": 80, "base_price": 100, "age": 25},
    {"name": "Krunal Pandya", "role": "All-Rounder", "batting_rating": 80, "bowling_rating": 82, "base_price": 50, "age": 33},
    {"name": "Abhishek Sharma", "role": "All-Rounder", "batting_rating": 87, "bowling_rating": 72, "base_price": 30, "age": 23},
    {"name": "Venkatesh Iyer", "role": "All-Rounder", "batting_rating": 83, "bowling_rating": 70, "base_price": 50, "age": 29},
    {"name": "Shivam Dube", "role": "All-Rounder", "batting_rating": 86, "bowling_rating": 68, "base_price": 50, "age": 31},
    {"name": "Washington Sundar", "role": "All-Rounder", "batting_rating": 78, "bowling_rating": 82, "base_price": 50, "age": 24},
    {"name": "Mitchell Marsh", "role": "All-Rounder", "batting_rating": 84, "bowling_rating": 75, "base_price": 75, "age": 32},
    {"name": "Nitish Kumar Reddy", "role": "All-Rounder", "batting_rating": 83, "bowling_rating": 78, "base_price": 20, "age": 21},
    {"name": "Wanindu Hasaranga", "role": "All-Rounder", "batting_rating": 75, "bowling_rating": 89, "base_price": 150, "age": 26},
    {"name": "Marco Jansen", "role": "All-Rounder", "batting_rating": 74, "bowling_rating": 86, "base_price": 75, "age": 26},
    {"name": "Rachin Ravindra", "role": "All-Rounder", "batting_rating": 86, "bowling_rating": 70, "base_price": 50, "age": 24},
    {"name": "Ravichandran Ashwin", "role": "All-Rounder", "batting_rating": 72, "bowling_rating": 85, "base_price": 100, "age": 37},
    {"name": "Moeen Ali", "role": "All-Rounder", "batting_rating": 81, "bowling_rating": 78, "base_price": 75, "age": 37},
    {"name": "Rahul Tewatia", "role": "All-Rounder", "batting_rating": 82, "bowling_rating": 72, "base_price": 40, "age": 31},
    {"name": "Shahbaz Ahmed", "role": "All-Rounder", "batting_rating": 76, "bowling_rating": 78, "base_price": 30, "age": 29},
    {"name": "Rishi Dhawan", "role": "All-Rounder", "batting_rating": 72, "bowling_rating": 75, "base_price": 20, "age": 34},
    {"name": "Harpreet Brar", "role": "All-Rounder", "batting_rating": 73, "bowling_rating": 81, "base_price": 20, "age": 28},
    {"name": "Vijay Shankar", "role": "All-Rounder", "batting_rating": 76, "bowling_rating": 70, "base_price": 30, "age": 33},
    {"name": "Krishnappa Gowtham", "role": "All-Rounder", "batting_rating": 72, "bowling_rating": 76, "base_price": 20, "age": 35},
    {"name": "Abdul Samad", "role": "All-Rounder", "batting_rating": 80, "bowling_rating": 60, "base_price": 20, "age": 22},
    {"name": "Mahipal Lomror", "role": "All-Rounder", "batting_rating": 78, "bowling_rating": 65, "base_price": 20, "age": 24},
    {"name": "Sikandar Raza", "role": "All-Rounder", "batting_rating": 81, "bowling_rating": 78, "base_price": 50, "age": 38},
    {"name": "Romario Shepherd", "role": "All-Rounder", "batting_rating": 82, "bowling_rating": 77, "base_price": 50, "age": 29},
    {"name": "Jason Holder", "role": "All-Rounder", "batting_rating": 75, "bowling_rating": 83, "base_price": 75, "age": 32},
    {"name": "Azmatullah Omarzai", "role": "All-Rounder", "batting_rating": 79, "bowling_rating": 80, "base_price": 30, "age": 24},
    {"name": "Mohammad Nabi", "role": "All-Rounder", "batting_rating": 76, "bowling_rating": 80, "base_price": 50, "age": 39},
    {"name": "Daniel Sams", "role": "All-Rounder", "batting_rating": 74, "bowling_rating": 79, "base_price": 30, "age": 31},
    {"name": "Mitchell Santner", "role": "All-Rounder", "batting_rating": 74, "bowling_rating": 84, "base_price": 50, "age": 32},
    {"name": "Kamindu Mendis", "role": "All-Rounder", "batting_rating": 80, "bowling_rating": 75, "base_price": 30, "age": 25},
    {"name": "Naman Dhir", "role": "All-Rounder", "batting_rating": 80, "bowling_rating": 68, "base_price": 20, "age": 24},
    {"name": "Ramandeep Singh", "role": "All-Rounder", "batting_rating": 81, "bowling_rating": 70, "base_price": 20, "age": 27},

    # ==================== WICKET-KEEPERS (161 - 200) ====================
    {"name": "MS Dhoni", "role": "Wicket-Keeper", "batting_rating": 88, "bowling_rating": 5, "base_price": 100, "age": 44},
    {"name": "Rishabh Pant", "role": "Wicket-Keeper", "batting_rating": 91, "bowling_rating": 5, "base_price": 200, "age": 28},
    {"name": "Sanju Samson", "role": "Wicket-Keeper", "batting_rating": 89, "bowling_rating": 5, "base_price": 100, "age": 29},
    {"name": "KL Rahul", "role": "Wicket-Keeper", "batting_rating": 89, "bowling_rating": 5, "base_price": 150, "age": 34},
    {"name": "Ishan Kishan", "role": "Wicket-Keeper", "batting_rating": 86, "bowling_rating": 5, "base_price": 100, "age": 27},
    {"name": "Nicholas Pooran", "role": "Wicket-Keeper", "batting_rating": 92, "bowling_rating": 5, "base_price": 150, "age": 30},
    {"name": "Quinton de Kock", "role": "Wicket-Keeper", "batting_rating": 86, "bowling_rating": 5, "base_price": 100, "age": 33},
    {"name": "Phil Salt", "role": "Wicket-Keeper", "batting_rating": 88, "bowling_rating": 5, "base_price": 75, "age": 29},
    {"name": "Jos Buttler", "role": "Wicket-Keeper", "batting_rating": 91, "bowling_rating": 5, "base_price": 150, "age": 35},
    {"name": "Heinrich Klaasen", "role": "Wicket-Keeper", "batting_rating": 93, "bowling_rating": 5, "base_price": 150, "age": 34},
    {"name": "Jitesh Sharma", "role": "Wicket-Keeper", "batting_rating": 81, "bowling_rating": 5, "base_price": 30, "age": 31},
    {"name": "Dhruv Jurel", "role": "Wicket-Keeper", "batting_rating": 83, "bowling_rating": 5, "base_price": 20, "age": 25},
    {"name": "Abishek Porel", "role": "Wicket-Keeper", "batting_rating": 80, "bowling_rating": 5, "base_price": 20, "age": 21},
    {"name": "Jonny Bairstow", "role": "Wicket-Keeper", "batting_rating": 87, "bowling_rating": 5, "base_price": 150, "age": 36},
    {"name": "Rahmanullah Gurbaz", "role": "Wicket-Keeper", "batting_rating": 85, "bowling_rating": 5, "base_price": 50, "age": 24},
    {"name": "Anuj Rawat", "role": "Wicket-Keeper", "batting_rating": 78, "bowling_rating": 5, "base_price": 20, "age": 26},
    {"name": "Wriddhiman Saha", "role": "Wicket-Keeper", "batting_rating": 79, "bowling_rating": 5, "base_price": 30, "age": 41},
    {"name": "Dinesh Karthik", "role": "Wicket-Keeper", "batting_rating": 82, "bowling_rating": 5, "base_price": 50, "age": 41},
    {"name": "Prabhsimran Singh", "role": "Wicket-Keeper", "batting_rating": 82, "bowling_rating": 5, "base_price": 30, "age": 23},
    {"name": "Donovan Ferreira", "role": "Wicket-Keeper", "batting_rating": 80, "bowling_rating": 25, "base_price": 20, "age": 25},
    {"name": "Josh Inglis", "role": "Wicket-Keeper", "batting_rating": 85, "bowling_rating": 5, "base_price": 75, "age": 29},
    {"name": "Alex Carey", "role": "Wicket-Keeper", "batting_rating": 80, "bowling_rating": 5, "base_price": 50, "age": 32},
    {"name": "Shai Hope", "role": "Wicket-Keeper", "batting_rating": 82, "bowling_rating": 5, "base_price": 50, "age": 30},
    {"name": "Kumar Kushagra", "role": "Wicket-Keeper", "batting_rating": 76, "bowling_rating": 5, "base_price": 20, "age": 19},
    {"name": "Robin Minz", "role": "Wicket-Keeper", "batting_rating": 76, "bowling_rating": 5, "base_price": 20, "age": 21},
    {"name": "Aryan Juyal", "role": "Wicket-Keeper", "batting_rating": 75, "bowling_rating": 5, "base_price": 20, "age": 22},
    {"name": "Luvnith Sisodia", "role": "Wicket-Keeper", "batting_rating": 74, "bowling_rating": 5, "base_price": 20, "age": 24},
    {"name": "Urvil Patel", "role": "Wicket-Keeper", "batting_rating": 76, "bowling_rating": 5, "base_price": 20, "age": 25},
    {"name": "Vishnu Vinod", "role": "Wicket-Keeper", "batting_rating": 75, "bowling_rating": 5, "base_price": 20, "age": 30},
    {"name": "Sheldon Jackson", "role": "Wicket-Keeper", "batting_rating": 74, "bowling_rating": 5, "base_price": 20, "age": 37},
    {"name": "KS Bharat", "role": "Wicket-Keeper", "batting_rating": 75, "bowling_rating": 5, "base_price": 20, "age": 30},
    {"name": "Baba Indrajith", "role": "Wicket-Keeper", "batting_rating": 73, "bowling_rating": 5, "base_price": 20, "age": 29},
    {"name": "Sam Billings", "role": "Wicket-Keeper", "batting_rating": 80, "bowling_rating": 5, "base_price": 50, "age": 33},
    {"name": "Matthew Breetzke", "role": "Wicket-Keeper", "batting_rating": 81, "bowling_rating": 5, "base_price": 30, "age": 25},
    {"name": "Josh Philippe", "role": "Wicket-Keeper", "batting_rating": 79, "bowling_rating": 5, "base_price": 30, "age": 27},
    {"name": "Tim Seifert", "role": "Wicket-Keeper", "batting_rating": 81, "bowling_rating": 5, "base_price": 50, "age": 29},
    {"name": "Tom Kohler-Cadmore", "role": "Wicket-Keeper", "batting_rating": 80, "bowling_rating": 5, "base_price": 30, "age": 29},
    {"name": "Upendra Yadav", "role": "Wicket-Keeper", "batting_rating": 73, "bowling_rating": 5, "base_price": 20, "age": 27},
    {"name": "Ricky Bhui", "role": "Wicket-Keeper", "batting_rating": 75, "bowling_rating": 5, "base_price": 20, "age": 27},
    {"name": "Harvik Desai", "role": "Wicket-Keeper", "batting_rating": 74, "bowling_rating": 5, "base_price": 20, "age": 24}
]

# --- SYSTEM INJECTIONS ---
for key in [
    "game_stage",
    "teams",
    "player_pool",
    "auction_index",
    "current_bid",
    "highest_bidder",
    "log_msg",
    "timer_seconds",
    "match_history",
    "stats_runs",
    "stats_wickets",
    "current_tab",
    "selected_headline_idx",
    "active_match_engine",
    "tournament_schedule",
]:
    if key not in st.session_state:
        if key == "current_tab":
            st.session_state[key] = "Home"
        elif key == "selected_headline_idx":
            st.session_state[key] = 0
        elif key == "active_match_engine":
            st.session_state[key] = {
                "state": "idle",
                "toss_winner": None,
                "toss_decision": None,
            }
        elif key == "tournament_schedule":
            st.session_state[key] = []
        elif key == "player_pool":
            st.session_state[key] = []
        else:
            st.session_state[key] = (
                []
                if "history" in key or "teams" in key
                else (
                    {}
                    if "stats" in key
                    else (
                        None
                        if "bidder" in key or "state" in key
                        else (
                            "setup"
                            if "stage" in key
                            else (
                                ""
                                if "msg" in key
                                else (4 if "timer" in key else 0)
                            )
                        )
                    )
                )
            )

if "match_day" not in st.session_state:
    st.session_state.match_day = 1
if "current_venue" not in st.session_state:
    st.session_state.current_venue = random.choice(VENUES)


# --- GENERATE DOUBLE ROUND-ROBIN FIXTURES ---
def generate_double_round_robin_schedule(teams):
    team_names = [t["team_name"] for t in teams]
    if len(team_names) % 2 != 0:
        team_names.append("BYE")

    n = len(team_names)
    schedule = []

    # First leg (Home)
    for round_idx in range(n - 1):
        day_matches = []
        for i in range(n // 2):
            t1, t2 = team_names[i], team_names[n - 1 - i]
            if t1 != "BYE" and t2 != "BYE":
                day_matches.append({"home": t1, "away": t2})
        schedule.append(day_matches)
        team_names.insert(1, team_names.pop())

    # Second leg (Reverse Away)
    second_leg = []
    for day in schedule:
        rev_day = [{"home": m["away"], "away": m["home"]} for m in day]
        second_leg.append(rev_day)

    return schedule + second_leg


# --- ULTRALUX DARK DESIGN & FLUID ANIMATION SYSTEM ENGINE ---
st.markdown(
    """
    <style>
    @keyframes fadeInSlide {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stApp { background-color: #0b0e14 !important; }
    .dashboard-transition-wrapper { animation: fadeInSlide 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
    [data-testid="stSidebar"] { background-color: #11141b !important; border-right: 1px solid #1c202a !important; min-width: 260px !important; }
    .top-badge-date { background-color: #16221f !important; border: 1px solid #1b4d3e !important; border-radius: 8px; padding: 8px 16px; color: #52d69b !important; font-weight: 700; font-family: 'Inter', sans-serif; }
    .sim-match-btn button { background: #1f242e !important; color: #ffffff !important; border: 1px solid #2d3748 !important; font-weight: 700 !important; border-radius: 8px !important; padding: 10px 20px !important; width: 100%; }
    .play-match-btn button { background: #10b981 !important; color: #000000 !important; border: none !important; font-weight: 800 !important; border-radius: 8px !important; padding: 10px 24px !important; width: 100%; }
    .dashboard-panel-card { background-color: #11141b; border: 1px solid #1c202a; border-radius: 12px; padding: 20px; min-height: 140px; }
    .panel-header-text { color: #8892b0 !important; font-size: 13px !important; font-weight: 600; text-transform: uppercase; margin-bottom: 12px; }
    .logo-square-icon { width: 50px; height: 50px; background: linear-gradient(135deg, #ea580c, #f97316); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 18px; color: #ffffff; }
    .opponent-badge-icon { width: 44px; height: 44px; background: #ea580c; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 15px; color: #ffffff; }
    .headline-stream-card { padding: 14px; border-radius: 8px; background-color: #11141b; border: 1px solid #1c202a; margin-bottom: 8px; }
    .headline-stream-card.active { border-color: #10b981 !important; background-color: #121e1a !important; }
    .stat-hero-ovr { font-size: 36px; font-weight: 800; color: #ffffff; }
    .stat-hero-delta-red { color: #f87171 !important; font-weight: 700; font-size: 16px; }
    .stat-hero-delta-green { color: #34d399 !important; font-weight: 700; font-size: 16px; }
    </style>
""",
    unsafe_allow_html=True,
)


def get_form_offset(form_string):
    mapping = {"Slumping": -4, "Steady": 0, "Good": 2, "Red-Hot": 5}
    return mapping.get(form_string, 0)


# --- SIMULATOR MATRIX USING BAT / BOWL DUAL RATINGS ---
def generate_detailed_scorecard(batting_team, bowling_team):
    batters = (
        batting_team["playing_11"]
        if len(batting_team["playing_11"]) == 11
        else batting_team["squad"][:11]
    )

    # Strictly pick Bowlers/All-Rounders for bowling (bowling_rating > 40)
    all_players = (
        bowling_team["playing_11"]
        if len(bowling_team["playing_11"]) == 11
        else bowling_team["squad"][:11]
    )
    bowlers = [p for p in all_players if p["bowling_rating"] > 40]
    if len(bowlers) < 5:
        bowlers = sorted(
            all_players, key=lambda x: x["bowling_rating"], reverse=True
        )[:5]
    else:
        bowlers = bowlers[:5]

    batting_performance = []
    total_runs = 0
    total_wickets = 0
    balls_tracked = 0

    for idx, b in enumerate(batters):
        if total_wickets >= 10 or balls_tracked >= 120:
            batting_performance.append({
                "name": b["name"],
                "status": "DNB",
                "runs": 0,
                "balls": 0,
                "fours": 0,
                "sixes": 0,
                "sr": 0.0,
            })
            continue

        ability = b["batting_rating"] + get_form_offset(b.get("form", "Steady"))
        balls_faced = (
            random.randint(3, 25) if ability < 50 else random.randint(10, 35)
        )
        if idx < 4 and ability >= 75:
            balls_faced = random.randint(18, 45)

        runs_scored = 0
        fours = 0
        sixes = 0
        got_out = False
        for _ in range(balls_faced):
            ball_roll = random.random()
            if ball_roll < (0.05 + (100 - ability) * 0.0015):
                got_out = True
                break  # Wicket
            elif ball_roll < 0.45:
                runs_scored += 1
            elif ball_roll < 0.60:
                runs_scored += 2
            elif ball_roll < 0.75:
                runs_scored += 4
                fours += 1
            elif ball_roll < 0.85:
                runs_scored += 6
                sixes += 1

        total_runs += runs_scored
        balls_tracked += balls_faced
        sr = round((runs_scored / max(1, balls_faced)) * 100, 1)

        st.session_state.stats_runs[b["name"]] = (
            st.session_state.stats_runs.get(b["name"], 0) + runs_scored
        )
        batting_performance.append({
            "name": b["name"],
            "status": "Out" if got_out else "Not Out",
            "runs": runs_scored,
            "balls": balls_faced,
            "fours": fours,
            "sixes": sixes,
            "sr": sr,
        })
        if batting_performance[-1]["status"] == "Out":
            total_wickets += 1

    total_runs += random.randint(4, 15)

    bowling_performance = []
    wickets_remaining = total_wickets
    for idx, bwl in enumerate(bowlers):
        overs = 4
        runs_conceded = random.randint(18, 45) - int(
            (bwl["bowling_rating"] - 75) * 0.35
        )
        runs_conceded = max(12, runs_conceded)
        wkt = 0
        if wickets_remaining > 0:
            wkt = random.randint(0, min(3, wickets_remaining))
            wickets_remaining -= wkt

        st.session_state.stats_wickets[bwl["name"]] = (
            st.session_state.stats_wickets.get(bwl["name"], 0) + wkt
        )
        bowling_performance.append({
            "name": bwl["name"],
            "overs": overs,
            "runs": runs_conceded,
            "wickets": wkt,
            "econ": round(runs_conceded / overs, 2),
        })

    return {
        "runs": total_runs,
        "wickets": min(10, total_wickets),
        "overs": round(min(120, balls_tracked) / 6, 1),
        "batting": batting_performance,
        "bowling": bowling_performance,
    }


# Helper to simulate rest of league matches on current match day
def simulate_league_background_matches(user_team_name, opp_team_name):
    if st.session_state.match_day > len(st.session_state.tournament_schedule):
        return

    # Guard against re-simulating the same matchday's background fixtures twice
    if st.session_state.get("bg_simulated_day") == st.session_state.match_day:
        return

    day_idx = st.session_state.match_day - 1
    fixtures = st.session_state.tournament_schedule[day_idx]
    team_dict = {t["team_name"]: t for t in st.session_state.teams}

    for fix in fixtures:
        t1_name, t2_name = fix["home"], fix["away"]
        # Skip user active match as it is simulated explicitly
        if (t1_name == user_team_name and t2_name == opp_team_name) or (
            t2_name == user_team_name and t1_name == opp_team_name
        ):
            continue

        t1, t2 = team_dict[t1_name], team_dict[t2_name]
        sc1 = generate_detailed_scorecard(t1, t2)
        sc2 = generate_detailed_scorecard(t2, t1)

        if sc1["runs"] > sc2["runs"]:
            t1["points"] += 2
            t1["wins"] += 1
            t2["losses"] += 1
        else:
            t2["points"] += 2
            t2["wins"] += 1
            t1["losses"] += 1

    st.session_state.bg_simulated_day = st.session_state.match_day


# --- STAGE 1: SETUP ---
if st.session_state.game_stage == "setup":
    st.header("🎮 IPL Double Round-Robin Manager Console")
    num_humans = st.slider(
        "How many human players?", min_value=1, max_value=4, value=1
    )
    human_configs = []
    used_teams = []
    for i in range(num_humans):
        st.subheader(f"Player {i+1} Configuration")
        h_name = st.text_input(
            f"Manager Name", value=f"Manager {i+1}", key=f"h_name_{i}"
        )
        available_choices = [t for t in TEAM_NAMES_POOL if t not in used_teams]
        selected_team = st.selectbox(
            f"Choose Franchise", options=available_choices, key=f"h_team_{i}"
        )
        used_teams.append(selected_team)
        human_configs.append({"manager": h_name, "team": selected_team})

    if st.button("Initialize Tournament League", type="primary"):
        teams = []
        for hc in human_configs:
            teams.append({
                "team_name": hc["team"],
                "manager": hc["manager"],
                "is_human": True,
                "purse": 15000,
                "squad": [],
                "points": 0,
                "wins": 0,
                "losses": 0,
                "playing_11": [],
                "impact_player": None,
                "tactic": "Balanced Alignment",
                "morale": 80,
                "nrr": 0.00,
            })
        for bot_team in [t for t in TEAM_NAMES_POOL if t not in used_teams]:
            teams.append({
                "team_name": bot_team,
                "manager": "AI Bot Executive",
                "is_human": False,
                "purse": 15000,
                "squad": [],
                "personality": random.choice(BOT_PERSONALITIES),
                "points": 0,
                "wins": 0,
                "losses": 0,
                "playing_11": [],
                "impact_player": None,
                "tactic": "Balanced Alignment",
                "morale": 75,
                "nrr": 0.00,
            })

        st.session_state.teams = teams
        st.session_state.tournament_schedule = (
            generate_double_round_robin_schedule(teams)
        )
        st.session_state.player_pool = MASTER_200_REAL_PLAYERS.copy()
        random.shuffle(st.session_state.player_pool)
        st.session_state.game_stage = "auction"
        st.session_state.auction_index = 0
        st.session_state.timer_seconds = 4

        st.session_state.match_history.append({
            "type": "WELCOME",
            "date": "Mar 22, 2026",
            "headline": "Double Round-Robin Schedule Standard Initialized",
            "body": (
                "18 Match Days compiled! Every franchise faces each other twice"
                " (Home & Away)."
            ),
            "detailed": False,
        })
        st.rerun()

# --- STAGE 2: LIVE AUCTION ROOM ---
elif st.session_state.game_stage == "auction":
    # GUARANTEE PLAYER POOL INITIALIZATION (prevents AttributeError)
    if "player_pool" not in st.session_state or not st.session_state.player_pool:
        st.session_state.player_pool = MASTER_200_REAL_PLAYERS.copy()
        random.shuffle(st.session_state.player_pool)

    player_pool = st.session_state.player_pool
    idx = st.session_state.auction_index

    if idx >= len(player_pool):
        st.success("Draft Concluded! Setting up league grids...")
        for t in st.session_state.teams:
            sorted_squad = sorted(
                t["squad"],
                key=lambda x: max(x["batting_rating"], x["bowling_rating"]),
                reverse=True,
            )
            t["playing_11"] = (
                sorted_squad[:11] if len(sorted_squad) >= 11 else sorted_squad
            )
            t["impact_player"] = (
                sorted_squad[11] if len(sorted_squad) > 11 else None
            )
        st.session_state.game_stage = "dashboard"
        st.rerun()
    else:
        player = player_pool[idx]
        if st.session_state.current_bid == 0:
            st.session_state.current_bid = player["base_price"]
            st.session_state.highest_bidder = None
            st.session_state.timer_seconds = 4

        st_autorefresh(interval=1000, key="auction_timer")
        st.markdown(
            f"<h3>🔨 LIVE AUCTION CARD ({idx+1}/{len(player_pool)})</h3>",
            unsafe_allow_html=True,
        )

        if st.button(
            "⚡ Fast-Track Rest of Auction",
            type="secondary",
            use_container_width=True,
        ):
            while st.session_state.auction_index < len(
                st.session_state.player_pool
            ):
                curr_idx = st.session_state.auction_index
                curr_p = st.session_state.player_pool[curr_idx]
                # Shuffle team order per player so no single team (e.g. the
                # first human team) always wins every contested pick.
                shuffled_teams = st.session_state.teams[:]
                random.shuffle(shuffled_teams)
                for t in shuffled_teams:
                    if len(t["squad"]) < 20 and t["purse"] >= curr_p["base_price"]:
                        t["purse"] -= curr_p["base_price"]
                        t["squad"].append(curr_p)
                        break
                st.session_state.auction_index += 1
            st.rerun()

        if st.session_state.timer_seconds > 0:
            st.session_state.timer_seconds -= 1
            bots = [
                t
                for t in st.session_state.teams
                if not t["is_human"]
                and len(t["squad"]) < 20
                and t["purse"] >= (st.session_state.current_bid + 50)
            ]
            if bots and random.random() < 0.45:
                valid_bots = [
                    b
                    for b in bots
                    if not st.session_state.highest_bidder
                    or b["team_name"]
                    != st.session_state.highest_bidder["team_name"]
                ]
                if valid_bots:
                    counter_bot = random.choice(valid_bots)
                    st.session_state.current_bid += 50
                    st.session_state.highest_bidder = counter_bot
                    st.session_state.timer_seconds = 4
                    st.rerun()
        else:
            if st.session_state.highest_bidder:
                st.session_state.highest_bidder["purse"] -= (
                    st.session_state.current_bid
                )
                st.session_state.highest_bidder["squad"].append(player)
            else:
                cb = [
                    t
                    for t in st.session_state.teams
                    if len(t["squad"]) < 20 and t["purse"] >= player["base_price"]
                ]
                if cb:
                    assigned = random.choice(cb)
                    assigned["purse"] -= player["base_price"]
                    assigned["squad"].append(player)
            st.session_state.auction_index += 1
            st.session_state.current_bid = 0
            st.session_state.highest_bidder = None
            st.session_state.timer_seconds = 4
            st.rerun()

        st.progress(st.session_state.timer_seconds / 4)
        st.markdown(
            f"**🏃 Active Asset:** {player['name']} | **🏏 Batting:**"
            f" {player['batting_rating']} | **🎯 Bowling:**"
            f" {player['bowling_rating']} | **📅 Age:** {player['age']}"
        )

        high_bidder_label = (
            st.session_state.highest_bidder["team_name"]
            if st.session_state.highest_bidder is not None
            else "No Bids"
        )
        st.metric(
            label="Current High Bid Status",
            value=f"₹{st.session_state.current_bid/100:.2f} CR",
            delta=f"Leader: {high_bidder_label}",
        )

        human_teams = [t for t in st.session_state.teams if t["is_human"]]
        eligible_humans = [
            t
            for t in human_teams
            if len(t["squad"]) < 20
            and t["purse"] >= (st.session_state.current_bid + 50)
        ]

        if eligible_humans:
            human_options = {
                f"{t['manager']} ({t['team_name']} - Purse: ₹{t['purse']/100:.2f}"
                " CR)": t
                for t in eligible_humans
            }
            selected_human_label = st.radio(
                "⚡ Select Active Human Bidding Manager:",
                options=list(human_options.keys()),
                key="active_human_bidder_selector",
            )
            active_bidding_team = human_options[selected_human_label]

            if st.button(
                f"⚡ Raise Bid for {active_bidding_team['manager']} (+₹50 L)",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.current_bid += 50
                st.session_state.highest_bidder = active_bidding_team
                st.session_state.timer_seconds = 4
                st.rerun()

# --- STAGE 3: INTERACTIVE OPERATIONS HUB ---
elif st.session_state.game_stage == "dashboard":
    human_squads = [t for t in st.session_state.teams if t["is_human"]]
    if "selected_human_idx" not in st.session_state:
        st.session_state.selected_human_idx = 0
    user_team = (
        human_squads[st.session_state.selected_human_idx]
        if human_squads
        else None
    )

    # Retrieve next opponent based on tournament schedule
    day_idx = min(
        st.session_state.match_day - 1,
        len(st.session_state.tournament_schedule) - 1,
    )
    day_fixtures = st.session_state.tournament_schedule[day_idx]

    opp_team_name = None
    for fix in day_fixtures:
        if fix["home"] == user_team["team_name"]:
            opp_team_name = fix["away"]
        elif fix["away"] == user_team["team_name"]:
            opp_team_name = fix["home"]

    if not opp_team_name:
        opp_team_name = [
            t["team_name"]
            for t in st.session_state.teams
            if t["team_name"] != user_team["team_name"]
        ][0]
    opponent_team = [
        t for t in st.session_state.teams if t["team_name"] == opp_team_name
    ][0]

    with st.sidebar:
        st.markdown("<br/>", unsafe_allow_html=True)

        if len(human_squads) > 1:
            manager_labels = [
                f"{t.get('manager', 'Manager')} ({t['team_name']})"
                for t in human_squads
            ]
            picked_label = st.selectbox(
                "🎮 Viewing dashboard as:",
                options=manager_labels,
                index=st.session_state.selected_human_idx,
                key="human_manager_switcher",
            )
            new_idx = manager_labels.index(picked_label)
            if new_idx != st.session_state.selected_human_idx:
                st.session_state.selected_human_idx = new_idx
                st.session_state.current_tab = "Home"
                st.session_state.active_match_engine = {
                    "state": "idle",
                    "toss_winner": None,
                    "toss_decision": None,
                }
                st.rerun()

        if user_team:
            st.markdown(f"### 🛡️ {user_team['team_name']}")
            st.caption(f"Manager: {user_team.get('manager', 'Franchise Owner')}")

        for tab in ["Home", "Squad", "Schedule", "Table", "Stats"]:
            if st.sidebar.button(tab, key=f"nav_btn_{tab}", use_container_width=True):
                st.session_state.current_tab = tab
                st.session_state.active_match_engine = {
                    "state": "idle",
                    "toss_winner": None,
                    "toss_decision": None,
                }
                st.rerun()

    top_col_left, top_col_mid, top_col_right = st.columns([3, 1, 1])
    with top_col_left:
        st.markdown(
            f"📅 **Matchday {st.session_state.match_day} /"
            f" {len(st.session_state.tournament_schedule)}** | Double Round-Robin"
            " League"
        )
    with top_col_mid:
        if st.button("⏩ Sim Match", key="global_sim_match_action"):
            simulate_league_background_matches(
                user_team["team_name"], opponent_team["team_name"]
            )
            sc1 = generate_detailed_scorecard(user_team, opponent_team)
            sc2 = generate_detailed_scorecard(opponent_team, user_team)

            if sc1["runs"] > sc2["runs"]:
                user_team["points"] += 2
                user_team["wins"] += 1
                opponent_team["losses"] += 1
                hl = (
                    f"{user_team['team_name']} win Matchday"
                    f" {st.session_state.match_day}"
                )
            else:
                opponent_team["points"] += 2
                opponent_team["wins"] += 1
                user_team["losses"] += 1
                hl = (
                    f"{opponent_team['team_name']} win Matchday"
                    f" {st.session_state.match_day}"
                )

            st.session_state.match_history.append({
                "type": "MATCH REPORT",
                "date": f"Matchday {st.session_state.match_day}",
                "headline": hl,
                "body": "Simulated instantly across all league grounds.",
                "scorecard": {
                    "sc1": sc1,
                    "sc2": sc2,
                    "t1": user_team["team_name"],
                    "t2": opponent_team["team_name"],
                },
            })
            st.session_state.match_day += 1
            st.rerun()
    with top_col_right:
        if st.button("▷ Play Match", key="global_play_match_action"):
            st.session_state.current_tab = "Match Engine"
            st.session_state.active_match_engine = {
                "state": "toss_phase",
                "toss_winner": None,
                "toss_decision": None,
            }
            st.rerun()

    st.markdown(
        "<div class='dashboard-transition-wrapper'>", unsafe_allow_html=True
    )

    if st.session_state.current_tab == "Match Engine":
        st.header(
            f"🏏 Matchday {st.session_state.match_day}: {user_team['team_name']}"
            f" vs {opponent_team['team_name']}"
        )
        engine = st.session_state.active_match_engine

        if engine["state"] == "toss_phase":
            call_selection = st.radio("Call the coin flip:", ["Heads", "Tails"])
            if st.button("🪙 Flip Coin", use_container_width=True):
                if call_selection == random.choice(["Heads", "Tails"]):
                    engine["toss_winner"] = user_team["team_name"]
                    engine["state"] = "toss_decision_human"
                else:
                    engine["toss_winner"] = opponent_team["team_name"]
                    engine["toss_decision"] = random.choice(
                        ["Bat First", "Bowl First"]
                    )
                    engine["state"] = "toss_complete"
                st.rerun()

        elif engine["state"] == "toss_decision_human":
            decision = st.radio(
                "Select tactical decision:", ["Bat First", "Bowl First"]
            )
            if st.button("Confirm Choice", use_container_width=True):
                engine["toss_decision"] = decision
                engine["state"] = "toss_complete"
                st.rerun()

        elif engine["state"] == "toss_complete":
            st.info(
                f"🪙 Toss Winner: **{engine['toss_winner']}** | Decision:"
                f" **{engine['toss_decision']}**"
            )
            if st.button(
                "⚡ Execute Live Match", type="primary", use_container_width=True
            ):
                simulate_league_background_matches(
                    user_team["team_name"], opponent_team["team_name"]
                )
                if (
                    engine["toss_decision"] == "Bat First"
                    and engine["toss_winner"] == user_team["team_name"]
                ):
                    sc1 = generate_detailed_scorecard(user_team, opponent_team)
                    sc2 = generate_detailed_scorecard(opponent_team, user_team)
                else:
                    sc1 = generate_detailed_scorecard(opponent_team, user_team)
                    sc2 = generate_detailed_scorecard(user_team, opponent_team)

                engine["sc1"], engine["sc2"], engine["state"] = (
                    sc1,
                    sc2,
                    "match_finished",
                )
                st.rerun()

        elif engine["state"] == "match_finished":
            sc1, sc2 = engine["sc1"], engine["sc2"]
            st.success("🏁 Match Concluded!")

            if st.button("💾 Finalize Results", use_container_width=True):
                if sc1["runs"] > sc2["runs"]:
                    user_team["points"] += 2
                    user_team["wins"] += 1
                    opponent_team["losses"] += 1
                    hl = f"{user_team['team_name']} win spectacular clash"
                else:
                    opponent_team["points"] += 2
                    opponent_team["wins"] += 1
                    user_team["losses"] += 1
                    hl = (
                        f"{opponent_team['team_name']} defeat"
                        f" {user_team['team_name']}"
                    )

                st.session_state.match_history.append({
                    "type": "MATCH REPORT",
                    "date": f"Matchday {st.session_state.match_day}",
                    "headline": hl,
                    "body": "Detailed ball-by-ball matrix completed.",
                    "scorecard": {
                        "sc1": sc1,
                        "sc2": sc2,
                        "t1": user_team["team_name"],
                        "t2": opponent_team["team_name"],
                    },
                })
                st.session_state.match_day += 1
                st.session_state.current_tab = "Home"
                st.rerun()

            st.markdown("### 📊 Interactive Scorecard")
            t1, t2 = st.tabs(["Innings 1 Overview", "Innings 2 Overview"])
            with t1:
                st.metric(
                    label="Innings 1",
                    value=f"{sc1['runs']}/{sc1['wickets']}",
                    delta=f"{sc1['overs']} Overs",
                )
                st.dataframe(pd.DataFrame(sc1["batting"]), use_container_width=True)
                st.dataframe(pd.DataFrame(sc1["bowling"]), use_container_width=True)
            with t2:
                st.metric(
                    label="Innings 2",
                    value=f"{sc2['runs']}/{sc2['wickets']}",
                    delta=f"{sc2['overs']} Overs",
                )
                st.dataframe(pd.DataFrame(sc2["batting"]), use_container_width=True)
                st.dataframe(pd.DataFrame(sc2["bowling"]), use_container_width=True)

    elif st.session_state.current_tab == "Home":
        met_col1, met_col2, met_col3 = st.columns(3)
        with met_col1:
            st.markdown(f"### 🔮 Next Match\n**vs {opponent_team['team_name']}**")
        with met_col2:
            sorted_teams = sorted(
                st.session_state.teams, key=lambda x: x["points"], reverse=True
            )
            my_pos = (
                sorted_teams.index(user_team) + 1
                if user_team in sorted_teams
                else 1
            )
            st.markdown(f"### 🏆 Position\n**#{my_pos}** ({user_team['points']} pts)")
        with met_col3:
            st.markdown(
                f"### 📈 Record\n**{user_team['wins']}W - {user_team['losses']}L**"
            )

    elif st.session_state.current_tab == "Squad":
        st.subheader(f"👥 Squad Management: {user_team['team_name']}")
        for p in user_team["squad"]:
            st.write(
                f"**{p['name']}** ({p['role']}) | 🏏 Bat Rating:"
                f" {p['batting_rating']} | 🎯 Bowl Rating: {p['bowling_rating']}"
            )

    elif st.session_state.current_tab == "Schedule":
        st.subheader("🗓️ Complete Double Round-Robin Fixtures (18 Match Days)")
        for day_num, day_fixes in enumerate(
            st.session_state.tournament_schedule, start=1
        ):
            with st.expander(
                f"Matchday {day_num}"
                f" {'(CURRENT)' if day_num == st.session_state.match_day else ''}"
            ):
                st.table(pd.DataFrame(day_fixes))

    elif st.session_state.current_tab == "Table":
        st.subheader("📊 Dynamic League Standings")
        standings = sorted(
            [
                {
                    "Team": t["team_name"],
                    "Played": t["wins"] + t["losses"],
                    "Wins": t["wins"],
                    "Losses": t["losses"],
                    "Points": t["points"],
                }
                for t in st.session_state.teams
            ],
            key=lambda x: x["Points"],
            reverse=True,
        )
        st.table(pd.DataFrame(standings))

    elif st.session_state.current_tab == "Stats":
        st.subheader("👑 Global League Leader Standings")
        col_o, col_p = st.columns(2)
        with col_o:
            st.markdown("### 🟠 Orange Cap (Top Batsmen)")
            for idx, (name, runs) in enumerate(
                sorted(
                    st.session_state.stats_runs.items(),
                    key=lambda x: x[1],
                    reverse=True,
                )[:10]
            ):
                st.write(f"**{idx+1}. {name}** — {runs} runs")
        with col_p:
            st.markdown("### 🟣 Purple Cap (Top Bowlers)")
            for idx, (name, wck) in enumerate(
                sorted(
                    st.session_state.stats_wickets.items(),
                    key=lambda x: x[1],
                    reverse=True,
                )[:10]
            ):
                st.write(f"**{idx+1}. {name}** — {wck} wickets")

    st.markdown("</div>", unsafe_allow_html=True)
