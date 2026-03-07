from flask import Flask, jsonify,request
from flask_cors import CORS
from attack_json import build_attack_json
from data_cleaning import clean_table, standardize_columns
from database_connectivity import connect_db, fetch_tables
from Point_Table_json import Point_Table
from roaster_json import build_roaster_json
from h2h_list_json import build_h2h_json
from defence_json import build_defence_json
from match_wise_json import build_match_wise
from LeaderBoard_season_json import LeaderBoard
from match_details_json import build_match_details_json
from season_player_stats import season_players_json
from player_profile import build_players_json

app = Flask(__name__)
CORS(app)

def load_clean_data():
    conn = connect_db()
    dfs = fetch_tables(conn)

    for key, df in dfs.items():
        dfs[key] = clean_table(standardize_columns(df), key)

    conn.close()
    return dfs

@app.route("/player-profile")
def get_player_season_profile():
    dfs=load_clean_data()
    data=build_players_json(dfs)
    return jsonify(data)

@app.route("/player-season")
def get_player_season_stats():
    dfs=load_clean_data()
    data=season_players_json(dfs)
    return jsonify(data)

@app.route("/match-details")
def get_match_details():
    dfs=load_clean_data()
    data=build_match_details_json(dfs)
    return jsonify(data)
    
@app.route("/point-table")
def get_point_table():
    filters = {}

    if request.args.get("tournament_id"):
        filters["tournament_id"] = int(request.args.get("tournament_id"))

    if request.args.get("season_id"):
        filters["season_id"] = int(request.args.get("season_id"))
    dfs = load_clean_data()
    data = Point_Table(dfs,filters)
    return jsonify(data)

@app.route("/roaster")
def get_roaster():
    filters={}
    if request.args.get("tournament_id"):
        filters["tournament_id"] = int(request.args.get("tournament_id"))

    if request.args.get("season_id"):
        filters["season_id"] = int(request.args.get("season_id"))

    if request.args.get("match_id"):
        filters["match_id"] = int(request.args.get("match_id"))

    if request.args.get("team_id"):
        filters["team_id"] = int(request.args.get("team_id"))

    if request.args.get("role"):
        filters["role"] = request.args.get("role")
    dfs=load_clean_data()
    data=build_roaster_json(dfs,filters)
    return jsonify(data)

@app.route("/attacker")
def get_attacker():
    filters = {}

    if request.args.get("tournament_id"):
        filters["tournament_id"] = int(request.args.get("tournament_id"))

    if request.args.get("season_id"):
        filters["season_id"] = int(request.args.get("season_id"))

    if request.args.get("match_id"):
        filters["match_id"] = int(request.args.get("match_id"))

    if request.args.get("team_id"):
        filters["team_id"] = int(request.args.get("team_id"))

    dfs=load_clean_data()
    data=build_attack_json(dfs,filters)
    return jsonify(data)

@app.route("/h2h")
def get_h2h():
    filters = {}

    if request.args.get("tournament_id"):
        filters["tournament_id"] = int(request.args.get("tournament_id"))

    if request.args.get("season_id"):
        filters["season_id"] = int(request.args.get("season_id"))

    if request.args.get("match_id"):
        filters["match_id"] = int(request.args.get("match_id"))

    if request.args.get("team_id"):
        filters["team_id"] = int(request.args.get("team_id"))
    dfs=load_clean_data()
    data=build_h2h_json(dfs,filters)
    return jsonify(data)

@app.route("/defence")
def get_defence():
    filters = {}

    if request.args.get("tournament_id"):
        filters["tournament_id"] = int(request.args.get("tournament_id"))

    if request.args.get("season_id"):
        filters["season_id"] = int(request.args.get("season_id"))

    if request.args.get("match_id"):
        filters["match_id"] = int(request.args.get("match_id"))

    if request.args.get("team_id"):
        filters["team_id"] = int(request.args.get("team_id"))
    dfs=load_clean_data()
    data=build_defence_json(dfs,filters)
    return jsonify(data)

@app.route("/match-wise")
def get_match_wise():
    filters = {}

    if request.args.get("tournament_id"):
        filters["tournament_id"] = int(request.args.get("tournament_id"))

    if request.args.get("season_id"):
        filters["season_id"] = int(request.args.get("season_id"))

    if request.args.get("match_id"):
        filters["match_id"] = int(request.args.get("match_id"))

    if request.args.get("team_id"):
        filters["team_id"] = int(request.args.get("team_id"))
    dfs=load_clean_data()
    data=build_match_wise(dfs,filters)
    return jsonify(data)

@app.route("/LeaderBoard-Season")
def get_leaderboard_season():
    dfs=load_clean_data()
    data=LeaderBoard(dfs)
    return jsonify(data)

if __name__ == "__main__":
   app.run(debug=True)

