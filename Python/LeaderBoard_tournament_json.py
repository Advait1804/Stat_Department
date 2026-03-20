def LeaderBoard_tournament(dfs, filters=None):
    pms = dfs.get("player_tournament_stat")
    player = dfs.get("player")
    tournament = dfs.get("tournament")

    if pms is None or player is None or tournament is None:
        return []

    result = []

    # -----------------------------
    # APPLY FILTER: tournament_name only
    # -----------------------------
    if filters and filters.get("tournament") is not None:
        matching_tournaments = tournament[
            tournament["tournament_name"] == filters["tournament"]
        ]["tournament_id"].tolist()
        pms = pms[pms["tournament_id"].isin(matching_tournaments)]

    # -----------------------------
    # Create maps
    # -----------------------------
    player_name_map = {row.player_id: row.player_name for _, row in player.iterrows()}
    player_role_map = {row.player_id: row.role for _, row in player.iterrows()}
    tournament_name_map = {row.tournament_id: row.tournament_name for _, row in tournament.iterrows()}

    # -----------------------------
    # Prepare dataframe
    # -----------------------------
    pms = pms.copy()
    pms["role"] = pms["player_id"].map(player_role_map)
    pms["total_attack_points"] = pms["total_attack_points"].fillna(0)
    pms["total_defence_points"] = pms["total_defence_points"].fillna(0)

    # -----------------------------
    # Group by tournament
    # -----------------------------
    for tournament_id, t_df in pms.groupby("tournament_id"):

        attackers = t_df[t_df["role"] == "Attacker"]
        defenders = t_df[t_df["role"] == "Defender"]

        # Best Attacker
        if not attackers.empty:
            row = attackers.loc[attackers["total_attack_points"].idxmax()]
            result.append({
                "Tournament": tournament_name_map.get(tournament_id, "Unknown"),
                "Player name": player_name_map.get(row["player_id"], "Unknown"),
                "Award": "Best Attacker",
                "Attack Points": int(row["total_attack_points"])
            })

        # Best Defender
        if not defenders.empty:
            row = defenders.loc[defenders["total_defence_points"].idxmax()]
            result.append({
                "Tournament": tournament_name_map.get(tournament_id, "Unknown"),
                "Player name": player_name_map.get(row["player_id"], "Unknown"),
                "Award": "Best Defender",
                "Defence Points": int(row["total_defence_points"])
            })

        # Best All-Rounder
        t_df["total_score"] = t_df["total_attack_points"] * 30 + t_df["total_defence_points"]
        row = t_df.loc[t_df["total_score"].idxmax()]
        result.append({
            "Tournament": tournament_name_map.get(tournament_id, "Unknown"),
            "Player name": player_name_map.get(row["player_id"], "Unknown"),
            "Award": "Best All-Rounder",
            "All Rounder Points": int(row["total_score"])
        })

    return result
