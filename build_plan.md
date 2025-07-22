# Project Build Plan: Python Sidebot

Here is a 10-step plan to build this Python Sidebot application from the ground up using Gemini LLM. You can follow the py-sidebot project

### Milestone 1: Project Scaffolding & Dependencies

*   **Goal:** Create the basic file and directory structure and install all necessary libraries.
*   **Steps:**
    1.  Create the main project directory (`bot`).
    2.  Set up a Python virtual environment (e.g., `.venv`).
    3.  Create the `requirements.txt` file with all necessary libraries: `shiny`, `pandas`, `duckdb`, `chatlas`, `faicons`, `shinywidgets`, `plotly`, `ridgeplot`, `python-dotenv`, `kaleido`, `google-generativeai`, `inspect-ai`.
    4.  Install the dependencies using `pip install -r requirements.txt`.
    5.  Create the initial empty Python files: `app.py`, `shared.py`, `query.py`, `explain_plot.py`, and `eval.py`.
    6.  Create the `www` and `eval-datasets` directories.

### Milestone 2: Data Loading and Preparation

*   **Goal:** Load the core dataset and make it available for querying.
*   **Steps:**
    1.  Add the `tips.csv` dataset to the root directory.
    2.  Implement the logic in `shared.py` to load `tips.csv` into a pandas DataFrame.
    3.  In `shared.py`, calculate the `percent` column (`tip / total_bill`).
    4.  Register the DataFrame with `duckdb` under the name "tips", making it available for SQL queries.

### Milestone 3: Basic Shiny Dashboard Layout

*   **Goal:** Create a minimal, functional dashboard that displays the raw data.
*   **Steps:**
    1.  In `app.py`, create the basic UI structure using `shiny.ui.page_sidebar`.
    2.  Add a title and a `ui.output_data_frame` to the main content area.
    3.  Implement the initial server logic to import the `tips` DataFrame from `shared.py`.
    4.  Create a `@render.data_frame` function to display the `tips` DataFrame in the UI.

### Milestone 4: Add Static Visualizations and Value Boxes

*   **Goal:** Enhance the dashboard with static plots and key performance indicators (KPIs).
*   **Steps:**
    1.  In `app.py`, add the three `ui.value_box` elements to the UI.
    2.  Implement the corresponding `@render.text` functions to calculate and display the total tippers, average tip, and average bill.
    3.  Add `output_widget` placeholders for a scatter plot and a ridge plot to the UI.
    4.  Implement the `@render_plotly` functions in the server logic to display a default scatter plot (`total_bill` vs. `tip`) and a default ridge plot.

### Milestone 5: System Prompt Engineering

*   **Goal:** Create the instructional prompt that will guide the LLM.
*   **Steps:**
    1.  Create the `prompt.md` file.
    2.  Write the detailed instructions for the LLM, defining its persona, tasks, and constraints. Include the `${SCHEMA}` placeholder.
    3.  In `query.py`, implement the `df_to_schema` function to dynamically generate a schema description from a DataFrame.
    4.  In `query.py`, implement the `system_prompt` function to read `prompt.md` and inject the generated schema.

### Milestone 6: Basic Chat Integration

*   **Goal:** Add a functional chat window to the UI that can communicate with an LLM.
*   **Steps:**
    1.  In `app.py`, add the `ui.chat_ui` to the sidebar.
    2.  In the server function, initialize the Gemini LLM chat object, using the `system_prompt` from `query.py`.
    3.  Implement the `@chat.on_user_submit` handler.
    4.  Inside the handler, send the user's input to Gemini LLM and stream the response back to the UI.

### Milestone 7: Implement Core LLM Tools

*   **Goal:** Empower the LLM to interact with and modify the dashboard state.
*   **Steps:**
    1.  In `app.py`, define the `async` functions `update_dashboard(query: str, title: str)` and `query_db(query: str)`.
    2.  Register these functions as tools with the `chat_session` object.
    3.  Create the `current_query = reactive.Value("")` and `current_title = reactive.Value("")`.
    4.  Modify the `tips_data` reactive calculation to execute the `current_query()` if it's not empty. This connects the LLM's `update_dashboard` tool to the live UI.

### Milestone 8: Implement "Explain Plot" Feature

*   **Goal:** Add the ability for the user to get an AI-powered explanation of the visualizations.
*   **Steps:**
    1.  Add the `stars.svg` icon to the `www` directory.
    2.  In `app.py`, add the `ui.input_action_link` with the icon to the card headers for the plots.
    3.  In `explain_plot.py`, implement the `explain_plot` function. This will handle saving the plot as an image, creating the modal dialog, and managing the separate, image-aware chat session.
    4.  In `app.py`, create the `@reactive.event` handlers for the action links that call the `explain_plot` function.

### Milestone 9: Styling and Final Touches

*   **Goal:** Polish the application's appearance and provide user guidance.
*   **Steps:**
    1.  Create `www/styles.css` and add the custom CSS rules to refine the layout, fonts, and colors.
    2.  Add the initial greeting message to the chat UI in `app.py` to provide users with example prompts.
    3.  Write the `README.md` file with a project description, setup instructions, and usage examples.

### Milestone 10: Build the Evaluation Suite

*   **Goal:** Create a robust testing framework to validate the LLM's performance.
*   **Steps:**
    1.  Create the evaluation datasets: `eval-datasets/update_dashboard.csv` and `eval-datasets/query_db.csv` with various test prompts.
    2.  In `eval.py`, implement mock versions of the `update_dashboard` and `query_db` tools for testing.
    3.  Define the `sidebot_solver` using `inspect-ai`.
    4.  Implement the custom `sql_scorer` to compare the DataFrame results of the generated SQL against the expected SQL.
    5.  Define the final `inspect-ai` tasks (`update_dashboard_sql`, `query_db_answer`) that bring together the data, solver, and scorer.
