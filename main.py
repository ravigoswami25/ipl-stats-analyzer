# main.py
# Responsibility: Interactive CLI menu — entry point of the app

from analyzer.loader import load_players, load_matches, save_results
from analyzer.stats import (
    get_top_scorers, get_top_wicket_takers,
    get_best_strike_rates, get_best_economy,
    get_players_by_team, get_players_by_role,
    get_player_by_name, get_all_rounders,
    get_team_wins, get_most_wins,
    get_team_matches, get_head_to_head,
    get_matches_by_season, get_player_of_match_count,
    get_all_seasons, get_all_teams, generate_summary
)
from analyzer.display import (
    display_top_scorers, display_top_wicket_takers,
    display_strike_rates, display_team_wins,
    display_player_card, display_team_players,
    display_player_of_match, display_summary,
    display_all_rounders, display_matches,
    display_head_to_head, print_header, print_divider
)


# ============================================================
# MENU SECTIONS
# ============================================================

def show_main_menu() -> None:
    """Print the main menu."""
    print_divider()
    print("  🏏 IPL STATS ANALYZER")
    print_divider()
    print("  1. Player Stats")
    print("  2. Team Stats")
    print("  3. Match Stats")
    print("  4. Full Summary")
    print("  5. Save Results to JSON")
    print("  0. Exit")
    print_divider()


def show_player_menu() -> None:
    """Print player submenu."""
    print_divider("-")
    print("  PLAYER STATS")
    print_divider("-")
    print("  1. Top Run Scorers")
    print("  2. Top Wicket Takers")
    print("  3. Best Strike Rates")
    print("  4. Best Economy Rates")
    print("  5. Search Player by Name")
    print("  6. View Team Squad")
    print("  7. View All Rounders")
    print("  0. Back to Main Menu")
    print_divider("-")


def show_team_menu() -> None:
    """Print team submenu."""
    print_divider("-")
    print("  TEAM STATS")
    print_divider("-")
    print("  1. Team Wins Leaderboard")
    print("  2. Most Successful Team")
    print("  3. Head to Head")
    print("  0. Back to Main Menu")
    print_divider("-")


def show_match_menu() -> None:
    """Print match submenu."""
    print_divider("-")
    print("  MATCH STATS")
    print_divider("-")
    print("  1. Matches by Season")
    print("  2. Player of Match Awards")
    print("  3. All Matches")
    print("  0. Back to Main Menu")
    print_divider("-")


# ============================================================
# MENU HANDLERS
# ============================================================

def handle_player_menu(players: list[dict], matches: list[dict]) -> None:
    """Handle all player menu choices."""

    while True:
        show_player_menu()
        choice = input("  Enter choice: ").strip()

        if choice == "1":
            try:
                n = int(input("  How many top scorers? (default 5): ") or 5)
            except ValueError:
                n = 5
            display_top_scorers(get_top_scorers(players, n))

        elif choice == "2":
            try:
                n = int(input("  How many top wicket takers? (default 5): ") or 5)
            except ValueError:
                n = 5
            display_top_wicket_takers(get_top_wicket_takers(players, n))

        elif choice == "3":
            display_strike_rates(get_best_strike_rates(players))

        elif choice == "4":
            display_top_wicket_takers(get_best_economy(players))

        elif choice == "5":
            name = input("  Enter player name: ").strip()
            player = get_player_by_name(players, name)
            if player:
                display_player_card(player)
            else:
                print(f"\n  ❌ Player '{name}' not found!")
                print(f"  💡 Try: Virat Kohli, MS Dhoni, Rohit Sharma")

        elif choice == "6":
            teams = get_all_teams(players)
            print(f"\n  Available teams: {', '.join(teams)}")
            team = input("  Enter team name: ").strip().upper()
            squad = get_players_by_team(players, team)
            if squad:
                display_team_players(squad, team)
            else:
                print(f"\n  ❌ No players found for '{team}'")

        elif choice == "7":
            display_all_rounders(get_all_rounders(players))

        elif choice == "0":
            break

        else:
            print("\n  ⚠️  Invalid choice. Try again!")


def handle_team_menu(players: list[dict], matches: list[dict]) -> None:
    """Handle all team menu choices."""

    while True:
        show_team_menu()
        choice = input("  Enter choice: ").strip()

        if choice == "1":
            display_team_wins(get_team_wins(matches))

        elif choice == "2":
            team, wins = get_most_wins(matches)
            print(f"\n  👑 Most Successful Team: {team} with {wins} wins!\n")

        elif choice == "3":
            teams = get_all_teams(players)
            print(f"\n  Available teams: {', '.join(teams)}")
            team1 = input("  Enter Team 1: ").strip().upper()
            team2 = input("  Enter Team 2: ").strip().upper()
            result = get_head_to_head(matches, team1, team2)
            if result["total_matches"] > 0:
                display_head_to_head(result, team1, team2)
            else:
                print(f"\n  ❌ No matches found between {team1} and {team2}")

        elif choice == "0":
            break

        else:
            print("\n  ⚠️  Invalid choice. Try again!")


def handle_match_menu(players: list[dict], matches: list[dict]) -> None:
    """Handle all match menu choices."""

    while True:
        show_match_menu()
        choice = input("  Enter choice: ").strip()

        if choice == "1":
            seasons = get_all_seasons(matches)
            print(f"\n  Available seasons: {', '.join(str(s) for s in seasons)}")
            try:
                season = int(input("  Enter season year: ").strip())
                season_matches = get_matches_by_season(matches, season)
                if season_matches:
                    display_matches(season_matches, f"IPL {season} MATCHES")
                else:
                    print(f"\n  ❌ No matches found for season {season}")
            except ValueError:
                print("\n  ❌ Please enter a valid year")

        elif choice == "2":
            counts = get_player_of_match_count(matches)
            display_player_of_match(counts)

        elif choice == "3":
            display_matches(matches, "ALL MATCHES")

        elif choice == "0":
            break

        else:
            print("\n  ⚠️  Invalid choice. Try again!")


# ============================================================
# MAIN — App Entry Point
# ============================================================

def main() -> None:
    """Main function — loads data and runs the menu loop."""

    print("\n  Loading IPL data...")
    players = load_players()
    matches = load_matches()

    # Exit if data failed to load
    if not players or not matches:
        print("❌ Failed to load data. Exiting.")
        return

    print("\n  ✅ Data loaded successfully!")

    # Main menu loop
    while True:
        show_main_menu()
        choice = input("  Enter choice: ").strip()

        if choice == "1":
            handle_player_menu(players, matches)

        elif choice == "2":
            handle_team_menu(players, matches)

        elif choice == "3":
            handle_match_menu(players, matches)

        elif choice == "4":
            summary = generate_summary(players, matches)
            display_summary(summary)

        elif choice == "5":
            summary = generate_summary(players, matches)
            save_results(summary)

        elif choice == "0":
            print("\n  👋 Thanks for using IPL Stats Analyzer!")
            print("  🏏 Cricket is life!\n")
            break

        else:
            print("\n  ⚠️  Invalid choice. Please try again!")


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()