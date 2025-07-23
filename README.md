# 🎬 Netflix Chatbot

This project is an intelligent chatbot built with Python and Mistral LLM that allows users to query a Netflix dataset using natural language. It can handle complex queries about shows and movies based on genres, countries, years, and types. Whether you want to find all action movies from India before 2010 or romantic TV shows released between 2015 and 2020, this chatbot understands your intent and fetches accurate results.

## 🚀 Features

- Natural language understanding using Mistral LLM
- Year-based filtering support: `before`, `after`, `between`, and exact years
- Category filtering based on `type` (Movie/TV Show), `genres`, `countries`, and `release_year`
- Uses Pandas for fast CSV querying
- Built-in sentence similarity search using Sentence Transformers
- Gradio interface for chat-based interaction
- Returns 5 to 15 high-quality results per query (not limited to 3)

## 🔧 Tech Stack

- Python
- Mistral via Ollama (or Hugging Face Transformers)
- Sentence Transformers
- Pandas
- Gradio
- spaCy (for NLP)
- Netflix Movies & TV Shows Dataset (CSV)

## 📂 Folder Structure

netflix_chatbot/
│
├── app.py # Main chatbot app (Gradio UI)
├── chatbot_utils.py # Query parsing, year filtering, response formatting
├── netflix_titles.csv # Netflix dataset file
├── requirements.txt # Python dependencies
└── README.md # Project documentation



## ▶️ How to Run the Project

### Step 1: Clone the repository

```bash
git clone https://github.com/Harshmohod/netflix_chatbot.git
cd netflix_chatbot

### Step 2: install dependencies
pip install -r requirements.txt

### Step 3: Start chatbot
python app.py


🧪 Example Queries to Try
"Show me romantic movies from India between 2010 and 2018"

"List all horror TV shows released after 2015"

"What are the comedy shows released in the US before 2010?"

"I want to watch action movies released in Japan"

"Give me movies between 2016 and 2018 that are about sports"

🗃 Dataset Source
This project uses the publicly available Netflix Movies and TV Shows dataset which includes fields like title, description, type, country, genre, and release year.

You can find the dataset on Kaggle or similar open data repositories.

👨‍💻 Author
Harsh Mohod
GitHub: @Harshmohod

📜 License
This project is licensed under the MIT License, which means you can use, modify, and distribute it freely for both personal and commercial use, with proper attribution.
