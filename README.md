# Food Safety Media Coverage Project 

## Overview 
This project is part of the **Food Knowledge Graph** intitiative. It collects media coverage of food safety violations in India (2019-2024), cleans and stores the articles, and then summarizes them using **LLMS with Rhetorical Structure Theory**

**Description:**
Project documentation for new users to reproduce and extend the Food Safety Media Coverage Pipeline. 

## Goals
1. Collect and clean food safety articles from MediaCloud. 
2. Summarize articles into structured outputs using Mistral (LLM)

## Requirements 
- Python 3.9+ 
- Libraries: 
`pandas`, `requests`, `mediacloud`, `newspaper3k`
- Local LLM environment: [Ollama](https://ollama.ai) with Mistral 7B

## Setup 
1. Clone or download this repositoru 
2. Install requirements:
    ```bash 
    pip install pandas requests mediacloud newspaper3k
