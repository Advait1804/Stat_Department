import pandas as pd

def build_match_details_json(dfs):
    matches = dfs.get("match_details")
    teams = dfs.get("team")
    pms = dfs.get("player_match_stat")
    player = dfs.get("player")

    if matches is None or pms is None:
        return {}

    detail_list = []

    # Create lookup maps
    player_name_map = {row.player_id: row.player_name for _, row in player.iterrows()} if player is not None else {}
    team_name_map = {row.team_id: row.team_name for _, row in teams.iterrows()} if teams is not None else {}
    player_role_map = {row.player_id: row.role for _, row in player.iterrows()} if player is not None else {}

    for _, m in matches.iterrows():

        m_id = int(m["match_id"])

        # Filter match players
        match_pms = pms[pms["match_id"] == m_id].copy()

        # Map roles
        match_pms["role"] = match_pms["player_id"].map(player_role_map)

        # Split by role
        attackers = match_pms[match_pms["role"] == "Attacker"]
        defenders = match_pms[match_pms["role"] == "Defender"]
        all_rounders = match_pms[match_pms["role"] == "All-Rounder"]

        # Best Attacker
        best_attacker_id = None
        if not attackers.empty:
            idx = attackers["attack_points"].fillna(0).idxmax()
            best_attacker_id = attackers.loc[idx]["player_id"]

        # Best Defender
        best_defender_id = None
        if not defenders.empty:
            idx = defenders["defense_points"].fillna(0).idxmax()
            best_defender_id = defenders.loc[idx]["player_id"]

        # Best All-Rounder (Formula applied directly)
        best_all_rounder_id = None
        if not all_rounders.empty:
            idx = (
                (all_rounders["attack_points"].fillna(0) * 20) +
                all_rounders["defense_points"].fillna(0)
            ).idxmax()
            best_all_rounder_id = all_rounders.loc[idx]["player_id"]

        # Team info
        home_team_name = team_name_map.get(m["home_team"], "Unknown")
        away_team_name = team_name_map.get(m["away_team"], "Unknown")
        winning_team_id = m.get("winning_team")
        if pd.isna(winning_team_id):
            winner_team_name = "Draw"
        else:
            winner_team_name = team_name_map.get(winning_team_id, "Unknown")
        
        
        # Converting match id 
        match_code = f"M{m_id:02d}"
        
        # Convert to names
        detail_list.append({
            "id": match_code,
            "name": f"{home_team_name} vs {away_team_name}",
            "winner": winner_team_name,
            "bestAttacker": player_name_map.get(best_attacker_id, "Unknown"),
            "bestDefender": player_name_map.get(best_defender_id, "Unknown"),
            "bestAllrounder": player_name_map.get(best_all_rounder_id, "Unknown")
        })

    return {"matches": detail_list}
