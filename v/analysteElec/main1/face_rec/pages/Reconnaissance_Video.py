import streamlit as st
import cv2
import face_recognition as frg
import yaml
from utils import recognize, build_dataset

# Configuration de la page
st.set_page_config(layout="wide")

# Charger le fichier de configuration
try:
    cfg = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)
    PICTURE_PROMPT = cfg['INFO']['PICTURE_PROMPT']
    WEBCAM_PROMPT = cfg['INFO']['WEBCAM_PROMPT']
except Exception as e:
    st.error(f"Erreur de chargement de la configuration : {e}")
    st.stop()

# Sidebar pour paramètres
st.sidebar.title("Paramètres")
menu = ["Video", "Webcam"]
choice = st.sidebar.selectbox("Type d'entrée", menu)
TOLERANCE = st.sidebar.slider("Tolérance", 0.0, 1.0, 0.5, 0.01)

# Conteneurs pour affichage d'informations utilisateur
st.sidebar.title("Informations sur l'utilisateur")
name_container = st.sidebar.empty()
id_container = st.sidebar.empty()
name_container.info("Nom : Inconnu")
id_container.success("ID : Inconnu")

# Gestion des choix
if choice == "Video":
    st.title("ODF - Reconnaissance faciale sur vidéo")
    st.write("Cette fonctionnalité permet la reconnaissance de visages sur des vidéos en temps réel.")
    uploaded_videos = st.file_uploader("Importer une vidéo", type=['avi', 'mp4', 'mkv'], accept_multiple_files=True)
    
    if uploaded_videos:
        for video_file in uploaded_videos:
            # Sauvegarde temporaire de la vidéo
            temp_video_path = f"/tmp/{video_file.name}"
            with open(temp_video_path, 'wb') as f:
                f.write(video_file.read())

            # Lecture et traitement de la vidéo
            video = cv2.VideoCapture(temp_video_path)
            stframe = st.empty()  # Conteneur pour afficher les frames
            while video.isOpened():
                ret, frame = video.read()
                if not ret:
                    break  # Fin de la vidéo
                
                # Reconnaissance faciale
                image, name, id = recognize(frame, TOLERANCE)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                # Mise à jour des informations
                name_container.info(f"Nom : {name}")
                id_container.success(f"ID : {id}")
                
                # Affichage de la frame
                stframe.image(image)

            video.release()
    else:
        st.info("Veuillez importer une vidéo pour commencer.")

elif choice == "Webcam":
    st.title("ODF - Module de reconnaissance faciale (Webcam)")
    st.write(WEBCAM_PROMPT)
    
    cam = cv2.VideoCapture(0)  # Initialisation de la webcam
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    FRAME_WINDOW = st.image([])  # Conteneur pour afficher les frames

    if cam.isOpened():
        while True:
            ret, frame = cam.read()
            if not ret:
                st.error("Échec de la capture de l’image de la webcam.")
                st.info("Veuillez vérifier que la webcam est bien connectée.")
                break
            
            # Reconnaissance faciale
            image, name, id = recognize(frame, TOLERANCE)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Mise à jour des informations
            name_container.info(f"Nom : {name}")
            id_container.success(f"ID : {id}")

            # Affichage de l'image
            FRAME_WINDOW.image(image)
    else:
        st.error("Impossible d'accéder à la webcam.")

    cam.release()
