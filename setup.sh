#!/bin/bash

# Installation des dépendances Python
pip install -r requirements.txt

# Téléchargement des modèles spaCy
python -m spacy download fr_core_news_md
python -m spacy download en_core_web_md

# Création du dossier pour les données
mkdir -p data

# Configuration des permissions
chmod -R 755 .
