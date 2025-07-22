# sidebot_app.py

from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_plotly
import google.generativeai as genai
from dotenv import load_dotenv
import os
import pandas as pd
import plotly.express as px

# Load environment variables
load_dotenv()

# Dummy dataset
tips = pd.DataFrame({
    "total_bill": [10, 20, 30, 15, 25],
    "tip": [1, 3, 5, 2, 4],
    "day": ["Sun", "Sun", "Sat", "Sat", "Fri"]
})
tips["percent"] = tips["tip"] / tips["total_bill"] * 100

# UI Layout
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h2("Python Sidebot Dashboard"),
        ui.input_text("user_input", "Ask Sidebot", placeholder="Type your question here..."),
        ui.input_action_button("send", "Send"),
        ui.output_text_verbatim("chat"),
    ),
    ui.layout_columns(
        ui.value_box("Total tippers", ui.output_text("total_tippers")),
        ui.value_box("Average tip", ui.output_text("average_tip")),
        ui.value_box("Average bill", ui.output_text("average_bill")),
        fill=False,
    ),
    ui.layout_columns(
        ui.card(
            ui.card_header("Tips data"),
            ui.output_data_frame("tips_table"),
            full_screen=True,
        ),
        ui.card(
            ui.card_header("Total bill vs. tip"),
            output_widget("scatterplot"),
            full_screen=True,
        ),
        ui.card(
            ui.card_header("Tip percentages"),
            output_widget("ridgeplot"),
            full_screen=True,
        ),
        col_widths=[4, 4, 4],
        min_height="400px",
    ),
)

# Server logic
def server(input, output, session):
    api_key = os.getenv("GEMINI_API_KEY", "")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(history=[])

    # In-memory chat history (reactive)
    chat_history = reactive.Value([])

    @output(id="chat")
    @render.text
    def chat_output():
        history = chat_history.get()
        return "\n".join(history) if history else "Welcome to Sidebot!"

    @reactive.effect
    @reactive.event(input.send)
    def handle_chat():
        user_input = input.user_input()
        if not user_input.strip():
            return

        history = chat_history.get().copy()
        history.append(f"User: {user_input}")
        try:
            response = chat.send_message(user_input)
            reply = getattr(response, "text", str(response))
            if not reply.strip():
                reply = "(No response from Gemini)"
        except Exception as e:
            reply = f"Error: {e}"

        history.append(f"Sidebot: {reply}")
        chat_history.set(history)

    @output()
    @render.data_frame
    def tips_table():
        return tips

    @output()
    @render.text
    def total_tippers():
        return str(len(tips))

    @output()
    @render.text
    def average_tip():
        return f"{(tips['tip'] / tips['total_bill']).mean():.1%}"

    @output()
    @render.text
    def average_bill():
        return f"${tips['total_bill'].mean():.2f}"

    @output()
    @render_plotly
    def scatterplot():
        fig = px.scatter(tips, x="total_bill", y="tip", title="Total Bill vs Tip")
        return fig

    @output()
    @render_plotly
    def ridgeplot():
        fig = px.box(tips, x="day", y="percent", color="day", title="Tip Percentages by Day")
        return fig


# Create the app
app = App(app_ui, server)
