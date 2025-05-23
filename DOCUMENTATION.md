# Documentation de DreamsEcho

## Table des matières
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Utilisation](#utilisation)
5. [Fonctionnalités](#fonctionnalités)
6. [Dépannage](#dépannage)
7. [FAQ](#faq)

## Introduction

DreamsEcho est une application qui vous permet d'enregistrer, d'analyser et de visualiser vos rêves grâce à l'intelligence artificielle. Transformez vos expériences oniriques en œuvres d'art uniques et découvrez des modèles récurrents dans vos rêves.

## Installation

### Prérequis
- Python 3.8 ou supérieur
- Un accès à Internet pour les fonctionnalités d'IA
- Comptes développeurs pour les API externes (OpenAI, etc.)

### Installation automatique (Windows)
1. Téléchargez le fichier `Install_DreamsEcho.bat`
2. Exécutez-le en tant qu'administrateur
3. Suivez les instructions à l'écran

### Installation manuelle
1. Clonez le dépôt :
   ```bash
   git clone [URL_DU_DEPOT]
   cd dreamsecho
   ```
2. Créez un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur macOS/Linux
   .\venv\Scripts\activate  # Sur Windows
   ```
3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Copiez le fichier `.env.example` vers `.env` :
   ```bash
   cp .env.example .env
   ```
2. Modifiez le fichier `.env` avec vos clés API :
   ```
   OPENAI_API_KEY=votre_cle_api_openai
   STABILITY_API_KEY=votre_cle_stability
   ```

## Utilisation

### Lancer l'application
```bash
streamlit run app/main.py
```

### Ajouter un nouveau rêve
1. Cliquez sur l'onglet "Accueil"
2. Remplissez le formulaire avec les détails de votre rêve
3. Cliquez sur "Enregistrer et Analyser"
4. Attendez que l'analyse et la génération d'image se terminent

### Parcourir vos rêves
1. Allez dans l'onglet "Ma Collection"
2. Parcourez vos rêves enregistrés
3. Utilisez la barre de recherche pour trouver des rêves spécifiques

### Consulter les analyses
1. Accédez à l'onglet "Analyses"
2. Consultez les statistiques et graphiques
3. Explorez les tendances sur différentes périodes

## Fonctionnalités

### Journal des rêves
- Enregistrement détaillé des rêves
- Mots-clés et étiquettes
- Recherche et filtrage avancés

### Analyse IA
- Détection des thèmes principaux
- Analyse des émotions
- Identification des symboles récurrents

### Génération de contenu
- Création d'images à partir des descriptions
- Styles artistiques personnalisables
- Exportation des créations

## Dépannage

### L'application ne se lance pas
- Vérifiez que Python 3.8+ est installé
- Assurez-vous que toutes les dépendances sont installées
- Consultez les journaux d'erreur dans la console

### Problèmes de génération d'images
- Vérifiez votre connexion Internet
- Assurez-vous que votre clé API est valide
- Réduisez la taille ou la complexité de l'image

## FAQ

### Puis-je utiliser l'application hors ligne ?
Certaines fonctionnalités nécessitent une connexion Internet pour les appels API d'IA.

### Comment sauvegarder mes données ?
Les données sont stockées localement dans le dossier `data/`. Faites-en des sauvegardes régulières.

### Puis-je importer/exporter mes rêves ?
Oui, utilisez la fonction d'exportation dans les paramètres pour sauvegarder ou transférer vos données.
