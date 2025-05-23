@echo off
REM Script d'installation pour DreamsEcho

echo ===================================================
echo Installation de DreamsEcho - Journal de rêves IA
echo ===================================================

echo [ÉTAPE 1/4] Vérification de Python...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Erreur: Python n'est pas installé ou n'est pas dans le PATH.
    echo Veuillez installer Python 3.8 ou supérieur depuis https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [ÉTAPE 2/4] Création de l'environnement virtuel...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo Erreur lors de la création de l'environnement virtuel.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo Erreur lors de l'activation de l'environnement virtuel.
    pause
    exit /b 1
)

echo [ÉTAPE 3/4] Installation des dépendances...
pip install --upgrade pip
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo Erreur lors de l'installation des dépendances.
    pause
    exit /b 1
)

echo [ÉTAPE 4/4] Configuration initiale...
if not exist .env (
    copy .env.example .env
    echo Un fichier .env a été créé. Veuillez le configurer avec vos clés API.
) else (
    echo Le fichier .env existe déjà. Assurez-vous qu'il est correctement configuré.
)

echo.
echo ===================================================
echo Installation terminée avec succès !
echo ===================================================
echo.
echo Pour lancer l'application, exécutez :
echo   1. venv\Scripts\activate.bat
echo   2. streamlit run app/main.py
echo.
pause
