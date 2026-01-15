# 🍽️ AI Recipe Generator

A web application built with **Streamlit**, powered by **OpenAI GPT-4o** and **Qdrant**, that allows users to generate cooking recipes:
- from a photo of ingredients  
- from a manually entered list of products  

Users can save recipes, download them as **PDF files**, and use the application in **three languages**: Polish, English, and Spanish.

---

## 🚀 Features

- 📸 Generate recipes from ingredient photos  
- 📝 Generate recipes from a typed list of ingredients  
- 🌍 Multilingual support (PL / EN / ES)  
- 🤖 AI acting as a professional chef  
- 💾 Save up to 10 recipes  
- 📄 Export recipes to PDF (full UTF-8 support, including special characters)  
- 🧠 Qdrant integration (ready for RAG and semantic search)  
- ☁️ Streamlit Cloud and Secrets support  

---

## 🛠️ Technology Stack

- **Python 3.10+**
- **Streamlit** – user interface  
- **OpenAI API** – content generation and embeddings  
- **Qdrant** – vector database  
- **ReportLab** – PDF generation  
- **Pillow (PIL)** – image processing  
- **python-dotenv** – environment variable management  

---

## 🧠 Role of Qdrant

Qdrant is used as a **vector database**, prepared for:
- storing embeddings  
- future semantic search  
- extending the application with a chatbot or RAG mechanism  

The collection is created automatically when the application starts.

---

## 📦 Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```
 ## ▶️ Live Application

The application is available online at:

🔗 **https://gonia5555recipegenerator.streamlit.app/**

---

## ▶️ Running the Application Locally

To start the application locally, run the following command in the project directory:

```bash
streamlit run app11.py
The application will be available at:

http://localhost:8501

```
## 🔑 OpenAI API Key Required

To use the application, an **OpenAI API Key is required**.

- The API key must be entered in the **sidebar input field** inside the application.
- The application **will not run** until a valid API key is provided.
- The API key is **not stored permanently** and is used only for the current session.



# 🍽️ Inteligentny Generator Przepisów z AI

Aplikacja webowa oparta na **Streamlit**, wykorzystująca **OpenAI GPT-4o** oraz **Qdrant**, która umożliwia generowanie przepisów kulinarnych:
- na podstawie zdjęcia składników  
- z listy produktów wpisanej ręcznie  

Użytkownik może zapisywać przepisy, pobierać je w formacie **PDF** oraz korzystać z aplikacji w **trzech językach**: polskim, angielskim i hiszpańskim.

---

## 🚀 Funkcjonalności

- 📸 Generowanie przepisów ze zdjęcia składników  
- 📝 Generowanie przepisów z wpisanej listy produktów  
- 🌍 Obsługa wielu języków (PL / EN / ES)  
- 🤖 AI w roli profesjonalnego szefa kuchni  
- 💾 Zapisywanie do 10 przepisów  
- 📄 Eksport przepisów do PDF (pełna obsługa UTF-8 / polskich znaków)  
- 🧠 Integracja z Qdrant (gotowa pod RAG i wyszukiwanie semantyczne)  
- ☁️ Obsługa Streamlit Cloud i Secrets  

---

## 🛠️ Stack technologiczny

- **Python 3.10+**
- **Streamlit** – interfejs użytkownika  
- **OpenAI API** – generowanie treści i embeddingów  
- **Qdrant** – wektorowa baza danych  
- **ReportLab** – generowanie plików PDF  
- **Pillow (PIL)** – obsługa obrazów  
- **python-dotenv** – zarządzanie zmiennymi środowiskowymi  

---

## 🧠 Rola Qdrant

Qdrant jest używany jako **wektorowa baza danych**, przygotowana do:
- przechowywania embeddingów  
- przyszłego wyszukiwania semantycznego  
- rozbudowy aplikacji o chatbot lub mechanizm RAG  

Kolekcja jest tworzona automatycznie przy starcie aplikacji.

---

## 📦 Instalacja lokalna

### 1. Klonowanie repozytorium
```bash
git clone https://github.com/twoj-login/twoje-repo.git
cd twoje-repo
```
## ▶️ Aplikacja online (Live)

Aplikacja jest dostępna online pod adresem:

🔗 **https://gonia5555recipegenerator.streamlit.app/**

---

## ▶️ Uruchomienie aplikacji lokalnie

Aby uruchomić aplikację lokalnie, w katalogu projektu wykonaj polecenie:

```bash
streamlit run app11.py
```
Aplikacja będzie dostępna pod adresem:

🔗 **http://localhost:8501**

---

## 🔑 Wymagany klucz OpenAI API

Do korzystania z aplikacji **wymagany jest klucz OpenAI API**.

- Klucz API należy wpisać w **polu bocznym (sidebar)** w aplikacji.
- Aplikacja **nie uruchomi się**, dopóki nie zostanie podany poprawny klucz API.
- Klucz API **nie jest zapisywany na stałe** i jest używany wyłącznie w trakcie bieżącej sesji.