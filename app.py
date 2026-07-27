import random
import json
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
if "playoffs" not in st.session_state:
    st.session_state.playoffs = {"stage": None, "seeds": [], "log": [], "champion": None}
if "unsold_pool" not in st.session_state:
    st.session_state.unsold_pool = []
if "bg_simulated_day" not in st.session_state:
    st.session_state.bg_simulated_day = None
if "selected_human_idx" not in st.session_state:
    st.session_state.selected_human_idx = 0


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


# --- BROADCAST-GRADE VISUAL SYSTEM ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap');

    :root {
        --bg: #070b12;
        --surface: #10151f;
        --surface-2: #161d2b;
        --border: #232c3d;
        --text: #eef2f8;
        --text-dim: #8a97ab;
        --pitch: #22c55e;
        --pitch-glow: rgba(34, 197, 94, 0.35);
        --gold: #f2b705;
        --gold-glow: rgba(242, 183, 5, 0.35);
        --danger: #ef4444;
        --info: #38bdf8;
    }

    @keyframes fadeInSlide {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 0px var(--gold-glow); }
        50% { box-shadow: 0 0 18px var(--gold-glow); }
    }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background:
            radial-gradient(circle at 12% -10%, rgba(34,197,94,0.10), transparent 40%),
            radial-gradient(circle at 88% 0%, rgba(242,183,5,0.08), transparent 35%),
            var(--bg) !important;
        color: var(--text);
    }

    .dashboard-transition-wrapper { animation: fadeInSlide 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards; }

    /* Headings — condensed scoreboard type */
    h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'Oswald', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        color: var(--text) !important;
    }
    h1 { border-left: 4px solid var(--pitch); padding-left: 12px; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--surface) !important;
        border-right: 1px solid var(--border) !important;
        min-width: 260px !important;
    }
    [data-testid="stSidebar"] h3 {
        color: var(--gold) !important;
    }

    /* Buttons */
    .stButton button, .stDownloadButton button {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        font-size: 13px !important;
        border-radius: 8px !important;
        border: 1px solid var(--border) !important;
        background: var(--surface-2) !important;
        color: var(--text) !important;
        padding: 10px 18px !important;
        transition: all 0.15s ease-in-out;
    }
    .stButton button:hover {
        border-color: var(--pitch) !important;
        color: var(--pitch) !important;
        transform: translateY(-1px);
    }
    button[kind="primary"], .stButton button[kind="primary"] {
        background: linear-gradient(135deg, var(--pitch), #16a34a) !important;
        color: #06210f !important;
        border: none !important;
        animation: pulseGlow 2.4s infinite;
    }
    button[kind="primary"]:hover {
        filter: brightness(1.08);
        color: #06210f !important;
    }

    /* Metrics (used for bid status + scorecards) */
    [data-testid="stMetric"] {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 14px 18px;
    }
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        color: var(--gold) !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricDelta"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Progress bar = auction countdown */
    [data-testid="stProgress"] > div > div {
        background: linear-gradient(90deg, var(--danger), var(--gold), var(--pitch)) !important;
    }

    /* Tables / dataframes */
    [data-testid="stDataFrame"], [data-testid="stTable"] {
        border: 1px solid var(--border);
        border-radius: 10px;
        overflow: hidden;
    }

    /* Expanders (Schedule tab) */
    [data-testid="stExpander"] {
        background: var(--surface);
        border: 1px solid var(--border) !important;
        border-radius: 10px;
    }

    /* Tabs (Match Engine innings) */
    [data-baseweb="tab-list"] {
        gap: 6px;
        border-bottom: 1px solid var(--border) !important;
    }
    [data-baseweb="tab"] {
        font-family: 'Oswald', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        color: var(--text-dim) !important;
    }
    [aria-selected="true"][data-baseweb="tab"] {
        color: var(--pitch) !important;
    }

    /* Multiselect / selectbox chips (Playing XI picker) */
    [data-baseweb="tag"] {
        background: var(--pitch) !important;
        color: #06210f !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
    }

    /* ---- Custom components ---- */
    .scoreboard-strip {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: linear-gradient(90deg, var(--surface), var(--surface-2));
        border: 1px solid var(--border);
        border-left: 4px solid var(--gold);
        border-radius: 10px;
        padding: 12px 20px;
        margin-bottom: 18px;
    }
    .scoreboard-strip .sb-label {
        font-family: 'Oswald', sans-serif;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--text-dim);
        font-size: 12px;
    }
    .scoreboard-strip .sb-value {
        font-family: 'JetBrains Mono', monospace;
        color: var(--gold);
        font-size: 20px;
        font-weight: 700;
    }

    .team-crest {
        width: 52px; height: 52px;
        background: linear-gradient(135deg, var(--pitch), #0f7a3d);
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        font-family: 'Oswald', sans-serif;
        font-weight: 700; font-size: 18px; color: #06210f;
        box-shadow: 0 0 14px var(--pitch-glow);
    }

    .stat-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 18px 20px;
        min-height: 110px;
    }
    .stat-card .stat-label {
        font-family: 'Oswald', sans-serif;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-dim);
        font-size: 12px;
        margin-bottom: 6px;
    }
    .stat-card .stat-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 26px;
        font-weight: 700;
        color: var(--text);
    }
    .stat-card .stat-value.gold { color: var(--gold); }
    .stat-card .stat-value.pitch { color: var(--pitch); }

    .pill {
        display: inline-block;
        font-family: 'Inter', sans-serif;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        padding: 2px 9px;
        border-radius: 999px;
        margin-left: 8px;
    }
    .pill-xi { background: var(--pitch-glow); color: var(--pitch); border: 1px solid var(--pitch); }
    .pill-impact { background: var(--gold-glow); color: var(--gold); border: 1px solid var(--gold); }

    .player-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 6px;
    }
    .player-row .p-name { font-weight: 600; color: var(--text); }
    .player-row .p-role { color: var(--text-dim); font-size: 12px; margin-left: 6px; }
    .player-row .p-ratings {
        font-family: 'JetBrains Mono', monospace;
        color: var(--text-dim);
        font-size: 13px;
    }

    .auction-card {
        background: linear-gradient(160deg, var(--surface), var(--surface-2));
        border: 1px solid var(--border);
        border-top: 3px solid var(--gold);
        border-radius: 12px;
        padding: 20px 22px;
        margin-bottom: 14px;
    }
    .auction-card .a-name {
        font-family: 'Oswald', sans-serif;
        font-size: 24px;
        text-transform: uppercase;
        color: var(--text);
    }
    .auction-card .a-meta {
        font-family: 'JetBrains Mono', monospace;
        color: var(--text-dim);
        font-size: 14px;
        margin-top: 4px;
    }

    .headline-card {
        padding: 12px 14px;
        border-radius: 8px;
        background-color: var(--surface);
        border: 1px solid var(--border);
        border-left: 3px solid var(--info);
        margin-bottom: 8px;
    }
    .headline-card .h-date {
        font-family: 'JetBrains Mono', monospace;
        color: var(--text-dim);
        font-size: 11px;
        text-transform: uppercase;
    }
    .headline-card .h-title {
        font-weight: 600;
        color: var(--text);
        margin-top: 2px;
    }
    </style>
""",
    unsafe_allow_html=True,
)


def get_form_offset(form_string):
    mapping = {"Slumping": -4, "Steady": 0, "Good": 2, "Red-Hot": 5}
    return mapping.get(form_string, 0)


# ==================== BOT INTELLIGENCE LAYER ====================
# Rough squad composition every AI franchise tries to build toward across
# its 20 roster slots. Used to steer auction bidding and, later, XI picks.
ROLE_TARGETS = {"Batsman": 6, "Bowler": 6, "All-Rounder": 5, "Wicket-Keeper": 3}


def get_squad_role_counts(team):
    counts = {"Batsman": 0, "Bowler": 0, "All-Rounder": 0, "Wicket-Keeper": 0}
    for p in team["squad"]:
        counts[p["role"]] = counts.get(p["role"], 0) + 1
    return counts


def calculate_bot_valuation(team, player):
    """How much (in the same units as base_price / current_bid) this team is
    willing to pay for a player, blending player quality, the team's draft
    personality, its current squad needs, and how much purse it has left to
    spread across its remaining roster slots."""
    personality = team.get("personality", "Balanced")
    overall = max(player["batting_rating"], player["bowling_rating"])
    quality_component = player["base_price"] * (0.6 + (overall / 100) * 1.4)

    personality_mult = 1.0
    if personality == "Batting-Heavy":
        if player["role"] in ("Batsman", "Wicket-Keeper"):
            personality_mult = 1.35
        elif player["role"] == "Bowler":
            personality_mult = 0.7
    elif personality == "Bowling-Heavy":
        if player["role"] == "Bowler":
            personality_mult = 1.35
        elif player["role"] in ("Batsman", "Wicket-Keeper"):
            personality_mult = 0.7
    elif personality == "Youth-Focus":
        if player["age"] <= 23:
            personality_mult = 1.4
        elif player["age"] >= 33:
            personality_mult = 0.6

    counts = get_squad_role_counts(team)
    target = ROLE_TARGETS.get(player["role"], 4)
    have = counts.get(player["role"], 0)
    if have < target:
        need_mult = 1.3
    elif have >= target + 2:
        need_mult = 0.7
    else:
        need_mult = 1.0

    # Pace spending so the team doesn't blow its whole purse on early players
    # and leave nothing for the rest of a 20-man squad.
    slots_left = max(1, 20 - len(team["squad"]))
    purse_pace_cap = (team["purse"] / slots_left) * 1.8

    max_bid = quality_component * personality_mult * need_mult
    max_bid = min(max_bid, purse_pace_cap, team["purse"])
    return max(player["base_price"], round(max_bid / 10) * 10)


def select_bot_playing_xi(team, venue=None):
    """Let an AI team pick its strongest available XI for the given venue,
    weighing player quality, current form, the venue's role boost, and the
    team's draft personality — then set the bench Impact Player."""
    if venue is None:
        venue = st.session_state.get("current_venue")
    boost_role = venue.get("boost_role") if venue else None
    boost_amount = venue.get("boost_amount", 0) if venue else 0
    personality = team.get("personality", "Balanced")

    def player_score(p):
        score = (
            max(p["batting_rating"], p["bowling_rating"])
            + p["batting_rating"] * 0.3
            + p["bowling_rating"] * 0.3
        )
        score += get_form_offset(p.get("form", "Steady")) * 2
        if boost_role == p["role"]:
            score += boost_amount * 1.5
        if personality == "Batting-Heavy" and p["role"] in ("Batsman", "Wicket-Keeper"):
            score += 4
        elif personality == "Bowling-Heavy" and p["role"] == "Bowler":
            score += 4
        elif personality == "Youth-Focus" and p["age"] <= 25:
            score += 4
        return score

    squad = team["squad"]
    if len(squad) <= 11:
        team["playing_11"] = squad[:]
        team["impact_player"] = None
        return

    ranked = sorted(squad, key=player_score, reverse=True)
    xi = ranked[:11]

    # Guarantee at least 5 bowling options, swapping in the strongest bench
    # bowler for the weakest specialist batter if the top-11 is bowler-light.
    bowler_count = sum(1 for p in xi if p["bowling_rating"] > 40)
    if bowler_count < 5:
        bench = ranked[11:]
        bench_bowlers = sorted(
            [p for p in bench if p["bowling_rating"] > 40],
            key=lambda p: p["bowling_rating"],
            reverse=True,
        )
        weak_batters_in_xi = sorted(
            [p for p in xi if p["bowling_rating"] <= 40], key=player_score
        )
        swaps = min(5 - bowler_count, len(bench_bowlers), len(weak_batters_in_xi))
        for i in range(swaps):
            xi[xi.index(weak_batters_in_xi[i])] = bench_bowlers[i]

    team["playing_11"] = xi
    remaining = [p for p in ranked if p not in xi]
    team["impact_player"] = remaining[0] if remaining else None


def bot_toss_decision(team, venue=None):
    """Simple tactical heuristic: bowler-friendly pitches nudge the AI to
    bowl first with a strong attack; batting-heavy pitches and batting-heavy
    lineups nudge it to bat first. A little randomness keeps it human."""
    if venue is None:
        venue = st.session_state.get("current_venue")
    boost_role = venue.get("boost_role") if venue else None
    xi = team.get("playing_11") or team.get("squad", [])[:11]
    if not xi:
        return random.choice(["Bat First", "Bowl First"])

    avg_bat = sum(p["batting_rating"] for p in xi) / len(xi)
    avg_bowl = sum(p["bowling_rating"] for p in xi) / len(xi)
    score = avg_bat - avg_bowl

    if boost_role == "Batsman":
        score += 5
    elif boost_role == "Bowler":
        score -= 5

    decision = "Bat First" if score >= 0 else "Bowl First"
    if random.random() < 0.15:
        decision = "Bowl First" if decision == "Bat First" else "Bat First"
    return decision


# --- SIMULATOR MATRIX USING BAT / BOWL DUAL RATINGS ---
def generate_detailed_scorecard(batting_team, bowling_team, venue=None):
    if venue is None:
        venue = st.session_state.get("current_venue")
    boost_role = venue.get("boost_role") if venue else None
    boost_amount = venue.get("boost_amount", 0) if venue else 0

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
    commentary = []
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
        if boost_role in (b.get("role"), "Balanced") and boost_role == b.get("role"):
            ability += boost_amount
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
                commentary.append(f"🔴 OUT! {b['name']} departs for {runs_scored}")
                break  # Wicket
            elif ball_roll < 0.45:
                runs_scored += 1
            elif ball_roll < 0.60:
                runs_scored += 2
            elif ball_roll < 0.75:
                runs_scored += 4
                fours += 1
                commentary.append(f"🔵 FOUR! {b['name']} finds the gap")
            elif ball_roll < 0.85:
                runs_scored += 6
                sixes += 1
                commentary.append(f"🟣 SIX! {b['name']} launches it into the stands")

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

        # Evolve batting form based on this innings
        if got_out and runs_scored < 10:
            b["form"] = "Slumping"
        elif runs_scored >= 50:
            b["form"] = "Red-Hot"
        elif runs_scored >= 25:
            b["form"] = "Good"
        else:
            b["form"] = "Steady"

    total_runs += random.randint(4, 15)

    bowling_performance = []
    wickets_remaining = total_wickets
    for idx, bwl in enumerate(bowlers):
        overs = 4
        runs_conceded = random.randint(18, 45) - int(
            (bwl["bowling_rating"] - 75) * 0.35
        )
        runs_conceded -= get_form_offset(bwl.get("form", "Steady"))
        if boost_role == bwl.get("role"):
            runs_conceded -= boost_amount
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
        if wkt > 0:
            commentary.append(f"🟢 {bwl['name']} strikes! {wkt}-wicket over")

        # Evolve bowling form based on this spell
        if wkt >= 3:
            bwl["form"] = "Red-Hot"
        elif wkt == 2:
            bwl["form"] = "Good"
        elif wkt == 0 and runs_conceded > 34:
            bwl["form"] = "Slumping"
        else:
            bwl["form"] = "Steady"

    # Player of the Innings: best combined batting/bowling performance
    potm_candidates = []
    for bp in batting_performance:
        if bp["status"] != "DNB":
            score = bp["runs"] + bp["fours"] * 1 + bp["sixes"] * 2
            potm_candidates.append((score, bp["name"], f"{bp['runs']} ({bp['balls']})"))
    for bwlp in bowling_performance:
        score = bwlp["wickets"] * 25 - bwlp["runs"] * 0.5
        potm_candidates.append(
            (score, bwlp["name"], f"{bwlp['wickets']}/{bwlp['runs']}")
        )
    potm_candidates.sort(key=lambda x: x[0], reverse=True)
    top_performer = (
        {"name": potm_candidates[0][1], "line": potm_candidates[0][2]}
        if potm_candidates
        else None
    )

    return {
        "runs": total_runs,
        "wickets": min(10, total_wickets),
        "overs": round(min(120, balls_tracked) / 6, 1),
        "batting": batting_performance,
        "bowling": bowling_performance,
        "commentary": commentary,
        "top_performer": top_performer,
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
        if not t1["is_human"]:
            select_bot_playing_xi(t1, st.session_state.current_venue)
        if not t2["is_human"]:
            select_bot_playing_xi(t2, st.session_state.current_venue)
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


SAVE_STATE_KEYS = [
    "game_stage", "teams", "player_pool", "auction_index", "current_bid",
    "highest_bidder", "match_history", "stats_runs", "stats_wickets",
    "current_tab", "active_match_engine", "tournament_schedule", "match_day",
    "current_venue", "bg_simulated_day", "playoffs", "unsold_pool",
    "selected_human_idx", "timer_seconds",
]


def _export_season_json():
    data = {k: st.session_state[k] for k in SAVE_STATE_KEYS if k in st.session_state}
    return json.dumps(data, default=str, indent=2)


def _import_season_json(raw_text):
    data = json.loads(raw_text)
    for k, v in data.items():
        st.session_state[k] = v


with st.sidebar:
    st.markdown("#### 💾 Save / Load Season")
    if st.session_state.get("game_stage") in ("auction", "dashboard"):
        st.download_button(
            "⬇️ Export Season",
            data=_export_season_json(),
            file_name="ipl_season_save.json",
            mime="application/json",
            use_container_width=True,
            key="export_season_btn",
        )
    uploaded_save = st.file_uploader(
        "Import a save file", type="json", key="season_import_uploader"
    )
    if uploaded_save is not None:
        if st.button("📂 Load Uploaded Season", use_container_width=True, key="load_season_btn"):
            try:
                _import_season_json(uploaded_save.read().decode("utf-8"))
                st.success("Season loaded! Reloading...")
                st.rerun()
            except Exception as e:
                st.error(f"Couldn't load save file: {e}")
    st.markdown("---")


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
            select_bot_playing_xi(t, st.session_state.current_venue)
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
                eligible = [
                    t
                    for t in st.session_state.teams
                    if len(t["squad"]) < 20 and t["purse"] >= curr_p["base_price"]
                ]
                if eligible:
                    # Every team values the player based on need/personality;
                    # the highest bidder wins, paying just above the
                    # runner-up's valuation (classic second-price auction).
                    valuations = sorted(
                        (
                            (t, calculate_bot_valuation(t, curr_p))
                            for t in eligible
                        ),
                        key=lambda x: x[1],
                        reverse=True,
                    )
                    winner, top_val = valuations[0]
                    runner_up_val = (
                        valuations[1][1] if len(valuations) > 1 else curr_p["base_price"]
                    )
                    price = max(curr_p["base_price"], min(top_val, runner_up_val + 50))
                    price = min(round(price / 10) * 10, winner["purse"])
                    winner["purse"] -= price
                    winner["squad"].append(curr_p)
                else:
                    st.session_state.unsold_pool.append(curr_p)
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
                and (
                    not st.session_state.highest_bidder
                    or t["team_name"] != st.session_state.highest_bidder["team_name"]
                )
            ]
            # Each bot only jumps in if the next bid is still under what it
            # actually thinks the player is worth to its squad right now.
            interested = [
                (b, calculate_bot_valuation(b, player))
                for b in bots
            ]
            interested = [
                (b, val) for b, val in interested
                if val >= st.session_state.current_bid + 50
            ]
            if interested and random.random() < 0.55:
                # Teams with more valuation headroom above the current bid
                # are more likely to be the ones who jump in next.
                weights = [max(1, val - st.session_state.current_bid) for _, val in interested]
                counter_bot = random.choices(
                    [b for b, _ in interested], weights=weights, k=1
                )[0]
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
                else:
                    st.session_state.unsold_pool.append(player)
            st.session_state.auction_index += 1
            st.session_state.current_bid = 0
            st.session_state.highest_bidder = None
            st.session_state.timer_seconds = 4
            st.rerun()

        st.progress(st.session_state.timer_seconds / 4)
        st.markdown(
            f"""<div class="auction-card">
                <div class="a-name">🏃 {player['name']}</div>
                <div class="a-meta">
                    ROLE {player['role'].upper()} &nbsp;·&nbsp;
                    BAT {player['batting_rating']} &nbsp;·&nbsp;
                    BOWL {player['bowling_rating']} &nbsp;·&nbsp;
                    AGE {player['age']}
                </div>
            </div>""",
            unsafe_allow_html=True,
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

    season_complete = st.session_state.match_day > len(st.session_state.tournament_schedule)

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
            crest_initials = "".join(
                w[0] for w in user_team["team_name"].split()[:2]
            ).upper()
            st.markdown(
                f"""
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:14px;">
                    <div class="team-crest">{crest_initials}</div>
                    <div>
                        <div style="font-family:'Oswald',sans-serif;text-transform:uppercase;
                             letter-spacing:0.03em;color:var(--text);font-size:15px;line-height:1.2;">
                             {user_team['team_name']}
                        </div>
                        <div style="color:var(--text-dim);font-size:12px;">
                             Manager: {user_team.get('manager', 'Franchise Owner')}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        nav_tabs = ["Home", "Squad", "Schedule", "Table", "Stats"]
        if season_complete:
            nav_tabs.append("Playoffs")
        for tab in nav_tabs:
            if st.sidebar.button(tab, key=f"nav_btn_{tab}", use_container_width=True):
                st.session_state.current_tab = tab
                st.session_state.active_match_engine = {
                    "state": "idle",
                    "toss_winner": None,
                    "toss_decision": None,
                }
                st.rerun()

    if season_complete:
        st.markdown(
            f"""
            <div class="scoreboard-strip" style="border-left-color:var(--gold);">
                <div>
                    <div class="sb-label">League Phase</div>
                    <div class="sb-value gold" style="color:var(--gold);">Complete</div>
                </div>
                <div>
                    <div class="sb-label">Next Up</div>
                    <div class="sb-value" style="color:var(--pitch);font-size:15px;">🏆 Playoffs</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.session_state.current_tab != "Playoffs":
            if st.button("🏆 Head to Playoffs", type="primary"):
                st.session_state.current_tab = "Playoffs"
                st.rerun()
    else:
        st.markdown(
            f"""
            <div class="scoreboard-strip">
                <div>
                    <div class="sb-label">Matchday</div>
                    <div class="sb-value">{st.session_state.match_day} / {len(st.session_state.tournament_schedule)}</div>
                </div>
                <div>
                    <div class="sb-label">Format</div>
                    <div class="sb-value" style="color:var(--pitch);font-size:15px;">Double Round-Robin</div>
                </div>
                <div>
                    <div class="sb-label">Venue</div>
                    <div class="sb-value" style="color:var(--info);font-size:15px;">{st.session_state.current_venue['short']}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        top_col_left, top_col_mid, top_col_right = st.columns([3, 1, 1])
        with top_col_left:
            st.markdown(
                f"🆚 **{user_team['team_name']}** vs **{opponent_team['team_name']}**"
            )
        with top_col_mid:
            if st.button("⏩ Sim Match", key="global_sim_match_action"):
                simulate_league_background_matches(
                    user_team["team_name"], opponent_team["team_name"]
                )
                if not opponent_team["is_human"]:
                    select_bot_playing_xi(opponent_team, st.session_state.current_venue)
                sc1 = generate_detailed_scorecard(user_team, opponent_team)
                sc2 = generate_detailed_scorecard(opponent_team, user_team)
                potm = sc1["top_performer"] if sc1["runs"] >= sc2["runs"] else sc2["top_performer"]

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
                    "body": (
                        f"🏅 Player of the Match: {potm['name']} ({potm['line']})"
                        if potm else "Simulated instantly across all league grounds."
                    ),
                    "scorecard": {
                        "sc1": sc1,
                        "sc2": sc2,
                        "t1": user_team["team_name"],
                        "t2": opponent_team["team_name"],
                    },
                })
                st.session_state.match_day += 1
                st.session_state.current_venue = random.choice(VENUES)
                if st.session_state.match_day > len(st.session_state.tournament_schedule):
                    st.session_state.current_tab = "Playoffs"
                st.rerun()
        with top_col_right:
            if st.button("▷ Play Match", key="global_play_match_action", type="primary"):
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
                if not opponent_team["is_human"]:
                    select_bot_playing_xi(opponent_team, st.session_state.current_venue)
                if call_selection == random.choice(["Heads", "Tails"]):
                    engine["toss_winner"] = user_team["team_name"]
                    engine["state"] = "toss_decision_human"
                else:
                    engine["toss_winner"] = opponent_team["team_name"]
                    engine["toss_decision"] = bot_toss_decision(
                        opponent_team, st.session_state.current_venue
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
            potm = sc1["top_performer"] if sc1["runs"] >= sc2["runs"] else sc2["top_performer"]
            st.success("🏁 Match Concluded!")
            if potm:
                st.markdown(
                    f"""<div class="headline-card" style="border-left-color:var(--gold);">
                        <div class="h-date">🏅 Player of the Match</div>
                        <div class="h-title">{potm['name']} — {potm['line']}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )

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
                    "body": (
                        f"🏅 Player of the Match: {potm['name']} ({potm['line']})"
                        if potm else "Detailed ball-by-ball matrix completed."
                    ),
                    "scorecard": {
                        "sc1": sc1,
                        "sc2": sc2,
                        "t1": user_team["team_name"],
                        "t2": opponent_team["team_name"],
                    },
                })
                st.session_state.match_day += 1
                st.session_state.current_venue = random.choice(VENUES)
                if st.session_state.match_day > len(st.session_state.tournament_schedule):
                    st.session_state.current_tab = "Playoffs"
                else:
                    st.session_state.current_tab = "Home"
                st.rerun()

            st.markdown("### 📊 Interactive Scorecard")
            t1, t2, t3 = st.tabs(
                ["Innings 1 Overview", "Innings 2 Overview", "📻 Commentary"]
            )
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
            with t3:
                st.caption("Key moments from both innings")
                feed = sc1.get("commentary", []) + sc2.get("commentary", [])
                if feed:
                    for line in feed:
                        st.markdown(
                            f"""<div class="headline-card" style="padding:8px 12px;margin-bottom:5px;">
                                <span style="font-family:'JetBrains Mono',monospace;">{line}</span>
                            </div>""",
                            unsafe_allow_html=True,
                        )
                else:
                    st.info("A quiet match — no boundaries or wickets recorded.")

    elif st.session_state.current_tab == "Playoffs":
        st.header("🏆 IPL Playoffs")
        po = st.session_state.playoffs
        team_dict = {t["team_name"]: t for t in st.session_state.teams}

        if po["stage"] is None:
            ranked = sorted(
                st.session_state.teams,
                key=lambda t: (t["points"], t["wins"]),
                reverse=True,
            )
            po["seeds"] = [t["team_name"] for t in ranked[:4]]
            po["stage"] = "Q1"
            st.rerun()

        seeds = po["seeds"]
        st.markdown("### 🎟️ Top 4 Seeds")
        seed_cols = st.columns(4)
        for i, name in enumerate(seeds):
            with seed_cols[i]:
                st.markdown(
                    f"""<div class="stat-card">
                        <div class="stat-label">Seed {i+1}</div>
                        <div class="stat-value" style="font-size:16px;">{name}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )

        def _play_playoff(team1_name, team2_name, stage_label):
            t1, t2 = team_dict[team1_name], team_dict[team2_name]
            if not t1["is_human"]:
                select_bot_playing_xi(t1, st.session_state.current_venue)
            if not t2["is_human"]:
                select_bot_playing_xi(t2, st.session_state.current_venue)
            sc1 = generate_detailed_scorecard(t1, t2)
            sc2 = generate_detailed_scorecard(t2, t1)
            winner = team1_name if sc1["runs"] > sc2["runs"] else team2_name
            loser = team2_name if winner == team1_name else team1_name
            po["log"].append({
                "stage": stage_label,
                "team1": team1_name, "team2": team2_name,
                "score1": f"{sc1['runs']}/{sc1['wickets']}",
                "score2": f"{sc2['runs']}/{sc2['wickets']}",
                "winner": winner,
            })
            return winner, loser

        st.markdown("---")

        if po["stage"] == "Q1":
            st.markdown(f"### ⚔️ Qualifier 1: {seeds[0]} vs {seeds[1]}")
            st.caption("Winner goes straight to the Final. Loser gets another shot in Qualifier 2.")
            if st.button("▶ Simulate Qualifier 1", type="primary"):
                winner, loser = _play_playoff(seeds[0], seeds[1], "Qualifier 1")
                po["final_a"] = winner
                po["q1_loser"] = loser
                po["stage"] = "ELIM"
                st.rerun()

        elif po["stage"] == "ELIM":
            st.markdown(f"### ⚔️ Eliminator: {seeds[2]} vs {seeds[3]}")
            st.caption("Loser is out of the tournament. Winner meets the Qualifier 1 loser next.")
            if st.button("▶ Simulate Eliminator", type="primary"):
                winner, loser = _play_playoff(seeds[2], seeds[3], "Eliminator")
                po["elim_winner"] = winner
                po["stage"] = "Q2"
                st.rerun()

        elif po["stage"] == "Q2":
            st.markdown(f"### ⚔️ Qualifier 2: {po['q1_loser']} vs {po['elim_winner']}")
            st.caption("Winner takes the last spot in the Final.")
            if st.button("▶ Simulate Qualifier 2", type="primary"):
                winner, _ = _play_playoff(po["q1_loser"], po["elim_winner"], "Qualifier 2")
                po["final_b"] = winner
                po["stage"] = "FINAL"
                st.rerun()

        elif po["stage"] == "FINAL":
            st.markdown(f"### 🏆 FINAL: {po['final_a']} vs {po['final_b']}")
            if st.button("▶ Simulate Final", type="primary"):
                winner, _ = _play_playoff(po["final_a"], po["final_b"], "Final")
                po["champion"] = winner
                po["stage"] = "DONE"
                st.rerun()

        elif po["stage"] == "DONE":
            st.markdown(
                f"""<div class="stat-card" style="text-align:center;border-top:3px solid var(--gold);">
                    <div class="stat-label">🏆 Champions</div>
                    <div class="stat-value gold" style="font-size:32px;">{po['champion']}</div>
                </div>""",
                unsafe_allow_html=True,
            )
            st.markdown("### 🎖️ Season Awards")
            award_cols = st.columns(2)
            with award_cols[0]:
                if st.session_state.stats_runs:
                    top_bat = max(st.session_state.stats_runs.items(), key=lambda x: x[1])
                    st.markdown(
                        f"""<div class="stat-card">
                            <div class="stat-label">🟠 Orange Cap</div>
                            <div class="stat-value" style="font-size:18px;">{top_bat[0]}</div>
                            <div style="color:var(--text-dim);font-size:13px;">{top_bat[1]} runs</div>
                        </div>""",
                        unsafe_allow_html=True,
                    )
            with award_cols[1]:
                if st.session_state.stats_wickets:
                    top_bowl = max(st.session_state.stats_wickets.items(), key=lambda x: x[1])
                    st.markdown(
                        f"""<div class="stat-card">
                            <div class="stat-label">🟣 Purple Cap</div>
                            <div class="stat-value" style="font-size:18px;">{top_bowl[0]}</div>
                            <div style="color:var(--text-dim);font-size:13px;">{top_bowl[1]} wickets</div>
                        </div>""",
                        unsafe_allow_html=True,
                    )

        if po["log"]:
            st.markdown("### 📜 Playoff Results")
            for entry in po["log"]:
                st.markdown(
                    f"""<div class="headline-card">
                        <div class="h-date">{entry['stage']}</div>
                        <div class="h-title">{entry['team1']} {entry['score1']} vs
                            {entry['team2']} {entry['score2']} — 🏆 {entry['winner']}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )

    elif st.session_state.current_tab == "Home":
        sorted_teams = sorted(
            st.session_state.teams, key=lambda x: x["points"], reverse=True
        )
        my_pos = (
            sorted_teams.index(user_team) + 1 if user_team in sorted_teams else 1
        )

        met_col1, met_col2, met_col3 = st.columns(3)
        with met_col1:
            st.markdown(
                f"""<div class="stat-card">
                    <div class="stat-label">🔮 Next Match</div>
                    <div class="stat-value">vs {opponent_team['team_name']}</div>
                </div>""",
                unsafe_allow_html=True,
            )
        with met_col2:
            st.markdown(
                f"""<div class="stat-card">
                    <div class="stat-label">🏆 League Position</div>
                    <div class="stat-value gold">#{my_pos}</div>
                    <div style="color:var(--text-dim);font-size:13px;margin-top:2px;">{user_team['points']} pts</div>
                </div>""",
                unsafe_allow_html=True,
            )
        with met_col3:
            st.markdown(
                f"""<div class="stat-card">
                    <div class="stat-label">📈 Season Record</div>
                    <div class="stat-value pitch">{user_team['wins']}W – {user_team['losses']}L</div>
                </div>""",
                unsafe_allow_html=True,
            )

        if st.session_state.match_history:
            st.markdown("### 📰 Latest Headlines")
            for entry in reversed(st.session_state.match_history[-5:]):
                st.markdown(
                    f"""<div class="headline-card">
                        <div class="h-date">{entry.get('date', '')} · {entry.get('type', '')}</div>
                        <div class="h-title">{entry.get('headline', '')}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )

    elif st.session_state.current_tab == "Squad":
        st.subheader(f"👥 Squad Management: {user_team['team_name']}")

        squad = user_team["squad"]
        name_to_player = {p["name"]: p for p in squad}

        def _label(p):
            return (
                f"{p['name']} ({p['role']}) | Bat {p['batting_rating']} /"
                f" Bowl {p['bowling_rating']}"
            )

        current_xi_names = [
            p["name"] for p in user_team.get("playing_11", []) if p["name"] in name_to_player
        ]
        current_impact_name = (
            user_team["impact_player"]["name"]
            if user_team.get("impact_player")
            and user_team["impact_player"]["name"] in name_to_player
            else None
        )

        st.markdown("### 🏏 Set Your Playing XI")
        st.caption(
            "Pick exactly 11 players to start the next match. The 12th player"
            " (Impact Player) is chosen separately below."
        )

        selected_names = st.multiselect(
            "Playing XI",
            options=list(name_to_player.keys()),
            default=current_xi_names,
            format_func=lambda n: _label(name_to_player[n]),
            key="playing_xi_multiselect",
        )

        remaining_count = 11 - len(selected_names)
        if remaining_count > 0:
            st.warning(f"Select {remaining_count} more player(s) to complete your XI.")
        elif remaining_count < 0:
            st.error(f"Remove {-remaining_count} player(s) — only 11 allowed.")
        else:
            st.success("✅ 11 players selected.")

        bench_names = [n for n in name_to_player if n not in selected_names]
        impact_options = ["(None)"] + bench_names
        impact_default = (
            current_impact_name if current_impact_name in bench_names else "(None)"
        )
        selected_impact = st.selectbox(
            "🔁 Impact Player (12th man, chosen from the bench)",
            options=impact_options,
            index=impact_options.index(impact_default),
            format_func=lambda n: "(None)" if n == "(None)" else _label(name_to_player[n]),
            key="impact_player_select",
        )

        if st.button(
            "💾 Save Playing XI", type="primary", disabled=(remaining_count != 0)
        ):
            user_team["playing_11"] = [name_to_player[n] for n in selected_names]
            user_team["impact_player"] = (
                name_to_player[selected_impact] if selected_impact != "(None)" else None
            )
            st.success("Playing XI saved for the next match!")

        st.markdown("---")
        st.markdown("### 📋 Full Squad")
        for p in squad:
            if p["name"] in selected_names:
                tag = '<span class="pill pill-xi">XI</span>'
            elif p["name"] == selected_impact:
                tag = '<span class="pill pill-impact">Impact</span>'
            else:
                tag = ""
            st.markdown(
                f"""<div class="player-row">
                    <div>
                        <span class="p-name">{p['name']}</span>{tag}
                        <span class="p-role">{p['role']}</span>
                    </div>
                    <div class="p-ratings">BAT {p['batting_rating']} · BOWL {p['bowling_rating']}</div>
                </div>""",
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.markdown("### 🔁 Transfer Market")
        st.caption(
            "Release players you don't need, or sign free agents from the"
            " unsold pool. Changes apply immediately — remember to update your"
            " Playing XI above if you release someone in it."
        )
        tm_col1, tm_col2 = st.columns(2)

        with tm_col1:
            st.markdown("**Release a Player**")
            if squad:
                release_name = st.selectbox(
                    "Choose a squad player to release",
                    options=[p["name"] for p in squad],
                    key="release_player_select",
                )
                if st.button("🚮 Release Player", use_container_width=True):
                    released = name_to_player[release_name]
                    user_team["squad"] = [
                        p for p in user_team["squad"] if p["name"] != release_name
                    ]
                    user_team["playing_11"] = [
                        p for p in user_team.get("playing_11", []) if p["name"] != release_name
                    ]
                    if (
                        user_team.get("impact_player")
                        and user_team["impact_player"]["name"] == release_name
                    ):
                        user_team["impact_player"] = None
                    st.session_state.unsold_pool.append(released)
                    st.success(f"{release_name} released to the free agent pool.")
                    st.rerun()
            else:
                st.info("Your squad is empty.")

        with tm_col2:
            st.markdown("**Sign a Free Agent**")
            if st.session_state.unsold_pool:
                fa_options = {
                    f"{p['name']} ({p['role']}) — ₹{p['base_price']/100:.2f} CR": p
                    for p in st.session_state.unsold_pool
                }
                fa_label = st.selectbox(
                    "Available free agents", options=list(fa_options.keys()), key="fa_select"
                )
                fa_player = fa_options[fa_label]
                can_afford = user_team["purse"] >= fa_player["base_price"]
                has_space = len(user_team["squad"]) < 20
                if not has_space:
                    st.warning("Squad is full (20 players).")
                elif not can_afford:
                    st.warning("Not enough purse remaining.")
                if st.button(
                    "✅ Sign Player",
                    use_container_width=True,
                    disabled=not (can_afford and has_space),
                ):
                    user_team["purse"] -= fa_player["base_price"]
                    user_team["squad"].append(fa_player)
                    st.session_state.unsold_pool = [
                        p for p in st.session_state.unsold_pool if p["name"] != fa_player["name"]
                    ]
                    st.success(f"Signed {fa_player['name']}!")
                    st.rerun()
                st.caption(f"Your purse: ₹{user_team['purse']/100:.2f} CR")
            else:
                st.info("No free agents available right now.")

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
