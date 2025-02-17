import streamlit as st
import pandas as pd
import tweepy

# Configuration de la page
st.set_page_config(
    page_title="ODF - Scraping et Stockage",
    page_icon="🔍",
    layout="wide"
)

# Clés d'API Twitter (remplacez par vos propres clés)
API_KEY = "VOTRE_API_KEY"
API_SECRET = "VOTRE_API_SECRET"
ACCESS_TOKEN = "VOTRE_ACCESS_TOKEN"
ACCESS_TOKEN_SECRET = "VOTRE_ACCESS_TOKEN_SECRET"

# Authentification Twitter
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Contenu principal
st.title("ODF - Scraping et Stockage des Données")

# Créer un conteneur principal avec deux colonnes
col1, col2 = st.columns([2, 1])

# --- Colonne 1 : Interface de recherche ---
with col1:
    st.markdown("### Recherche sur Twitter")
    search_query = st.text_input("Entrez un mot-clé ou un hashtag pour commencer la recherche")
    max_tweets = st.number_input("Nombre de tweets à récupérer", min_value=10, max_value=1000, step=10, value=50)
    
    if st.button("Lancer la recherche"):
        try:
            # Récupérer les tweets
            tweets = tweepy.Cursor(api.search_tweets, q=search_query, lang="fr", tweet_mode="extended").items(max_tweets)
            
            # Stocker les données dans un DataFrame
            tweets_data = []
            for tweet in tweets:
                tweets_data.append({
                    "Utilisateur": tweet.user.screen_name,
                    "Texte": tweet.full_text,
                    "Date de publication": tweet.created_at,
                })
            
            df = pd.DataFrame(tweets_data)
            
            st.success(f"{len(df)} tweets récupérés avec succès !")
            
            # Afficher les résultats sous forme de tableau
            st.dataframe(df)
            
            # Permettre le téléchargement des données au format CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Télécharger les résultats en CSV",
                data=csv,
                file_name="tweets.csv",
                mime="text/csv",
            )
        
        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")

# --- Colonne 2 : Menu à droite ---
with col2:
    st.markdown("### Menu")
    st.markdown(
        """
        <ul style="list-style-type: none; padding: 0; font-size: 18px;">
            <li>🏠 <a href="">Accueil</a></li>
            <li>📊 <a href="#">Tableau de Bord</a></li>
            <li>🔍 <a href="#">Scraping et Stockage</a></li>
            <li>🗺️ <a href="#">Visualiser sur la carte</a></li>
        </ul>
        """,
        unsafe_allow_html=True
    )
    
    # Ajouter un bouton de déconnexion
    if st.button("🔒 Déconnexion"):
        st.session_state["authenticated"] = False
        st.experimental_rerun()
