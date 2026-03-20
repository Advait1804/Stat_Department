import pandas as pd

def build_attack_json(dfs, filters=None):
    matches = dfs.get("match_details")
    teams = dfs.get("team")
    attack = dfs.get("team_attack")
    tournament = dfs.get("tournament")

    attack_dic = {}

    # Mappings
    team_name_map = {
        row.team_id: row.team_name for _, row in teams.iterrows()
    } if teams is not None else {}

    tournament_name_map = {
        row.tournament_id: row.tournament_name for _, row in tournament.iterrows()
    } if tournament is not None else {}

    if matches is None or attack is None:
        return attack_dic

    # Apply filters (optional)
    if filters:

        # Tournament filter (your exact pattern)
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
            
    # Loop through matches
    for _, m in matches.iterrows():
        m_id = m["match_id"]
        t_id = m["tournament_id"]
        match_name = m.get("match_name")

        # 🔥 Replace ID with NAME
        tournament_name = tournament_name_map.get(t_id, f"Tournament_{t_id}")

        if tournament_name not in attack_dic:
            attack_dic[tournament_name] = {}

        phase_dic = {}

        # Filter attack rows for this match
        match_attack = attack[attack["match_id"] == m_id]

        for _, a in match_attack.iterrows():
            team_id = a["team_id"]
            team_name = team_name_map.get(team_id, -1)

            inning = "inning" + str(a["inning"])
            phase = a["phase"]
            points = a["points"]

            if inning not in phase_dic:
                phase_dic[inning] = {}

            if phase not in phase_dic[inning]:
                phase_dic[inning][phase] = {}

            phase_dic[inning][phase][team_name] = points

        attack_dic[tournament_name][match_name] = phase_dic

    return attack_dic
