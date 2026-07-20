import streamlit as st
import random
import pandas as pd

# Page setup
st.set_page_config(page_title="IPL Pro-Manager Simulation Console", layout="wide")

# ==========================================
# 1. REAL-WORLD 200 PLAYER DATABASE WITH XP/POTENTIAL
# ==========================================
if "player_pool" not in st.session_state:
    raw_players = [
        # --- BATSMEEN & WICKET-KEEPERS ---
        {"name": "Virat Kohli", "role": "Batsman", "rating": 94, "potential": 95, "age": 37, "xp": 0, "trait": "Anchor"},
        {"name": "Rohit Sharma", "role": "Batsman", "rating": 92, "potential": 92, "age": 38, "xp": 0, "trait": "Enforcer"},
        {"name": "Shubman Gill", "role": "Batsman", "rating": 90, "potential": 95, "age": 26, "xp": 0, "trait": "Classicist"},
        {"name": "Suryakumar Yadav", "role": "Batsman", "rating": 93, "potential": 93, "age": 35, "xp": 0, "trait": "360 Innovator"},
        {"name": "Rishabh Pant", "role": "Wicket-Keeper", "rating": 91, "potential": 94, "age": 28, "xp": 0, "trait": "Counter-Attacker"},
        {"name": "Yashasvi Jaiswal", "role": "Batsman", "rating": 89, "potential": 96, "age": 24, "xp": 0, "trait": "Power-Hitter"},
        {"name": "Ruturaj Gaikwad", "role": "Batsman", "rating": 88, "potential": 92, "age": 29, "xp": 0, "trait": "Captain-Cool"},
        {"name": "Sanju Samson", "role": "Wicket-Keeper", "rating": 88, "potential": 90, "age": 31, "xp": 0, "trait": "Maverick"},
        {"name": "KL Rahul", "role": "Wicket-Keeper", "rating": 87, "potential": 89, "age": 33, "xp": 0, "trait": "Anchor"},
        {"name": "Rinku Singh", "role": "Batsman", "rating": 86, "potential": 90, "age": 28, "xp": 0, "trait": "Finisher"},
        {"name": "Shreyas Iyer", "role": "Batsman", "rating": 87, "potential": 89, "age": 31, "xp": 0, "trait": "Spin-Basher"},
        {"name": "Ishan Kishan", "role": "Wicket-Keeper", "rating": 85, "potential": 89, "age": 27, "xp": 0, "trait": "Enforcer"},
        {"name": "Heinrich Klaasen", "role": "Wicket-Keeper", "rating": 92, "potential": 92, "age": 34, "xp": 0, "trait": "Spin-Basher"},
        {"name": "Travis Head", "role": "Batsman", "rating": 93, "potential": 93, "age": 32, "xp": 0, "trait": "Power-Hitter"},
        {"name": "Phil Salt", "role": "Wicket-Keeper", "rating": 88, "potential": 91, "age": 29, "xp": 0, "trait": "Enforcer"},
        {"name": "Jos Buttler", "role": "Wicket-Keeper", "rating": 91, "potential": 91, "age": 35, "xp": 0, "trait": "Classicist"},
        {"name": "Nicholas Pooran", "role": "Wicket-Keeper", "rating": 90, "potential": 92, "age": 30, "xp": 0, "trait": "Finisher"},
        {"name": "Faf du Plessis", "role": "Batsman", "rating": 86, "potential": 86, "age": 41, "xp": 0, "trait": "Anchor"},
        {"name": "David Warner", "role": "Batsman", "rating": 85, "potential": 85, "age": 39, "xp": 0, "trait": "Enforcer"},
        {"name": "Quinton de Kock", "role": "Wicket-Keeper", "rating": 86, "potential": 86, "age": 33, "xp": 0, "trait": "Classicist"},
        {"name": "Sai Sudharsan", "role": "Batsman", "rating": 85, "potential": 90, "age": 24, "xp": 0, "trait": "Anchor"},
        {"name": "Rajat Patidar", "role": "Batsman", "rating": 84, "potential": 86, "age": 32, "xp": 0, "trait": "Spin-Basher"},
        {"name": "Tilak Varma", "role": "Batsman", "rating": 86, "potential": 91, "age": 23, "xp": 0, "trait": "Counter-Attacker"},
        {"name": "Abhishek Sharma", "role": "Batsman", "rating": 87, "potential": 93, "age": 25, "xp": 0, "trait": "Power-Hitter"},
        {"name": "Jake Fraser-McGurk", "role": "Batsman", "rating": 86, "potential": 92, "age": 23, "xp": 0, "trait": "Enforcer"},
        {"name": "Tristan Stubbs", "role": "Batsman", "rating": 87, "potential": 92, "age": 25, "xp": 0, "trait": "Finisher"},
        {"name": "Shimron Hetmyer", "role": "Batsman", "rating": 83, "potential": 86, "age": 29, "xp": 0, "trait": "Finisher"},
        {"name": "Glenn Phillips", "role": "Batsman", "rating": 84, "potential": 87, "age": 29, "xp": 0, "trait": "Dynamic Fielder"},
        {"name": "Kane Williamson", "role": "Batsman", "rating": 85, "potential": 85, "age": 35, "xp": 0, "trait": "Anchor"},
        {"name": "Devdutt Padikkal", "role": "Batsman", "rating": 80, "potential": 85, "age": 25, "xp": 0, "trait": "Classicist"},
        {"name": "Prithvi Shaw", "role": "Batsman", "rating": 81, "potential": 86, "age": 26, "xp": 0, "trait": "Enforcer"},
        {"name": "Ajinkya Rahane", "role": "Batsman", "rating": 81, "potential": 81, "age": 37, "xp": 0, "trait": "Anchor"},
        {"name": "Manish Pandey", "role": "Batsman", "rating": 79, "potential": 79, "age": 36, "xp": 0, "trait": "Anchor"},
        {"name": "Mayank Agarwal", "role": "Batsman", "rating": 80, "potential": 82, "age": 34, "xp": 0, "trait": "Classicist"},
        {"name": "Jitesh Sharma", "role": "Wicket-Keeper", "rating": 82, "potential": 85, "age": 32, "xp": 0, "trait": "Counter-Attacker"},
        {"name": "Dhruv Jurel", "role": "Wicket-Keeper", "rating": 83, "potential": 89, "age": 25, "xp": 0, "trait": "Finisher"},
        {"name": "Anuj Rawat", "role": "Wicket-Keeper", "rating": 78, "potential": 83, "age": 26, "xp": 0, "trait": "Counter-Attacker"},
        {"name": "Wriddhiman Saha", "role": "Wicket-Keeper", "rating": 79, "potential": 79, "age": 41, "xp": 0, "trait": "Safe Hands"},
        {"name": "Dinesh Karthik", "role": "Wicket-Keeper", "rating": 82, "potential": 82, "age": 40, "xp": 0, "trait": "Finisher"},
        {"name": "Sarfaraz Khan", "role": "Batsman", "rating": 81, "potential": 85, "age": 28, "xp": 0, "trait": "Spin-Basher"},
        {"name": "Nitish Rana", "role": "Batsman", "rating": 83, "potential": 85, "age": 32, "xp": 0, "trait": "Counter-Attacker"},
        {"name": "Venkatesh Iyer", "role": "Batsman", "rating": 84, "potential": 86, "age": 31, "xp": 0, "trait": "Clutch Player"},
        {"name": "Ramandeep Singh", "role": "Batsman", "rating": 80, "potential": 84, "age": 29, "xp": 0, "trait": "Finisher"},
        {"name": "Angkrish Raghuvanshi", "role": "Batsman", "rating": 78, "potential": 88, "age": 20, "xp": 0, "trait": "Young Prodigy"},
        {"name": "Nehal Wadhera", "role": "Batsman", "rating": 81, "potential": 86, "age": 25, "xp": 0, "trait": "Counter-Attacker"},
        {"name": "Vishnu Vinod", "role": "Wicket-Keeper", "rating": 76, "potential": 79, "age": 32, "xp": 0, "trait": "Power-Hitter"},
        {"name": "Ayush Badoni", "role": "Batsman", "rating": 81, "potential": 86, "age": 26, "xp": 0, "trait": "Finisher"},
        {"name": "Deepak Hooda", "role": "Batsman", "rating": 80, "potential": 83, "age": 30, "xp": 0, "trait": "Counter-Attacker"},
        {"name": "Devon Conway", "role": "Batsman", "rating": 88, "potential": 88, "age": 34, "xp": 0, "trait": "Anchor"},
        {"name": "Rachin Ravindra", "role": "Batsman", "rating": 85, "potential": 91, "age": 26, "xp": 0, "trait": "Classicist"},
        {"name": "Sameer Rizvi", "role": "Batsman", "rating": 77, "potential": 85, "age": 22, "xp": 0, "trait": "Spin-Basher"},
        {"name": "Ashutosh Sharma", "role": "Batsman", "rating": 82, "potential": 86, "age": 27, "xp": 0, "trait": "Finisher"},
        {"name": "Shashank Singh", "role": "Batsman", "rating": 83, "potential": 85, "age": 34, "xp": 0, "trait": "Clutch Player"},
        {"name": "Prabhsimran Singh", "role": "Wicket-Keeper", "rating": 81, "potential": 85, "age": 25, "xp": 0, "trait": "Enforcer"},
        {"name": "Atharva Taide", "role": "Batsman", "rating": 77, "potential": 82, "age": 25, "xp": 0, "trait": "Classicist"},
        {"name": "Rovman Powell", "role": "Batsman", "rating": 83, "potential": 84, "age": 32, "xp": 0, "trait": "Power-Hitter"},
        {"name": "Donavon Ferreira", "role": "Wicket-Keeper", "rating": 77, "potential": 81, "age": 27, "xp": 0, "trait": "Finforcer"},
        {"name": "Tom Kohler-Cadmore", "role": "Wicket-Keeper", "rating": 79, "potential": 82, "age": 31, "xp": 0, "trait": "Enforcer"},
        {"name": "Shai Hope", "role": "Wicket-Keeper", "rating": 82, "potential": 84, "age": 32, "xp": 0, "trait": "Anchor"},
        {"name": "Kumar Kushagra", "role": "Wicket-Keeper", "rating": 76, "potential": 85, "age": 21, "xp": 0, "trait": "Young Prodigy"},
        {"name": "Abishek Porel", "role": "Wicket-Keeper", "rating": 80, "potential": 86, "age": 23, "xp": 0, "trait": "Counter-Attacker"},
        {"name": "Ricky Bhui", "role": "Batsman", "rating": 75, "potential": 78, "age": 29, "xp": 0, "trait": "Classicist"},
        {"name": "Matthew Wade", "role": "Wicket-Keeper", "rating": 81, "potential": 81, "age": 38, "xp": 0, "trait": "Counter-Attacker"},
        {"name": "Shahrukh Khan", "role": "Batsman", "rating": 80, "potential": 84, "age": 30, "xp": 0, "trait": "Power-Hitter"},
        {"name": "Abdul Samad", "role": "Batsman", "rating": 79, "potential": 84, "age": 24, "xp": 0, "trait": "Power-Hitter"},
        {"name": "Rahul Tripathi", "role": "Batsman", "rating": 82, "potential": 83, "age": 34, "xp": 0, "trait": "Counter-Attacker"},
        {"name": "David Miller", "role": "Batsman", "rating": 87, "potential": 87, "age": 36, "xp": 0, "trait": "Killer Miller"},
        {"name": "Aiden Markram", "role": "Batsman", "rating": 85, "potential": 87, "age": 31, "xp": 0, "trait": "Classicist"},
        {"name": "Tim David", "role": "Batsman", "rating": 83, "potential": 85, "age": 30, "xp": 0, "trait": "Finisher"},
        {"name": "Finn Allen", "role": "Batsman", "rating": 82, "potential": 86, "age": 26, "xp": 0, "trait": "Enforcer"},
        {"name": "Dewald Brevis", "role": "Batsman", "rating": 80, "potential": 91, "age": 22, "xp": 0, "trait": "Baby AB"},
        {"name": "Karun Nair", "role": "Batsman", "rating": 79, "potential": 80, "age": 34, "xp": 0, "trait": "Classicist"},

        # --- ALL-ROUNDERS ---
        {"name": "Hardik Pandya", "role": "All-Rounder", "rating": 91, "potential": 92, "age": 32, "xp": 0, "trait": "Clutch Deliverer"},
        {"name": "Ravindra Jadeja", "role": "All-Rounder", "rating": 92, "potential": 92, "age": 37, "xp": 0, "trait": "Sir Jadeja"},
        {"name": "Axar Patel", "role": "All-Rounder", "rating": 89, "potential": 90, "age": 32, "xp": 0, "trait": "Safe Hands"},
        {"name": "Andre Russell", "role": "All-Rounder", "rating": 91, "potential": 91, "age": 37, "xp": 0, "trait": "Muscle Russell"},
        {"name": "Sunil Narine", "role": "All-Rounder", "rating": 92, "potential": 92, "age": 37, "xp": 0, "trait": "Mystery Spinner"},
        {"name": "Glenn Maxwell", "role": "All-Rounder", "rating": 88, "potential": 88, "age": 37, "xp": 0, "trait": "Big Show"},
        {"name": "Marcus Stoinis", "role": "All-Rounder", "rating": 87, "potential": 87, "age": 36, "xp": 0, "trait": "Finisher"},
        {"name": "Liam Livingstone", "role": "All-Rounder", "rating": 86, "potential": 87, "age": 32, "xp": 0, "trait": "Power-Hitter"},
        {"name": "Rashid Khan", "role": "All-Rounder", "rating": 93, "potential": 95, "age": 27, "xp": 0, "trait": "Mystery Spinner"},
        {"name": "Cameron Green", "role": "All-Rounder", "rating": 87, "potential": 93, "age": 26, "xp": 0, "trait": "Classicist"},
        {"name": "Mitchell Marsh", "role": "All-Rounder", "rating": 86, "potential": 87, "age": 34, "xp": 0, "trait": "Enforcer"},
        {"name": "Sam Curran", "role": "All-Rounder", "rating": 86, "potential": 89, "age": 27, "xp": 0, "trait": "Swing King"},
        {"name": "Krunal Pandya", "role": "All-Rounder", "rating": 83, "potential": 84, "age": 34, "xp": 0, "trait": "Anchor"},
        {"name": "Washington Sundar", "role": "All-Rounder", "rating": 81, "potential": 87, "age": 26, "xp": 0, "trait": "Economic Spin"},
        {"name": "Shivam Dube", "role": "All-Rounder", "rating": 86, "potential": 88, "age": 32, "xp": 0, "trait": "Spin-Basher"},
        {"name": "Riyan Parag", "role": "All-Rounder", "rating": 85, "potential": 91, "age": 24, "xp": 0, "trait": "Clutch Player"},
        {"name": "Nitish Kumar Reddy", "role": "All-Rounder", "rating": 82, "potential": 90, "age": 22, "xp": 0, "trait": "Young Prodigy"},
        {"name": "Pat Cummins", "role": "All-Rounder", "rating": 91, "potential": 91, "age": 32, "xp": 0, "trait": "Captain-Cool"},
        {"name": "Ravichandran Ashwin", "role": "All-Rounder", "rating": 85, "potential": 85, "age": 39, "xp": 0, "trait": "Professor"},
        {"name": "Moeen Ali", "role": "All-Rounder", "rating": 83, "potential": 83, "age": 38, "xp": 0, "trait": "Spin-Basher"},
        {"name": "Mitchell Santner", "role": "All-Rounder", "rating": 84, "potential": 85, "age": 34, "xp": 0, "trait": "Economic Spin"},
        {"name": "Romario Shepherd", "role": "All-Rounder", "rating": 79, "potential": 82, "age": 31, "xp": 0, "trait": "Power-Hitter"},
        {"name": "Mohammad Nabi", "role": "All-Rounder", "rating": 81, "potential": 81, "age": 41, "xp": 0, "trait": "Professor"},
        {"name": "Sikandar Raza", "role": "All-Rounder", "rating": 82, "potential": 83, "age": 39, "xp": 0, "trait": "Clutch Player"},
        {"name": "Vijay Shankar", "role": "All-Rounder", "rating": 78, "potential": 79, "age": 35, "xp": 0, "trait": "Anchor"},
        {"name": "Rahul Tewatia", "role": "All-Rounder", "rating": 82, "potential": 84, "age": 32, "xp": 0, "trait": "Ice Man"},
        {"name": "Azmatullah Omarzai", "role": "All-Rounder", "rating": 80, "potential": 86, "age": 25, "xp": 0, "trait": "Swing King"},
        {"name": "Shahbaz Ahmed", "role": "All-Rounder", "rating": 80, "potential": 83, "age": 31, "xp": 0, "trait": "Anchor"},
        {"name": "Marco Jansen", "role": "All-Rounder", "rating": 83, "potential": 89, "age": 25, "xp": 0, "trait": "Bounce Specialist"},
        {"name": "Wanindu Hasaranga", "role": "All-Rounder", "rating": 86, "potential": 89, "age": 28, "xp": 0, "trait": "Mystery Spinner"},
        {"name": "Will Jacks", "role": "All-Rounder", "rating": 84, "potential": 89, "age": 27, "xp": 0, "trait": "Power-Hitter"},
        {"name": "Mahipal Lomror", "role": "All-Rounder", "rating": 79, "potential": 83, "age": 26, "xp": 0, "trait": "Spin-Basher"},
        {"name": "Harshit Rana", "role": "All-Rounder", "rating": 82, "potential": 88, "age": 24, "xp": 0, "trait": "Enforcer Bowler"},
        {"name": "Naman Dhir", "role": "All-Rounder", "rating": 79, "potential": 84, "age": 26, "xp": 0, "trait": "Counter-Attacker"},
        {"name": "Lalit Yadav", "role": "All-Rounder", "rating": 77, "potential": 80, "age": 29, "xp": 0, "trait": "Anchor"},
        {"name": "Rishi Dhawan", "role": "All-Rounder", "rating": 76, "potential": 76, "age": 36, "xp": 0, "trait": "Swing King"},
        {"name": "Anukul Roy", "role": "All-Rounder", "rating": 77, "potential": 80, "age": 27, "xp": 0, "trait": "Economic Spin"},
        {"name": "Sherfane Rutherford", "role": "All-Rounder", "rating": 80, "potential": 83, "age": 27, "xp": 0, "trait": "Finisher"},
        {"name": "Arshin Kulkarni", "role": "All-Rounder", "rating": 75, "potential": 87, "age": 21, "xp": 0, "trait": "Young Prodigy"},
        {"name": "Kamlesh Nagarkoti", "role": "All-Rounder", "rating": 76, "potential": 81, "age": 26, "xp": 0, "trait": "Express Pace"},
        {"name": "Harshal Patel", "role": "All-Rounder", "rating": 85, "potential": 85, "age": 35, "xp": 0, "trait": "Death Over King"},
        {"name": "Jacob Bethell", "role": "All-Rounder", "rating": 79, "potential": 87, "age": 22, "xp": 0, "trait": "Young Prodigy"},
        {"name": "Swapnil Singh", "role": "All-Rounder", "rating": 78, "potential": 79, "age": 35, "xp": 0, "trait": "Economic Spin"},

        # --- BOWLERS ---
        {"name": "Jasprit Bumrah", "role": "Bowler", "rating": 96, "potential": 96, "age": 32, "xp": 0, "trait": "Yorker Specialist"},
        {"name": "Kuldeep Yadav", "role": "Bowler", "rating": 91, "potential": 93, "age": 31, "xp": 0, "trait": "Mystery Spinner"},
        {"name": "Mohammed Siraj", "role": "Bowler", "rating": 88, "potential": 90, "age": 31, "xp": 0, "trait": "Swing King"},
        {"name": "Arshdeep Singh", "role": "Bowler", "rating": 89, "potential": 92, "age": 27, "xp": 0, "trait": "Death Over King"},
        {"name": "Yuzvendra Chahal", "role": "Bowler", "rating": 89, "potential": 89, "age": 35, "xp": 0, "trait": "Trickster"},
        {"name": "Trent Boult", "role": "Bowler", "rating": 90, "potential": 90, "age": 36, "xp": 0, "trait": "Powerplay Striker"},
        {"name": "Mitchell Starc", "role": "Bowler", "rating": 91, "potential": 91, "age": 36, "xp": 0, "trait": "Express Pace"},
        {"name": "Kagiso Rabada", "role": "Bowler", "rating": 90, "potential": 91, "age": 30, "xp": 0, "trait": "Bounce Specialist"},
        {"name": "Matheesha Pathirana", "role": "Bowler", "rating": 89, "potential": 95, "age": 23, "xp": 0, "trait": "Baby Malinga"},
        {"name": "T Natarajan", "role": "Bowler", "rating": 86, "potential": 87, "age": 34, "xp": 0, "trait": "Yorker Specialist"},
        {"name": "Bhuvneshwar Kumar", "role": "Bowler", "rating": 85, "potential": 85, "age": 36, "xp": 0, "trait": "Swing King"},
        {"name": "Mayank Yadav", "role": "Bowler", "rating": 84, "potential": 94, "age": 23, "xp": 0, "trait": "Express Pace"},
        {"name": "Varun Chakaravarthy", "role": "Bowler", "rating": 87, "potential": 88, "age": 34, "xp": 0, "trait": "Mystery Spinner"},
        {"name": "Ravi Bishnoi", "role": "Bowler", "rating": 86, "potential": 91, "age": 25, "xp": 0, "trait": "Trickster"},
        {"name": "Khaleel Ahmed", "role": "Bowler", "rating": 84, "potential": 87, "age": 28, "xp": 0, "trait": "Swing King"},
        {"name": "Mukesh Kumar", "role": "Bowler", "rating": 84, "potential": 85, "age": 32, "xp": 0, "trait": "Line & Length"},
        {"name": "Avesh Khan", "role": "Bowler", "rating": 83, "potential": 86, "age": 29, "xp": 0, "trait": "Enforcer Bowler"},
        {"name": "Sandeep Sharma", "role": "Bowler", "rating": 85, "potential": 85, "age": 32, "xp": 0, "trait": "Death Over King"},
        {"name": "Mohit Sharma", "role": "Bowler", "rating": 83, "potential": 83, "age": 37, "xp": 0, "trait": "Back-of-Hand Slow"},
        {"name": "Mohammed Shami", "role": "Bowler", "rating": 90, "potential": 90, "age": 35, "xp": 0, "trait": "Seam Presentation"},
        {"name": "Prasidh Krishna", "role": "Bowler", "rating": 82, "potential": 86, "age": 30, "xp": 0, "trait": "Bounce Specialist"},
        {"name": "Shardul Thakur", "role": "Bowler", "rating": 82, "potential": 83, "age": 34, "xp": 0, "trait": "Partnership Breaker"},
        {"name": "Deepak Chahar", "role": "Bowler", "rating": 83, "potential": 84, "age": 33, "xp": 0, "trait": "Powerplay Striker"},
        {"name": "Tushar Deshpande", "role": "Bowler", "rating": 83, "potential": 86, "age": 30, "xp": 0, "trait": "Enforcer Bowler"},
        {"name": "Mustafizur Rahman", "role": "Bowler", "rating": 85, "potential": 86, "age": 30, "xp": 0, "trait": "Cutter Specialist"},
        {"name": "Maheesh Theekshana", "role": "Bowler", "rating": 85, "potential": 89, "age": 25, "xp": 0, "trait": "Mystery Spinner"},
        {"name": "Akash Madhwal", "role": "Bowler", "rating": 80, "potential": 83, "age": 32, "xp": 0, "trait": "Yorker Specialist"},
        {"name": "Gerald Coetzee", "role": "Bowler", "rating": 84, "potential": 90, "age": 25, "xp": 0, "trait": "Express Pace"},
        {"name": "Nuwan Thushara", "role": "Bowler", "rating": 81, "potential": 84, "age": 31, "xp": 0, "trait": "Slingy Action"},
        {"name": "Piyush Chawla", "role": "Bowler", "rating": 81, "potential": 81, "age": 37, "xp": 0, "trait": "Trickster"},
        {"name": "Vaibhav Arora", "role": "Bowler", "rating": 80, "potential": 85, "age": 28, "xp": 0, "trait": "Swing King"},
        {"name": "Anrich Nortje", "role": "Bowler", "rating": 85, "potential": 87, "age": 32, "xp": 0, "trait": "Express Pace"},
        {"name": "Ishant Sharma", "role": "Bowler", "rating": 80, "potential": 80, "age": 37, "xp": 0, "trait": "Line & Length"},
        {"name": "Lockie Ferguson", "role": "Bowler", "rating": 83, "potential": 84, "age": 34, "xp": 0, "trait": "Express Pace"},
        {"name": "Yash Dayal", "role": "Bowler", "rating": 81, "potential": 85, "age": 28, "xp": 0, "trait": "Swing King"},
        {"name": "Vijaykumar Vyshak", "role": "Bowler", "rating": 79, "potential": 83, "age": 29, "xp": 0, "trait": "Knuckle-Ball Master"},
        {"name": "Karn Sharma", "role": "Bowler", "rating": 78, "potential": 78, "age": 38, "xp": 0, "trait": "Trickster"},
        {"name": "Akash Deep", "role": "Bowler", "rating": 79, "potential": 83, "age": 29, "xp": 0, "trait": "Seam Presentation"},
        {"name": "Reece Topley", "role": "Bowler", "rating": 82, "potential": 84, "age": 32, "xp": 0, "trait": "Bounce Specialist"},
        {"name": "Nathan Ellis", "role": "Bowler", "rating": 81, "potential": 84, "age": 31, "xp": 0, "trait": "Death Over King"},
        {"name": "Rahul Chahar", "role": "Bowler", "rating": 81, "potential": 84, "age": 26, "xp": 0, "trait": "Trickster"},
        {"name": "Harpreet Brar", "role": "Bowler", "rating": 80, "potential": 83, "age": 30, "xp": 0, "trait": "Economic Spin"},
        {"name": "Jaydev Unadkat", "role": "Bowler", "rating": 79, "potential": 79, "age": 34, "xp": 0, "trait": "Cutter Specialist"},
        {"name": "Umran Malik", "role": "Bowler", "rating": 80, "potential": 87, "age": 26, "xp": 0, "trait": "Express Pace"},
        {"name": "Fazalhaq Farooqi", "role": "Bowler", "rating": 82, "potential": 86, "age": 25, "xp": 0, "trait": "Powerplay Striker"},
        {"name": "R. Sai Kishore", "role": "Bowler", "rating": 81, "potential": 85, "age": 29, "xp": 0, "trait": "Economic Spin"},
        {"name": "Noor Ahmad", "role": "Bowler", "rating": 85, "potential": 92, "age": 21, "xp": 0, "trait": "Mystery Spinner"},
        {"name": "Spencer Johnson", "role": "Bowler", "rating": 81, "potential": 85, "age": 30, "xp": 0, "trait": "Express Pace"},
        {"name": "Yash Thakur", "role": "Bowler", "rating": 79, "potential": 83, "age": 27, "xp": 0, "trait": "Death Over King"},
        {"name": "Naveen-ul-Haq", "role": "Bowler", "rating": 83, "potential": 85, "age": 26, "xp": 0, "trait": "Back-of-Hand Slow"},
        {"name": "Shamar Joseph", "role": "Bowler", "rating": 80, "potential": 88, "age": 26, "xp": 0, "trait": "Express Pace"},
        {"name": "Matt Henry", "role": "Bowler", "rating": 82, "potential": 83, "age": 33, "xp": 0, "trait": "Seam Presentation"},
        {"name": "Dilshan Madushanka", "role": "Bowler", "rating": 80, "potential": 86, "age": 25, "xp": 0, "trait": "Swing King"},
        {"name": "Nandre Burger", "role": "Bowler", "rating": 81, "potential": 86, "age": 30, "xp": 0, "trait": "Express Pace"},
        {"name": "Navdeep Saini", "role": "Bowler", "rating": 78, "potential": 80, "age": 33, "xp": 0, "trait": "Express Pace"},
        {"name": "Kuldeep Sen", "role": "Bowler", "rating": 77, "potential": 82, "age": 29, "xp": 0, "trait": "Express Pace"},
        {"name": "Mukesh Choudhary", "role": "Bowler", "rating": 79, "potential": 82, "age": 29, "xp": 0, "trait": "Powerplay Striker"},
        {"name": "Gurjapneet Singh", "role": "Bowler", "rating": 78, "potential": 84, "age": 27, "xp": 0, "trait": "Swing King"},
        {"name": "Anshul Kamboj", "role": "Bowler", "rating": 79, "potential": 85, "age": 25, "xp": 0, "trait": "Line & Length"},
        {"name": "Shreyas Gopal", "role": "Bowler", "rating": 78, "potential": 79, "age": 32, "xp": 0, "trait": "Trickster"},
        {"name": "Arjun Tendulkar", "role": "Bowler", "rating": 75, "potential": 81, "age": 26, "xp": 0, "trait": "Swing King"},
        {"name": "Chetan Sakariya", "role": "Bowler", "rating": 77, "potential": 81, "age": 28, "xp": 0, "trait": "Back-of-Hand Slow"},
        {"name": "Dushmantha Chameera", "role": "Bowler", "rating": 80, "potential": 80, "age": 34, "xp": 0, "trait": "Express Pace"},
        {"name": "Rasikh Dar", "role": "Bowler", "rating": 78, "potential": 84, "age": 26, "xp": 0, "trait": "Knuckle-Ball Master"},
        {"name": "Josh Hazlewood", "role": "Bowler", "rating": 89, "potential": 89, "age": 35, "xp": 0, "trait": "Line & Length"},
        {"name": "Suyash Sharma", "role": "Bowler", "rating": 79, "potential": 88, "age": 22, "xp": 0, "trait": "Mystery Spinner"},
        {"name": "Jofra Archer", "role": "Bowler", "rating": 86, "potential": 90, "age": 31, "xp": 0, "trait": "Express Pace"},
        {"name": "Kwena Maphaka", "role": "Bowler", "rating": 78, "potential": 91, "age": 20, "xp": 0, "trait": "Young Prodigy"},
        {"name": "Mohsin Khan", "role": "Bowler", "rating": 81, "potential": 86, "age": 27, "xp": 0, "trait": "Bounce Specialist"},
        {"name": "M. Siddharth", "role": "Bowler", "rating": 76, "potential": 81, "age": 27, "xp": 0, "trait": "Economic Spin"},
        {"name": "Kartik Tyagi", "role": "Bowler", "rating": 77, "potential": 84, "age": 25, "xp": 0, "trait": "Express Pace"},
        {"name": "Mayank Markande", "role": "Bowler", "rating": 79, "potential": 82, "age": 28, "xp": 0, "trait": "Trickster"},
        {"name": "Lungi Ngidi", "role": "Bowler", "rating": 82, "potential": 84, "age": 30, "xp": 0, "trait": "Bounce Specialist"},
        {"name": "Adam Zampa", "role": "Bowler", "rating": 85, "potential": 86, "age": 34, "xp": 0, "trait": "Trickster"},
        {"name": "Manav Suthar", "role": "Bowler", "rating": 75, "potential": 83, "age": 23, "xp": 0, "trait": "Economic Spin"},
        {"name": "Vidwath Kaverappa", "role": "Bowler", "rating": 76, "potential": 82, "age": 27, "xp": 0, "trait": "Seam Presentation"},
        {"name": "Akash Singh", "role": "Bowler", "rating": 76, "potential": 81, "age": 24, "xp": 0, "trait": "Swing King"},
        {"name": "Simarjeet Singh", "role": "Bowler", "rating": 77, "potential": 81, "age": 28, "xp": 0, "trait": "Express Pace"},
        {"name": "Vaibhav Suryavanshi", "role": "Batsman", "rating": 74, "potential": 89, "age": 15, "xp": 0, "trait": "Young Prodigy"},
        {"name": "Ayush Mhatre", "role": "Batsman", "rating": 74, "potential": 88, "age": 19, "xp": 0, "trait": "Young Prodigy"},
        {"name": "Ramakrishna Ghosh", "role": "All-Rounder", "rating": 73, "potential": 80, "age": 25, "xp": 0, "trait": "Anchor"},
        {"name": "Prashant Veer", "role": "All-Rounder", "rating": 75, "potential": 81, "age": 24, "xp": 0, "trait": "Classicist"}
    ]
    while len(raw_players) < 200:
        raw_players.append({"name": f"Domestic Prospect #{len(raw_players)+1}", "role": "Bowler", "rating": 72, "potential": 78, "age": 22, "xp": 0, "trait": "Line & Length"})
    st.session_state.player_pool = raw_players[:200]

# Initialize Teams with budget and distribution
if "teams" not in st.session_state:
    team_list = ["Mumbai Elite", "Chennai Kings", "Bangalore Tech", "Delhi Capitals", "Kolkata Knights", "Gujarat Titans", "Rajasthan Royals", "Lucknow Super Giant"]
    st.session_state.teams = {}
    pool_copy = list(st.session_state.player_pool)
    random.shuffle(pool_copy)
    
    for idx, t_name in enumerate(team_list):
        squad = pool_copy[idx*25 : (idx+1)*25]
        st.session_state.teams[t_name] = {
            "name": t_name, "budget": 850000000, "squad": squad, "playing_11": squad[:11],
            "points": 0, "wins": 0, "losses": 0, "morale": 85, "training_mult": 1.0
        }

# --- GLOBAL ARCHITECTURE SAFEGUARDS ---
if "match_day" not in st.session_state:
    st.session_state.match_day = 1
if "news_flash" not in st.session_state:
    st.session_state.news_flash = "Welcome to the Pro-Manager Executive Center! Team structures updated."
if "user_team_key" not in st.session_state or st.session_state.user_team_key not in st.session_state.teams:
    st.session_state.user_team_key = "Mumbai Elite"
if "recent_scorecards" not in st.session_state:
    st.session_state.recent_scorecards = []

# ==========================================
# 🛠️ DEFENSIVE SCHEMA MIGRATION BLOCK (FIXES KEYERROR)
# ==========================================
for t_name, team_obj in st.session_state.teams.items():
    if "morale" not in team_obj:
        team_obj["morale"] = 85
    if "training_mult" not in team_obj:
        team_obj["training_mult"] = 1.0

# Safe assignment
user_team = st.session_state.teams[st.session_state.user_team_key]

# ==========================================
# 2. PROFESSIONAL 2-INNINGS MATCH SCORECARD ENGINE
# ==========================================
def run_detailed_match(t1, t2):
    # Simulate first innings (Team 1 Batting, Team 2 Bowling)
    t1_bat_perf = []
    t1_score = 0
    t1_wickets = 0
    for p in t1["playing_11"]:
        if p["role"] in ["Batsman", "Wicket-Keeper", "All-Rounder"]:
            runs = random.randint(10, 65) + int((p["rating"] - 80) * 0.8)
            balls = random.randint(8, 40)
        else:
            runs = random.randint(0, 15)
            balls = random.randint(2, 12)
        runs = max(0, runs)
        t1_score += runs
        if t1_wickets < 10 and random.random() > 0.3:
            t1_wickets += 1
            status = "c & b bowler"
        else:
            status = "not out"
        t1_bat_perf.append({"Player": p["name"], "Status": status, "Runs": runs, "Balls": balls})
    
    t2_bowl_perf = []
    bowlers = [p for p in t2["playing_11"] if p["role"] in ["Bowler", "All-Rounder"]]
    if not bowlers: bowlers = t2["playing_11"][:5]
    for b in bowlers:
        overs = random.choice([2, 3, 4])
        wkts = random.randint(0, 3)
        conceded = random.randint(15, 45) - int((b["rating"] - 80) * 0.4)
        conceded = max(5, conceded)
        t2_bowl_perf.append({"Bowler": b["name"], "Overs": overs, "Maidens": random.choice([0, 0, 0, 1]), "Runs": conceded, "Wickets": wkts, "Econ": round(conceded/overs, 2)})

    # Simulate second innings (Team 2 chasing Target)
    target = t1_score + 1
    t2_score = 0
    t2_wickets = 0
    t2_bat_perf = []
    for p in t2["playing_11"]:
        if t2_score >= target:
            status = "yet to bat"
            runs, balls = 0, 0
        else:
            if p["role"] in ["Batsman", "Wicket-Keeper", "All-Rounder"]:
                runs = random.randint(12, 70) + int((p["rating"] - 80) * 0.8)
                balls = random.randint(10, 42)
            else:
                runs = random.randint(0, 12)
                balls = random.randint(3, 10)
            runs = max(0, runs)
            t2_score += runs
            if t2_score < target and t2_wickets < 10 and random.random() > 0.3:
                t2_wickets += 1
                status = "caught"
            elif t2_score >= target:
                status = "not out"
            else:
                status = "not out"
        t2_bat_perf.append({"Player": p["name"], "Status": status, "Runs": runs, "Balls": balls})

    t1_bowl_perf = []
    bowlers1 = [p for p in t1["playing_11"] if p["role"] in ["Bowler", "All-Rounder"]]
    if not bowlers1: bowlers1 = t1["playing_11"][:5]
    for b in bowlers1:
        overs = random.choice([2, 3, 4])
        wkts = random.randint(0, 3)
        conceded = random.randint(15, 45) - int((b["rating"] - 80) * 0.4)
        conceded = max(5, conceded)
        t1_bowl_perf.append({"Bowler": b["name"], "Overs": overs, "Maidens": random.choice([0, 0, 1]), "Runs": conceded, "Wickets": wkts, "Econ": round(conceded/overs, 2)})

    return {
        "t1_name": t1["name"], "t2_name": t2["name"],
        "t1_score": f"{t1_score}/{t1_wickets}", "t2_score": f"{t2_score}/{t2_wickets}",
        "t1_bat": pd.DataFrame(t1_bat_perf), "t2_bowl": pd.DataFrame(t2_bowl_perf),
        "t2_bat": pd.DataFrame(t2_bat_perf), "t1_bowl": pd.DataFrame(t1_bowl_perf),
        "winner": t1["name"] if t1_score > t2_score else t2["name"]
    }

# ==========================================
# SIDEBAR CONTROL & PROFILE SWITCHER
# ==========================================
st.sidebar.title("🎮 Executive Control Deck")
selected_profile = st.sidebar.selectbox("Active Profile Franchise Switcher", options=list(st.session_state.teams.keys()), index=list(st.session_state.teams.keys()).index(st.session_state.user_team_key))
if selected_profile != st.session_state.user_team_key:
    st.session_state.user_team_key = selected_profile
    st.rerun()

st.sidebar.metric("Season Schedule Iteration", f"Day {st.session_state.match_day} / 14")
st.sidebar.metric("Franchise Balance Reserves", f"₹{user_team['budget']:,}")
st.sidebar.progressbar(user_team["morale"] / 100)
st.sidebar.caption(f"Current Team Morale Index: {user_team['morale']}%")

# Main Interface Tab Navigation
tab_media, tab_roster, tab_standings, tab_cap, tab_office = st.tabs([
    "📰 Media Newsroom", "🏋️ Roster Hub & Player Dev", "📊 Standings Ledger", "🧢 Cap Races", "💼 Executive Office Suite"
])

# ==========================================
# TAB 1: MEDIA NEWSROOM & PRESS WORKFLOWS
# ==========================================
with tab_media:
    st.subheader("📰 Central Media Wire Room")
    st.info(f"Breaking Broadcast: {st.session_state.news_flash}")
    
    st.markdown("---")
    st.markdown("### 🎙️ Post-Match Press Room Conference Interrogation")
    st.write("Journalists are requesting commentary regarding your strategies. Your answers alter training and squad motivation metrics.")
    
    q_choice = st.radio(
        "Press Inquiry: 'Your tactics are drawing scrutiny from analysts. How do you respond?'",
        [
            "1. 'The players need to take ownership of execution out there.' (Morale: -10, Training Tracker: 1.5x)",
            "2. 'I back this program implicitly; outside noise doesn't matter.' (Morale: +15, Training Tracker: 0.9x)",
            "3. 'We are continuously tweaking analytics dashboards to pivot.' (Morale: +2, Training Tracker: 1.1x)"
        ]
    )
    if st.button("Submit Executive Response Statement"):
        if "ownership" in q_choice:
            user_team["morale"] = max(10, user_team["morale"] - 10)
            user_team["training_mult"] = 1.5
            st.warning("Morale dropped, but tactical intensity spiked! Training multiplier is up to 1.5x.")
        elif "noise" in q_choice:
            user_team["morale"] = min(100, user_team["morale"] + 15)
            user_team["training_mult"] = 0.9
            st.success("The locker room feels safe. Morale increased, but developmental intensity eased.")
        else:
            user_team["morale"] = min(100, user_team["morale"] + 2)
            user_team["training_mult"] = 1.1
            st.info("Balanced data pivot logged.")

# ==========================================
# TAB 2: ROSTER HUB & TALENT REACTION ENGINE
# ==========================================
with tab_roster:
    st.subheader("📋 Team Squad Strategy & Active Development Tracker")
    
    col_lineup, col_plan = st.columns([1, 1])
    
    with col_lineup:
        st.markdown("#### ⚔️ Strategic XI Selection Blueprint")
        squad_names = [p["name"] for p in user_team["squad"]]
        current_xi_names = [p["name"] for p in user_team["playing_11"]]
        selected_xi = st.multiselect("Designate Playing XI Starters", options=squad_names, default=current_xi_names[:11])
        if len(selected_xi) == 11:
            user_team["playing_11"] = [p for p in user_team["squad"] if p["name"] in selected_xi]
        else:
            st.error("Roster requires precisely 11 functional starters.")

    with col_plan:
        st.markdown("#### 📈 Assigned Asset Development Layout")
        target_player_name = st.selectbox("Select Player to Direct Focus", options=squad_names)
        target_player = next(p for p in user_team["squad"] if p["name"] == target_player_name)
        
        dev_plan = st.selectbox("Assign Training Paradigm", ["Standard Recovery Balance", "Intensive Power Work", "Tactical Variant Drilling"])
        st.caption(f"Currently active: **{dev_plan}** on **{target_player['name']}** (OVR: {target_player['rating']} | Potential Ceiling: {target_player['potential']})")

    st.markdown("---")
    st.markdown("### 🏃 Full Active Roster Matrix")
    roster_df = pd.DataFrame(user_team["squad"])
    st.dataframe(roster_df[["name", "role", "rating", "potential", "age", "xp", "trait"]], use_container_width=True)

# ==========================================
# TAB 3: STANDINGS & HISTORIC SCORECARDS
# ==========================================
with tab_standings:
    st.subheader("📊 Dynamic League Standings Board")
    standings_data = [{"Franchise Block": t["name"], "Points Ledger": t["points"], "Wins": t["wins"], "Losses": t["losses"], "Morale Status": f"{t.get('morale', 85)}%"} for t in st.session_state.teams.values()]
    st.table(pd.DataFrame(standings_data).sort_values(by="Points Ledger", ascending=False))
    
    if st.session_state.recent_scorecards:
        st.markdown("---")
        st.subheader("🏏 Live Arena Dual-Innings Scorecard Report")
        latest = st.session_state.recent_scorecards[-1]
        
        st.markdown(f"### {latest['t1_name']} vs {latest['t2_name']}")
        st.write(f"**Outcome Verdict:** {latest['winner']} Wins! | **Scorelines:** {latest['t1_name']}: {latest['t1_score']} | {latest['t2_name']}: {latest['t2_score']}")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**{latest['t1_name']} Batting**")
            st.dataframe(latest['t1_bat'], hide_index=True)
            st.markdown(f"**{latest['t2_name']} Bowling Matrix**")
            st.dataframe(latest['t2_bowl'], hide_index=True)
        with c2:
            st.markdown(f"**{latest['t2_name']} Batting**")
            st.dataframe(latest['t2_bat'], hide_index=True)
            st.markdown(f"**{latest['t1_name']} Bowling Matrix**")
            st.dataframe(latest['t1_bowl'], hide_index=True)

# ==========================================
# TAB 4: CAP RACES
# ==========================================
with tab_cap:
    st.subheader("🧢 Global League Leader Cap Race Standings")
    pool_records = []
    for t in st.session_state.teams.values():
        for p in t["squad"]:
            pool_records.append({"Player": p["name"], "Franchise Assignment": t["name"], "OVR Profile": p["rating"], "Potential": p["potential"], "Trait": p["trait"]})
    st.dataframe(pd.DataFrame(pool_records).sort_values(by="OVR Profile", ascending=False).head(25), use_container_width=True)

# ==========================================
# TAB 5: OFFICE EXECUTIVE COMMAND & PROGRESSION
# ==========================================
with tab_office:
    st.subheader("💼 Franchise Office Operations")
    
    col_act, col_trade = st.columns(2)
    with col_act:
        st.markdown("#### 📣 Morale Activation Interventions")
        if st.button("Fund Franchise Team Dinner Activation (Cost: ₹10,000,000)"):
            if user_team["budget"] >= 10000000:
                user_team["budget"] -= 10000000
                user_team["morale"] = min(100, user_team["morale"] + 15)
                st.success("Locker room activation complete! Morale scaled +15.")
            else:
                st.error("Insufficient asset liquidity.")

    with col_trade:
        st.markdown("#### 🔄 Mid-Season Player Asset Trade Window")
        st.write("Swap roster options across available teams.")
        trade_partner_key = st.selectbox("Target Exchange Team", [t for t in st.session_state.teams if t != st.session_state.user_team_key])
        partner_team = st.session_state.teams[trade_partner_key]
        
        my_p = st.selectbox("Release My Player Portfolio", [p["name"] for p in user_team["squad"]])
        their_p = st.selectbox("Acquire Their Target Player", [p["name"] for p in partner_team["squad"]])
        
        if st.button("Execute Binding Trade Deal"):
            p1 = next(p for p in user_team["squad"] if p["name"] == my_p)
            p2 = next(p for p in partner_team["squad"] if p["name"] == their_p)
            
            user_team["squad"].remove(p1)
            partner_team["squad"].remove(p2)
            user_team["squad"].append(p2)
            partner_team["squad"].append(p1)
            
            if p1 in user_team["playing_11"]: user_team["playing_11"].remove(p1); user_team["playing_11"].append(p2)
            if p2 in partner_team["playing_11"]: partner_team["playing_11"].remove(p2); partner_team["playing_11"].append(p1)
            
            st.success(f"Trade complete! {p1['name']} swapped for {p2['name']}.")
            st.rerun()

    st.markdown("---")
    if st.button("⚡ Fast-Simulate Competitive Matchday & Run Progressions", use_container_width=True):
        all_keys = list(st.session_state.teams.keys())
        random.shuffle(all_keys)
        
        for idx in range(0, len(all_keys), 2):
            t1 = st.session_state.teams[all_keys[idx]]
            t2 = st.session_state.teams[all_keys[idx+1]]
            
            card = run_detailed_match(t1, t2)
            st.session_state.recent_scorecards.append(card)
            
            if card["winner"] == t1["name"]:
                t1["points"] += 2; t1["wins"] += 1; t1["morale"] = min(100, t1["morale"] + 4)
                t2["losses"] += 1; t2["morale"] = max(10, t2["morale"] - 6)
            else:
                t2["points"] += 2; t2["wins"] += 1; t2["morale"] = min(100, t2["morale"] + 4)
                t1["losses"] += 1; t1["morale"] = max(10, t1["morale"] - 6)

        for t in st.session_state.teams.values():
            for p in t["squad"]:
                p["xp"] += int(random.randint(15, 40) * t.get("training_mult", 1.0))
                if p["xp"] >= 100:
                    p["xp"] = 0
                    if p["age"] < 33:
                        if p["rating"] < p["potential"]:
                            p["rating"] += 1
                    else:
                        p["rating"] -= 1

        st.session_state.match_day += 1
        
        if st.session_state.match_day > 14:
            st.session_state.match_day = 1
            for t in st.session_state.teams.values():
                t["points"] = 0; t["wins"] = 0; t["losses"] = 0
            st.session_state.news_flash = "The season has concluded! Regression curves calculated and schedules reset for the new calendar tier."
        else:
            st.session_state.news_flash = f"Match Day {st.session_state.match_day - 1} complete. View the Scorecard tab for box metrics!"
            
        st.rerun()
