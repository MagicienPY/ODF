# chefs_tracker.py
import streamlit as st
import pandas as pd
import pydeck as pdk
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from pydeck.types import String

class ChefsTracker:
    def __init__(self):
        self.apply_style()
        self.filename = "chefs_data.json"

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
                .status-active {
                    color: #FF4B4B;
                    font-weight: bold;
                }
                .status-inactive {
                    color: #808080;
                    font-weight: bold;
                }
                .status-neutralized {
                    color: #000000;
                    font-weight: bold;
                }
                .status-unknown {
                    color: #FFA500;
                    font-weight: bold;
                }
            </style>
        """, unsafe_allow_html=True)

    def save_to_json(self, data):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []
        
        # Générer un ID unique basé sur le timestamp
        data['id'] = str(datetime.now().timestamp())
        existing_data.append(data)
        
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def delete_chef(self, chef_id):
        data = self.load_data()
        data = [d for d in data if d['id'] != chef_id]
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def update_chef(self, chef_id, updated_data):
        data = self.load_data()
        for i, chef in enumerate(data):
            if chef['id'] == chef_id:
                data[i].update(updated_data)
                break
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def create_map(self, df):
        SCENEGRAPH_URL = "https://raw.githubusercontent.com/KhronosGroup/glTF-Sample-Models/master/2.0/BoxAnimated/glTF-Binary/BoxAnimated.glb"
        color_map = {
            "Actif": [255, 0, 0, 160],
            "Inactif": [128, 128, 128, 160],
            "Neutralisé": [36, 249, 64, 160],
            "Localisation Inconnue": [255, 165, 0, 160]
        }
        
        df['color'] = df['statut'].map(color_map)
        
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position=['lon', 'lat'],
            get_color='color',
            get_radius=3000,
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True
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

        view_state = pdk.ViewState(
            latitude=7.0,
            longitude=11.0,
            zoom=6,
            pitch=50
        )

        tooltip = {
            "html": "<b>Nom:</b> {prenom} {nom}<br/>"
                   "<b>Affiliation:</b> {affiliation}<br/>"
                   "<b>Localisation:</b> {lieu_naissance}<br/>"
                   "<b>Statut:</b> {statut}<br/>"
                   "<b>Description:</b> {description}",
            "style": {
                "backgroundColor": "steelblue",
                "color": "white"
            }
        }

        return pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v10",
            initial_view_state=view_state,
            layers=[layer],
            tooltip=tooltip
        )

    def show_statistics(self, df):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Répartition par statut")
            status_counts = df['statut'].value_counts()
            fig1, ax1 = plt.subplots()
            colors = ['#FF4B4B', '#808080', '#000000', '#FFA500']
            ax1.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', colors=colors)
            ax1.axis('equal')
            st.pyplot(fig1)
        
        with col2:
            st.subheader("Répartition par affiliation")
            affiliation_counts = df['affiliation'].value_counts()
            fig2, ax2 = plt.subplots()
            ax2.pie(affiliation_counts, labels=affiliation_counts.index, autopct='%1.1f%%')
            ax2.axis('equal')
            st.pyplot(fig2)

    def main(self):
        st.title("🎯 Suivi des Chefs Sécessionnistes")
        
        menu = ["Carte & Stats", "Gestion", "Rapports"]
        choice = st.sidebar.selectbox("Menu", menu)
        
        if choice == "Carte & Stats":
            data = self.load_data()
            if data:
                df = pd.DataFrame(data)
                
                # Filtres
                col1, col2 = st.columns(2)
                with col1:
                    statut_filter = st.multiselect(
                        "Filtrer par statut",
                        options=df['statut'].unique()
                    )
                with col2:
                    affiliation_filter = st.multiselect(
                        "Filtrer par affiliation",
                        options=df['affiliation'].unique()
                    ) 
                
                # Appliquer les filtres
                if statut_filter:
                    df = df[df['statut'].isin(statut_filter)]
                if affiliation_filter:
                    df = df[df['affiliation'].isin(affiliation_filter)]
                
                st.pydeck_chart(self.create_map(df))
                
                st.header("📊 Statistiques")
                self.show_statistics(df)
                
            else:
                st.info("Aucune donnée disponible. Commencez par ajouter des chefs dans la section Gestion.")
        
        elif choice == "Gestion":
            st.header("📝 Gestion des Chefs")
            
            tab1, tab2 = st.tabs(["Ajouter", "Modifier/Supprimer"])
            
            with tab1:
                with st.form("nouveau_chef"):
                    st.subheader("Nouveau Chef")
                    nom = st.text_input("Nom")
                    prenom = st.text_input("Prénom")
                    date_naissance = st.date_input("Date de naissance")
                    lieu_naissance = st.text_input("Lieu de naissance")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        lat = st.number_input("Latitude", value=7.0, format="%.6f")
                    with col2:
                        lon = st.number_input("Longitude", value=11.0, format="%.6f")
                    
                    affiliation = st.selectbox("Affiliation", 
                        ["Inconnu", "VAMPIRES OF BAMUNKA", "BABESSI LIBERATION FORCES", "NGO-KETUNDJA","BAMBALANG MARINE","BABANKI MARINE FORCES", "BUI UNITY WARRIOR","Autre"])
                    
                    statut = st.selectbox("Statut", 
                        ["Actif", "Inactif", "Neutralisé", "Localisation Inconnue"])
                    
                    description = st.text_area("Description/Notes")
                    
                    if st.form_submit_button("Enregistrer"):
                        if nom and prenom:
                            new_chef = {
                                "nom": nom,
                                "prenom": prenom,
                                "date_naissance": str(date_naissance),
                                "lieu_naissance": lieu_naissance,
                                "lat": lat,
                                "lon": lon,
                                "affiliation": affiliation,
                                "statut": statut,
                                "description": description,
                                "date_ajout": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            self.save_to_json(new_chef)
                            st.success("Chef ajouté avec succès!")
                        else:
                            st.error("Le nom et le prénom sont requis.")
            
            with tab2:
                data = self.load_data()
                if data:
                    df = pd.DataFrame(data)
                    chef_to_edit = st.selectbox(
                        "Sélectionner un chef à modifier/supprimer",
                        options=df.apply(lambda x: f"{x['prenom']} {x['nom']} ({x['affiliation']})", axis=1)
                    )
                    
                    if chef_to_edit:
                        selected_chef = df[df.apply(lambda x: f"{x['prenom']} {x['nom']} ({x['affiliation']})" == chef_to_edit, axis=1)].iloc[0]
                        
                        with st.form("modifier_chef"):
                            st.subheader("Modifier les informations")
                            new_statut = st.selectbox("Nouveau statut", 
                                ["Actif", "Inactif", "Neutralisé", "Localisation Inconnue"],
                                index=["Actif", "Inactif", "Neutralisé", "Localisation Inconnue"].index(selected_chef['statut'])
                            )
                            
                            new_lat = st.number_input("Nouvelle latitude", value=float(selected_chef['lat']))
                            new_lon = st.number_input("Nouvelle longitude", value=float(selected_chef['lon']))
                            
                            new_description = st.text_area("Nouvelle description", value=selected_chef['description'])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("Mettre à jour"):
                                    updated_data = {
                                        "statut": new_statut,
                                        "lat": new_lat,
                                        "lon": new_lon,
                                        "description": new_description
                                    }
                                    self.update_chef(selected_chef['id'], updated_data)
                                    st.success("Informations mises à jour!")
                                    st.rerun()
                            
                            with col2:
                                if st.form_submit_button("Supprimer", type="primary"):
                                    self.delete_chef(selected_chef['id'])
                                    st.success("Chef supprimé avec succès!")
                                    st.rerun()
                else:
                    st.info("Aucun chef enregistré pour le moment.")
        
        elif choice == "Rapports":
            st.header("📊 Rapports")
            data = self.load_data()
            
            if data:
                df = pd.DataFrame(data)
                
                st.subheader("Vue d'ensemble")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total des chefs", len(df))
                with col2:
                    st.metric("Chefs actifs", len(df[df['statut'] == "Actif"]))
                with col3:
                    st.metric("Neutralisés", len(df[df['statut'] == "Neutralisé"]))
                with col4:
                    st.metric("Localisation inconnue", len(df[df['statut'] == "Localisation Inconnue"]))
                
                st.subheader("Liste complète")
                st.dataframe(
                    df[['prenom', 'nom', 'affiliation', 'statut', 'lieu_naissance', 'date_ajout', 'description']],
                    use_container_width=True
                )
                
                # Export options
                if st.button("Exporter en CSV"):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Télécharger le CSV",
                        data=csv,
                        file_name="chefs_rapport.csv",
                        mime="text/csv"
                    )
            else:
                st.info("Aucune donnée disponible pour générer des rapports.")

def main():
    tracker = ChefsTracker()
    tracker.main()
