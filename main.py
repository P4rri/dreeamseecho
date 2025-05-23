"""
Application principale DreamsEcho - Plateforme d'analyse et de visualisation de rêves
"""
import os
import json
import base64
import streamlit as st
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Configuration
from dotenv import load_dotenv
load_dotenv()

# Import des services
from app.services.dream_analyzer import DreamAnalyzer
from app.services.image_generator import ImageGenerator
from app.utils.ui_components import (
    display_sidebar,
    display_dream_form,
    display_dream_analysis,
    display_dream_gallery
)

# Configuration des dossiers
BASE_DIR = Path(__file__).parent.parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
GENERATED_FOLDER = BASE_DIR / "generated"

# Création des dossiers nécessaires
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)

# Initialisation des services avec cache
@st.cache_resource
def get_dream_analyzer():
    return DreamAnalyzer()

@st.cache_resource
def get_image_generator():
    return ImageGenerator(output_dir=str(GENERATED_FOLDER))

# Configuration de la page
st.set_page_config(
    page_title="DreamsEcho - Votre journal de rêves intelligent",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Variables de session
if 'dreams' not in st.session_state:
    st.session_state.dreams = []
if 'current_dream' not in st.session_state:
    st.session_state.current_dream = None
if 'show_analysis' not in st.session_state:
    st.session_state.show_analysis = False

# Fonctions utilitaires
def save_dream(dream_data: Dict[str, Any]) -> Dict[str, Any]:
    """Sauvegarde un nouveau rêve avec analyse et génération d'image si demandé."""
    try:
        # Générer un ID unique pour le rêve
        dream_id = len(st.session_state.dreams) + 1
        dream_data['id'] = dream_id
        
        # Ajouter la date de création si non fournie
        if 'created_at' not in dream_data:
            dream_data['created_at'] = datetime.now().isoformat()
        
        # Générer une image si demandé
        if dream_data.get('generate_image'):
            try:
                image_gen = get_image_generator()
                image_path = Path(GENERATED_FOLDER) / f"dream_{dream_id}_{int(datetime.now().timestamp())}.png"
                
                # Créer un prompt à partir du contenu du rêve
                prompt = f"Une illustration de style {dream_data.get('style', 'fantasy')} représentant: {dream_data['content'][:500]}"
                
                # Générer l'image
                success = image_gen.generate_image(
                    prompt=prompt,
                    style=dream_data.get('style', 'fantasy'),
                    size_preset=dream_data.get('size', 'hd'),
                    output_path=str(image_path)
                )
                
                if success and image_path.exists():
                    dream_data['image_path'] = str(image_path)
                    st.session_state.current_dream = dream_data  # Mettre à jour le rêve courant
                else:
                    st.error("Échec de la génération de l'image.")
            except Exception as e:
                st.error(f"Erreur lors de la génération de l'image: {str(e)}")
        
        # Analyser le rêve si demandé
        if dream_data.get('analyze_dream', True):
            try:
                analyzer = get_dream_analyzer()
                analysis = analyzer.analyze_dream_content(dream_data['content'])
                dream_data['analysis'] = analysis
                st.session_state.show_analysis = True
            except Exception as e:
                st.error(f"Erreur lors de l'analyse du rêve: {str(e)}")
        
        # Ajouter le rêve à la liste
        st.session_state.dreams.append(dream_data)
        
        # Sauvegarder dans un fichier (pour la démo)
        save_dreams_to_file()
        
        return dream_data
        
    except Exception as e:
        st.error(f"Une erreur est survenue lors de la sauvegarde du rêve: {str(e)}")
        return None

def save_dreams_to_file():
    """Sauvegarde les rêves dans un fichier JSON."""
    try:
        with open(Path(GENERATED_FOLDER) / 'dreams.json', 'w', encoding='utf-8') as f:
            json.dump(st.session_state.dreams, f, ensure_ascii=False, indent=2, default=str)
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde des rêves: {str(e)}")

def load_dreams_from_file():
    """Charge les rêves depuis le fichier JSON."""
    try:
        dreams_file = Path(GENERATED_FOLDER) / 'dreams.json'
        if dreams_file.exists():
            with open(dreams_file, 'r', encoding='utf-8') as f:
                st.session_state.dreams = json.load(f)
    except Exception as e:
        st.error(f"Erreur lors du chargement des rêves: {str(e)}")
        st.session_state.dreams = []

def clear_form():
    """Réinitialise le formulaire."""
    st.session_state.current_dream = None
    st.session_state.show_analysis = False

# Pages de l'application
def show_home_page():
    """Affiche la page d'accueil avec le formulaire de nouveau rêve."""
    st.title("🌙 DreamsEcho")
    st.markdown("""
    ### Votre journal de rêves intelligent
    
    Découvrez la signification de vos rêves et créez des illustrations uniques 
    grâce à la puissance de l'intelligence artificielle.
    """)
    
    # Affichage du formulaire
    dream_data = display_dream_form()
    
    # Traitement du formulaire
    if dream_data:
        with st.spinner("Analyse de votre rêve en cours..."):
            saved_dream = save_dream(dream_data)
            if saved_dream:
                st.session_state.current_dream = saved_dream
                st.success("Votre rêve a été enregistré avec succès !")
                
                # Afficher l'image générée si disponible
                if 'image_path' in saved_dream and os.path.exists(saved_dream['image_path']):
                    st.image(
                        saved_dream['image_path'],
                        caption=f"Illustration de votre rêve - Style {saved_dream.get('style', 'fantasy')}",
                        use_column_width=True
                    )
                
                # Afficher l'analyse si disponible
                if 'analysis' in saved_dream and saved_dream['analysis']:
                    display_dream_analysis(saved_dream['analysis'])
                
                # Bouton pour ajouter un autre rêve
                if st.button("Ajouter un autre rêve", type="primary"):
                    clear_form()
                    st.rerun()
    
    # Afficher l'analyse du rêve courant si disponible
    elif st.session_state.get('show_analysis') and st.session_state.get('current_dream') and 'analysis' in st.session_state.current_dream:
        display_dream_analysis(st.session_state.current_dream['analysis'])

def show_gallery_page():
    """Affiche la galerie des rêves enregistrés."""
    st.title("📚 Ma Collection de Rêves")
    
    # Charger les rêves depuis le fichier
    if not st.session_state.dreams:
        load_dreams_from_file()
    
    # Afficher la galerie
    display_dream_gallery(st.session_state.dreams)

def show_analysis_page():
    """Affiche les analyses et statistiques des rêves."""
    st.title("📊 Analyses et Statistiques")
    
    if not st.session_state.dreams:
        st.info("Aucun rêve à analyser. Commencez par ajouter un rêve !")
        return
    
    # Statistiques de base
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total des rêves", len(st.session_state.dreams))
    with col2:
        st.metric("Dernier ajout", 
                 datetime.fromisoformat(max(d['created_at'] for d in st.session_state.dreams)).strftime('%d/%m/%Y') 
                 if st.session_state.dreams else "-")
    with col3:
        styles = [d.get('style', 'inconnu') for d in st.session_state.dreams if 'style' in d]
        if styles:
            most_common_style = max(set(styles), key=styles.count)
            st.metric("Style le plus utilisé", most_common_style.capitalize())
    
    # Graphique des émotions
    st.subheader("Émotions dominantes")
    if any('analysis' in d and 'emotions' in d['analysis'] for d in st.session_state.dreams):
        # Préparer les données pour le graphique
        emotions_data = []
        for dream in st.session_state.dreams:
            if 'analysis' in dream and 'emotions' in dream['analysis']:
                for emotion, intensity in dream['analysis']['emotions'].items():
                    emotions_data.append({
                        'date': dream.get('created_at', ''),
                        'emotion': emotion,
                        'intensity': intensity
                    })
        
        if emotions_data:
            import pandas as pd
            import plotly.express as px
            
            df = pd.DataFrame(emotions_data)
            if not df.empty:
                # Convertir la date en datetime
                df['date'] = pd.to_datetime(df['date']).dt.date
                
                # Créer un graphique à barres groupées
                fig = px.bar(
                    df.groupby(['date', 'emotion'])['intensity'].mean().reset_index(),
                    x='date',
                    y='intensity',
                    color='emotion',
                    title='Évolution des émotions dans le temps',
                    labels={'intensity': 'Intensité', 'date': 'Date', 'emotion': 'Émotion'}
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Liste des rêves avec analyses
    st.subheader("Dernières analyses")
    for dream in sorted(st.session_state.dreams, 
                       key=lambda x: x.get('created_at', ''), 
                       reverse=True)[:5]:
        if 'analysis' in dream:
            with st.expander(f"{dream.get('title', 'Sans titre')} - {dream.get('created_at', '')}"):
                display_dream_analysis(dream['analysis'])

def show_settings_page():
    """Affiche la page des paramètres."""
    st.title("⚙️ Paramètres")
    
    st.subheader("Compte")
    st.text_input("Nom d'utilisateur", value="utilisateur")
    st.text_input("Email", value="utilisateur@example.com")
    
    st.subheader("Préférences")
    theme = st.selectbox("Thème de l'application", ["Clair", "Sombre", "Système"])
    language = st.selectbox("Langue", ["Français", "Anglais", "Espagnol"])
    
    st.subheader("Confidentialité")
    st.checkbox("Partager les données de manière anonyme pour améliorer le service", value=True)
    
    if st.button("Enregistrer les paramètres", type="primary"):
        st.success("Paramètres enregistrés avec succès !")

def show_dreams_list():
    """Affiche la liste des rêves enregistrés."""
    st.header("📚 Mes Rêves")
    
    # Filtres
    st.subheader("Filtres")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date_filter = st.selectbox(
            "Période",
            ["Tous", "Aujourd'hui", "7 derniers jours", "30 derniers jours", "Personnalisé"]
        )
    
    with col2:
        mood_filter = st.multiselect(
            "Humeur",
            ["😊 Heureux", "😐 Neutre", "😔 Triste", "😨 Effrayé", "😡 En colère", "😴 Paisible"]
        )
    
    with col3:
        type_filter = st.multiselect(
            "Type de rêve",
            ["Normal", "Lucid", "Cauchemar", "Rêve éveillé", "Rêve récurrent"]
        )
    
    # Requête de base
    db = get_db_session()
    try:
        query = db.query(Dream).filter(Dream.user_id == st.session_state.user_id)
        
        # Application des filtres
        if date_filter == "Aujourd'hui":
            today = datetime.now().date()
            query = query.filter(Dream.date == today)
        elif date_filter == "7 derniers jours":
            week_ago = datetime.now().date() - timedelta(days=7)
            query = query.filter(Dream.date >= week_ago)
        elif date_filter == "30 derniers jours":
            month_ago = datetime.now().date() - timedelta(days=30)
            query = query.filter(Dream.date >= month_ago)
        
        if mood_filter:
            query = query.filter(Dream.mood.in_(mood_filter))
            
        if type_filter:
            query = query.filter(Dream.dream_type.in_(type_filter))
        
        # Tri et pagination
        dreams = query.order_by(Dream.date.desc()).all()
        
        # Affichage des résultats
        st.subheader(f"Résultats ({len(dreams)} rêves trouvés)")
        
        if not dreams:
            st.info("Aucun rêve trouvé avec les critères sélectionnés.")
            return
        
        # Affichage des rêves
        for dream in dreams:
            display_dream(dream)
            
    except Exception as e:
        st.error(f"Une erreur est survenue: {str(e)}")
    finally:
        db.close()

def show_gallery():
    """Affiche la galerie des rêves sous forme visuelle."""
    st.header("🎨 Galerie des Rêves")
    
    # Récupération des rêves avec images
    db = get_db_session()
    try:
        dreams = db.query(Dream).filter(
            Dream.user_id == st.session_state.user_id,
            Dream.image_path.isnot(None)
        ).order_by(Dream.date.desc()).all()
        
        if not dreams:
            st.info("Aucune image de rêve disponible. Créez des rêves avec des images pour les voir ici !")
            return
        
        # Affichage en grille
        cols = st.columns(3)
        
        for idx, dream in enumerate(dreams):
            with cols[idx % 3]:
                if dream.image_path and os.path.exists(dream.image_path):
                    st.image(
                        dream.image_path,
                        caption=f"{dream.title} - {dream.date.strftime('%d/%m/%Y')}",
                        use_column_width=True
                    )
                    st.caption(f"{dream.mood} • {dream.dream_type}")
    
    except Exception as e:
        st.error(f"Une erreur est survenue: {str(e)}")
    finally:
        db.close()

def show_statistics():
    """Affiche les statistiques et analyses des rêves."""
    st.header("📊 Statistiques")
    
    # Récupération des données
    db = get_db_session()
    try:
        dreams = db.query(Dream).filter(
            Dream.user_id == st.session_state.user_id
        ).all()
        
        if not dreams:
            st.info("Aucun rêve enregistré pour le moment. Commencez par ajouter des rêves pour voir les statistiques !")
            return
        
        # Préparation des données pour les graphiques
        df = pd.DataFrame([{
            'date': dream.date,
            'mood': dream.mood,
            'sleep_quality': dream.sleep_quality,
            'dream_type': dream.dream_type,
            'word_count': len(dream.content.split()) if dream.content else 0
        } for dream in dreams])
        
        # Statistiques générales
        st.subheader("Aperçu général")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Nombre total de rêves", len(dreams))
        with col2:
            avg_quality = df['sleep_quality'].mean()
            st.metric("Qualité moyenne du sommeil", f"{avg_quality:.1f}/10")
        with col3:
            avg_length = df['word_count'].mean()
            st.metric("Longueur moyenne des rêves", f"{avg_length:.0f} mots")
        
        # Graphique des humeurs
        st.subheader("Répartition des humeurs")
        mood_counts = df['mood'].value_counts()
        fig1 = px.pie(
            mood_counts,
            values=mood_counts.values,
            names=mood_counts.index,
            hole=0.4
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Graphique de l'évolution de la qualité du sommeil
        st.subheader("Évolution de la qualité du sommeil")
        if len(df) > 1:
            df_sorted = df.sort_values('date')
            fig2 = px.line(
                df_sorted,
                x='date',
                y='sleep_quality',
                title='Qualité du sommeil au fil du temps',
                markers=True
            )
            fig2.update_layout(yaxis_range=[0, 10])
            st.plotly_chart(fig2, use_container_width=True)
        
        # Nuage de mots des thèmes (exemple simplifié)
        st.subheader("Thèmes récurrents")
        st.info("Cette fonctionnalité nécessite l'analyse des thèmes pour chaque rêve.")
        
        # Statistiques par type de rêve
        st.subheader("Répartition par type de rêve")
        type_counts = df['dream_type'].value_counts()
        fig3 = px.bar(
            type_counts,
            x=type_counts.index,
            y=type_counts.values,
            labels={'x': 'Type de rêve', 'y': 'Nombre de rêves'}
        )
        st.plotly_chart(fig3, use_container_width=True)
        
    except Exception as e:
        st.error(f"Une erreur est survenue lors de la génération des statistiques: {str(e)}")
    finally:
        db.close()

# Fonction principale
def main():
    """Fonction principale de l'application."""
    # Configuration du thème
    st.markdown(f"""
        <style>
            .main {{
                background-color: {get_theme('background')};
                color: {get_theme('text')};
            }}
            .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div>div>div {{
                background-color: {get_theme('secondaryBackground')} !important;
                color: {get_theme('text')} !important;
            }}
            .st-bb, .st-at, .st-ae, .st-af, .st-ag, .st-ah, .st-ai, .st-aj, .st-ak, .st-al, .st-am, .st-an, .st-ao, .st-ap, .st-aq, .st-ar, .st-as {{
                background-color: {get_theme('primaryColor')} !important;
            }}
        </style>
    """, unsafe_allow_html=True)
    
    # Charger les rêves au démarrage
    if not st.session_state.dreams:
        load_dreams_from_file()
    
    # Afficher la barre latérale
    display_sidebar()
    
    # Navigation par onglets
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 Accueil", "📚 Ma Collection", "📊 Analyses", "⚙️ Paramètres"])
    
    with tab1:
        show_home_page()
    
    with tab2:
        show_gallery_page()
    
    with tab3:
        show_analysis_page()
    
    with tab4:
        show_settings_page()
    
    # Pied de page
    st.markdown("---")
    st.caption("© 2023 DreamsEcho - Tous droits réservés")

# Point d'entrée de l'application
if __name__ == "__main__":
    # Configuration de la page pour cacher le menu et le pied de page par défaut
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # Exécution de l'application
    main()
