import pandas as pd
import numpy as np
import requests
import re
import streamlit as st 



st.title("Configuración del bot")

enable_day_kill_flip = st.checkbox(
    label = "¿Revelar roles tras asesinato diurno?",
    value = False,
    help = "Marca esta casilla para que el bot revele el obituario de un jugador asesinado durante el día,"
)

enable_lynch_flip = st.checkbox(
    label = "¿Revelar roles tras linchamiento?",
    value = False,
    help = "Marca esta casilla para revelar roles tras linchamiento."
)

enable_eod_flip = st.checkbox(
    label = "¿Resolver final del día?",
    value = False,
    help = "Marca esta casilla para permitir al bot revelar el rol del linchado tras el final del día"
)

enable_count_after_msgs=st.checkbox(
        label = "¿Postear recuentos por número total de mensajes?",
        value = False,
        help = "Si se marca la casilla, el bot generará un recuento automático periódicamente aunque no haya cambios en la votación."
    )

if enable_count_after_msgs:
    msgs_to_wait = st.slider(
        label="Número de mensajes antes del recuento",
        min_value=1,
        max_value=300,
        value=30,
        step=1
        )
else:
    msgs_to_wait = 30000


enable_count_after_votes=st.checkbox(
    label = "¿Postear recuentos en función del número de votos emitidos?",
    value = True,
    help = "Si se marca la casilla, el bot generará recuentos en intervalos definidos por la cantidad de votos emitidos."
)

if enable_count_after_votes:
    votes_to_wait = st.slider(
        label="Número de votos antes del recuento",
        min_value=1,
        max_value=100,
        value=1,
        step=1
    )
else:
    votes_to_wait = 30000

## Define cfg
bot_config = {
        "push_vote_count_interval": [int(msgs_to_wait)],
        "votes_until_update": [int(votes_to_wait)],
        "update_time_seconds":[30],
        "GM": [""],
        "Moderators":[""]
    }


bot_config_pd = pd.DataFrame(bot_config)

if  "bot_config" not in st.session_state:
    st.session_state["bot_config"] = bot_config_pd


st.write(bot_config_pd)