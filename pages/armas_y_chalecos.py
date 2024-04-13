import pandas as pd
import streamlit as st


st.title("Configuración de armas y chalecos")

attack_defense = {
    "player": [],
    "attack": [],
    "defense": [],
    "last_shot": []
}


attack_and_defense = pd.DataFrame.from_dict(attack_defense)

if  "vote_config" not in st.session_state:
    st.write("**ERROR: ¡Rellena primero la configuración principal!**")
else:
    ## get players
    player_list = st.session_state["vote_config"]["player"].tolist()[1:]

    if  "attack_and_defense" not in st.session_state:
        ## make default 0 table
        attack_and_defense_table = pd.DataFrame(
            {"player": player_list,
            "attack": [0] * len(player_list),
            "defense": [0] * len(player_list),
            "last_shot": [0] * len(player_list)
            }
        )

        st.session_state["attack_and_defense"] = attack_and_defense_table
    else:
        attack_and_defense_table = st.session_state["attack_and_defense"]
    
    this_player = st.selectbox("Selecciona un jugador", options = player_list, index=0)

    max_attack = st.slider(
                    label = "Disparos disponibles para este jugador",
                    min_value = 0,
                    max_value = 10,
                    value = 0,
                    step = 1,
                    help = "Número de disparos que puede ejecutar este jugador."
                    )
    
    max_defense = st.slider(
                    label = "Chalecos disponibles para este jugador",
                    min_value = 0,
                    max_value = 10,
                    value = 0,
                    step = 1,
                    help = "Número de chalecos antibalas que tiene este jugador."
                    )

    change_attack_defense = st.button(label = "Confirmar ataque y defensa")

    if change_attack_defense:
        if this_player in attack_and_defense_table["player"].tolist():
            attack_and_defense_table.loc[
                attack_and_defense_table["player"] == this_player,
                ["attack", "defense"]] = [int(max_attack), int(max_defense)]
        else:
            new_player = pd.DataFrame.from_dict(
                            {
                                "player": [this_player],
                                "attack": [int(max_attack)],
                                "defense": [int(max_defense)],
                                "last_shot": [0]
                            }
                        )
            attack_and_defense_table = pd.concat(
                [attack_and_defense_table, new_player]
                )
  
        
    ## SAVE attack and defense to session s tate
    st.session_state["attack_and_defense"] = attack_and_defense_table
    st.subheader("Tabla de disparos actual")
    st.write(st.session_state.attack_and_defense)

    col_left,col_center,col_right = st.columns(3, gap = "small")

    with col_left:
        st.download_button(
            label = "Descargar configuración",
            data = st.session_state.attack_and_defense.to_csv(index=False).encode("utf8"),
            file_name = "attack_and_defense.csv")

    with col_right:
        show_as_text = st.button(label = "Mostrar en texto plano")

    if show_as_text:
        st.code(st.session_state.attack_and_defense.to_csv(index=False))
