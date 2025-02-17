import streamlit as st
import sqlite3
import hashlib

# Connexion à la base de données
conn = sqlite3.connect("users.db")
c = conn.cursor()

# Création de la table si elle n'existe pas
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password_hash TEXT,
                role TEXT
            )''')
conn.commit()

def verify_password(stored_password, provided_password):
    return hashlib.sha256(provided_password.encode()).hexdigest() == stored_password

# Interface utilisateur avec Streamlit
st.title("Connexion")

username = st.text_input("Identifiant")
password = st.text_input("Mot de passe", type="password")

if st.button("Se connecter"):
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    
    if user and verify_password(user[2], password):
        st.session_state["user_id"] = user[0]
        st.session_state["username"] = user[1]
        
        role_redirects = {
            "osint": "http://localhost:8501/osint",
            "admin": "http://localhost:8501/admin",
            "AE": "http://212.83.168.217:8501/",
            "AM": "http://212.83.168.217:8502/",
            "SA": "http://localhost:8501/",
            "SUP": "http://212.83.168.217:8505/"
        }
        
        st.success(f"Bienvenue, {user[1]}!")
        if user[3] in role_redirects:
            st.markdown(f"[Accéder à votre espace]({role_redirects[user[3]]})")
        else:
            st.error("Rôle inconnu.")
    else:
        st.error("Nom d'utilisateur ou mot de passe incorrect.")

