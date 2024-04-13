import streamlit as st
import pandas as pd

st.header("Tabla de roles", divider = True)
st.write("Esta tabla es opcional y de texto libre.")


if  "vote_config" not in st.session_state:
    st.write("**ERROR: ¡Rellena primero la configuración principal!**")
else:
    ## get players
    player_list = st.session_state["vote_config"]["player"].tolist()[1:]

    if  "role_list" not in st.session_state:
        ## make default 0 table
        role_list_table = pd.DataFrame(
            {"player": player_list,
            "team": [""] * len(player_list),
            "role": [""] * len(player_list),
            }
        )

        st.session_state["role_list"] = role_list_table
    else:
        role_list_table = st.session_state["role_list"]
    
    this_player = st.selectbox("**Selecciona un jugador**", options = player_list, index=0)

    # teams to choose
    teams_to_choose = ["pueblo", "mafia", "independiente", "neutral"]

    this_player_team = st.selectbox("**Bando**", teams_to_choose, index=0)
    this_player_role = st.text_input(label = "**Rol**", value = "vanilla")

    set_player_role = st.button(label = "Añadir bando y rol")
    
    if set_player_role:
        if this_player in role_list_table["player"].tolist():
            role_list_table.loc[
                role_list_table["player"] == this_player,
                ["team", "role"]] = [this_player_team, this_player_role]
        else:
            new_player = pd.DataFrame.from_dict(
                            {
                                "player": [this_player],
                                "team": [this_player_team],
                                "role": [this_player_role]
                            }
                        )
            role_list_table = pd.concat(
                [role_list_table, new_player]
                )


    ## SAVE attack and defense to session s tate
    st.session_state["role_list"] = role_list_table
    st.subheader("Tabla de roles actual")
    st.write(st.session_state.role_list)

    col_left,col_center,col_right = st.columns(3, gap = "small")

    with col_left:
        st.download_button(
            label = "Descargar configuración",
            data = st.session_state.role_list.to_csv(index=False).encode("utf8"),
            file_name = "role_list.csv")

    with col_right:
        show_as_text = st.button(label = "Mostrar en texto plano")

    if show_as_text:
        st.code(st.session_state.role_list.to_csv(index=False))

