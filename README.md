# **📰 News Summarization & Categorization App** 🧠📑  

A **Flask-based web application** that extracts, summarizes, and categorizes news articles from **India Today**. The system retrieves the **news content**, applies **text processing and NLP techniques**, and classifies the news into different categories like **Politics, Business, Technology, Health, Environment, Entertainment, and Sports**. It also features **GitHub OAuth authentication** and an **admin panel** to view historical summaries.  

---

## **🚀 Features**  

✅ **News Extraction** – Scrapes full news articles from **India Today**.  

✅ **AI-Powered Summarization** – Uses **LSA (Latent Semantic Analysis)** from **Sumy** for automatic summarization.  

✅ **News Categorization** – Classifies news into categories like **Politics, Business, Technology, Health, Entertainment, etc.**  

✅ **POS (Part of Speech) Tagging** – Identifies **nouns, verbs, adjectives**, and other word types in the article.  

✅ **Database Storage** – Stores news summaries, word counts, POS tags, and categories in **PostgreSQL**.  

✅ **Admin Panel & History** – View saved summaries and access the full database of extracted articles.  

✅ **GitHub OAuth Login** – Users can log in via **GitHub authentication** to access news history.  

✅ **User-Friendly Interface** – Simple **Flask-based UI** with search and history features.  

---

## **⚙️ Tech Stack**  

| **Technology**      | **Usage** |
|--------------------|-------------|
| 🐍 **Flask (Python)** | Backend framework |
| 🌐 **BeautifulSoup** | Web scraping for extracting news articles |
| 🧠 **Sumy (LSA Summarizer)** | Automatic text summarization |
| 📊 **NLTK (Natural Language Toolkit)** | Tokenization, POS tagging, stopwords |
| 🗄️ **PostgreSQL** | Database for storing news summaries |
| 🔐 **Authlib (OAuth 2.0)** | GitHub authentication |
| 🏗 **HTML, CSS, Jinja** | Web UI templates |

---

## **📥 Installation & Setup**  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/PuneetKumar747/News_Analyzer.git
cd News-Summarizer
```

### **2️⃣ Set Up a Virtual Environment (Optional but Recommended)**  
```bash
python -m venv env
source env/bin/activate  # On macOS/Linux
env\Scripts\activate     # On Windows
```

### **3️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**  
Create a `.env` file in the project root and add the following:  
```
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
SECRET_KEY=your_secret_key
DB_HOST=your_postgres_host
DB_NAME=your_database_name
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
```

### **5️⃣ Initialize the Database**  
- Ensure **PostgreSQL** is running.  
- Create a database (e.g., `news_summarizer_db`).  
- Run the script to create the necessary tables.  

### **6️⃣ Run the Flask App**  
```bash
python app.py
```
- Open your browser and go to:  
  ```bash
  http://127.0.0.1:5000
  ```

---

## **🎯 How It Works**  

1️⃣ **Enter a News URL** – The app extracts news content from **India Today articles**.  

2️⃣ **Summarization** – Uses **LSA summarization** to generate a **15-sentence summary**.  

3️⃣ **Categorization** – Determines whether the news is about **Politics, Business, Technology, etc.**.  

4️⃣ **POS Tagging** – Extracts **noun, verb, and adjective counts** from the article.  

5️⃣ **History & Admin Panel** – Admins can view all past news extractions with stored metadata.  

6️⃣ **GitHub Login (Optional)** – Users can authenticate via GitHub OAuth.  

---

## **🛠️ Contributing**  

Want to improve this project?  

1. **Fork** the repository.  
2. **Create a new branch** (`git checkout -b feature-newFeature`).  
3. **Commit your changes** (`git commit -m "Added new feature"`).  
4. **Push to GitHub** (`git push origin feature-newFeature`).  
5. **Open a Pull Request** and describe your changes.  
