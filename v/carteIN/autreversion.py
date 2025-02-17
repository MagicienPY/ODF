import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
from datetime import datetime
import os
import json

# Configuration de l'application
st.set_page_config(layout="wide", page_title="Système de Publications", page_icon="🌍")

# Activer le mode sombre
st.markdown("""
    <style>
        body {
            background-color: #000;
            color: white;
        }
        .stButton>button {
            background-color: #FF4B4B;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state pour les coordonnées
if 'clicked_lat_lon' not in st.session_state:
    st.session_state.clicked_lat_lon = None

# Fonction pour sauvegarder les données
def save_to_json(data, filename="data_publications.json"):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []
    existing_data.append(data)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

# [Autres fonctions existantes restent identiques]
# Fonction pour sauvegarder les données
def save_to_json(data, filename="data_publications.json"):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []
    existing_data.append(data)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)

# Charger les données JSON
def load_data(filename="data_publications.json"):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return data
            except json.JSONDecodeError:
                return []
    return []

# Classification simple
def classify_text(text):
    text = text.lower()
    if any(word in text for word in ['politique', 'gouvernement', 'ministre', 'président']):
        return "Politique"
    elif any(word in text for word in ['social', 'santé', 'education', 'école']):
        return "Social"
    elif any(word in text for word in ['économie', 'finance', 'entreprise', 'commerce']):
        return "Économique"
    elif any(word in text for word in [
    'militaire', 'armée', 'sécurité', 'défense', 'opération', 'neutraliser', 'munitions', 'BIR', 
    'terroristes', 'attaque', 'assaut', 'embuscade', 'riposte', 'patrouille', 'combat', 'fusillade', 
    'neutralisation', 'blessés', 'assailants', 'explosion', 'charge explosive', 'moto', 'engagement', 
    'intervention', 'armés', 'forces de l\'ordre', 'incursion', 'fuite', 'attaque à main armée', 
    'récupérer', 'matériel', 'armes', 'FAL', 'AK47', 'munition', 'roquettes', 'grenades', 'chargeurs', 
    'cibles', 'coup de feu', 'camp', 'raid', 'plan d\'attaque', 'combat intense', 'général', 'terroristes', 
    'bandits', 'terroriste', 'blessure', 'armée alliée', 'forces de l\'ordre', 'opfor', 'bataillon', 
    'prisonniers', 'camp militaire', 'bilan', 'restes de guerre', 'tactiques', 'infiltration', 'postes militaires',
    'embuscade', 'assaut sur base', 'missions', 'guerre', 'conflit', 'réaction militaire', 'armée nigériane', 
    'résistance', 'engins explosifs', 'victoire', 'défense frontalière', 'combattants', 'réfugiés', 'territoire contrôlé',
    'insurrection', 'attaque repoussée', 'attaque ennemie', 'lutte contre le terrorisme', 'sécurisation', 'raid de reconnaissance'
]):

        return "Militaire"
    return "Autre"

# Charger les données GeoJSON des frontières régionales
def load_geojson(filename="cm.json"):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Le fichier {filename} est introuvable. Veuillez le télécharger et l'ajouter au répertoire.")
        return None

def main():
    st.title("🌍 ODF-SIG - DES INCIDENTS PAR DEPARTEMENTS")
    
    # Création d'une colonne principale pour la carte et d'une sidebar
    main_col, sidebar = st.columns([3, 1])
    
    with sidebar:
        st.header("📋 Nouvelle Publication")
        title = st.text_input("Titre")
        content = st.text_area("Contenu")
        
        # Création des champs pour les coordonnées
        st.write("Coordonnées:")
        col1, col2 = st.columns(2)
        with col1:
            lat = st.number_input("Latitude", value=7.0, format="%.6f", key="lat_input")
        with col2:
            lon = st.number_input("Longitude", value=11.0, format="%.6f", key="lon_input")
        
        st.info("Double-cliquez sur la carte pour copier les coordonnées")
        
        if st.button("Publier"):
            if title and content:
                category = classify_text(content)
                new_entry = {
                    "title": title,
                    "contenus": content,
                    "category": category,
                    "lat": lat,
                    "lon": lon,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                save_to_json(new_entry)
                st.success("Publication ajoutée avec succès!")
                st.experimental_rerun()
    
    with main_col:
        data = load_data()
        if data:
            df = pd.DataFrame(data)
            
            st.header("📍 Carte des Publications")
            color_map = {
                "Politique": [255, 99, 71, 160],
                "Social": [144, 238, 144, 160],
                "Économique": [30, 144, 255, 160],
                "Militaire": [255, 215, 0, 160],
                "Autre": [128, 128, 128, 160]
            }
            df['color'] = df['category'].map(color_map)
            
            regions_geojson = load_geojson()
            
            if regions_geojson:
                # Création des layers
                layers = [
                    # Layer des régions
                    pdk.Layer(
                        "GeoJsonLayer",
                        data=regions_geojson,
                        get_fill_color=[100, 150, 200, 100],
                        get_line_color=[255, 255, 255],
                        line_width_min_pixels=2,
                        pickable=True,
                        auto_highlight=True
                    ),
                    # Layer des points
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=df,
                        get_position=['lon', 'lat'],
                        get_color='color',
                        get_radius=5000,
                        pickable=True
                    )
                ]
                
                view_state = pdk.ViewState(
                    latitude=7.0,
                    longitude=11.0,
                    zoom=6,
                    pitch=50
                )
                
                # Tooltip amélioré
                tooltip = {
                    "html": """
                        <style>
                            .tooltip {
                                background-color: steelblue;
                                color: white;
                                padding: 10px;
                                border-radius: 5px;
                                font-family: Arial, sans-serif;
                            }
                        </style>
                        <div class="tooltip">
                            <div><b>Région:</b> {name}</div>
                            <div><b>Titre:</b> {title}</div>
                            <div><b>Contenu:</b> {contenus}</div>
                            <div><b>Catégorie:</b> {category}</div>
                            <div><b>Coordonnées:</b> ({lat}, {lon})</div>
                        </div>
                    """,
                    "style": {
                        "backgroundColor": "steelblue",
                        "color": "white"
                    }
                }
                
                # Création et affichage de la carte
                st.pydeck_chart(pdk.Deck(
                    map_style="mapbox://styles/mapbox/dark-v10",
                    initial_view_state=view_state,
                    layers=layers,
                    tooltip=tooltip
                ))
                
                # Ajout d'un message d'aide pour les coordonnées
                st.info("""
                Pour copier les coordonnées d'un point sur la carte :
                1. Faites un clic droit sur l'emplacement souhaité
                2. Sélectionnez 'What\'s here?' ou 'Qu'y a-t-il ici ?'
                3. Les coordonnées apparaîtront et pourront être copiées
                """)
            
            # Affichage des statistiques
            st.header("📊 Statistiques")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Répartition par catégorie")
                category_counts = df['category'].value_counts()
                pie_colors = ["#FF6347", "#90EE90", "#1E90FF", "#FFD700", "#808080"]
                fig, ax = plt.subplots()
                ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140, colors=pie_colors)
                ax.axis('equal')
                st.pyplot(fig)
            
            with col2:
                st.subheader("Liste des Publications")
                st.dataframe(df[['title', 'category', 'contenus', 'date']], hide_index=True)

if __name__ == "__main__":
    main()