import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

ROLE_PROMPT = """You are an AI assistant helping a company fill out the R&D Tax Incentive Application form.
Based on the meeting notes provided, respond only to the specific section mentioned.
Make sure your answer is detailed, formal, and specific to the question.
Do not add information that is not present in the notes provided, except for the background section in the hypothesis or new knowledge.
This is very important: If experiments, results, or procedures are missing, do not add them from the web.
Do not invent information, if the information is not found.
"""

QUESTION_TEMPLATES = {
    "hypothesis": "What was the hypothesis of this R&D activity?",
    "new_knowledge": "What new knowledge was this core activity intended to produce?",
    "technical_uncertainty": "Why could the outcome not have been known in advance?",
    "experiment_steps": "What was the experiment and how did it test the hypothesis?",
    "result_evaluation": "How did you evaluate or plan to evaluate the results from your experiment?",
    "conclusions": "If you reached conclusions, describe them here.",
}

def ask_gemma(project_description, section_key):
    question = QUESTION_TEMPLATES[section_key]
    full_prompt = f"{ROLE_PROMPT}\n\nProject Description:\n{project_description}\n\nQuestion:\n{question}\n\nAnswer:"

    payload = {
        "model": "gemma3",
        "prompt": full_prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        return result["response"]
    else:
        return f"Error: {response.status_code}, {response.text}"
    
def chat_with_gemma(project_description, user_message):
    followup_prompt = f"{ROLE_PROMPT}\n\nProject Description:\n{project_description}\n\nUser Message:\n{user_message}\n\nPlease respond accordingly:"

    payload = {
        "model": "gemma3",
        "prompt": followup_prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        return result["response"]
    else:
        return f"Error: {response.status_code}, {response.text}"