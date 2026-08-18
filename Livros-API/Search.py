
import streamlit as st
import requests as r
from features import Enginer
from rotas import API

fix_features = Enginer()
api = API()

if "filtros_select" not in st.session_state:
    st.session_state["filtros_select"] = {}


@st.dialog("O que você de deseja?")
def filtros():
    if st.checkbox("Termo"):
        term, term_value = st.columns([2,4], vertical_alignment="top")
        st.session_state["filtros_select"]["terms"] = term.selectbox("Termo", ("intitle","inauthor","inpublisher","subject","isbn","lccn","oclc"))
        st.session_state["filtros_select"]["terms_value"] = term_value.text_input(label="Value", placeholder="Search", label_visibility="hidden")
    else:
        st.session_state["filtros_select"].pop("terms", "")
        st.session_state["filtros_select"].pop("terms_value", "")

    if st.checkbox("Viz"):
        st.session_state["filtros_select"]["filter"] = st.selectbox("Viz", ("partial", "full", "free-ebooks", "paid-ebooks", "ebooks"))
    else:
        st.session_state["filtros_select"].pop("filter", "")

    if st.checkbox("Print"):
        st.session_state["filtros_select"]["printType"] = st.selectbox("Print",("all", "books", "magazines"))
    else:
        st.session_state["filtros_select"].pop("printType", "")

    if st.checkbox("Sort"):
        st.session_state["filtros_select"]["orderBy"] = st.selectbox("Sort", ("relevance","newest"))
    else:
        st.session_state["filtros_select"].pop("orderBy", "")


st.set_page_config(
		page_title= "Tarot Reading", # String or None. Strings get appended with "• Streamlit".
		 layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
		 #initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
		 #page_icon=None,  # String, anything supported by st.image, or None.
)


# front end elements of the web page 
html_temp = """ 
    <div style ="background-color:white;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Tarot Reading App</h1> 
    </div> 
    """
      
# display the front end aspect
st.markdown(html_temp, unsafe_allow_html = True) 
st.session_state["filtros_select"]["q"] = st.text_input(label="Search",placeholder="Search...")

left_button, right_button = st.columns([1,12], vertical_alignment="top")

if right_button.button("Filtros"):

   filtros()


if left_button.button("Search"):  

    with st.status("Requisitando data...", expanded=True) as status:

        st.write("Buscando Livro...")
        base = api.get_requisicao("https://www.googleapis.com/books/v1/volumes?", st.session_state["filtros_select"])

        if base == None:
            st.text("Nenhum livro com essa combinação")
        else:
            st.write("Filtrando...")
            dados = fix_features.clean_data(base)
            st.session_state["df"] = dados

            st.write("Montando Exibição..")
            st.switch_page("pages/Livros.py")
                
            status.update(
                label="Livros encontrado!", state="complete", expanded=False
            )
        
st.sidebar.subheader("About App")

feedback = st.sidebar.slider('How much would you rate this app?',min_value=0,max_value=5,step=1)

if feedback:
  st.header("Thank you for rating the app!")
  st.info("Caution: This is just a prediction and not doctoral advice. Kindly see a doctor if you feel the symptoms persist.")