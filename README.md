# 🌙 DreamsEcho

Une application qui transforme vos rêves en une expérience visuelle et auditive unique en utilisant l'IA.

## 🚀 Fonctionnalités

- **Journal des rêves** : Enregistrez et suivez vos rêves quotidiennement
- **Analyse IA** : Détection des thèmes, émotions et symboles récurrents
- **Génération de contenu** : Création d'images et vidéos basées sur vos rêves
- **Rapports personnalisés** : Analyses détaillées de vos tendances de sommeil
- **Interface intuitive** : Navigation facile et design moderne
- **Sécurisé** : Données stockées en toute sécurité avec chiffrement

## 🛠 Installation Locale

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/votre-utilisateur/dreamsecho-ai.git
   cd dreamsecho-ai
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**
   - Créez un fichier `.streamlit/secrets.toml`
   - Copiez le contenu de `.streamlit/secrets.example.toml`
   - Remplacez les valeurs par vos clés API

5. **Lancer l'application**
   ```bash
   streamlit run app/main.py
   ```

## ☁️ Déploiement sur Streamlit Cloud

1. **Prérequis**
   - Compte GitHub
   - Compte Streamlit Cloud (gratuit)
   - Clé API OpenAI (obligatoire)

2. **Étapes de déploiement**
   1. Poussez votre code sur GitHub
   2. Connectez-vous à [Streamlit Cloud](https://share.streamlit.io/)
   3. Cliquez sur "New app"
   4. Sélectionnez votre dépôt et la branche
   5. Dans "Main file path", entrez: `app/main.py`
   6. Dans "Advanced settings", ajoutez vos clés API:
      ```
      OPENAI_API_KEY=votre_cle_openai
      STABILITY_API_KEY=votre_cle_stability
      ```
   7. Cliquez sur "Deploy!"

3. **Configuration des secrets**
   - Allez dans les paramètres de votre application Streamlit Cloud
   - Sélectionnez "Secrets"
   - Ajoutez vos clés API au format:
     ```
     OPENAI_API_KEY=votre_cle_openai
     STABILITY_API_KEY=votre_cle_stability
     ```

## 🔑 Configuration requise

### Clés API nécessaires

1. **OpenAI API** (obligatoire)
   - Pour l'analyse des rêves et la génération d'images
   - Obtenez une clé sur [platform.openai.com](https://platform.openai.com/api-keys)
   - Variable d'environnement: `OPENAI_API_KEY`

2. **Stability AI** (optionnel)
   - Pour la génération d'images avancée
   - Obtenez une clé sur [platform.stability.ai](https://platform.stability.ai/)
   - Variable d'environnement: `STABILITY_API_KEY`

## 📁 Structure du projet

```
dreamsecho-ai/
├── app/                      # Code source principal
│   ├── database/            # Modèles et accès aux données
│   ├── services/            # Logique métier
│   ├── static/              # Fichiers statiques (CSS, images)
│   └── main.py              # Point d'entrée de l'application
├── .streamlit/              # Configuration Streamlit
│   ├── config.toml          # Configuration de l'application
│   └── secrets.toml         # Clés API (ne pas versionner)
├── data/                    # Données de l'application
├── tests/                   # Tests unitaires
├── .env.example             # Exemple de configuration
├── .gitignore
├── requirements.txt         # Dépendances Python
├── setup.sh                 # Script d'installation
└── README.md
```

## 🔧 Technologies utilisées

- **Backend** : Python, Streamlit
- **Base de données** : SQLite (pour le développement), PostgreSQL (pour la production)
- **IA** : OpenAI (GPT-4, DALL-E), Stable Diffusion
- **Traitement vidéo** : MoviePy

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📬 Contact

Pour toute question ou suggestion, contactez-nous à [votre@email.com]
