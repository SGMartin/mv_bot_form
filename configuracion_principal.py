import pandas as pd
import numpy as np
import requests
import re
import streamlit as st 

from bs4 import BeautifulSoup

st.title("Configurador de partidas de mafia")

with st.sidebar:
    cfg_config = st.radio(
        "Elige una opción de configuración",
        ("Desde 0", "Tengo mi propio fichero")
    )

st.subheader("Tu configuración")

if cfg_config == "Desde 0":
    
    no_lynch_allowed = st.checkbox(
        label = "¿Está permitido el no linchamiento?",
        value = True,
        help = "Si no quieres habilitar el no linchamiento, desmarca la casilla."
    )

    next_player = st.text_input(
        label = "Añadir jugador",
        value = "",
        help = "Introduce el nick del jugador en mediavida",
        placeholder = "Jiub"
        )

    vote_config = {
        "player": ["no_lynch"],
        "can_be_voted": [int(no_lynch_allowed)],
        "allowed_votes": [0],
        "mod_to_lynch":[0],
        "is_mayor": [0]
    }

    pd_config = pd.DataFrame.from_dict(vote_config)

    if  "vote_config" not in st.session_state:
        st.session_state["vote_config"] = pd_config

    is_valid_player = False
    if next_player != "":
        ## check if player exists in MV
        this_player = requests.get(f"https://www.mediavida.com/id/{next_player}")

        if this_player.status_code != 404:
            this_profile = BeautifulSoup(this_player.text, "html.parser")
            profile_header = this_profile.find("h1")

            if re.findall("^ERROR", profile_header.text):
                st.write("Este perfil no existe en MV")
            else:
                this_avatar = this_profile.find("div", class_ = ["user-avatar"]).find("img")
                this_avatar = this_avatar["src"]
                st.write(f"![test]({this_avatar})")

                is_valid_player = True
                allowed_votes = st.slider(
                    label = "Votos simultáneos para este jugador",
                    min_value = 0,
                    max_value = 10,
                    value = 1,
                    step = 1,
                    help = "Número de votos simultáneos que puede emitir este jugador"
                    )
                
                mods = {-1: "Odiado", 0: "Neutral", 1: "Amado"}
                mod_to_lynch = st.selectbox(
                    label = "Modificadores de voto",
                    options = [-1,0,1],
                    index = 1,
                    format_func=lambda x: mods[x]
                )
    
                can_be_voted = st.checkbox(
                    label = "Este jugador puede ser linchado",
                    value = True,
                    help = "Marca la casilla si este jugador puede ser votado y linchado."
                    )

                is_mayor = st.checkbox(
                    label = "Este jugador puede ser alcalde",
                    value = False,
                    help = "Marca la casilla si este jugador puede revelarse como alcalde."
                    )


                add_player = st.button(
                    label = "Añadir jugador"
                )

                if add_player:
                    ## Check if our player is already in the data.frame and in that case
                    ## update it instead of appending

                    if next_player in st.session_state["vote_config"]["player"].tolist():
                        pd_config = st.session_state["vote_config"]
                        pd_config.loc[
                            pd_config["player"] == next_player,
                            ["can_be_voted", "allowed_votes", "mod_to_lynch", "is_mayor"]] = [
                                int(can_be_voted),
                                allowed_votes,
                                mod_to_lynch,
                                int(is_mayor)
                            ]
                    else:
                        new_player = pd.DataFrame.from_dict(
                            {
                                "player": [next_player],
                                "can_be_voted": [int(can_be_voted)],
                                "allowed_votes": [allowed_votes],
                                "mod_to_lynch": [mod_to_lynch],
                                "is_mayor": [int(is_mayor)]
                            }
                        )
                        pd_config = pd.concat([st.session_state["vote_config"], new_player])
                    st.session_state["vote_config"] = pd_config

    st.write(st.session_state.vote_config)

col_left,col_center,col_right = st.columns(3, gap = "small")

with col_left:
    st.download_button(
        label = "Descargar configuración",
        data = st.session_state.vote_config.to_csv(index=False).encode("utf8"),
        file_name = "vote_config.csv")

with col_right:
    show_as_text = st.button(label = "Mostrar en texto plano")

if show_as_text:
    st.code(st.session_state.vote_config.to_csv(index=False))