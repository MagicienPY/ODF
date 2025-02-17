import streamlit as st  
import pandas as pd  
import pydeck as pdk  
import json  
import os  

def run():  
    # Vérifier si le fichier existe  
    if not os.path.exists('data_publications.json'):  
        st.error("Le fichier 'data_publications.json' est introuvable. Veuillez vérifier son emplacement.")  
        return  

    # Charger les données depuis le fichier JSON avec gestion d'erreurs  
    try:  
        with open('data_publications.json', 'r', encoding='utf-8') as f:  
            data_publications = json.load(f)  
    except json.JSONDecodeError:  
        st.error("Erreur lors du chargement du fichier JSON. Veuillez vérifier le format.")  
        return  

    # Convertir les données en DataFrame pandas  
    try:  
        df_publications = pd.DataFrame(data_publications)  
    except ValueError:  
        st.error("Erreur : Les données JSON ne sont pas au format attendu.")  
        return  

    # Vérifier si les colonnes nécessaires existent  
    required_columns = ['lat', 'lon', 'category', 'title', 'contenus']  
    missing_columns = [col for col in required_columns if col not in df_publications.columns]  
    if missing_columns:  
        st.error(f"Colonnes manquantes dans les données : {', '.join(missing_columns)}")  
        return  

    # Ajouter une colonne pour la taille des icônes  
    df_publications['icon_data'] = [{  
        "url": "https://cdn-icons-png.flaticon.com/512/64/64113.png",  
        "width": 128,  
        "height": 128,  
        "anchorY": 128  
    }] * len(df_publications)  

    # Fonction pour attribuer des couleurs en fonction de la catégorie  
    def get_color_by_category(category):  
        colors = {  
            "Politique": [255, 0, 0, 160],  
            "Social": [0, 255, 0, 160],  
            "Économique": [0, 0, 255, 160],  
            "Militaire": [255, 165, 0, 160]  # Couleur pour les opérations militaires  
        }  
        return colors.get(category, [128, 128, 128, 160])  

    # Appliquer les couleurs aux données  
    df_publications['color'] = df_publications['category'].apply(get_color_by_category)  

    # Diviser l'interface en colonnes  
    col1, col2 = st.columns([2, 1])  

    # Colonne 1 : Carte  
    with col1:  
        st.subheader("Carte des publications par catégorie")  
        st.pydeck_chart(pdk.Deck(  
            map_style="mapbox://styles/mapbox/light-v10",  
            initial_view_state=pdk.ViewState(  
                latitude=4.5,  
                longitude=11.5,  
                zoom=5,  
                pitch=70,  
            ),  
            layers=[  
                # Layer de localisation (icônes)  
                pdk.Layer(  
                    "IconLayer",  
                    data=df_publications,  
                    get_position='[lon, lat]',  
                    get_icon='icon_data',  
                    get_size=44,  
                    pickable=True,  
                ),  
                # Layer des cercles  
                pdk.Layer(  
                    "ScatterplotLayer",  
                    data=df_publications,  
                    get_position='[lon, lat]',  
                    get_color='color',  
                    get_radius=20000,  
                    pickable=True  
                )  
            ],  
            tooltip={  
                "html": """  
                    <div style="background-color: white; padding: 10px; border-radius: 5px; width: 300px;">  
                        <strong>Titre:</strong> {title}<br/>  
                        <strong>Catégorie:</strong> {category}<br/>  
                        <strong>Détails:</strong> {contenus}  
                    </div>  
                """,  
                "style": {  
                    "color": "black",  
                    "font-family": "Arial, sans-serif",  
                    "z-index": "1000"  
                }  
            }  
        ))  

    # Colonne 2 : Légende et tableau  
    with col2:  
        st.markdown("### Légende des catégories")  
        st.markdown("""  
        - **Politique** : 🔴 Rouge  
        - **Social** : 🟢 Vert  
        - **Économique** : 🔵 Bleu  
        - **Militaire** : 🟠 Orange  
        """)  

        # Tableau des régions, départements et arrondissements  
        # Tableau des régions, départements et arrondissements
        st.markdown("### Détails des régions")
        data_regions = {
            "Région": ["Centre", "Littoral", "Nord", "Ouest", "Adamaoua"],
            "Département": ["Mfoundi", "Wouri", "Bénoué", "Noun", "Vina"],
            "Arrondissement": ["Yaoundé 1er", "Douala 3e", "Garoua 2e", "Foumban", "Ngaoundéré 1er"],
            "Population": ["3,500,000", "3,000,000", "2,000,000", "1,500,000", "1,200,000"]
        }
        df_regions = pd.DataFrame(data_regions)
        st.dataframe(df_regions)

    # Bouton pour revenir au dashboard
    st.markdown("---")
    if st.button("Revenir au Dashboard"):
        st.success("Redirection vers le Dashboard...")
        st.markdown