import pandas as pd
def build_match_details_json(dfs, filters=None):

    matches = dfs.get("match_details")
    teams = dfs.get("team")
    pms = dfs.get("player_match_stat")
    player = dfs.get("player")
    tournament = dfs.get("tournament")

    if matches is None or pms is None:
        return {}

    # APPLY FILTERS
    if filters:

        # Filter by tournament_name
        if filters.get("tournament") and tournament is not None:

            # Get matching tournament_id(s)
            t_ids = tournament[
                tournament["tournament_name"] == filters["tournament"]
            ]["tournament_id"].tolist()

            matches = matches[matches["tournament_id"].isin(t_ids)]

        # Filter by match_name (M01, M02)
        if filters.get("match_name"):
            matches = matches[matches["match_name"] == filters["match"]]

    detail_list = []

    # Lookup maps
    player_name_map = {row.player_id: row.player_name for _, row in player.iterrows()} if player is not None else {}
    team_name_map = {row.team_id: row.team_name for _, row in teams.iterrows()} if teams is not None else {}
    player_role_map = {row.player_id: row.role for _, row in player.iterrows()} if player is not None else {}

    for _, m in matches.iterrows():

        m_id = int(m["match_id"])

        match_pms = pms[pms["match_id"] == m_id].copy()
        match_pms["role"] = match_pms["player_id"].map(player_role_map)

        attackers = match_pms[match_pms["role"] == "Attacker"]
        defenders = match_pms[match_pms["role"] == "Defender"]
        all_rounders = match_pms[match_pms["role"] == "All-Rounder"]

        best_attacker_id = attackers.loc[attackers["attack_points"].fillna(0).idxmax()]["player_id"] if not attackers.empty else None
        best_defender_id = defenders.loc[defenders["defense_points"].fillna(0).idxmax()]["player_id"] if not defenders.empty else None

        best_all_rounder_id = None
        if not all_rounders.empty:
            idx = (
                (all_rounders["attack_points"].fillna(0) * 20) +
                all_rounders["defense_points"].fillna(0)
            ).idxmax()
            best_all_rounder_id = all_rounders.loc[idx]["player_id"]

        home_team_name = team_name_map.get(m["home_team"], "Unknown")
        away_team_name = team_name_map.get(m["away_team"], "Unknown")

        winning_team_id = m.get("winning_team")
        winner_team_name = "Draw" if pd.isna(winning_team_id) else team_name_map.get(winning_team_id, "Unknown")

        detail_list.append({
            "id": m.get("match_name"),
            "name": f"{home_team_name} vs {away_team_name}",
            "winner": winner_team_name,
            "bestAttacker": player_name_map.get(best_attacker_id, "Unknown"),
            "bestDefender": player_name_map.get(best_defender_id, "Unknown"),
            "bestAllrounder": player_name_map.get(best_all_rounder_id, "Unknown")
        })

    return {"matches": detail_list}
