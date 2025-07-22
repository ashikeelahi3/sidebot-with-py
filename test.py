import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY", "")
print("Loaded GEMINI_API_KEY:", api_key)

genai.configure(api_key=api_key)

try:
    print("Listing available Gemini models...")
    models = genai.list_models()
    for m in models:
        print("Model:", m.name, "Supported methods:", m.supported_generation_methods)
    # Try the first available model for chat
    print("Trying model: gemini-1.5-flash")
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(history=[])
    response = chat.send_message("Hello, Gemini! You are a test bot.")
    print("Gemini response:", getattr(response, "text", str(response)))
except Exception as e:
    print("Gemini error:", e)

try:
    import pandas as pd
    import plotly.express as px
    import shiny
    import shinywidgets
    print("All required packages are installed and importable.")
except Exception as e:
    print("Package import error:", e)
