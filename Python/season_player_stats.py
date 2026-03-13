def season_players_json(dfs):
    # Fetch required dataframes
    pms = dfs.get("player_season_stat")
    player = dfs.get("player")
    team = dfs.get("team")

    # If essential data is missing, return empty list
    if pms is None or player is None:
        return []

    
    # Create lookup maps for fast access
    

    # Map: player_id → {name, role, jersey_no}
    player_map = {
        row.player_id: {
            "name": row.player_name,
            "role": row.role,
            "jersey_no": row.jersey_no
        }
        for _, row in player.iterrows()
    }

    # Map: team_id → team_name
    team_map = {
        row.team_id: row.team_name
        for _, row in team.iterrows()
    }

    result = {}

    
    # Loop season-wise
    
    for season_id in pms["season_id"].unique():

        # Filter data for that specific season
        season_df = pms[pms["season_id"] == season_id]

        players_list = []

        
        # Loop player-wise within season
        
        for _, row in season_df.iterrows():

            player_id = int(row["player_id"])

            # Extract attack & defense stats (handle NULL safely)
            attack = int(row["total_attack_points"] or 0)
            defense = int(row["total_defence_points"] or 0)

            # Get player info from lookup map
            player_info = player_map.get(player_id, {})

            role = str(player_info.get("role", "Unknown"))
            name = str(player_info.get("name", "Unknown"))
            jersey_no = player_info.get("jersey_no")

            
            # Role-based points calculation
            
            if role == "Attacker":
                points = attack
            elif role == "Defender":
                points = defense
            elif role == "All-Rounder":
                # Custom scoring logic for all-rounders
                points = (attack * 30) + defense
            else:
                points = 0

           
            # Generate formatted player ID
            
            team_name = str(team_map.get(row.get("team_id"), "Unknown"))
            team_code = team_name[:3].upper()

            # Extract initials from player name
            initials = "".join([part[0] for part in name.split() if part]).upper()

            formatted_id = f"{team_code}_{initials}"

            players_list.append({
                "id": formatted_id,           # Frontend-friendly ID (e.g., MAH_SP)
                "player_id": player_id,       # Original numeric DB ID
                "name": str(name),
                "jersey_no": int(jersey_no) if jersey_no is not None else None,
                "team": team_name,
                "role": str(role),
                "stats": {
                    "matches": int(row["matches_played"]),
                    "points": int(points)
                }
            })

        # Append season-wise data
        result["players"]=players_list

    return result
