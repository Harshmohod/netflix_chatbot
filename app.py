import gradio as gr
import pandas as pd
import re
import spacy
from sentence_transformers import SentenceTransformer, util
import subprocess
import json

# Load models and data
df = pd.read_csv("netflix_titles.csv")
df["release_year"] = pd.to_numeric(df["release_year"], errors='coerce')
df.dropna(subset=["title", "description", "release_year"], inplace=True)
df.reset_index(drop=True, inplace=True)

model = SentenceTransformer("all-MiniLM-L6-v2")
nlp = spacy.load("en_core_web_sm")

# Function to extract filters
def extract_filters(user_query):
    doc = nlp(user_query.lower())
    filters = {
        "type": None,
        "country": None,
        "listed_in": None,
        "release_year": None,
        "before_year": None,
        "after_year": None,
        "between_years": None,
    }

    before_match = re.search(r"before\s+(19|20)\d{2}", user_query)
    if before_match:
        filters["before_year"] = int(before_match.group().split()[-1])

    after_match = re.search(r"after\s+(19|20)\d{2}", user_query)
    if after_match:
        filters["after_year"] = int(after_match.group().split()[-1])

    between_match = re.search(r"between\s+(19|20)\d{2}\s+and\s+(19|20)\d{2}", user_query)
    if between_match:
        years = re.findall(r"(19|20)\d{2}", between_match.group())
        if len(years) == 2:
            filters["between_years"] = (int(years[0]), int(years[1]))

    exact_year = re.search(r"(in|from|of|released in)?\s*(19|20)\d{2}", user_query)
    if exact_year and not (filters["before_year"] or filters["after_year"] or filters["between_years"]):
        filters["release_year"] = int(re.search(r"(19|20)\d{2}", exact_year.group()).group())

    for ent in doc.ents:
        if ent.label_ == "GPE":
            filters["country"] = ent.text.title()

    genre_keywords = {
        "action", "comedy", "drama", "horror", "romance", "thriller",
        "documentary", "sci-fi", "crime", "kids", "family", "anime"
    }
    for token in doc:
        if token.text.lower() in genre_keywords:
            filters["listed_in"] = token.text.title()

    if "movie" in user_query:
        filters["type"] = "Movie"
    elif "show" in user_query or "series" in user_query:
        filters["type"] = "TV Show"

    return filters

# Function to apply filters to dataframe
def filter_data(filters):
    temp = df.copy()

    if filters["type"]:
        temp = temp[temp["type"].str.lower() == filters["type"].lower()]
    if filters["country"]:
        temp = temp[temp["country"].str.contains(filters["country"], case=False, na=False)]
    if filters["listed_in"]:
        temp = temp[temp["listed_in"].str.contains(filters["listed_in"], case=False, na=False)]

    if filters["between_years"]:
        start, end = filters["between_years"]
        temp = temp[(temp["release_year"] >= start) & (temp["release_year"] <= end)]
    elif filters["after_year"] and filters["before_year"]:
        temp = temp[(temp["release_year"] > filters["after_year"]) & (temp["release_year"] < filters["before_year"])]
    elif filters["after_year"]:
        temp = temp[temp["release_year"] > filters["after_year"]]
    elif filters["before_year"]:
        temp = temp[temp["release_year"] < filters["before_year"]]
    elif filters["release_year"]:
        temp = temp[temp["release_year"] == filters["release_year"]]

    return temp

# Function to build prompt
def build_prompt(user_query, results):
    prompt = f"User asked: '{user_query}'\n\nHere are some matching Netflix titles:\n"
    top_5 = results.head(5).to_dict(orient="records")

    for item in top_5:
        prompt += f"- **{item['title']}** ({item['release_year']}): {item['description']}\n"
    
    return prompt

# Function to call Mistral using Ollama (modify if you're using Hugging Face API)
def call_mistral(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral", "--", prompt],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout.strip() if result.returncode == 0 else "LLM error: No output."
    except subprocess.TimeoutExpired:
        return "Request timed out. Please try again."

# Main chatbot logic
def chatbot_response(message, chat_history):
    filters = extract_filters(message)
    results = filter_data(filters)

    if results.empty:
        return "Sorry, no matching titles found."

    prompt = build_prompt(message, results)
    reply = call_mistral(prompt)

    return reply

# Gradio Chat Interface
chat_ui = gr.ChatInterface(
    chatbot_response,
    title="Netflix ChatBot 🎬",
    theme="soft",
    examples=[
        "Suggest comedy shows after 2010 from India",
        "Romantic movies from 2017 in United Kingdom",
        "Show horror series between 2015 and 2020",
        "Movies before 2012 in Japan",
    ]
)

if __name__ == "__main__":
    chat_ui.launch(server_name="0.0.0.0", server_port=7860)

