import logging
logging.basicConfig(level=logging.DEBUG)  # Activer les logs détaillés

from kafka import KafkaProducer
import json
import time
import random
from faker import Faker
from fhir.resources.observation import Observation
from fhir.resources.patient import Patient


# Initialisation du générateur de données fictives
fake = Faker()


# Configuration du producteur Kafka
producer = KafkaProducer(
    bootstrap_servers="localhost:9093",
    value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')
)


# Génération d'une observation FHIR de pression artérielle
def generate_fhir_observation():
    patient_id = fake.uuid4()


    # Création d'un patient FHIR
    patient = Patient.parse_obj({
        "resourceType": "Patient",
        "id": patient_id,
        "name": [{"use": "official", "family": fake.last_name(), "given": [fake.first_name()]}],
        "gender": random.choice(["male", "female"]),
        "birthDate": fake.date_of_birth(minimum_age=20, maximum_age=80).isoformat(),
    })


    # Génération des valeurs de pression artérielle
    systolic = random.randint(90, 180)
    diastolic = random.randint(60, 120)


    # Création de l'observation FHIR
    observation = Observation.parse_obj({
        "resourceType": "Observation",
        "id": fake.uuid4(),
        "status": "final",
        "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "vital-signs"}]}],
        "code": {"coding": [{"system": "http://loinc.org", "code": "85354-9", "display": "Blood pressure panel"}]},
        "subject": {"reference": f"Patient/{patient_id}"},
        "component": [
            {
                "code": {"coding": [{"system": "http://loinc.org", "code": "8480-6", "display": "Systolic blood pressure"}]},
                "valueQuantity": {"value": systolic, "unit": "mmHg", "system": "http://unitsofmeasure.org", "code": "mm[Hg]"}
            },
            {
                "code": {"coding": [{"system": "http://loinc.org", "code": "8462-4", "display": "Diastolic blood pressure"}]},
                "valueQuantity": {"value": diastolic, "unit": "mmHg", "system": "http://unitsofmeasure.org", "code": "mm[Hg]"}
            }
        ]
    })


    return {
        "patient": patient.dict(),
        "observation": observation.dict()
    }


# Envoi des messages à Kafka
topic = "blood_pressure_readings"


print(f"🔵 Envoi des messages sur Kafka (Topic: {topic})...")


for _ in range(10):  # Envoi de 10 messages pour tester
    data = generate_fhir_observation()
    producer.send(topic, value=data)
    print(f"✅ Message envoyé : {data['observation']['id']} (Systolic: {data['observation']['component'][0]['valueQuantity']['value']} mmHg, Diastolic: {data['observation']['component'][1]['valueQuantity']['value']} mmHg)")
    time.sleep(1)


print("🔴 Fin de l'envoi des messages.")
producer.close()
