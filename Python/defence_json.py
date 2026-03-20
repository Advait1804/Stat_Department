def build_defence_json(dfs, filters=None):

    matches = dfs.get("match_details")
    teams = dfs.get("team")
    tournaments = dfs.get("tournament")
    defence = dfs.get("team_defence")

    defence_dict = {}

    if matches is None or defence is None:
        return defence_dict

    # Mappings
    team_name_map = {
        row.team_id: row.team_name
        for _, row in teams.iterrows()
    } if teams is not None else {}

    tournament_name_map = {
        row.tournament_id: row.tournament_name
        for _, row in tournaments.iterrows()
    } if tournaments is not None else {}

    # Filters
    if filters:

    # Tournament filter 
        if filters.get("tournament") and filters["tournament"] != "all":
            matches = matches[
                matches["tournament_id"].isin([
                    tid for tid, tname in tournament_name_map.items()
                    if tname == filters["tournament"]
                ])
            ]

        # Match filter
        if filters.get("match"):
            matches = matches[matches["match_name"] == filters["match"]]
    # Filter defence only once
    defence = defence[
        defence["match_id"].isin(matches["match_id"])
    ]

    # Loop through matches
    for _, m in matches.iterrows():

        m_id = int(m.get("match_id"))
        t_id = m.get("tournament_id")
        match_name = m.get("match_name")

        tournament_name = tournament_name_map.get(
            t_id, f"Tournament_{t_id}"
        )

        # Create tournament level
        if tournament_name not in defence_dict:
            defence_dict[tournament_name] = {}

        match_defence = defence[defence["match_id"] == m_id]

        match_structure = {
            "defence": {
                "inning1": {},
                "inning2": {}
            }
        }

        # Loop defence rows
        for _, d in match_defence.iterrows():

            inning = int(d.get("inning_no"))
            inning_key = f"inning{inning}"

            team_id = int(d.get("team_id"))
            team_name = team_name_map.get(team_id, "Unknown")

            batch_data = {
                "batch": f"Batch {int(d.get('batch_no'))}",
                "start": float(d.get("start_time")),
                "end_time": float(d.get("end_time")),
                "duration": float(d.get("duration"))
            }

            if team_name not in match_structure["defence"][inning_key]:
                match_structure["defence"][inning_key][team_name] = []

            match_structure["defence"][inning_key][team_name].append(batch_data)

        # Store under tournament → match
        defence_dict[tournament_name][match_name] = match_structure

    return defence_dict
