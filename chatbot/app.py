import pandas as pd
import gradio as gr
import ollama

# Load CSV
df = pd.read_csv("netflix_titles.csv")  # Make sure this file is in the same folder

# Create context from top 100 rows
def generate_context():
    rows = df.head(100)[['title', 'description', 'cast', 'director']].fillna('')
    context = "\n\n".join(
        f"Title: {row['title']}\nDescription: {row['description']}\nCast: {row['cast']}\nDirector: {row['director']}"
        for _, row in rows.iterrows()
    )
    return context

context_data = generate_context()

# Bot function
def ask_bot(user_input):
    prompt = f"""You are a Netflix chatbot. Based on this data:\n\n{context_data}\n\nUser: {user_input}\nAnswer:"""
    response = ollama.chat(model='tinyllama', messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Gradio interface
interface = gr.Interface(fn=ask_bot,
                         inputs=gr.Textbox(lines=3, label="Ask about Netflix shows or movies"),
                         outputs=gr.Textbox(label="TinyLLaMA's Answer"),
                         title="Netflix Chatbot with TinyLLaMA")

interface.launch()