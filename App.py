import streamlit as st
import feedparser
import os
from google import genai

st.set_page_config(page_title="Agente Noticias Energía", layout="centered")

st.title("⚡ Agente IA: Noticias del Sector Energético")
st.caption("Recopila noticias diarias, clasifica por temas y genera resúmenes.")

# Configurar cliente API
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

# Obtener noticias de un feed RSS
@st.cache_data(ttl=3600)
def fetch_news():
    feed_url = "https://www.energynews.es/feed/"  # Fuente RSS sectorial
    feed = feedparser.parse(feed_url)
    items = []
    for entry in feed.entries[:8]:
        items.append(f"Titular: {entry.title}\nDetalle: {entry.summary}\n")
    return "\n---\n".join(items)

news_data = fetch_news()

st.subheader("1. Titulares detectados hoy")
with st.expander("Ver titulares brutos recopilados"):
    st.text(news_data)

st.subheader("2. Procesamiento del Agente")
if st.button("Generar análisis y resumen clasificado"):
    if not client:
        st.error("No se ha configurado la variable GEMINI_API_KEY.")
    else:
        with st.spinner("Analizando, clasificando y resumiendo..."):
            prompt = f"""
            Actúa como un analista experto del sector energético.
            A partir de las siguientes noticias recopiladas, clasifica y resume los puntos clave en las siguientes categorías obligatorias:
            - Precios
            - Renovables
            - Almacenamiento
            - Regulación
            - Demanda

            Para cada categoría, indica únicamente los cambios o novedades más relevantes. Si en alguna categoría no hay noticias, indica "Sin novedades relevantes hoy".

            Noticias:
            {news_data}
            """
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            st.markdown("### Resumen Clasificado")
            st.markdown(response.text)
