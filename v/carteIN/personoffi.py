# main.py
import streamlit as st
from incident import Incidents
from mapop import Mapop
from chefsecetionniste import ChefsTracker
from datetime import datetime
import os
import json
import pandas as pd

def save_to_json(data, filename):
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

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return data
            except json.JSONDecodeError:
                return []
    return []

def show_incident_page():
    incidents = Incidents()
    incidents.main()
    
def show_matop():
    mapop = Mapop()
    mapop.main()
def show_matamba():
    mapop = ChefsTracker()
    mapop.main()
def show_persons_page():
    st.title("👥 Personnes d'Intérêt")
    
    with st.sidebar:
        st.header("📋 Nouvelle Personne")
        nom = st.text_input("Nom")
        prenom = st.text_input("Prénom")
        date_naissance = st.date_input("Date de naissance")
        lieu_naissance = st.text_input("Lieu de naissance")
        affiliation = st.selectbox("Affiliation", 
            ["Inconnue", "Groupe A", "Groupe B", "Groupe C", "Autre"])
        description = st.text_area("Description/Notes")
        photo = st.file_uploader("Photo", type=['jpg', 'png', 'jpeg'])
        
        if st.button("Enregistrer"):
            if nom and prenom:
                new_person = {
                    "nom": nom,
                    "prenom": prenom,
                    "date_naissance": str(date_naissance),
                    "lieu_naissance": lieu_naissance,
                    "affiliation": affiliation,
                    "description": description,
                    "date_ajout": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                save_to_json(new_person, "personnes_interet.json")
                st.success("Personne ajoutée avec succès!")

    st.header("📋 Liste des Personnes")
    persons_data = load_data("personnes_interet.json")
    
    if persons_data:
        df_persons = pd.DataFrame(persons_data)
        
        col1, col2 = st.columns(2)
        with col1:
            affiliation_filter = st.multiselect(
                "Filtrer par affiliation",
                options=df_persons['affiliation'].unique()
            )
        with col2:
            search_term = st.text_input("Rechercher par nom")
        
        if affiliation_filter:
            df_persons = df_persons[df_persons['affiliation'].isin(affiliation_filter)]
        if search_term:
            mask = df_persons['nom'].str.contains(search_term, case=False) | \
                   df_persons['prenom'].str.contains(search_term, case=False)
            df_persons = df_persons[mask]
        
        cols = st.columns(3)
        for idx, person in df_persons.iterrows():
            with cols[idx % 3]:
                st.markdown("---")
                st.markdown(f"### {person['prenom']} {person['nom']}")
                st.markdown(f"**Affiliation:** {person['affiliation']}")
                st.markdown(f"**Date de naissance:** {person['date_naissance']}")
                st.markdown(f"**Lieu de naissance:** {person['lieu_naissance']}")
                if person['description']:
                    with st.expander("Description"):
                        st.write(person['description'])
    else:
        st.info("Aucune personne enregistrée pour le moment.")

def main():
    st.set_page_config(layout="wide", page_title="Système de Surveillance", page_icon="🌍")

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
            .menu-item {
                padding: 10px;
                text-align: center;
                cursor: pointer;
            }
            .menu-item:hover {
                background-color: #FF4B4B;
            }
        </style>
    """, unsafe_allow_html=True)

    menu = ["Incidents", "Map operationnel","Personnes d'intérêt","Map chef sececetioniste"]
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "Incidents":
        show_incident_page()
    elif choice == "Map operationnel":
        show_matop()
    elif choice == "Map chef sececetioniste":
        show_matamba()
    else:
        show_persons_page()

if __name__ == "__main__":
    main()