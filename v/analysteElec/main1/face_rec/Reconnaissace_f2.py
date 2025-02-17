import streamlit as st
import cv2
from deepface import DeepFace
import face_recognition as frg
import yaml

st.set_page_config(layout="wide")

# Charger les configurations
cfg = yaml.load(open('config.yaml', 'r'), Loader=yaml.FullLoader)
PICTURE_PROMPT = cfg['INFO']['PICTURE_PROMPT']
WEBCAM_PROMPT = cfg['INFO']['WEBCAM_PROMPT']

# Menu latéral
st.sidebar.title("Paramètres")
menu = ["Photo", "Webcam"]
choice = st.sidebar.selectbox("Type d'entrée", menu)
TOLERANCE = st.sidebar.slider("Tolérance", 0.0, 1.0, 0.5, 0.01)

# Informations utilisateur
st.sidebar.title("Information sur utilisateur")
name_container = st.sidebar.empty()
id_container = st.sidebar.empty()
emotion_container = st.sidebar.empty()
age_container = st.sidebar.empty()
gender_container = st.sidebar.empty()

name_container.info('Nom: Inconnu')
id_container.success('ID: Inconnu')
emotion_container.warning('Émotion: Inconnue')
age_container.warning('Âge: Inconnu')
gender_container.warning('Sexe: Inconnu')

# Fonction pour analyser une image
def analyze_image(image):
    results = DeepFace.analyze(image, actions=["age", "gender", "emotion"], enforce_detection=False)
    return results

# Gestion des images
if choice == "Photo":
    st.title("ODF-Reconnaissance faciale - IMAGE")
    st.write("Cette fonctionnalité permet de faire la reconnaissance et l'analyse faciale sur image en temps réel.")
    uploaded_images = st.file_uploader("Importer", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)
    
    if len(uploaded_images) != 0:
        for image_file in uploaded_images:
            image = frg.load_image_file(image_file)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Analyse avec DeepFace
            try:
                results = analyze_image(image_rgb)
                emotion = max(results['emotion'], key=results['emotion'].get)
                name_container.info(f"Nom: Inconnu")
                id_container.success(f"ID: Inconnu")
                emotion_container.info(f"Émotion: {emotion}")
                age_container.info(f"Âge: {results['age']}")
                gender_container.info(f"Sexe: {results['gender']}")
                st.image(image_rgb)
            except Exception as e:
                st.error(f"Erreur d'analyse : {str(e)}")
    else:
        st.info("S'il vous plaît importer une image")

# Gestion de la webcam
elif choice == "Webcam":
    st.title("ODF-Reconnaissance faciale - WEBCAM")
    st.write(WEBCAM_PROMPT)
    
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    FRAME_WINDOW = st.image([])

    while True:
        ret, frame = cam.read()
        if not ret:
            st.error("Échec de la capture de l’image de l’appareil photo")
            st.stop()
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Analyse avec DeepFace
        try:
            results = analyze_image(frame_rgb)
            emotion = max(results['emotion'], key=results['emotion'].get)
            name_container.info(f"Nom: Inconnu")
            id_container.success(f"ID: Inconnu")
            emotion_container.info(f"Émotion: {emotion}")
            age_container.info(f"Âge: {results['age']}")
            gender_container.info(f"Sexe: {results['gender']}")
            FRAME_WINDOW.image(frame_rgb)
        except Exception as e:
            st.error(f"Erreur d'analyse : {str(e)}")
