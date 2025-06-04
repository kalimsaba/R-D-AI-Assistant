from flask import Flask, render_template, request, redirect, url_for, session
import requests
from RD_Agent import ask_gemma, QUESTION_TEMPLATES, ROLE_PROMPT, OLLAMA_URL

app = Flask(__name__)
app.secret_key = "00000000000000"  # Needed for session handling

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        project_desc = request.form["project_description"]
        responses = {}

        for key in QUESTION_TEMPLATES:
            responses[key] = ask_gemma(project_desc, key)

        session["project_description"] = project_desc
        session["responses"] = responses
        session["chat_history"] = []

        return redirect(url_for("results"))

    return render_template("index.html")

@app.route("/results")
def results():
    responses = session.get("responses", {})
    chat_history = session.get("chat_history", [])
    return render_template("results.html", responses=responses, chat_history=chat_history)

@app.route("/chatbox", methods=["POST"])
def chatbox():
    user_input = request.form["user_input"]
    project_desc = session.get("project_description", "")
    chat_history = session.get("chat_history", [])

    followup_prompt = f"{ROLE_PROMPT}\n\nProject Description:\n{project_desc}\n\nUser Message:\n{user_input}\n\nPlease refine or respond accordingly:"

    payload = {
        "model": "gemma3",
        "prompt": followup_prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    ai_response = response.json().get("response", "Sorry, I couldn't process that.") if response.status_code == 200 else f"Error: {response.status_code}"

    chat_history.append({"user": user_input, "ai": ai_response})
    session["chat_history"] = chat_history

    return redirect(url_for("results"))