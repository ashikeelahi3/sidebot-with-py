"""
Python Sidebot - Shiny Dashboard App

This file implements the main UI and server logic for the Sidebot application.
Follow the build plan milestones to complete the implementation.
"""

# Milestone 1: Project Scaffolding & Dependencies
from shiny import App, ui, render
from shiny import reactive
from dotenv import load_dotenv
load_dotenv()
import plotly.express as px
from shinywidgets import output_widget, render_plotly
import os
import google.generativeai as genai
import pandas as pd

from shared import tips

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h2("Python Sidebot Dashboard"),
        ui.div(
            {"style": "display: flex; gap: 10px; margin-bottom: 10px;"},
            ui.input_text("user_input", "", placeholder="Type your question here...", width="100%"),
            ui.input_action_button("send", "Send", class_="btn-primary"),
        ),
        ui.div(
            {"style": "height: 400px; overflow-y: auto; border: 1px solid #ddd; padding: 10px; background-color: #f8f9fa; border-radius: 5px;"},
            ui.output_ui("chat_messages")
        ),
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

def server(input, output, session):
    
    # Setup Gemini
    api_key = os.getenv("GEMINI_API_KEY", "")
    print(f"[DEBUG] API key found: {'Yes' if api_key else 'No'}")
    
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat(history=[])
        print("[DEBUG] Gemini model initialized successfully")
    else:
        print("[DEBUG] Warning: GEMINI_API_KEY not found")
        chat = None

    # Use reactive.Value for proper state management
    chat_history = reactive.Value([])
    
    print("[DEBUG] Chat history initialized")

    @output
    @render.ui
    def chat_messages():
        print("[DEBUG] Rendering chat messages...")
        history = chat_history.get()
        print(f"[DEBUG] Current history length: {len(history)}")
        
        if not history:
            return ui.div(
                {"style": "color: #666; font-style: italic; text-align: center; margin-top: 50px;"},
                "👋 Welcome to Sidebot! Ask me anything about the tips data."
            )
        
        messages = []
        for i, msg in enumerate(history):
            print(f"[DEBUG] Processing message {i}: {msg[:50]}...")
            
            if msg.startswith("User: "):
                # User message - align right
                content = msg[6:]  # Remove "User: " prefix
                messages.append(
                    ui.div(
                        {"style": "text-align: right; margin-bottom: 10px;"},
                        ui.div(
                            {"style": "display: inline-block; background-color: #007bff; color: white; padding: 8px 12px; border-radius: 15px 15px 5px 15px; max-width: 80%; word-wrap: break-word;"},
                            content
                        )
                    )
                )
            elif msg.startswith("Sidebot: "):
                # Bot message - align left
                content = msg[9:]  # Remove "Sidebot: " prefix
                messages.append(
                    ui.div(
                        {"style": "text-align: left; margin-bottom: 10px;"},
                        ui.div(
                            {"style": "display: inline-block; background-color: #e9ecef; color: #333; padding: 8px 12px; border-radius: 15px 15px 15px 5px; max-width: 80%; word-wrap: break-word;"},
                            "🤖 " + content
                        )
                    )
                )
        
        print(f"[DEBUG] Returning {len(messages)} rendered messages")
        return ui.div(messages)

    @reactive.effect
    @reactive.event(input.send)
    def handle_chat():
        print("[DEBUG] Handle chat triggered!")
        user_input_text = input.user_input()
        print(f"[DEBUG] User input received: '{user_input_text}'")
        print(f"[DEBUG] Input length: {len(user_input_text) if user_input_text else 0}")
        
        if not user_input_text or not user_input_text.strip():
            print("[DEBUG] Empty input, returning")
            return

        # Get current history and add user message
        current_history = chat_history.get().copy()
        print(f"[DEBUG] Current history length before adding: {len(current_history)}")
        
        current_history.append(f"User: {user_input_text.strip()}")
        print("[DEBUG] Added user message to history")
        
        # Update history to show user message immediately
        chat_history.set(current_history)
        print("[DEBUG] Updated chat history with user message")
        
        try:
            if chat:
                print("[DEBUG] Sending message to Gemini...")
                system_context = f"""You are Sidebot, a helpful assistant analyzing a tips dataset. 
                The dataset has {len(tips)} records with columns: {', '.join(tips.columns.tolist())}.
                Key statistics:
                - Average tip: ${tips['tip'].mean():.2f}
                - Average bill: ${tips['total_bill'].mean():.2f}
                - Average tip percentage: {tips['percent'].mean():.1f}%
                
                Please provide helpful, concise insights about this data. Keep responses under 200 words.
                
                User question: {user_input_text}"""
                
                response = chat.send_message(system_context)
                reply = getattr(response, "text", str(response))
                print(f"[DEBUG] Gemini response received: {reply[:100]}...")
                
                if not reply.strip():
                    reply = "I'm sorry, I didn't get a proper response. Could you try asking in a different way?"
                    print("[DEBUG] Empty response from Gemini, using fallback")
            else:
                reply = "Error: Gemini API key not configured. Please set GEMINI_API_KEY environment variable."
                print("[DEBUG] No API key, using error message")
                
        except Exception as e:
            print(f"[DEBUG] Gemini error: {e}")
            reply = f"Sorry, I encountered an error: {str(e)}"

        # Add bot response to history
        current_history.append(f"Sidebot: {reply}")
        chat_history.set(current_history)
        print(f"[DEBUG] Final history length: {len(current_history)}")
        
        # Clear the input field
        ui.update_text("user_input", value="")
        print("[DEBUG] Cleared input field")

    @output()
    @render.data_frame
    def tips_table():
        print("[DEBUG] Rendering tips table")
        return tips

    @output()
    @render.text
    def total_tippers():
        result = str(tips.shape[0])
        print(f"[DEBUG] Total tippers: {result}")
        return result

    @output()
    @render.text
    def average_tip():
        perc = tips['tip'] / tips['total_bill']
        result = f"{perc.mean():.1%}"
        print(f"[DEBUG] Average tip: {result}")
        return result

    @output()
    @render.text
    def average_bill():
        result = f"${tips['total_bill'].mean():.2f}"
        print(f"[DEBUG] Average bill: {result}")
        return result

    @output()
    @render_plotly
    def scatterplot():
        print("[DEBUG] Rendering scatterplot")
        fig = px.scatter(
            tips,
            x="total_bill",
            y="tip",
            title="Total Bill vs Tip",
            labels={"total_bill": "Total Bill ($)", "tip": "Tip ($)"}
        )
        return fig

    @output()
    @render_plotly
    def ridgeplot():
        print("[DEBUG] Rendering ridgeplot")
        fig = px.box(
            tips,
            x="day",
            y="percent",
            color="day",
            title="Tip Percentages by Day",
            labels={"percent": "Tip Percentage (%)", "day": "Day of Week"}
        )
        return fig

app = App(app_ui, server)