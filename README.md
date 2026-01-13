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
