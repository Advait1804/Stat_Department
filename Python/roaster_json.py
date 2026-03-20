import pandas as pd

def build_roaster_json(dfs, filters=None):
    
    matches = dfs.get("match_details")
    players = dfs.get("player")
    pms = dfs.get("player_match_stat")
    teams = dfs.get("team")
    tournament = dfs.get("tournament")

    roster_dict = {}

    if matches is None:
        return roster_dict

    # ---------------------------
    # Apply filters
    # ---------------------------
    tournament_name_map = (
        {int(row.tournament_id): row.tournament_name for _, row in tournament.iterrows()}
        if tournament is not None else {}
    )

    if filters:

        # Tournament filter
        if filters.get("tournament") and tournament is not None:
            matches = matches[
                matches["tournament_id"].isin([
                    tid for tid, tname in tournament_name_map.items()
                    if tname == filters["tournament"]
                ])
            ]

        # Match filter (id = M01, M02)
        if filters.get("match"):
            matches = matches[matches["match_name"] == filters["match"]]
            # Also filter player stats for this match only
            pms = pms[pms["match_id"].isin(matches["match_id"])]


    if matches.empty:
        return roster_dict

    # ---------------------------
    # Maps
    # ---------------------------
    team_name_map = {row.team_id: row.team_name for _, row in teams.iterrows()} if teams is not None else {}
    player_name_map = {row.player_id: row.player_name for _, row in players.iterrows()} if players is not None else {}
    player_role_map = {row.player_id: row.role for _, row in players.iterrows()} if players is not None else {}
    player_team_map = {int(row.player_id): int(row.team_id) for _, row in players.iterrows()} if players is not None else {}

    # ---------------------------
    # Build roster
    # ---------------------------
    for _, m in matches.iterrows():

        match_id = int(m["match_id"])
        match_date = m.get("match_date")
        home_team = m.get("home_team")
        away_team = m.get("away_team")
        tournament_id = m.get("tournament_id")
        tournament_name = tournament_name_map.get(tournament_id, "Unknown")

        if tournament_name not in roster_dict:
            roster_dict[tournament_name] = {}

        # Filter match stats for current match
        match_players = pms[pms["match_id"] == match_id]

        def get_team_data(team_id):
            attackers = []
            defenders = []
            all_rounders = []

            for _, prow in match_players.iterrows():
                pid = int(prow["player_id"])
                if player_team_map.get(pid) == int(team_id):
                    pname = player_name_map.get(pid, "Unknown")
                    role = player_role_map.get(pid, "").lower()
                    if role == "attacker":
                        attackers.append(pname)
                    elif role == "defender":
                        defenders.append(pname)
                    elif role == "all-rounder":
                        all_rounders.append(pname)

            return {
                "name": team_name_map.get(team_id, "Unknown"),
                "attackers": attackers,
                "defenders": defenders,
                "allRounders": all_rounders
            }

        roster_dict[tournament_name][m.get("match_name")] = {
            "match_date": str(match_date) if pd.notna(match_date) else None,
            "home_team": get_team_data(home_team),
            "away_team": get_team_data(away_team)
        }

    return roster_dict
