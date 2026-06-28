import random

import streamlit as st


TEAMS = [
    "Chennai Super Kings",
    "Delhi Capitals",
    "Gujarat Titans",
    "Kolkata Knight Riders",
    "Lucknow Super Giants",
    "Mumbai Indians",
    "Punjab Kings",
    "Rajasthan Royals",
    "Royal Challengers Bengaluru",
    "Sunrisers Hyderabad",
]

BOT_PERSONALITIES = [
    {"name": "Aggressive Finisher", "min_value": 0.92, "max_squad": 9, "raise_bias": 0.65},
    {"name": "Data-Driven Buyer", "min_value": 1.02, "max_squad": 8, "raise_bias": 0.5},
    {"name": "Budget Hawk", "min_value": 0.84, "max_squad": 8, "raise_bias": 0.35},
    {"name": "Youth Scout", "min_value": 0.9, "max_squad": 10, "raise_bias": 0.52},
    {"name": "All-Rounder Collector", "min_value": 0.95, "max_squad": 9, "raise_bias": 0.55},
]

PLAYERS = [
    {"name": "Virat Kohli", "role": "Batter", "base_price": 14, "rating": 95},
    {"name": "Jasprit Bumrah", "role": "Bowler", "base_price": 13, "rating": 94},
    {"name": "Rashid Khan", "role": "Bowler", "base_price": 12, "rating": 92},
    {"name": "Jos Buttler", "role": "Wicketkeeper", "base_price": 12, "rating": 91},
    {"name": "Shubman Gill", "role": "Batter", "base_price": 11, "rating": 90},
    {"name": "Suryakumar Yadav", "role": "Batter", "base_price": 11, "rating": 90},
    {"name": "Ruturaj Gaikwad", "role": "Batter", "base_price": 10, "rating": 88},
    {"name": "KL Rahul", "role": "Wicketkeeper", "base_price": 10, "rating": 88},
    {"name": "Hardik Pandya", "role": "All-Rounder", "base_price": 10, "rating": 87},
    {"name": "Andre Russell", "role": "All-Rounder", "base_price": 9, "rating": 87},
    {"name": "Trent Boult", "role": "Bowler", "base_price": 9, "rating": 86},
    {"name": "Rinku Singh", "role": "Batter", "base_price": 8, "rating": 84},
    {"name": "Ishan Kishan", "role": "Wicketkeeper", "base_price": 8, "rating": 84},
    {"name": "Yashasvi Jaiswal", "role": "Batter", "base_price": 8, "rating": 85},
    {"name": "Axar Patel", "role": "All-Rounder", "base_price": 7, "rating": 83},
    {"name": "Mohammed Siraj", "role": "Bowler", "base_price": 7, "rating": 82},
    {"name": "Arshdeep Singh", "role": "Bowler", "base_price": 6, "rating": 80},
    {"name": "Heinrich Klaasen", "role": "Wicketkeeper", "base_price": 7, "rating": 83},
    {"name": "Ravindra Jadeja", "role": "All-Rounder", "base_price": 8, "rating": 85},
    {"name": "Kuldeep Yadav", "role": "Bowler", "base_price": 7, "rating": 82},
]

BID_STEP = 1
MAX_BID_BUDGET_SHARE = 0.28
RATING_TO_BID_DIVISOR = 6
BASE_TEAM_STRENGTH = 55
MATCH_VARIANCE_RANGE = 15
SUPER_OVER_THRESHOLD = 0.25
NRR_DIVISOR = 20
TOP_PLAYERS_COUNT = 5


def player_pool():
    pool = [dict(player) for player in PLAYERS]
    random.shuffle(pool)
    return pool


def build_schedule(team_ids):
    rotation = list(team_ids)
    rounds = []
    for _ in range(len(rotation) - 1):
        pairings = []
        for idx in range(len(rotation) // 2):
            pairings.append((rotation[idx], rotation[-idx - 1]))
        rounds.append(pairings)
        rotation = [rotation[0], rotation[-1], *rotation[1:-1]]
    return rounds


def initialise_league(owners):
    teams = []
    bot_index = 0
    for team_id, franchise in enumerate(TEAMS):
        owner = owners.get(franchise, "").strip()
        is_human = bool(owner)
        personality = None if is_human else BOT_PERSONALITIES[bot_index % len(BOT_PERSONALITIES)]
        bot_number = bot_index + 1
        if not is_human:
            bot_index += 1
        teams.append(
            {
                "id": team_id,
                "name": franchise,
                "owner": owner or f"Bot GM {bot_number}",
                "is_human": is_human,
                "personality": personality,
                "budget": 100,
                "squad": [],
            }
        )

    st.session_state.teams = teams
    st.session_state.players = player_pool()
    st.session_state.auction_log = []
    st.session_state.auction = {}
    st.session_state.pending_dilemma = None
    st.session_state.team_boosts = {}
    st.session_state.injuries = []
    st.session_state.match_history = []
    st.session_state.schedule = build_schedule([team["id"] for team in teams])
    st.session_state.standings = {
        team["id"]: {"played": 0, "wins": 0, "losses": 0, "points": 0, "nrr": 0.0}
        for team in teams
    }
    nominate_next_player()


def team_lookup(team_id):
    return next(team for team in st.session_state.teams if team["id"] == team_id)


def current_player():
    return st.session_state.auction.get("player")


def max_bid_for_team(team):
    personality = team["personality"] or {"min_value": 1.0}
    squad_factor = 1 if len(team["squad"]) < personality.get("max_squad", 9) else 0.92
    return (
        max(team["budget"], 0) * MAX_BID_BUDGET_SHARE * squad_factor
        + current_player()["rating"] * personality["min_value"] / RATING_TO_BID_DIVISOR
    )


def find_next_bidder():
    auction = st.session_state.auction
    team_count = len(st.session_state.teams)
    for step in range(1, team_count + 1):
        candidate_index = (auction["current_index"] + step) % team_count
        candidate = st.session_state.teams[candidate_index]
        if candidate["id"] == auction["leading_team"]:
            continue
        needed = auction["current_bid"] if auction["leading_team"] is None else auction["current_bid"] + BID_STEP
        if candidate["id"] not in auction["passed"] and candidate["budget"] >= needed:
            auction["current_index"] = candidate_index
            return True
    resolve_current_player()
    return False


def nominate_next_player():
    if not st.session_state.players:
        st.session_state.auction = {"complete": True}
        return
    player = st.session_state.players.pop(0)
    st.session_state.auction = {
        "player": player,
        "current_bid": player["base_price"],
        "leading_team": None,
        "current_index": 0,
        "passed": set(),
    }
    if not find_next_bidder():
        st.rerun()


def resolve_current_player():
    auction = st.session_state.auction
    player = auction["player"]
    if auction["leading_team"] is None:
        st.session_state.auction_log.append(f"{player['name']} went unsold at ₹{player['base_price']} Cr.")
        nominate_next_player()
        return

    winner = team_lookup(auction["leading_team"])
    winner["budget"] -= auction["current_bid"]
    winner["squad"].append(player)
    st.session_state.auction_log.append(
        f"{winner['name']} signed {player['name']} for ₹{auction['current_bid']} Cr."
    )
    nominate_next_player()


def place_bid(team_id, bid_value):
    st.session_state.auction["leading_team"] = team_id
    st.session_state.auction["current_bid"] = bid_value
    st.session_state.auction["passed"] = set()
    find_next_bidder()


def process_bots():
    while current_player() and not st.session_state.auction.get("complete"):
        auction = st.session_state.auction
        team = st.session_state.teams[auction["current_index"]]
        if team["is_human"]:
            break

        threshold = max_bid_for_team(team)
        next_bid = auction["current_bid"] if auction["leading_team"] is None else auction["current_bid"] + BID_STEP
        personality = team["personality"]
        wants_raise = next_bid <= threshold and random.random() <= personality["raise_bias"]
        if wants_raise:
            place_bid(
                team["id"],
                current_player()["base_price"] if auction["leading_team"] is None else auction["current_bid"] + BID_STEP,
            )
        else:
            auction["passed"].add(team["id"])
            if not find_next_bidder():
                break


def strongest_available_players(team):
    injured_names = {
        injury["player_name"]
        for injury in st.session_state.injuries
        if injury["team_id"] == team["id"] and injury["matchdays_left"] > 0
    }
    available = [player["rating"] for player in team["squad"] if player["name"] not in injured_names]
    top_ratings = sorted(available, reverse=True)[:TOP_PLAYERS_COUNT]
    if not top_ratings:
        return BASE_TEAM_STRENGTH
    return BASE_TEAM_STRENGTH + sum(top_ratings) / len(top_ratings)


def register_random_twist():
    roll = random.random()
    if roll < 0.4:
        candidates = [team for team in st.session_state.teams if team["squad"]]
        if not candidates:
            return None
        team = random.choice(candidates)
        player = random.choice(team["squad"])
        injury = {
            "team_id": team["id"],
            "team_name": team["name"],
            "player_name": player["name"],
            "matchdays_left": random.choice([1, 2]),
        }
        st.session_state.injuries.append(injury)
        return f"Injury twist: {player['name']} ({team['name']}) is unavailable for {injury['matchdays_left']} matchday(s)."
    if roll < 0.75:
        team = random.choice(st.session_state.teams)
        st.session_state.pending_dilemma = {
            "team_id": team["id"],
            "team_name": team["name"],
            "question": f"{team['name']} must decide whether to back youth or trust experience before the next game.",
            "options": [
                {"label": "Back youth", "effect": 6, "summary": "Youngsters are energised: +6 strength next matchday."},
                {"label": "Trust experience", "effect": 3, "summary": "Veterans steady the room: +3 strength next matchday."},
            ],
        }
        return f"Management dilemma: {team['name']} has a selection call to make."
    return "Quiet day: no major twist hit the league today."


def resolve_dilemma(option_index):
    dilemma = st.session_state.pending_dilemma
    option = dilemma["options"][option_index]
    boosts = st.session_state.team_boosts
    boosts[dilemma["team_id"]] = boosts.get(dilemma["team_id"], 0) + option["effect"]
    st.session_state.auction_log.append(
        f"{dilemma['team_name']} chose '{option['label']}' - {option['summary']}"
    )
    st.session_state.pending_dilemma = None


def simulate_matchday():
    day_index = len(st.session_state.match_history)
    if day_index >= len(st.session_state.schedule) or st.session_state.pending_dilemma:
        return

    twist = register_random_twist()
    if st.session_state.pending_dilemma:
        return

    results = []
    for home_id, away_id in st.session_state.schedule[day_index]:
        home_team = team_lookup(home_id)
        away_team = team_lookup(away_id)
        home_strength = strongest_available_players(home_team) + st.session_state.team_boosts.get(home_id, 0)
        away_strength = strongest_available_players(away_team) + st.session_state.team_boosts.get(away_id, 0)
        home_score = home_strength + random.uniform(-MATCH_VARIANCE_RANGE, MATCH_VARIANCE_RANGE)
        away_score = away_strength + random.uniform(-MATCH_VARIANCE_RANGE, MATCH_VARIANCE_RANGE)
        margin = abs(home_score - away_score)
        decided_in_super_over = False
        if abs(home_score - away_score) < SUPER_OVER_THRESHOLD:
            winner, loser = random.choice([(home_team, away_team), (away_team, home_team)])
            margin = max(margin, random.uniform(0.5, 3.0))
            decided_in_super_over = True
        else:
            winner, loser = (home_team, away_team) if home_score > away_score else (away_team, home_team)
        st.session_state.standings[winner["id"]]["wins"] += 1
        st.session_state.standings[winner["id"]]["points"] += 2
        st.session_state.standings[loser["id"]]["losses"] += 1
        for team_id, delta in ((winner["id"], margin / NRR_DIVISOR), (loser["id"], -margin / NRR_DIVISOR)):
            st.session_state.standings[team_id]["played"] += 1
            st.session_state.standings[team_id]["nrr"] += delta
        if decided_in_super_over:
            results.append(f"{winner['name']} edged {loser['name']} in a super over after a tie.")
        else:
            results.append(f"{winner['name']} beat {loser['name']} by {margin:.1f} simulation points.")

    st.session_state.match_history.append({"day": day_index + 1, "twist": twist, "results": results})
    st.session_state.team_boosts = {}
    for injury in st.session_state.injuries:
        injury["matchdays_left"] -= 1
    st.session_state.injuries = [injury for injury in st.session_state.injuries if injury["matchdays_left"] > 0]


def render_team_cards():
    for start in range(0, len(st.session_state.teams), 2):
        columns = st.columns(2)
        for offset, column in enumerate(columns):
            index = start + offset
            if index >= len(st.session_state.teams):
                continue
            team = st.session_state.teams[index]
            with column:
                caption = team["owner"] if team["is_human"] else team["personality"]["name"]
                st.markdown(f"### {team['name']}")
                st.caption(caption)
                st.metric("Budget", f"₹{team['budget']} Cr")
                st.write(f"Squad size: {len(team['squad'])}")
                if team["squad"]:
                    st.write(", ".join(player["name"] for player in team["squad"][-3:]))


st.set_page_config(page_title="IPL Auction and Season Simulator", layout="wide")
st.title("🏏 IPL Auction and Season Simulator")
st.write("Set up all 10 franchises, run a live Raise Bid/Pass auction, then simulate a twist-filled season.")

with st.sidebar:
    st.header("League Setup")
    owner_inputs = {}
    for franchise in TEAMS:
        owner_inputs[franchise] = st.text_input(
            f"{franchise} manager",
            value=st.session_state.get("owner_inputs", {}).get(franchise, ""),
            placeholder="Leave blank for bot control",
        )
    st.session_state.owner_inputs = owner_inputs
    human_count = sum(1 for owner in owner_inputs.values() if owner.strip())
    st.caption(f"Human-controlled teams: {human_count} | Bot teams: {10 - human_count}")
    if st.button("Start fresh auction", use_container_width=True):
        initialise_league(owner_inputs)
        st.rerun()

if "teams" not in st.session_state:
    st.info("Enter any human managers in the sidebar, leave the rest blank for dynamic bot personalities, then start the auction.")
    st.stop()

process_bots()

auction_tab, season_tab = st.tabs(["Live Auction", "Season Simulator"])

with auction_tab:
    if st.session_state.auction.get("complete"):
        st.success("Auction complete. Move to the Season Simulator tab to begin the campaign.")
    else:
        player = current_player()
        st.subheader("Live Auction - Option 1: Raise Bid or Pass")
        st.caption("The project brief specifically asked for the Option 1 bidding flow, so this screen focuses on Raise Bid/Pass.")
        left, right = st.columns([1.2, 1])
        with left:
            st.markdown(f"## {player['name']}")
            st.write(f"**Role:** {player['role']}")
            st.write(f"**Base Price:** ₹{player['base_price']} Cr")
            st.progress(min(player["rating"], 100) / 100, text=f"Player card rating: {player['rating']}")
            lead_name = "No bids yet"
            if st.session_state.auction["leading_team"] is not None:
                lead_name = team_lookup(st.session_state.auction["leading_team"])["name"]
            st.info(f"Current bid: ₹{st.session_state.auction['current_bid']} Cr | Leader: {lead_name}")
        with right:
            active_team = st.session_state.teams[st.session_state.auction["current_index"]]
            st.markdown(f"### On the clock: {active_team['name']}")
            st.write(active_team["owner"] if active_team["is_human"] else active_team["personality"]["name"])
            next_bid = (
                st.session_state.auction["current_bid"]
                if st.session_state.auction["leading_team"] is None
                else st.session_state.auction["current_bid"] + BID_STEP
            )
            if active_team["is_human"]:
                raise_col, pass_col = st.columns(2)
                with raise_col:
                    if st.button(f"Raise to ₹{next_bid} Cr", use_container_width=True):
                        place_bid(active_team["id"], next_bid)
                        st.rerun()
                with pass_col:
                    if st.button("Pass", use_container_width=True):
                        st.session_state.auction["passed"].add(active_team["id"])
                        find_next_bidder()
                        st.rerun()
            else:
                st.warning("Bots are processing this turn automatically.")

        st.divider()
        render_team_cards()
        st.subheader("Auction Feed")
        recent_updates = list(reversed(st.session_state.auction_log[-8:]))
        if recent_updates:
            for entry in recent_updates:
                st.write(f"- {entry}")
        else:
            st.write("No completed sales yet.")

with season_tab:
    st.subheader("Match Day Simulator")
    if st.session_state.pending_dilemma:
        dilemma = st.session_state.pending_dilemma
        st.warning(dilemma["question"])
        option_columns = st.columns(2)
        for idx, option_column in enumerate(option_columns):
            option = dilemma["options"][idx]
            with option_column:
                if st.button(option["label"], key=f"dilemma-{idx}", use_container_width=True):
                    resolve_dilemma(idx)
                    st.rerun()
                st.caption(option["summary"])

    if st.button("Simulate next matchday", disabled=bool(st.session_state.pending_dilemma)):
        simulate_matchday()
        st.rerun()

    standings_rows = []
    for team in st.session_state.teams:
        stats = st.session_state.standings[team["id"]]
        standings_rows.append(
            {
                "Team": team["name"],
                "P": stats["played"],
                "W": stats["wins"],
                "L": stats["losses"],
                "Pts": stats["points"],
                "NRR": round(stats["nrr"], 2),
            }
        )
    standings_rows.sort(key=lambda row: (row["Pts"], row["NRR"]), reverse=True)
    st.dataframe(standings_rows, use_container_width=True, hide_index=True)

    if st.session_state.injuries:
        st.markdown("### Injury Report")
        for injury in st.session_state.injuries:
            st.write(f"- {injury['player_name']} ({injury['team_name']}) - {injury['matchdays_left']} matchday(s) left")

    if st.session_state.match_history:
        st.markdown("### Matchday Recap")
        for day in reversed(st.session_state.match_history[-3:]):
            st.markdown(f"**Matchday {day['day']}**")
            st.write(day["twist"])
            for result in day["results"]:
                st.write(f"- {result}")
