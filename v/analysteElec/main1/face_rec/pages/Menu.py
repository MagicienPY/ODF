import streamlit as st 
import cv2
import yaml 
import pickle 
from utils import submitNew, get_info_from_id, deleteOne
import numpy as np

st.set_page_config(layout="wide")
st.title("ODF-reconnaissance faciale")
st.write("Cette fonctionnalité est utilisée pour ajouter de nouveaux visages.")

menu = ["Ajouter","Supprimer"]
choice = st.sidebar.selectbox("Options",menu)
if choice == "Ajouter":
    name = st.text_input("Name",placeholder='Entrer le nom')
    id = st.text_input("ID",placeholder='Entrer ID')
    upload = st.radio("Importer une image ou utiliser la webcam",("Upload","Webcam"))
    if upload == "Upload":
        uploaded_image = st.file_uploader("Upload",type=['jpg','png','jpeg'])
        if uploaded_image is not None:
            st.image(uploaded_image)
            submit_btn = st.button("Soumettre",key="submit_btn")
            if submit_btn:
                if name == "" or id == "":
                    st.error("entrez le nom et l'ID")
                else:
                    ret = submitNew(name, id, uploaded_image)
                    if ret == 1: 
                        st.success("Ajout reussi")
                    elif ret == 0: 
                        st.error("l'ID existe deja")
                    elif ret == -1: 
                        st.error("Il y'a pas de visage dans cette photo")
    elif upload == "Webcam":
        img_file_buffer = st.camera_input("Prendre une photo")
        submit_btn = st.button("Submit",key="submit_btn")
        if img_file_buffer is not None:
            bytes_data = img_file_buffer.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            if submit_btn: 
                if name == "" or id == "":
                    st.error("Entrez le nom et l'ID ")
                else:
                    ret = submitNew(name, id, cv2_img)
                    if ret == 1: 
                        st.success("Ajout reussi")
                    elif ret == 0: 
                        st.error("l'ID existe deja")
                    elif ret == -1: 
                        st.error("Il y'a pas de visage dans cette photo")
elif choice == "Supprimer":
    def del_btn_callback(id):
        deleteOne(id)
        st.success("Personnage supprime")
        
    id = st.text_input("ID",placeholder='Entrer id')
    submit_btn = st.button("Submit",key="submit_btn")
    if submit_btn:
        name, image,_ = get_info_from_id(id)
        if name == None and image == None:
            st.error("le personnage n'existe pas.")
        else:
            st.success(f"le nom du personnage avec l'ID {id} est: {name}")
            st.warning("Verifiez l'image avant pour vous auurez que vous supprimez le bon personnage")
            st.image(image)
            del_btn = st.button("Delete",key="del_btn",on_click=del_btn_callback, args=(id,)) 
        
