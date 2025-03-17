# Tempo Assistant: A Weather and Information Agent

This project is a conversational AI agent designed to provide weather information, company details, meteorological glossary definitions, and technical support. It leverages the power of LangGraph and LangChain to orchestrate multiple tools and the Gemini model for natural language understanding and response generation. This assistant is integrated with an external weather API to provide real-time weather data and runs within a Streamlit application for a user-friendly interface.

## Overview

The Tempo Assistant is a multi-functional AI agent that can:

*   **Provide Weather Information:** Retrieve weather details for specific cities using a connected weather API.
*   **Offer Company Insights:** Share information about the company, CTA-CIA, its history, and its AI, Ken.
*   **Define Meteorological Terms:** Explain meteorological concepts to users.
*   **Give Technical Support:** Provide guidance and assistance regarding the application's features and usage.
* **Get temperature:** get the temperature in a specific city.

The agent's core functionality is built around:

*   **LangGraph:** Manages the flow of information between different tools and the language model.
*   **LangChain:** Facilitates prompt engineering, model interaction, and the use of tools.
*   **Gemini Models (Vertex AI):** Powers the agent's natural language understanding and generation capabilities.
*   **Google Cloud Functions:** (implicit) interacts with external functions or microservices.
*   **Streamlit:** Provides the interactive web application interface.
*   **Tools:** Specific functions are packaged as tools, each with a defined purpose.

## Features

*   **Conversational Interface:** Users can interact with the assistant in a natural, conversational way.
*   **Weather Data Retrieval:** Fetches real-time weather data from a weather API.
*   **Information:** Accesses and shares information about the company.
*   **Meteorological Glossary:** Provides definitions of weather-related terms.
*   **Technical Support:** Offers support and guidance to users.
* **Temperature check**: You can ask directly the temperature in a specific city.
*   **Multiple Tools:** Employs a range of tools to address different user needs.
*   **Gemini-Powered:** Leverages Gemini's advanced language model for superior understanding.
*   **Streamlit UI:**  A user-friendly web interface for seamless interaction.
* **Google Cloud integration**: the application is ready to be deployed in a google cloud environment, and use its id tokens.

## Getting Started

### Prerequisites

*   **Python 3.9+:** Ensure you have a compatible Python version.
*   **Poetry (Recommended) or pip:**  For managing dependencies.
*   **Google Cloud Project:**  You'll need a Google Cloud project to use Vertex AI and set up the Google Cloud Function integration.
*   **Google Gemini API Key:** Obtain a key from the Google AI Studio or better use VertexAI sdk present in this project.
*   **Google Cloud Function deployed** : you need to have the functions described in the code deployed in Google Cloud.
*   **Environment variables**: You must have a `API_WEATHER_URL` environment variable, pointing to your google cloud function.

### Installation

1.  **Clone the Repository:**

    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2.  **Install Dependencies:**

    **(Using Poetry, recommended):**

    ```bash
    poetry install
    ```

    **(Or using pip):**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set API Keys and Environment variables:**

    ```bash
    export GOOGLE_API_KEY="your_gemini_api_key"
    export API_WEATHER_URL="https://your-cloud-function-url"
    ```

    Replace `"your_gemini_api_key"` and `"https://your-cloud-function-url"` with your actual values.

### Usage

1.  **Activate the Virtual Environment (if using Poetry):**

    ```bash
    poetry shell
    ```

2.  **Run the Streamlit App:**

    ```bash
    streamlit run frontend/cta_agent.py
    ```

3.  **Interact:** Open the Streamlit app in your browser and start interacting with the Tempo Assistant.

## Project Structure

Langgraph_agent/ 
├── frontend-assistant/ │ 
├── frontend/ │ 
│ └── cta_agent.py # Main Streamlit app and agent logic 
├── ... # Other potential directories for your Langgraph app. 
├── requirements.txt # Project dependencies (if managed by pip) 
└── pyproject.toml # Project dependencies (if managed by poetry) 
└── README.md # This file