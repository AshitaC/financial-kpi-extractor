# Financial KPI Extractor

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38-FF4B4B)
![LangChain](https://img.shields.io/badge/LangChain-0.2-green)
![Llama 3](https://img.shields.io/badge/Model-Llama_3.3-purple)

**An AI-powered application that extracts structured financial data (Revenue & EPS) from unstructured news articles and earnings reports.**

## About The Project
Financial analysts often spend hours reading through earnings reports to find key metrics. This tool automates that process using **Large Language Models (LLMs)**.

The application uses **LangChain** to orchestrate the extraction pipeline. By feeding raw text (e.g., a news snippet or earnings release) into specialized **Prompt Templates**, it guides **Llama 3.3 (via Groq)** to accurately identify and extract:

*   **Revenue:** Actual vs. Expected
*   **EPS (Earnings Per Share):** Actual vs. Expected

The data is then cleaned and visualized interactively using **Plotly**.

---
### Key Features
*   **LangChain Orchestration**: Utilizes LangChain to manage API calls and parse LLM responses into structured JSON.
*   **Prompt Engineering**: Implements strict system prompts to ensure the model correctly distinguishes between "GAAP" and "Adjusted" metrics.
*   **Dynamic Visualization:** Side-by-side bar charts for instant performance comparison.
*   **Data Export:** Download extracted results as a CSV file.
*   **Robust Parsing:** Handles variations in text (e.g., "$25 billion" vs "25B") through context-aware **prompts**.
---

## [Live App](https://financial-kpi-extractor.streamlit.app/)

<img width="733" height="736" alt="image" src="https://github.com/user-attachments/assets/b64e0beb-da26-4cf3-9b99-b842f2077f23" />
<img width="733" height="389" alt="image" src="https://github.com/user-attachments/assets/f82c0022-653b-4b91-bbc4-52a2c87b210e" />
---

## Project Structure
```
financial-kpi-extractor/
├── .streamlit/
│   └── config.toml      # Theme configuration (Light Mode settings)
├── main.py              # Frontend UI and visualization logic
├── data_extractor.py    # Backend LLM chain and prompt engineering
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```
----

## Tech Stack
*   **Frontend:** [Streamlit](https://streamlit.io/) (UI/UX)
*   **Backend:** [LangChain](https://www.langchain.com/) (LLM Orchestration)
*   **AI Model:** Llama 3.3-70b-versatile (via [Groq API](https://groq.com/))
*   **Data Viz:** Plotly & Pandas
*   **Language:** Python
---

## How It Works

1. User pastes financial news text  
2. `data_extractor.extract()` sends prompt → Groq Llama 3.3  
3. LangChain returns structured KPIs in JSON  
4. Streamlit displays:
   - A table  
   - Interactive bar charts  
   - CSV download option  

---


Contact

Ashita C

[LinkedIn Profile](https://www.linkedin.com/in/ashita-chandnani/)
