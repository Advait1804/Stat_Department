import pandas as pd

def build_match_wise(dfs, filters=None):

    matches = dfs.get("match_details")
    teams = dfs.get("team")
    season = dfs.get("season")
    tournament = dfs.get("tournament")

    if matches is None:
        return {"matches": []}

    # -------------------
    # FILTERING
    # -------------------

    if filters:

        if filters.get("tournament_id") is not None and season is not None:
            valid_seasons = season.loc[
                season["tournament_id"] == filters["tournament_id"],
                "season_id"
            ]
            matches = matches[matches["season_id"].isin(valid_seasons)]

        if filters.get("season_id") is not None:
            matches = matches[matches["season_id"] == filters["season_id"]]

        if filters.get("match_id") is not None:
            matches = matches[matches["match_id"] == filters["match_id"]]

        if filters.get("team_id") is not None:
            matches = matches[
                (matches["home_team"] == filters["team_id"]) |
                (matches["away_team"] == filters["team_id"])
            ]

    # -------------------
    # LOOKUP TABLES
    # -------------------

    team_name_map = {
        row.team_id: row.team_name
        for _, row in teams.iterrows()
    } if teams is not None else {}

    season_name_map = {}
    season_tournament_map = {}

    if season is not None:
        for _, row in season.iterrows():
            season_name_map[row.season_id] = row.season_name
            season_tournament_map[row.season_id] = row.tournament_id

    tournament_name_map = {
        row.tournament_id: row.tournament_name
        for _, row in tournament.iterrows()
    } if tournament is not None else {}

    # -------------------
    # BUILD JSON
    # -------------------

    match_list = []

    for _, m in matches.iterrows():

        match_id = int(m["match_id"])
        season_id = int(m["season_id"])

        home_team_id = int(m["home_team"])
        away_team_id = int(m["away_team"])

        home_team_name = team_name_map.get(home_team_id, "Unknown")
        away_team_name = team_name_map.get(away_team_id, "Unknown")

        winner_raw = m.get("winning_team")

        if pd.isna(winner_raw):
            winner_name = "Draw"
        else:
            winner_name = team_name_map.get(int(winner_raw), "Draw")

        season_name = season_name_map.get(season_id, "Unknown")

        tournament_id = season_tournament_map.get(season_id)
        tournament_name = tournament_name_map.get(tournament_id, "Unknown")

        home_score = m.get("home_team_score", "")
        away_score = m.get("away_team_score", "")

        score_text = f"{home_team_name} {home_score} - {away_score} {away_team_name}"

        match_list.append({
            "id": f"M{match_id:02d}",
            "name": f"{home_team_name} vs {away_team_name}",
            "date": str(m["match_date"]),
            "season": season_name,
            "tournament": tournament_name,
            "score": score_text,
            "winner": winner_name
        })

    return {
        "matches": match_list
    }
