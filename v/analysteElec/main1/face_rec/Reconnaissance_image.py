import streamlit as st
import cv2
import face_recognition as frg
import yaml
from utils import recognize, build_dataset

# Configuration de la page
st.set_page_config(layout="wide")

# Charger le fichier de configuration
cfg = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)
PICTURE_PROMPT = cfg['INFO']['PICTURE_PROMPT']
WEBCAM_PROMPT = cfg['INFO']['WEBCAM_PROMPT']

# Menu latéral
st.sidebar.title("Paramètres")
menu = ["Photo", "Webcam"]
choice = st.sidebar.selectbox("Input type", menu)
TOLERANCE = st.sidebar.slider("Tolérance", 0.0, 1.0, 0.5, 0.01)

st.sidebar.title("Information sur utilisateur")
name_container = st.sidebar.empty()
id_container = st.sidebar.empty()
name_container.info('Nom: Inconnu')
id_container.success('ID: Inconnu')

# Gestion des options de reconnaissance faciale
if choice == "Photo":
    st.title("ODF-reconnaissance faciale")
    st.write("Cette fonctionnalité permet de faire la reconnaissance de visages sur image et vidéo en temps réel.")
    
    uploaded_images = st.file_uploader("Importer", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)
    if uploaded_images:
        for image_file in uploaded_images:
            # Charger l'image
            image = frg.load_image_file(image_file)
            # Reconnaissance faciale
            image, name, id = recognize(image, TOLERANCE)
            
            # Mise à jour des informations utilisateur
            name_container.info(f"Nom: {name}")
            id_container.success(f"ID: {id}")
            
            # Afficher l'image annotée
            st.image(image)
    else:
        st.info("S'il vous plaît importer une image.")
    
elif choice == "Webcam":
    st.title("Module de reconnaissance faciale")
    st.write(WEBCAM_PROMPT)
    
    # Capture vidéo depuis la webcam
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    FRAME_WINDOW = st.image([])

    while True:
        ret, frame = cam.read()
        if not ret:
            st.error("Échec de la capture de l’image de l’appareil photo")
            st.info("Veuillez fermer l’application qui utilise l’appareil photo et redémarrer l’application")
            st.stop()

        # Reconnaissance faciale sur le flux vidéo
        frame, name, id = recognize(frame, TOLERANCE)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Mise à jour des informations utilisateur
        name_container.info(f"Nom: {name}")
        id_container.success(f"ID: {id}")

        # Afficher le flux vidéo annoté
        FRAME_WINDOW.image(frame)
