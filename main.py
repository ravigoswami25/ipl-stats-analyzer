# main.py — testing models
from analyzer.models import Player, Match, Team

# ── Test Player ───────────────────────────────────────
print("=== Testing Player Class ===")

virat = Player(
    id=1, name="Virat Kohli", team="RCB",
    role="Batsman", matches=237, runs=7263,
    highest_score=113, average=37.25,
    strike_rate=130.02, centuries=7,
    fifties=50, wickets=4, economy=8.5
)

print(virat)
print(repr(virat))
print(f"Runs per match: {virat.get_runs_lpa()}")
print(f"Is batsman: {virat.is_batsman()}")
print(f"Is all rounder: {virat.is_all_rounder()}")
print(f"Rating: {virat.get_performance_rating()}")

data = {
    "id": 2, "name": "MS Dhoni", "team": "CSK",
    "role": "Wicket-Keeper", "matches": 250,
    "runs": 5243, "highest_score": 84,
    "average": 39.42, "strike_rate": 135.92,
    "centuries": 0, "fifties": 24,
    "wickets": 0, "economy": 0
}
dhoni = Player.from_dict(data)
print(f"\nFrom dict: {dhoni}")
print(f"To dict: {dhoni.to_dict()}")

players = [virat, dhoni]
sorted_players = sorted(players)
print(f"\nSorted by runs: {[p.name for p in sorted_players]}")

# ── Test Match ────────────────────────────────────────
print("\n=== Testing Match Class ===")

match = Match.from_dict({
    "id": 1, "season": 2023,
    "team1": "RCB", "team2": "CSK",  # ✅ RCB is playing now
    "winner": "RCB",                  # ✅ RCB won
    "margin": "8 runs",
    "venue": "Bangalore",
    "player_of_match": "Virat Kohli"  # ✅ makes sense now
})

print(match)
print(f"Loser: {match.get_loser()}")
print(f"RCB involved: {match.involves_team('RCB')}")
print(f"RCB won: {match.is_won_by('RCB')}")

# ── Test Team ─────────────────────────────────────────
print("\n=== Testing Team Class ===")

rcb = Team("RCB")
rcb.add_player(virat)
rcb.add_match(match)               # ✅ RCB vs CSK match

print(rcb)
print(f"Top scorer: {rcb.get_top_scorer().name}")
print(f"Win rate: {rcb.get_win_rate()}%")