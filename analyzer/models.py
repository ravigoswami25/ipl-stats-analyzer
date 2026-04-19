# analyzer/models.py
# Responsibility: Data classes — Player, Match, Team


# ============================================================
# PLAYER CLASS
# ============================================================

class Player:
    """Represents an IPL player with stats."""

    def __init__(
        self,
        id: int,
        name: str,
        team: str,
        role: str,
        matches: int,
        runs: int,
        highest_score: int,
        average: float,
        strike_rate: float,
        centuries: int,
        fifties: int,
        wickets: int,
        economy: float
    ):
        # Store all attributes
        self.id = id
        self.name = name
        self.team = team
        self.role = role
        self.matches = matches
        self.runs = runs
        self.highest_score = highest_score
        self.average = average
        self.strike_rate = strike_rate
        self.centuries = centuries
        self.fifties = fifties
        self.wickets = wickets
        self.economy = economy

    # ── Computed Properties ───────────────────────────────

    def get_runs_lpa(self) -> float:
        """Return runs per match."""
        if self.matches == 0:
            return 0.0
        return round(self.runs / self.matches, 2)

    def is_batsman(self) -> bool:
        """Check if player is primarily a batsman."""
        return self.role in ["Batsman", "Wicket-Keeper"]

    def is_bowler(self) -> bool:
        """Check if player is primarily a bowler."""
        return self.role == "Bowler"

    def is_all_rounder(self) -> bool:
        """Check if player is a genuine all rounder."""
        return self.runs > 500 and self.wickets > 20

    def get_performance_rating(self) -> str:
        """
        Rate player performance based on runs and wickets.
        Returns: Elite / Good / Average
        """
        if self.runs > 5000 or self.wickets > 100:
            return "🌟 Elite"
        elif self.runs > 2000 or self.wickets > 50:
            return "✅ Good"
        else:
            return "📈 Average"

    # ── Class Method — alternative constructor ────────────

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        """
        Create a Player object from a dictionary.
        This is how we convert JSON data → Player object.

        Usage:
            player = Player.from_dict({"name": "Virat", ...})
        """
        return cls(
            id=data["id"],
            name=data["name"],
            team=data["team"],
            role=data["role"],
            matches=data["matches"],
            runs=data["runs"],
            highest_score=data["highest_score"],
            average=data["average"],
            strike_rate=data["strike_rate"],
            centuries=data["centuries"],
            fifties=data["fifties"],
            wickets=data["wickets"],
            economy=data["economy"]
        )

    def to_dict(self) -> dict:
        """
        Convert Player object back to dictionary.
        Used when saving to JSON.
        """
        return {
            "id": self.id,
            "name": self.name,
            "team": self.team,
            "role": self.role,
            "matches": self.matches,
            "runs": self.runs,
            "highest_score": self.highest_score,
            "average": self.average,
            "strike_rate": self.strike_rate,
            "centuries": self.centuries,
            "fifties": self.fifties,
            "wickets": self.wickets,
            "economy": self.economy
        }

    # ── Magic Methods ─────────────────────────────────────

    def __str__(self) -> str:
        """What prints when you do print(player)."""
        return (
            f"{self.name} | {self.team} | {self.role} | "
            f"{self.runs} runs | {self.wickets} wkts"
        )

    def __repr__(self) -> str:
        """What shows in debugger/console."""
        return f"Player(name={self.name!r}, team={self.team!r})"

    def __eq__(self, other) -> bool:
        """Check if two players are equal by id."""
        if not isinstance(other, Player):
            return False
        return self.id == other.id

    def __lt__(self, other) -> bool:
        """Less than — enables sorting players by runs."""
        return self.runs < other.runs


# ============================================================
# MATCH CLASS
# ============================================================

class Match:
    """Represents a single IPL match."""

    def __init__(
        self,
        id: int,
        season: int,
        team1: str,
        team2: str,
        winner: str,
        margin: str,
        venue: str,
        player_of_match: str
    ):
        self.id = id
        self.season = season
        self.team1 = team1
        self.team2 = team2
        self.winner = winner
        self.margin = margin
        self.venue = venue
        self.player_of_match = player_of_match

    def get_loser(self) -> str:
        """Return the losing team."""
        return self.team2 if self.winner == self.team1 else self.team1

    def involves_team(self, team: str) -> bool:
        """Check if a team played in this match."""
        return team.upper() in [self.team1.upper(), self.team2.upper()]

    def is_won_by(self, team: str) -> bool:
        """Check if given team won this match."""
        return self.winner.upper() == team.upper()

    @classmethod
    def from_dict(cls, data: dict) -> "Match":
        """Create Match object from dictionary."""
        return cls(
            id=data["id"],
            season=data["season"],
            team1=data["team1"],
            team2=data["team2"],
            winner=data["winner"],
            margin=data["margin"],
            venue=data["venue"],
            player_of_match=data["player_of_match"]
        )

    def to_dict(self) -> dict:
        """Convert Match back to dictionary."""
        return {
            "id": self.id,
            "season": self.season,
            "team1": self.team1,
            "team2": self.team2,
            "winner": self.winner,
            "margin": self.margin,
            "venue": self.venue,
            "player_of_match": self.player_of_match
        }

    def __str__(self) -> str:
        return (
            f"IPL {self.season} | "
            f"{self.team1} vs {self.team2} | "
            f"Won: {self.winner} by {self.margin}"
        )

    def __repr__(self) -> str:
        return f"Match(id={self.id}, {self.team1} vs {self.team2})"


# ============================================================
# TEAM CLASS
# ============================================================

class Team:
    """Represents an IPL team — built from players and matches."""

    def __init__(self, name: str):
        self.name = name
        self.players: list[Player] = []     # list of Player objects
        self.matches: list[Match] = []      # list of Match objects

    def add_player(self, player: Player) -> None:
        """Add a player to this team."""
        self.players.append(player)

    def add_match(self, match: Match) -> None:
        """Add a match this team played in."""
        self.matches.append(match)

    # ── Computed Stats ────────────────────────────────────

    def get_wins(self) -> int:
        """Total wins for this team."""
        return sum(1 for m in self.matches if m.is_won_by(self.name))

    def get_losses(self) -> int:
        """Total losses for this team."""
        return len(self.matches) - self.get_wins()

    def get_win_rate(self) -> float:
        """Win percentage."""
        if not self.matches:
            return 0.0
        return round((self.get_wins() / len(self.matches)) * 100, 2)

    def get_top_scorer(self) -> Player | None:
        """Return player with most runs in this team."""
        if not self.players:
            return None
        return max(self.players, key=lambda p: p.runs)

    def get_top_bowler(self) -> Player | None:
        """Return player with most wickets in this team."""
        bowlers = [p for p in self.players if p.wickets > 0]
        if not bowlers:
            return None
        return max(bowlers, key=lambda p: p.wickets)

    def get_total_runs(self) -> int:
        """Total runs scored by all players."""
        return sum(p.runs for p in self.players)

    def __str__(self) -> str:
        return (
            f"{self.name} | "
            f"Players: {len(self.players)} | "
            f"W: {self.get_wins()} L: {self.get_losses()} | "
            f"Win Rate: {self.get_win_rate()}%"
        )

    def __repr__(self) -> str:
        return f"Team(name={self.name!r})"