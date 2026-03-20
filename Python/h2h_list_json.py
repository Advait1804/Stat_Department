import pandas as pd

def build_h2h_json(dfs, filters=None):

    matches = dfs.get("match_details")
    teams = dfs.get("team")
    pms = dfs.get("player_match_stat")
    players = dfs.get("player")
    tournament = dfs.get("tournament")

    if matches is None or matches.empty:
        return {}

    team_name_map = {row.team_id: row.team_name for _, row in teams.iterrows()} if teams is not None else {}
    player_team_map = {row.player_id: row.team_id for _, row in players.iterrows()} if players is not None else {}
    tournament_name_map = {row.tournament_id: row.tournament_name for _, row in tournament.iterrows()} if tournament is not None else {}

    
    # APPLY FILTERS
    
    if filters:

        # Tournament filter 
        if filters.get("tournament") and filters["tournament"] != "all":
            matches = matches[
                matches["tournament_id"].isin([
                    tid for tid, tname in tournament_name_map.items()
                    if tname == filters["tournament"]
                ])
            ]

    if matches.empty:
        return {}

    
    # IF MATCH (M01) GIVEN → RETURN LAST 5 H2H
    
    if filters and filters.get("match"):

        base_match = matches[matches["match_name"] == filters["match"]]

        if base_match.empty:
            return {}

        base_match = base_match.iloc[0]

        teamA_id = base_match["home_team"]
        teamB_id = base_match["away_team"]

        # Get ALL matches between these teams
        h2h_matches = matches[
            ((matches["home_team"] == teamA_id) & (matches["away_team"] == teamB_id)) |
            ((matches["home_team"] == teamB_id) & (matches["away_team"] == teamA_id))
        ]

        # ✅ SORT + LIMIT TO LAST 5
        h2h_matches = h2h_matches.sort_values("match_date", ascending=False).head(5)

        key_name = f"{team_name_map.get(teamA_id)} vs {team_name_map.get(teamB_id)}"

        return {
            key_name: build_match_list(h2h_matches, team_name_map, pms, player_team_map)
        }

    
    # NO MATCH → RETURN ALL H2H GROUPS
    
    h2h_result = {}

    matches["pair"] = matches.apply(
        lambda row: tuple(sorted([row["home_team"], row["away_team"]])),
        axis=1
    )

    grouped = matches.groupby("pair")

    for pair, group in grouped:

        team1, team2 = pair
        key_name = f"{team_name_map.get(team1)} vs {team_name_map.get(team2)}"

        # (Optional: limit to 5 here also if needed)
        group = group.sort_values("match_date", ascending=False)

        h2h_result[key_name] = build_match_list(
            group,
            team_name_map,
            pms,
            player_team_map
        )

    return h2h_result



# Helper Function
def build_match_list(matches, team_name_map, pms, player_team_map):

    result_list = []

    for _, m in matches.iterrows():

        match_id = m["match_id"]
        teamA_id = m["home_team"]
        teamB_id = m["away_team"]
        teamA_score = m["home_team_score"]
        teamB_score = m["away_team_score"]

        # Calculate score if missing
        if (teamA_score == 0 and teamB_score == 0) and pms is not None:
            pm_match = pms[pms["match_id"] == match_id].copy()

            if "team_id" not in pm_match.columns:
                pm_match["team_id"] = pm_match["player_id"].map(player_team_map)

            if "points" in pm_match.columns:
                team_scores = pm_match.groupby("team_id")["points"].sum().to_dict()
                teamA_score = team_scores.get(teamA_id, 0)
                teamB_score = team_scores.get(teamB_id, 0)

        # Winner
        if pd.isna(m.get("winning_team")):
            winner_name = "Draw"
        else:
            winner_name = team_name_map.get(m.get("winning_team"))

        score_string = f"{team_name_map.get(teamA_id)} {teamA_score}-{teamB_score} {team_name_map.get(teamB_id)}"

        result_list.append({
            "match": m.get("match_name"),
            "date": str(m.get("match_date")) if pd.notna(m.get("match_date")) else None,
            "score": score_string,
            "winner": winner_name
        })

    return result_list
