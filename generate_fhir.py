from fhir.resources.observation import Observation
from faker import Faker
import json

# Initialisation de Faker pour générer des données aléatoires
fake = Faker()

def generate_fhir_observation(patient_id, systolic, diastolic):
    """Génère une ressource FHIR Observation pour la pression artérielle."""
    observation = Observation(
        resourceType="Observation",
        id=fake.uuid4(),
        status="final",
        category=[{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "vital-signs",
                "display": "Vital Signs"
            }]
        }],
        code={
            "coding": [{
                "system": "http://loinc.org",
                "code": "85354-9",
                "display": "Blood pressure panel"
            }]
        },
        subject={"reference": f"Patient/{patient_id}"},
        component=[
            {
                "code": {"coding": [{"code": "8480-6", "display": "Systolic Blood Pressure"}]},
                "valueQuantity": {"value": systolic, "unit": "mmHg", "system": "http://unitsofmeasure.org"}
            },
            {
                "code": {"coding": [{"code": "8462-4", "display": "Diastolic Blood Pressure"}]},
                "valueQuantity": {"value": diastolic, "unit": "mmHg", "system": "http://unitsofmeasure.org"}
            }
        ]
    )
    return observation.dict()

# Exemple d'utilisation
if __name__ == "__main__":
    patient_id = "patient-123"
    systolic = 120  # Exemple de pression systolique
    diastolic = 80  # Exemple de pression diastolique
    observation = generate_fhir_observation(patient_id, systolic, diastolic)
    
    # Sauvegarder le message dans un fichier JSON
    with open("blood_pressure.json", "w") as f:
        json.dump(observation, f, indent=2)

    print("Message FHIR généré et sauvegardé dans blood_pressure.json")