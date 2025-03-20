# Projet_Pression_Arterielle_FHIR

# Surveillance des Données de Pression Artérielle avec FHIR et Kafka  

## Introduction  

Ce projet met en place un **système de surveillance des données de pression artérielle** en **temps réel** à l’aide de **FHIR (Fast Healthcare Interoperability Resources)** et **Apache Kafka**.  
L'objectif est d'assurer une **collecte, analyse et visualisation efficace** des données de pression artérielle, en utilisant **Elasticsearch et Kibana** pour détecter et suivre les anomalies telles que l'hypertension et l'hypotension.  

## Objectifs  

✔ **Générer des messages FHIR** contenant les mesures de pression artérielle.  
✔ **Transmettre ces messages** via Kafka.  
✔ **Analyser les données en temps réel** pour détecter les anomalies.  
✔ **Stocker et indexer les données** dans Elasticsearch.  
✔ **Visualiser les résultats** sur un tableau de bord Kibana.  

## Technologies utilisées  

**Interopérabilité Santé** : FHIR (Fast Healthcare Interoperability Resources)  
**Streaming & Messaging** : Apache Kafka  
**Stockage & Indexation** : Elasticsearch  
**Visualisation** : Kibana  
**Langages** : Python  
**Bibliothèques** : `fhir.resources`, `kafka-python`, `elasticsearch`, `faker`  
**Orchestration** : Docker & Docker Compose  

## Installation et configuration  

### 1️⃣ **Cloner le dépôt**  
```bash
git clone https://github.com/jalakshana/Projet_Pression_Arterielle_FHIR.git
```
2️⃣ **Démarrer l’environnement Docker**
```bash
docker-compose up -d
```
3️⃣ **Installer les dépendances Python**
```bash
pip install -r requirements.txt
```
4️⃣ **Générer et publier des messages FHIR**
```bash
python generate_fhir.py
python producer.py
```
5️⃣ **Consommer les messages et analyser les données**
```bash
python consumer.py
```
6️⃣ **Accéder au Tableau de Bord Kibana**
Ouvrir un navigateur et aller à : http://localhost:5601

## Fonctionnement du Système

**Génération des messages FHIR**
* Le script generate_fhir.py crée des données conformes à la norme FHIR avec des valeurs aléatoires pour la pression systolique et diastolique.
* Les données sont stockées sous forme de fichiers JSON avant d’être envoyées à Kafka.

**Transmission des données via Kafka**
* producer.py publie les messages sur un topic Kafka appelé blood_pressure_readings.
* Kafka assure la distribution des messages à plusieurs consommateurs.

**Analyse des données et détection des anomalies**

consumer.py récupère les données Kafka et vérifie les valeurs de pression :
* Hypertension : Systolique > 140 mmHg ou Diastolique > 90 mmHg
* Hypotension : Systolique < 90 mmHg ou Diastolique < 60 mmHg

Les anomalies sont indexées dans Elasticsearch pour un suivi à long terme.

**Visualisation dans Kibana**
Un dashboard Kibana permet de voir :
* Distribution des pressions artérielles
* Détection des anomalies en temps réel
* Évolution des anomalies sur une période donnée
