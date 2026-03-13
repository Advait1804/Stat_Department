def LeaderBoard_season(dfs):
    pms = dfs.get("player_season_stat")
    player = dfs.get("player")

    if pms is None or player is None:
        return []

    result = []

    player_name_map = {
        row.player_id: row.player_name
        for _, row in player.iterrows()
    }

    player_role_map = {
        row.player_id: row.role
        for _, row in player.iterrows()
    }

    pms = pms.copy()
    pms["role"] = pms["player_id"].map(player_role_map)
    pms["total_attack_points"] = pms["total_attack_points"].fillna(0)
    pms["total_defense_points"] = pms["total_defense_points"].fillna(0)

    for season_id, season_df in pms.groupby("season_id"):

        attackers = season_df[season_df["role"] == "Attacker"]
        defenders = season_df[season_df["role"] == "Defender"]

        # Best Attacker
        if not attackers.empty:
            idx = attackers["total_attack_points"].idxmax()
            row = attackers.loc[idx]
            result.append({
                "Season ID": int(season_id),
                "Player name": player_name_map.get(row["player_id"], "Unknown"),
                "Award": "Best Attacker",
                "Attack Points": int(row["total_attack_points"])
            })

        # Best Defender
        if not defenders.empty:
            idx = defenders["total_defense_points"].idxmax()
            row = defenders.loc[idx]
            result.append({
                "Season ID": int(season_id),
                "Player name": player_name_map.get(row["player_id"], "Unknown"),
                "Award": "Best Defender",
                "Defence Points": int(row["total_defense_points"])
            })

        # Best All-Rounder (no role restriction)
        idx = (
            (season_df["total_attack_points"] * 30) +
            season_df["total_defense_points"]
        ).idxmax()

        row = season_df.loc[idx]
        total_score = (row["total_attack_points"] * 30) + row["total_defense_points"]

        result.append({
            "Season ID": int(season_id),
            "Player name": player_name_map.get(row["player_id"], "Unknown"),
            "Award": "Best All-Rounder",
            "All Rounder Points": int(total_score)
        })

    return result
