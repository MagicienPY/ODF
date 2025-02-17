# incidents.py
import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
from datetime import datetime
import os
import json
from pydeck.types import String
from pydeck import Layer, Deck

class Incidents:
    def __init__(self):
        self.apply_style()

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

    def load_data(self, filename="data_publications.json"):
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    return data
                except json.JSONDecodeError:
                    return []
        return []

    def classify_text(self, text):
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

    def load_geojson(self, filename="cm.json"):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            st.error(f"Le fichier {filename} est introuvable. Veuillez le télécharger et l'ajouter au répertoire.")
            return None

    def create_map(self, df, regions_geojson):
        SCENEGRAPH_URL = "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/BoxAnimated/glTF-Binary/BoxAnimated.glb"
        color_map = {
            "Politique": [255, 99, 71, 160],
            "Social": [144, 238, 144, 160],
            "Économique": [30, 144, 255, 160],
            "Militaire": [255, 215, 0, 160],
            "Autre": [128, 128, 128, 160]
        }
        df['color'] = df['category'].map(color_map)
        
        layers = [
            pdk.Layer(
                "GeoJsonLayer",
                data=regions_geojson,
                get_fill_color=[100, 150, 200, 100],
                get_line_color=[255, 255, 255],
                line_width_min_pixels=2,
                pickable=True,
                auto_highlight=True
            ),
           pdk.Layer(
                    "ScatterplotLayer",
                    data=df,
                    get_position=['lon', 'lat'],
                    get_color='color',
                    get_radius=3000,
                    pickable=True
                ),
           
            pdk.Layer(
                "ScenegraphLayer",
                data=df,
                id="scenegraph-layer",
                scenegraph=SCENEGRAPH_URL,
                get_position=['lon', 'lat'],
                get_orientation=[0, 180, 90],
                size_scale=1500,
                _animations={"*": {"speed": 2}},
                _lighting=String("pbr"),
            )
            
        ]
        
        return pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v10",
            initial_view_state=pdk.ViewState(
                latitude=7.0,
                longitude=11.0,
                zoom=6,
                pitch=50
            ),
            layers=layers,
            tooltip={
                "html": "<b>Région:</b> {name}<br/>"
                        "<b>Titre:</b> {title}<br/>"
                        "<b>Contenu:</b> {contenus}<br/>"
                        "<b>Catégorie:</b> {category}<br/>",
                "style": {
                    "backgroundColor": "steelblue",
                    "color": "white"
                }
            }
        )

    def show_statistics(self, df):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Répartition par catégorie")
            category_counts = df['category'].value_counts()
            pie_colors = ["#FF6347", "#90EE90", "#1E90FF", "#FFD700", "#808080"]
            fig, ax = plt.subplots()
            ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140, colors=pie_colors)
            ax.axis('equal')
            st.pyplot(fig)
        
        with col2:
            st.subheader("Liste de Publications")
            st.dataframe(df[['title', 'category', 'contenus', 'date']], hide_index=False)

        with col3:
            st.markdown("### Stats par catégories")
            st.write(category_counts)
            st.markdown("### Légende des catégories")
            st.markdown("""
            - **Politique** : 🔴 Rouge
            - **Social** : 🟢 Vert
            - **Économique** : 🔵 Bleu
            - **Militaire** : 🟠 Orange
            """)

    def main(self):
        st.title("🌍 ODF-SIG - DES INCIDENTS PAR DEPARTEMENTS")
        
        with st.sidebar:
            st.header("📋 Nouvelle Publication")
            title = st.text_input("Titre")
            content = st.text_area("Contenu")
            col1, col2 = st.columns(2)
            with col1:
                lat = st.number_input("Latitude", value=4.5, format="%.6f")
            with col2:
                lon = st.number_input("Longitude", value=4.5, format="%.6f")
            
            if st.button("Publier"):
                if title and content:
                    category = self.classify_text(content)
                    new_entry = {
                        "title": title,
                        "contenus": content,
                        "category": category,
                        "lat": lat,
                        "lon": lon,
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    self.save_to_json(new_entry)
                    st.success("Publication ajoutée avec succès!")

        data = self.load_data()
        if data:
            df = pd.DataFrame(data)
            st.header("📍 Carte de Publications")
            st.markdown("### Légende des catégories")
            st.markdown("""
                - **Politique** : 🔴 Rouge
                - **Social** : 🟢 Vert
                - **Économique** : 🔵 Bleu
                - **Militaire** : 🟠 Orange
            """)
            
            regions_geojson = self.load_geojson()
            if regions_geojson:
                st.pydeck_chart(self.create_map(df, regions_geojson))
            
            st.header("📊 Statistiques")
            self.show_statistics(df)
            
