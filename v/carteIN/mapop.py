import streamlit as st
import pandas as pd
import pydeck as pdk
from datetime import datetime
import os
import json

class Mapop:
    def __init__(self):
        self.apply_style()
        # Définition des limites géographiques du Cameroun
        self.BOUNDS = [
            [8.4, 1.6],   # Sud-Ouest
            [8.4, 13.1],  # Nord-Ouest
            [16.2, 13.1], # Nord-Est
            [16.2, 1.6]   # Sud-Est
        ]
    
    def apply_style(self):
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

    def save_to_json(self, data, filename="data_publications.json"):
        existing_data = []
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    pass
        existing_data.append(data)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)

    def load_data(self, filename="data_publications.json"):
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    return [item for item in data if item.get('category') == 'Militaire']
                except json.JSONDecodeError:
                    return []
        return []

    @staticmethod
    def classify_text(text):
        text = text.lower()
        if any(word in text for word in [
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

    def create_map(self, df):
        df['icon_data'] = [{  
            "url": "https://cdn-icons-png.flaticon.com/512/64/64113.png",  
            "width": 128,  
            "height": 128,  
            "anchorY": 128  
        }] * len(df)
        
        military_layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=['lon', 'lat'],
            get_color=[255, 140, 0, 200],  # Orange pour militaire
            get_radius=2000,
            pickable=True
        )

        icon_layer = pdk.Layer(
            "IconLayer",
            data=df,
            get_position='[lon, lat]',
            get_icon='icon_data',
            get_size=44,
            pickable=True,
        )
        
        return pdk.Deck(
            map_style="mapbox://styles/mapbox/satellite-streets-v11",
            initial_view_state=pdk.ViewState(
                latitude=7.0,
                longitude=11.0,
                zoom=6,
                pitch=60,
                bearing=0
            ),
            layers=[military_layer, icon_layer],
            tooltip={
                "html": "<b>Titre:</b> {title}<br/>"
                        "<b>Contenu:</b> {contenus}<br/>"
                        "<b>Date:</b> {date}<br/>"
            }
        )

    def show_statistics(self, df):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Liste des Opérations Militaires")
            st.dataframe(df[['title', 'contenus', 'date']], hide_index=False)

        with col2:
            st.subheader("Statistiques")
            st.write(f"Nombre total d'opérations: {len(df)}")
            st.markdown("### Légende")
            st.markdown("🟠 Points Orange: Incidents militaires")
            
    def load_geojson(self, filename="cm.json"):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            st.error(f"Le fichier {filename} est introuvable. Veuillez le télécharger et l'ajouter au répertoire.")
            return None
        
    def main(self):
        st.title("🎯 ODF-SIG - Carte des Opérations Militaires")
        
        with st.sidebar:
            st.header("📋 Nouvelle Opération Militaire")
            title = st.text_input("Titre de l'opération")
            content = st.text_area("Description")
            col1, col2 = st.columns(2)
            with col1:
                lat = st.number_input("Latitude", value=7.0, format="%.6f")
            with col2:
                lon = st.number_input("Longitude", value=11.0, format="%.6f")
            
            if st.button("Enregistrer"):
                if title and content:
                    new_entry = {
                        "title": title,
                        "contenus": content,
                        "category": "Militaire",
                        "lat": lat,
                        "lon": lon,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    self.save_to_json(new_entry)
                    st.success("Opération enregistrée!")
        
        data = self.load_data()
        if data:
            # Charger le GeoJSON des régions
            regions_geojson = self.load_geojson()
            
            # Afficher la carte avec les régions
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
                        "HexagonLayer",
                        data=data,
                        get_position="[lon, lat]",
                        radius=3000,
                        get_color='color',
                        elevation_scale=6,
                        elevation_range=[0, 1000],
                        pickable=True,
                        extruded=True,
                    ),
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=data,
                        get_position=['lon', 'lat'],
                        get_color='color',
                        get_radius=3000,
                        pickable=True
                    )
                ]
                
                # Configuration de la carte
                view_state = pdk.ViewState(
                    latitude=3.8,
                    longitude=11.0,
                    zoom=6,
                    pitch=50
                )
                
                # Création du tooltip personnalisé
                tooltip = {
                    "html": "<b>Région:</b> {name}<br/>"
                            "<b>Titre:</b> {title}<br/>"
                            "<b>Contenu:</b> {contenus}<br/>"
                            "<b>Catégorie:</b> {category}<br/>",
                    "style": {
                        "backgroundColor": "steelblue",
                        "color": "white"
                    }
                }
                
                # Affichage de la carte
                st.pydeck_chart(pdk.Deck(
                    map_style="mapbox://styles/mapbox/dark-v10",
                    initial_view_state=view_state,
                    layers=layers,
                    tooltip=tooltip
                ))
                df = pd.DataFrame(data)
                st.header("📍 Carte des Opérations")
                st.pydeck_chart(self.create_map(df))
                
                st.header("📊 Statistiques d'Opérations")
                self.show_statistics(df)
