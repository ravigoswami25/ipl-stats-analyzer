# analyzer/display.py
# Responsibility: All print/display functions — UI of the CLI

# ============================================================
# HELPERS
# ============================================================

def print_divider(char: str = "=", length: int = 55) -> None:
    """Print a divider line."""
    print(char * length)


def print_header(title: str) -> None:
    """Print a formatted section header."""
    print_divider()
    print(f"  🏏 {title}")
    print_divider()


def print_no_data(message: str = "No data found") -> None:
    """Print when no results found."""
    print(f"  ⚠️  {message}")


# ============================================================
# PLAYER DISPLAY
# ============================================================

def display_player_card(player: dict) -> None:
    """
    Display full profile card for a single player.
    """
    print_divider()
    print(f"  👤 {player['name']} — {player['team']}")
    print_divider("-")
    print(f"  Role         : {player['role']}")
    print(f"  Matches      : {player['matches']}")
    print(f"  Runs         : {player['runs']:,}")
    print(f"  Highest Score: {player['highest_score']}")
    print(f"  Average      : {player['average']}")
    print(f"  Strike Rate  : {player['strike_rate']}")
    print(f"  Centuries    : {player['centuries']}")
    print(f"  Fifties      : {player['fifties']}")

    if player["wickets"] > 0:
        print(f"  Wickets      : {player['wickets']}")
        print(f"  Economy      : {player['economy']}")

    print_divider()


def display_top_scorers(players: list[dict]) -> None:
    """
    Display top scorers in a ranked table.
    """
    print_header("TOP RUN SCORERS")

    if not players:
        print_no_data("No batsmen found")
        return

    print(f"  {'Rank':<5} {'Name':<20} {'Team':<6} {'Runs':>6} {'Avg':>7} {'SR':>7}")
    print_divider("-")

    for rank, player in enumerate(players, 1):
        print(
            f"  {rank:<5}"
            f" {player['name']:<20}"
            f" {player['team']:<6}"
            f" {player['runs']:>6,}"
            f" {player['average']:>7.2f}"
            f" {player['strike_rate']:>7.2f}"
        )
    print_divider()


def display_top_wicket_takers(players: list[dict]) -> None:
    """
    Display top wicket takers in a ranked table.
    """
    print_header("TOP WICKET TAKERS")

    if not players:
        print_no_data("No bowlers found")
        return

    print(f"  {'Rank':<5} {'Name':<20} {'Team':<6} {'Wkts':>5} {'Eco':>6}")
    print_divider("-")

    for rank, player in enumerate(players, 1):
        print(
            f"  {rank:<5}"
            f" {player['name']:<20}"
            f" {player['team']:<6}"
            f" {player['wickets']:>5}"
            f" {player['economy']:>6.2f}"
        )
    print_divider()


def display_strike_rates(players: list[dict]) -> None:
    """
    Display players ranked by strike rate.
    """
    print_header("BEST STRIKE RATES")

    if not players:
        print_no_data()
        return

    print(f"  {'Rank':<5} {'Name':<20} {'Team':<6} {'SR':>7} {'Runs':>6}")
    print_divider("-")

    for rank, player in enumerate(players, 1):
        print(
            f"  {rank:<5}"
            f" {player['name']:<20}"
            f" {player['team']:<6}"
            f" {player['strike_rate']:>7.2f}"
            f" {player['runs']:>6,}"
        )
    print_divider()


def display_team_players(players: list[dict], team: str) -> None:
    """
    Display all players from a team.
    """
    print_header(f"{team} — SQUAD")

    if not players:
        print_no_data(f"No players found for {team}")
        return

    print(f"  {'Name':<20} {'Role':<15} {'Runs':>6} {'Wkts':>5}")
    print_divider("-")

    for player in players:
        print(
            f"  {player['name']:<20}"
            f" {player['role']:<15}"
            f" {player['runs']:>6,}"
            f" {player['wickets']:>5}"
        )
    print_divider()


def display_all_rounders(players: list[dict]) -> None:
    """
    Display all-rounders with both batting and bowling stats.
    """
    print_header("ALL ROUNDERS")

    if not players:
        print_no_data("No all-rounders found")
        return

    print(f"  {'Name':<20} {'Team':<6} {'Runs':>6} {'Wkts':>5}")
    print_divider("-")

    for player in players:
        print(
            f"  {player['name']:<20}"
            f" {player['team']:<6}"
            f" {player['runs']:>6,}"
            f" {player['wickets']:>5}"
        )
    print_divider()


# ============================================================
# TEAM DISPLAY
# ============================================================

def display_team_wins(wins: dict) -> None:
    """
    Display team wins leaderboard.
    """
    print_header("TEAM WINS LEADERBOARD")

    sorted_wins = sorted(wins.items(), key=lambda x: x[1], reverse=True)

    print(f"  {'Rank':<5} {'Team':<8} {'Wins':>5}")
    print_divider("-")

    for rank, (team, win_count) in enumerate(sorted_wins, 1):
        bar = "█" * win_count           # visual bar chart!
        print(f"  {rank:<5} {team:<8} {win_count:>5}  {bar}")

    print_divider()


def display_head_to_head(result: dict, team1: str, team2: str) -> None:
    """
    Display head to head record between two teams.
    """
    print_header(f"HEAD TO HEAD: {team1} vs {team2}")
    print(f"  Total Matches : {result['total_matches']}")
    print(f"  {team1} Wins   : {result[f'{team1}_wins']}")
    print(f"  {team2} Wins   : {result[f'{team2}_wins']}")

    print(f"\n  {'Season':<8} {'Winner':<8} {'Margin'}")
    print_divider("-")

    for match in result["matches"]:
        print(
            f"  {match['season']:<8}"
            f" {match['winner']:<8}"
            f" {match['margin']}"
        )
    print_divider()


# ============================================================
# MATCH DISPLAY
# ============================================================

def display_matches(matches: list[dict], title: str = "MATCHES") -> None:
    """
    Display a list of matches in table format.
    """
    print_header(title)

    if not matches:
        print_no_data("No matches found")
        return

    print(f"  {'Season':<8} {'Teams':<22} {'Winner':<8} {'Margin'}")
    print_divider("-")

    for match in matches:
        teams = f"{match['team1']} vs {match['team2']}"
        print(
            f"  {match['season']:<8}"
            f" {teams:<22}"
            f" {match['winner']:<8}"
            f" {match['margin']}"
        )
    print_divider()


def display_player_of_match(counts: dict) -> None:
    """
    Display Player of Match award counts.
    """
    print_header("PLAYER OF MATCH AWARDS")
    print(f"  {'Name':<25} {'Awards':>6}")
    print_divider("-")

    for player, count in counts.items():
        stars = "⭐" * count
        print(f"  {player:<25} {count:>6}  {stars}")

    print_divider()


# ============================================================
# SUMMARY DISPLAY
# ============================================================

def display_summary(summary: dict) -> None:
    """
    Display full tournament summary.
    """
    print_header("IPL STATS — FULL SUMMARY")
    print(f"  Total Players  : {summary['total_players']}")
    print(f"  Total Matches  : {summary['total_matches']}")
    print(f"  Teams          : {', '.join(summary['teams'])}")
    print(f"  Seasons        : {', '.join(str(s) for s in summary['seasons_covered'])}")

    print_divider("-")
    print(f"  🏏 Top Scorer  : {summary['top_scorer']['name']}"
          f" ({summary['top_scorer']['team']})"
          f" — {summary['top_scorer']['runs']:,} runs")

    print(f"  🎳 Top Bowler  : {summary['top_wicket_taker']['name']}"
          f" ({summary['top_wicket_taker']['team']})"
          f" — {summary['top_wicket_taker']['wickets']} wickets")

    print(f"  🏆 Most Wins   : {summary['most_wins']['team']}"
          f" — {summary['most_wins']['wins']} wins")

    print(f"  ⭐ Best Player : {summary['most_player_of_match']['player']}"
          f" — {summary['most_player_of_match']['count']} awards")

    print_divider()