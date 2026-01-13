from flask import Flask, render_template, request, jsonify
import os
import json
from datetime import datetime

# Konfigurasi
DATA_DIR = 'data'
DATA_FILE = os.path.join(DATA_DIR, 'user_data.json')
os.makedirs(DATA_DIR, exist_ok=True)

# Basis pengetahuan gejala → rekomendasi
KNOWLEDGE_BASE = {
    "demam": "Anda mungkin mengalami infeksi ringan seperti flu atau demam biasa. Istirahat cukup, minum air putih, dan pantau suhu tubuh. Jika demam >3 hari atau >39°C, segera ke fasilitas kesehatan.",
    "batuk": "Batuk bisa disebabkan oleh alergi, infeksi saluran napas, atau iritasi. Hindari asap rokok dan minum air hangat. Jika batuk berdahak hijau/kuning atau berlangsung >2 minggu, periksakan ke dokter.",
    "sakit kepala": "Sakit kepala sering disebabkan oleh stres, kurang tidur, atau dehidrasi. Coba istirahat di tempat tenang dan minum air. Jika sakit kepala sangat hebat atau disertai muntah/penglihatan kabur, segera cari pertolongan medis.",
    "mual": "Mual bisa terjadi karena masalah pencernaan, mabuk perjalanan, atau infeksi. Hindari makanan berminyak. Jika mual disertai muntah terus-menerus atau nyeri perut hebat, segera ke puskesmas.",
    "nyeri sendi": "Nyeri sendi bisa akibat aktivitas berlebihan atau radang sendi. Istirahat dan kompres hangat. Jika bengkak atau tidak membaik dalam 3 hari, konsultasikan ke tenaga kesehatan.",
    "sesak napas": "SESUATU YANG SERIUS! Segera cari pertolongan medis. Sesak napas bisa tanda asma, infeksi paru, atau masalah jantung.",
    "diare": "Minum oralit untuk cegah dehidrasi. Hindari makanan pedas dan susu. Jika diare >3 hari atau disertai darah, segera ke fasilitas kesehatan.",
}

COMMON_SYMPTOMS = sorted(KNOWLEDGE_BASE.keys())

app = Flask(__name__)

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"profile": {}, "history": []}
    return {"profile": {}, "history": []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('index.html', symptoms=COMMON_SYMPTOMS)

# API: Simpan profil
@app.route('/api/profile', methods=['POST'])
def save_profile():
    data = load_data()
    profile = request.json
    data['profile'] = profile
    save_data(data)
    return jsonify({"status": "success"})

# API: Analisis gejala
@app.route('/api/check', methods=['POST'])
def check_symptom():
    data = load_data()
    symptom = request.json.get('symptom', '').lower().strip()
    
    # Cari rekomendasi
    recommendation = "Gejala tidak dikenali. Kami sarankan Anda segera berkonsultasi dengan tenaga kesehatan profesional."
    for key in KNOWLEDGE_BASE:
        if key in symptom:
            recommendation = KNOWLEDGE_BASE[key]
            break

    # Simpan ke riwayat
    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "gejala": symptom,
        "rekomendasi": recommendation
    }
    data['history'].append(record)
    save_data(data)

    return jsonify({
        "gejala": symptom,
        "rekomendasi": recommendation
    })

# API: Ambil data
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(load_data())

if __name__ == '__main__':
    print("\n🚀 SehatPintar Web App Siap Digunakan!")
    print("Buka di browser: http://127.0.0.1:5000\n")
    app.run(debug=False, host='127.0.0.1', port=5000)