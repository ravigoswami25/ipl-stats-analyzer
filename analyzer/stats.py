# analyzer/stats.py
# Responsibility: All IPL stat calculations

# ============================================================
# PLAYER STATS
# ============================================================

def get_top_scorers(players: list[dict], top_n: int = 5) -> list[dict]:
    """
    Return top N batsmen sorted by total runs.
    """
    batsmen = [p for p in players if p["runs"] > 0]
    sorted_batsmen = sorted(batsmen, key=lambda p: p["runs"], reverse=True)
    return sorted_batsmen[:top_n]


def get_top_wicket_takers(players: list[dict], top_n: int = 5) -> list[dict]:
    """
    Return top N bowlers sorted by wickets.
    """
    bowlers = [p for p in players if p["wickets"] > 0]
    sorted_bowlers = sorted(bowlers, key=lambda p: p["wickets"], reverse=True)
    return sorted_bowlers[:top_n]


def get_best_strike_rates(players: list[dict], min_runs: int = 500) -> list[dict]:
    """
    Return players with best strike rate (min runs filter to avoid noise).
    """
    qualified = [p for p in players if p["runs"] >= min_runs]
    return sorted(qualified, key=lambda p: p["strike_rate"], reverse=True)


def get_best_economy(players: list[dict], min_wickets: int = 10) -> list[dict]:
    """
    Return bowlers with best economy rate (lower is better).
    """
    qualified = [p for p in players if p["wickets"] >= min_wickets]
    return sorted(qualified, key=lambda p: p["economy"])


def get_players_by_team(players: list[dict], team: str) -> list[dict]:
    """
    Return all players from a specific team.
    """
    return [p for p in players if p["team"].upper() == team.upper()]


def get_players_by_role(players: list[dict], role: str) -> list[dict]:
    """
    Return all players with a specific role.
    """
    return [p for p in players if p["role"].lower() == role.lower()]


def get_player_by_name(players: list[dict], name: str) -> dict | None:
    """
    Find a single player by name (case insensitive).
    Returns None if not found.
    """
    for player in players:
        if player["name"].lower() == name.lower():
            return player
    return None


def get_all_rounders(players: list[dict]) -> list[dict]:
    """
    Return players who have both runs > 500 and wickets > 20.
    """
    return [
        p for p in players
        if p["runs"] > 500 and p["wickets"] > 20
    ]


# ============================================================
# TEAM STATS
# ============================================================

def get_all_teams(players: list[dict]) -> list[str]:
    """
    Return sorted list of unique team names.
    """
    teams = {p["team"] for p in players}    # set — auto removes duplicates
    return sorted(teams)


def get_team_wins(matches: list[dict]) -> dict:
    """
    Return dict of team → total wins.
    Example: {'CSK': 3, 'MI': 3, 'RCB': 2, 'SRH': 1}
    """
    wins = {}
    for match in matches:
        winner = match["winner"]
        if winner in wins:
            wins[winner] += 1
        else:
            wins[winner] = 1
    return wins


def get_most_wins(matches: list[dict]) -> tuple:
    """
    Return (team_name, win_count) for team with most wins.
    """
    wins = get_team_wins(matches)
    best_team = max(wins, key=lambda team: wins[team])
    return best_team, wins[best_team]


def get_team_matches(matches: list[dict], team: str) -> list[dict]:
    """
    Return all matches where the team played (win or loss).
    """
    return [
        m for m in matches
        if m["team1"].upper() == team.upper()
        or m["team2"].upper() == team.upper()
    ]


def get_head_to_head(matches: list[dict], team1: str, team2: str) -> dict:
    """
    Return head to head record between two teams.
    """
    h2h_matches = [
        m for m in matches
        if (m["team1"].upper() == team1.upper() and m["team2"].upper() == team2.upper())
        or (m["team1"].upper() == team2.upper() and m["team2"].upper() == team1.upper())
    ]

    team1_wins = sum(1 for m in h2h_matches if m["winner"].upper() == team1.upper())
    team2_wins = sum(1 for m in h2h_matches if m["winner"].upper() == team2.upper())

    return {
        "total_matches": len(h2h_matches),
        f"{team1}_wins": team1_wins,
        f"{team2}_wins": team2_wins,
        "matches": h2h_matches
    }


# ============================================================
# MATCH STATS
# ============================================================

def get_matches_by_season(matches: list[dict], season: int) -> list[dict]:
    """
    Return all matches from a specific season/year.
    """
    return [m for m in matches if m["season"] == season]


def get_player_of_match_count(matches: list[dict]) -> dict:
    """
    Return dict of player → number of Player of Match awards.
    """
    counts = {}
    for match in matches:
        player = match["player_of_match"]
        counts[player] = counts.get(player, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


def get_all_seasons(matches: list[dict]) -> list[int]:
    """
    Return sorted list of unique seasons.
    """
    return sorted({m["season"] for m in matches})


# ============================================================
# SUMMARY STATS
# ============================================================

def generate_summary(players: list[dict], matches: list[dict]) -> dict:
    """
    Generate a complete summary dict for saving to results.json
    """
    wins = get_team_wins(matches)
    best_team, best_wins = get_most_wins(matches)
    top_scorer = get_top_scorers(players, top_n=1)[0]
    top_wickets = get_top_wicket_takers(players, top_n=1)[0]
    pom_counts = get_player_of_match_count(matches)
    best_pom = list(pom_counts.keys())[0]

    return {
        "total_players": len(players),
        "total_matches": len(matches),
        "teams": get_all_teams(players),
        "seasons_covered": get_all_seasons(matches),
        "top_scorer": {
            "name": top_scorer["name"],
            "team": top_scorer["team"],
            "runs": top_scorer["runs"]
        },
        "top_wicket_taker": {
            "name": top_wickets["name"],
            "team": top_wickets["team"],
            "wickets": top_wickets["wickets"]
        },
        "team_wins": wins,
        "most_wins": {"team": best_team, "wins": best_wins},
        "most_player_of_match": {"player": best_pom, "count": pom_counts[best_pom]}
    }