"""
Python Sidebot - Shiny Dashboard App

This file implements the main UI and server logic for the Sidebot application.
Follow the build plan milestones to complete the implementation.
"""

# Milestone 1: Project Scaffolding & Dependencies
# (Imports will be added as features are implemented)

# Milestone 2: Data Loading and Preparation
from shiny import App, ui, render
import plotly.express as px
from shinywidgets import output_widget, render_plotly
from shared import tips

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h2("Python Sidebot Dashboard"),
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
    @output()
    @render.data_frame
    def tips_table():
        return tips

    @output()
    @render.text
    def total_tippers():
        return str(tips.shape[0]) # Calculate the dimension and take No. of rows

    @output()
    @render.text
    def average_tip():
        perc = tips['tip'] / tips['total_bill']
        return f"{perc.mean():.1%}"

    @output()
    @render.text
    def average_bill():
        return f"${tips['total_bill'].mean():.2f}"

    from shinywidgets import render_plotly

    @output()
    @render_plotly
    def scatterplot():
        fig = px.scatter(
            tips,
            x="total_bill",
            y="tip",
            title="Total Bill vs Tip",
            labels={"total_bill": "Total Bill", "tip": "Tip"}
        )
        return fig

    @output()
    @render_plotly
    def ridgeplot():
        # Example: show percent distribution by day using box plot
        fig = px.box(
            tips,
            x="day",
            y="percent",
            color="day",
            title="Tip Percentages by Day",
            labels={"percent": "Tip %", "day": "Day"}
        )
        return fig

app = App(app_ui, server)

# Milestone 3: Basic Shiny Dashboard Layout
# - Create UI structure using shiny.ui.page_sidebar
# - Add title and ui.output_data_frame
# - Render tips DataFrame in UI

# Milestone 4: Add Static Visualizations and Value Boxes
# - Add value boxes and plot placeholders

# Milestone 5: System Prompt Engineering
# - Integrate system prompt from query.py

# Milestone 6: Basic Chat Integration
# - Add chat UI and handlers

# Milestone 7: Implement Core LLM Tools
# - Define update_dashboard and query_db functions

# Milestone 8: Implement "Explain Plot" Feature
# - Add action links and explain_plot integration

# Milestone 9: Styling and Final Touches
# - Import custom CSS and greeting message

# Milestone 10: Build the Evaluation Suite
# - Add evaluation hooks if needed

# Entry point for Shiny app will be added here
