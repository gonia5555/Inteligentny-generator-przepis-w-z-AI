import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
import io
import json
import os
import traceback

# ======== UTF8 PDF — nowy import ========
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
from dotenv import dotenv_values
# do pracy z qdrantem
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from qdrant_client.models import VectorParams, Distance
# do pracy z openai
from openai import OpenAI

QDRANT_COLLECTION_NAME = "Inteligentny generator przepisów z AI"

env = dotenv_values(".env")
### Secrets using Streamlit Cloud Mechanism
# https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management
if 'QDRANT_URL' in st.secrets:
    env['QDRANT_URL'] = st.secrets['QDRANT_URL']
if 'QDRANT_API_KEY' in st.secrets:
    env['QDRANT_API_KEY'] = st.secrets['QDRANT_API_KEY']
##


EMBEDDING_DIM = 1536

EMBEDDING_MODEL = "text-embedding-3-small"

def get_openai_client():
    return OpenAI(api_key=env["OPENAI_API_KEY"])

@st.cache_resource
def get_qdrant_client():
    return QdrantClient(
    url=env["QDRANT_URL"], 
    api_key=env["QDRANT_API_KEY"],
)


def assure_db_collection_exists():
    qdrant_client = get_qdrant_client()
    if not qdrant_client.collection_exists(QDRANT_COLLECTION_NAME):
        print("Tworzę kolekcję")
        qdrant_client.create_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBEDDING_DIM,
                distance=Distance.COSINE,
            ),
        )
    else:
        print("Kolekcja już istnieje")


def get_embeddings(text):
    openai_client = get_openai_client()
    result = openai_client.embeddings.create(
        input=[text],
        model=EMBEDDING_MODEL,
        dimensions=EMBEDDING_DIM,
    )

    return result.data[0].embedding

# >>>>>>>>>> WAŻNE <<<<<<<<<<<
# Tworzymy kolekcję przy starcie aplikacji
assure_db_collection_exists()

# ================================================================
# FUNKCJA TWORZENIA PDF Z OBSŁUGĄ POLSKICH ZNAKÓW
# ================================================================
def create_pdf_from_text(text: str) -> bytes:
    buffer = io.BytesIO()

    pdfmetrics.registerFont(TTFont("DejaVu", "DejaVuSans.ttf"))
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    c.setFont("DejaVu", 12)

    lines = simpleSplit(text, "DejaVu", 12, width - 80)

    y = height - 50
    for line in lines:
        if y < 40:
            c.showPage()
            c.setFont("DejaVu", 12)
            y = height - 50
        c.drawString(40, y, line)
        y -= 18

    c.save()
    buffer.seek(0)
    return buffer.read()


# ================================================================
# KONFIGURACJA JĘZYKÓW
# ================================================================
TEXT = {
    "pl": {
        "title": "🍽️ Inteligentny generator przepisów z AI",
        "sidebar_settings": "🔑 Ustawienia",
        "api_key": "Podaj OpenAI API Key:",
        "need_key": "Podaj API Key w panelu bocznym, aby uruchomić aplikację.",
        "tab1": "🍳 Generator przepisów",
        "tab2": "📚 Zapisane przepisy",
        "select_mode": "Wybierz sposób wyszukiwania przepisu:",
        "mode_photo": "📸 Ze zdjęcia",
        "mode_text": "📝 Z wpisanych produktów",
        "upload": "Wgraj zdjęcie składników",
        "enter_products": "Wpisz produkty oddzielone przecinkami:",
        "recipe_type": "Rodzaj przepisu:",
        "sweet": "Słodki",
        "salty": "Słony",
        "extra_notes": "Dodatkowe uwagi (opcjonalnie)",
        "generate": "🔍 Generuj przepis",
        "must_photo": "Musisz dodać zdjęcie!",
        "must_products": "Wpisz produkty!",
        "recipe_ready": "Przepis gotowy!",
        "save": "💾 Zapisz przepis",
        "download_pdf": "📄 Pobierz PDF",
        "max_saved": "Osiągnięto maksymalną liczbę 10 zapisanych przepisów.",
        "saved_recipes_header": "📚 Twoje zapisane przepisy",
        "delete": "❌ Usuń",
        "clear_all": "🗑️ Wyczyść wszystkie przepisy",
        "no_saved": "Brak zapisanych przepisów.",
        "deleted": "Usunięto przepis",
        "cleared": "Wszystkie przepisy zostały usunięte."
    },

    "en": {
        "title": "🍽️ AI Recipe Generator",
        "sidebar_settings": "🔑 Settings",
        "api_key": "Enter your OpenAI API Key:",
        "need_key": "Enter your API key in the sidebar to run the app.",
        "tab1": "🍳 Recipe Generator",
        "tab2": "📚 Saved Recipes",
        "select_mode": "Choose how to generate the recipe:",
        "mode_photo": "📸 From photo",
        "mode_text": "📝 From written ingredients",
        "upload": "Upload photo of ingredients",
        "enter_products": "Type ingredients separated by commas:",
        "recipe_type": "Recipe type:",
        "sweet": "Sweet",
        "salty": "Savory",
        "extra_notes": "Additional notes (optional)",
        "generate": "🔍 Generate recipe",
        "must_photo": "Please upload a photo!",
        "must_products": "Please enter ingredients!",
        "recipe_ready": "Recipe ready!",
        "save": "💾 Save recipe",
        "download_pdf": "📄 Download PDF",
        "max_saved": "You reached the limit of 10 saved recipes.",
        "saved_recipes_header": "📚 Your saved recipes",
        "delete": "❌ Delete",
        "clear_all": "🗑️ Clear all recipes",
        "no_saved": "No saved recipes.",
        "deleted": "Recipe deleted",
        "cleared": "All recipes cleared."
    },

    "es": {
        "title": "🍽️ Generador Inteligente de Recetas con IA",
        "sidebar_settings": "🔑 Ajustes",
        "api_key": "Ingresa tu clave API de OpenAI:",
        "need_key": "Ingresa la clave API en el panel lateral para ejecutar la aplicación.",
        "tab1": "🍳 Generador de recetas",
        "tab2": "📚 Recetas guardadas",
        "select_mode": "Elige cómo generar la receta:",
        "mode_photo": "📸 Desde una foto",
        "mode_text": "📝 Desde ingredientes escritos",
        "upload": "Sube una foto de los ingredientes",
        "enter_products": "Escribe los ingredientes separados por comas:",
        "recipe_type": "Tipo de receta:",
        "sweet": "Dulce",
        "salty": "Salado",
        "extra_notes": "Notas adicionales (opcional)",
        "generate": "🔍 Generar receta",
        "must_photo": "¡Debes subir una foto!",
        "must_products": "¡Escribe los ingredientes!",
        "recipe_ready": "¡Receta lista!",
        "save": "💾 Guardar receta",
        "download_pdf": "📄 Descargar PDF",
        "max_saved": "Se alcanzó el límite de 10 recetas guardadas.",
        "saved_recipes_header": "📚 Tus recetas guardadas",
        "delete": "❌ Eliminar",
        "clear_all": "🗑️ Borrar todas las recetas",
        "no_saved": "No hay recetas guardadas.",
        "deleted": "Receta eliminada",
        "cleared": "Todas las recetas fueron eliminadas."
    }
}


# ================================================================
# SIDEBAR (chef.png + opis)
# ================================================================
st.sidebar.header("🌍 Language / Idioma / Język")
lang = st.sidebar.selectbox(
    "Choose language:",
    ["pl", "en", "es"],
    format_func=lambda x: {"pl": "Polski", "en": "English", "es": "Español"}[x]
)

T = TEXT[lang]
st.sidebar.image("chef.png", width=140)
st.sidebar.markdown("### 👨‍🍳 **Chef AI**\nTwój asystent kulinarny\n")

st.sidebar.header("🔑 API Key")
api_key = st.sidebar.text_input("OpenAI API Key:", type="password")

st.sidebar.header("🌍 Language / Idioma / Język")
lang = st.sidebar.selectbox(
    "Choose language:",
    ["pl", "en", "es"],
    format_func=lambda x: {"pl": "Polski", "en": "English", "es": "Español"}[x]
)

T = TEXT[lang]


# ================================================================
# STRONA GŁÓWNA
# ================================================================
st.set_page_config(page_title=T["title"], page_icon="🍽️")
st.title(T["title"])

# ▶ ▶ ▶ **NOWE – MAŁE ZDJĘCIE POD TYTUŁEM**
st.image(
    "dania1.jpg",
    width=500,
    caption=" "
)

if not api_key:
    st.warning(T["need_key"])
    st.stop()

client = OpenAI(api_key=api_key)


# ================================================================
# TRWAŁE ZAPISYWANIE
# ================================================================
SAVE_FILE = "recipes.json"

def load_recipes():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_recipes(recipes):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(recipes, f, ensure_ascii=False, indent=2)


if "saved_recipes" not in st.session_state:
    st.session_state.saved_recipes = load_recipes()

if "current_recipe" not in st.session_state:
    st.session_state.current_recipe = None


# ================================================================
# CALLBACKS
# ================================================================
def delete_recipe_by_index(index: int):
    try:
        st.session_state.saved_recipes.pop(index)
        save_recipes(st.session_state.saved_recipes)
        st.session_state.deletion_message = T["deleted"]
    except:
        st.session_state.deletion_message = "Error"

def clear_all_recipes():
    st.session_state.saved_recipes = []
    save_recipes([])
    st.session_state.deletion_message = T["cleared"]


# ================================================================
# ZAKŁADKI
# ================================================================
tab1, tab2 = st.tabs([T["tab1"], T["tab2"]])


# ================================================================
# TAB 1 — GENERATOR
# ================================================================
with tab1:

    st.subheader(T["select_mode"])
    mode = st.radio("Mode:", [T["mode_photo"], T["mode_text"]])

    uploaded = None
    product_text = ""

    if mode == T["mode_photo"]:
        uploaded = st.file_uploader(T["upload"], type=["jpg", "jpeg", "png"])

    if mode == T["mode_text"]:
        product_text = st.text_area(T["enter_products"])

    option = st.radio(T["recipe_type"], [T["sweet"], T["salty"]])
    additional_text = st.text_input(T["extra_notes"])


    def generate_recipe(prompt, image_bytes=None):
        try:
            content = [{"type": "text", "text": prompt}]

            if image_bytes:
                img_b64 = base64.b64encode(image_bytes).decode()
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{img_b64}"}
                })

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are a professional chef and always answer in {lang}."},
                    {"role": "user", "content": content}
                ],
                max_tokens=800,
                temperature=0.7
            )
            return response.choices[0].message.content

        except Exception as e:
            return f"Error: {e}"


    if st.button(T["generate"]):
        if mode == T["mode_photo"] and not uploaded:
            st.error(T["must_photo"])
        elif mode == T["mode_text"] and not product_text.strip():
            st.error(T["must_products"])
        else:
            try:
                if mode == T["mode_photo"]:
                    image_bytes = uploaded.read()
                    prompt = (
                        f"Recognize ingredients from the photo and create a simple {option} recipe "
                        f"in {lang}. Notes: {additional_text}"
                    )
                    recipe = generate_recipe(prompt, image_bytes=image_bytes)

                    st.image(Image.open(io.BytesIO(image_bytes)), use_container_width=True)

                else:
                    prompt = (
                        f"Ingredients: {product_text}. Create a {option} recipe in {lang}. "
                        f"Notes: {additional_text}"
                    )
                    recipe = generate_recipe(prompt)

                st.session_state.current_recipe = recipe
                st.success(T["recipe_ready"])
                st.markdown(recipe)

                # PDF
                pdf_bytes = create_pdf_from_text(recipe)
                st.download_button(
                    T["download_pdf"],
                    data=pdf_bytes,
                    file_name="recipe.pdf",
                    mime="application/pdf"
                )

            except:
                st.error("Error")
                st.code(traceback.format_exc())


    if st.session_state.current_recipe:
        if len(st.session_state.saved_recipes) < 10:
            if st.button(T["save"]):
                st.session_state.saved_recipes.append(st.session_state.current_recipe)
                save_recipes(st.session_state.saved_recipes)
                st.success("Saved!")
        else:
            st.warning(T["max_saved"])


# ================================================================
# TAB 2 — ZAPISANE PRZEPISY
# ================================================================
with tab2:
    st.subheader(T["saved_recipes_header"])

    if "deletion_message" in st.session_state and st.session_state.deletion_message:
        st.info(st.session_state.deletion_message)
        st.session_state.deletion_message = ""

    if st.session_state.saved_recipes:
        for idx, r in enumerate(st.session_state.saved_recipes, 1):
            st.markdown(f"### 🥘 Recipe {idx}")
            st.markdown(r)

            pdf_bytes = create_pdf_from_text(r)
            st.download_button(
                f"{T['download_pdf']} #{idx}",
                data=pdf_bytes,
                file_name=f"recipe_{idx}.pdf",
                mime="application/pdf",
                key=f"pdf_{idx}"
            )

            st.button(T["delete"], key=f"del_{idx}", on_click=delete_recipe_by_index, args=(idx - 1,))
            st.markdown("---")

        st.button(T["clear_all"], on_click=clear_all_recipes)

    else:
        st.info(T["no_saved"])
