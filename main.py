# main.py
import streamlit as st
import streamlit_option_menu as option_menu
from page1 import show_page as show_page1
from page2 import show_page as show_page2
from page3 import show_page as show_page3

def streamlit_menu(menubar):
    if menubar:
        selected = option_menu.option_menu(
            menu_title=None,  # required
            options=["Page 1", "Page 2", "Page 3"],  # required
            icons=["house", "list-task", "gear"],  # optional
            menu_icon="cast",  # optional
            default_index=0,  # optional
            orientation="horizontal",
            styles={
                "container": {"padding": "5px","margin": "0px", "background-color": "#F1F1F1"},
                "icon": {"color": "crimson", "font-size": "15px"},
                "nav-link": {
                    "font-size": "15px",
                    "color": "black",
                    "text-align": "center",
                    "margin-top": "1px",
                    "padding":"5px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#6739B7","color": "white"},
            },
        )
        return selected
    
selected = streamlit_menu(menubar=True)

if selected == "Page 1":
    show_page1()
elif selected == "Page 2":
    show_page2()
elif selected == "Page 3":
    show_page3()
