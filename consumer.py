import json
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from datetime import datetime  # ✅ Importation du module datetime
import os

# 🔌 Configuration Kafka
KAFKA_BROKER = "localhost:9093"  # Vérifie si ce port est correct
TOPIC_NAME = "blood_pressure_readings"

# 📊 Configuration Elasticsearch
ELASTICSEARCH_HOST = "http://host.docker.internal:9200"
INDEX_NAME = "blood_pressure_anomalies_v2"

# 🔗 Connexion à Elasticsearch
es = Elasticsearch([ELASTICSEARCH_HOST])

# 📌 Vérifier et créer l'index si nécessaire
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME, body={})

# 🛠 Connexion au Kafka Consumer
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    group_id="blood_pressure_group",
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("🔵 En attente de messages...")

# 🔄 Lecture des messages Kafka
for message in consumer:
    data = message.value
    
    patient_id = data["patient"]["id"]
    
    systolic = None
    diastolic = None

    # 🔍 Extraction des valeurs de pression artérielle
    for component in data["observation"]["component"]:
        code = component["code"]["coding"][0]["code"]
        value = component["valueQuantity"]["value"]

        if code == "8480-6":  # Systolic Blood Pressure
            systolic = value
        elif code == "8462-4":  # Diastolic Blood Pressure
            diastolic = value

    # ✅ Ajout du timestamp correct
    if "effectiveDateTime" in data["observation"]:
        timestamp = data["observation"]["effectiveDateTime"]  # ✅ Timestamp fourni dans le message
    else:
        timestamp = datetime.utcnow().isoformat()  # ✅ Génération d'un timestamp UTC

    print(f"📥 Message reçu - Patient {patient_id} : {systolic}/{diastolic} mmHg à {timestamp}")

    # 🔍 Détection des anomalies
    anomaly_type = None
    if systolic and diastolic:
        if systolic > 140 or diastolic > 90:
            anomaly_type = "Hypertension"
        elif systolic < 90 or diastolic < 60:
            anomaly_type = "Hypotension"

    # 🚨 Si une anomalie est détectée, l'indexer dans Elasticsearch
    if anomaly_type:
        print(f"⚠️ Anomalie détectée pour le patient {patient_id} ({anomaly_type}) !")

        anomaly_data = {
            "patient_id": patient_id,
            "systolic_pressure": systolic,
            "diastolic_pressure": diastolic,
            "anomaly_type": anomaly_type,
            "timestamp": timestamp  # ✅ Timestamp correct
        }

        es.index(index=INDEX_NAME, document=anomaly_data)
        print(f"✅ Anomalie indexée dans Elasticsearch : {anomaly_data}")
