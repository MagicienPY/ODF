import streamlit as st
import pandas as pd
import pydeck as pdk
import carteE  # Importer le fichier carteE.py
from utils import stat_card


# Configuration de la page
st.set_page_config(
    page_title="ODF - Tableau de Bord",
    page_icon="📊",
    layout="wide"
)

# Initialiser l'état pour gérer les pages
if "page" not in st.session_state:
    st.session_state["page"] = "dashboard"  # Page par défaut

# Fonction pour changer de page
def navigate_to(page_name):
    st.session_state["page"] = page_name

# Fonction de redirection vers une page externe
def redirect_to_login():
    st.write(
        """
        <meta http-equiv="refresh" content="0; url=http://212.83.168.217/ODF3/">
        """,
        unsafe_allow_html=True
    )

# Gestion de la navigation
if st.session_state["page"] == "dashboard":
    # Contenu principal du tableau de bord
    st.title("ODF - Tableau de Bord Analytique Élection")

    # Créer un conteneur principal avec deux colonnes
    col1, col2 = st.columns([2, 1])

    # --- Colonne 1 : Affichage des statistiques et de la carte ---
    with col1:
        # Statistiques Globales
        st.markdown("### Statistiques Globales")
        col1_1, col1_2, col1_3 = st.columns(3)

        # Style pour les cartes
        

        # Cartes des statistiques
        with col1_1:
            st.markdown(stat_card("Analyses Électorales", 125, "#ff5c93", "#a044ff"), unsafe_allow_html=True)
        with col1_2:
            st.markdown(stat_card("Prédictions Réalisées", 35, "#00b09b", "#96c93d"), unsafe_allow_html=True)
        with col1_3:
            st.markdown(stat_card("Cartes Électorales Sociales", 10, "#ff7e5f", "#feb47b"), unsafe_allow_html=True)

        # Carte interactive du Cameroun
        st.markdown("### Carte du Cameroun avec points")
        data_points = pd.DataFrame({
            'lat': [3.848, 4.047, 6.369, 3.848],
            'lon': [11.502, 11.517, 9.307, 10.502],
            'name': ['Yaoundé', 'Douala', 'Garoua', 'Bertoua']
        })

        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v10",
            initial_view_state=pdk.ViewState(
                latitude=4.5,
                longitude=11.5,
                zoom=6,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=data_points,
                    get_position='[lon, lat]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=50000,
                ),
            ],
        ))

    # --- Colonne 2 : Menu et déconnexion ---
    with col2:
        st.markdown("### Menu")
        if st.button("🏠 Accueil"):
            navigate_to("dashboard")
        if st.button("🗺️ Scrapping & Stockage"):
            navigate_to("scraping")
        if st.button("📊 Analyse"):
            navigate_to("analysis")
        if st.button("🗺️ Gérer carte électorale sociale"):
            navigate_to("social_map")
        if st.button("🗺️ Carte d'incidents'"):
            navigate_to("carteE")


        # Bouton de déconnexion
        if st.button("🔒 Déconnexion"):
            redirect_to_login()

elif st.session_state["page"] == "carteE":
    # Charger la carte de publication
    carteE.run()  # Appeler la fonction principale dans carteE.py
