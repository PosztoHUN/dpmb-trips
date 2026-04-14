from flask import Flask, jsonify, render_template
import random
from datetime import datetime

app = Flask(__name__)

# ------------------------
# VONALRENDSZER
# ------------------------

TRAM = list(range(1, 11)) + [12]
TROLLEY = list(range(25, 28)) + list(range(30, 40))

BUS = (
    [40, 41, 42, 44, 46, 47, 49, 50, "E50", 52, 54, 55, "E56", 57, 58, 62]
    + list(range(64, 73))
    + [75, "E75", "E76", 77, 78, 80, 84, "š85", "š86", "š88"]
)

NIGHT = [f"N{i}" for i in range(89, 100)]

# minden együtt (szimulációhoz)
ALL_LINES = TRAM + TROLLEY + BUS + NIGHT 

def line_type(line):
    s = str(line)

    if s.startswith("N"):
        return "night"
    if line in TRAM:
        return "tram"
    if line in TROLLEY:
        return "trolley"
    return "bus"


def generate_event():
    line = random.choice(ALL_LINES)
    ltype = line_type(line)

    events = [
        "Menetrend módosítás",
        "Késés frissítés",
        "Járműcsere",
        "Rövidített útvonal",
        "Sűrítés csúcsidőben",
        "Forgalmi zavar",
    ]

    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "line": str(line),
        "type": ltype,
        "event": random.choice(events)
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/history")
def history():
    return jsonify([generate_event() for _ in range(20)])


if __name__ == "__main__":
    app.run(debug=True)
    
    
from flask import Flask, jsonify, render_template
import requests
from collections import defaultdict

app = Flask(__name__)

API_URL = "https://mapa.idsjmk.cz/api/vehicles.json"


def format_vehicle(v):
    parts = []

    # csak ha nem 0
    if v.get("ID", 0):
        parts.append(str(v["ID"]))
    if v.get("IDB", 0):
        parts.append(str(v["IDB"]))
    if v.get("IDC", 0):
        parts.append(str(v["IDC"]))

    return " ".join(parts)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/lines")
def lines():
    data = requests.get(API_URL, timeout=10).json()

    grouped = defaultdict(list)

    for v in data:
        line = v.get("LineID")
        grouped[line].append(format_vehicle(v))

    result = []

    for line, vehicles in grouped.items():
        # üres stringeket kiszűrjük
        vehicles = [v for v in vehicles if v.strip() != ""]

        result.append({
            "line": line,
            "vehicles": vehicles
        })

    # rendezés vonal szerint
    result.sort(key=lambda x: str(x["line"]))

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)