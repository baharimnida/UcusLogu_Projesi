from flask import Flask, jsonify
import json

app = Flask(__name__)

def load_data():
    with open('logs.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/flight/<int:team_id>', methods=['GET'])
def get_flight(team_id):
    all_time_steps = load_data()
    team_route = []

    # JSON içindeki her bir zaman dilimini geziyoruz
    for time_step in all_time_steps:
        # Her dilimin içindeki 'konumBilgileri' listesine bakıyoruz
        for entry in time_step.get("konumBilgileri", []):
            if entry["takim_numarasi"] == team_id:
                # Koordinatları standart isimlere (lat, lon, alt) çevirerek listeye ekliyoruz
                team_route.append({
                    "lat": entry["iha_enlem"],
                    "lon": entry["iha_boylam"],
                    "alt": entry["iha_irtifa"]
                })
    
    if team_route:
        return jsonify({
            "status": "success",
            "team": team_id,
            "data": team_route
        })
    else:
        return jsonify({"status": "error", "message": f"Takım {team_id} bulunamadı!"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)