import streamlit as st
import requests
import json

# Configuration de la page
st.set_page_config(page_title="ProxyAPI - Recommandations", page_icon="📡", layout="centered")

st.title("Application ProxyAPI (Azure → Render)")
st.write("Cette application appelle la fonction Azure Function `proxyAPI` pour interroger l'API FastAPI hébergée sur Render.")

# Entrées utilisateur
user_id = st.text_input("ID Utilisateur", placeholder="Ex: 3")
method = st.selectbox("Méthode", ["content_based", "collaborative"])

# URL de ton Azure Function.
azure_function_url = st.text_input(
    "URL de ton Azure Function",
    value="https://jadore-azure.azurewebsites.net/api/proxyAPI",
)

# Bouton d’envoi
if st.button("Obtenir les recommandations"):
    if not user_id or not method:
        st.error("Merci de renseigner un ID utilisateur et une méthode.")
    elif not azure_function_url:
        st.error("Merci de renseigner l'URL de l'Azure Function.")
    else:
        with st.spinner("Envoi de la requête à Azure Function..."):
            try:
                # Appel à ton Azure Function (GET)
                response = requests.get(
                    azure_function_url,
                    params={"user_id": user_id, "method": method},
                    timeout=15
                )

                if response.status_code == 200:
                    data = response.json()
                    st.success("Recommandations reçues !")

                    # Affichage formaté
                    st.json(data)

                    # Si le retour contient une liste de recommandations, on les affiche joliment
                    if isinstance(data, dict) and "recommandations" in data:
                        st.write("### Liste des recommandations :")
                        for idx, reco in enumerate(data["recommandations"], start=1):
                            st.write(f"**{idx}.** {reco}")

                else:
                    st.error(f"Erreur {response.status_code} : {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"Erreur de connexion : {e}")

# Pied de page
st.markdown("---")
st.caption("App développée avec Streamlit • Azure Functions • FastAPI • Render")
