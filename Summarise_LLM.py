import pandas as pd
import requests
import time

#Ensure the characters in the text allow it to be read
df = pd.read_csv('summarised.csv', encoding='latin1')

# Query for mistral
def summarize_with_mistral(text):
    try:
        response = requests.post(
            'http://localhost:11434/api/chat',
            json={
                "model": "mistral",
                "messages": [
                    {
                        "role": "system",
                        "content": """You are a summarization expert using Rhetorical Structure Theory.
Analyse the article given with the following steps:
1. Break it down into Elementary Discourse Units (EDUs), and list them.
2. Make separate sections for different relations (e.g., Cause, Result, Background, Evidence, Elaboration) 
    [Example: 
        Background:
        - NFHS-4 points out that the overall prevalence of anaemia among women in Karnataka is 51.2%. (nucleus)
        - The study was published in the Journal of Nutrition. (satellite)

        Cause:
        - The current estimate of iron requirement is lower by 6 mg per day compared to the 2010 recommendation. (nucleus) 
        etc]
3. Create a hybrid summary that:
   - Extracts the most critical nucleus sentences (esp. Cause-Result & Evidence).
   - Rewrites supporting satellites concisely.
   - Preserves logical flow: what happened, why, and consequences.
   - Always include: date, location, authorities involved, type of food/items, cause of issue if given.
Return output as:
SUMMARY: <your summary here>
RST_COMPONENT: <your RST analysis here>
Here is the article:"""
                    },
                    {"role": "user", "content": text}
                ],
                "stream": False
            }
        )
        response.raise_for_status()
        content = response.json()['message']['content']

        # Divide RST and summary
        summary, rst_component = "", ""
        if "SUMMARY:" in content and "RST_COMPONENT:" in content:
            parts = content.split("RST_COMPONENT:")
            summary = parts[0].replace("SUMMARY:", "").strip()
            rst_component = parts[1].strip()
        else:
            summary = content.strip()

        return summary, rst_component

    except Exception as e:
        return f"Error: {e}", ""

# Process each article and add to csv
summaries = []
rst_components = []
for i, row in df.iterrows():
    text = str(row['Text'])[:3000] 
    print(f"Summarizing article {i + 1}/{len(df)}...")
    summary, rst_component = summarize_with_mistral(text)
    summaries.append(summary)
    rst_components.append(rst_component)
    time.sleep(1)  # Prevent overload

# Save results
df['Summary'] = summaries
df['RST_Component'] = rst_components
df.to_csv('summarised.csv', index=False, encoding='utf-8')
print("Saved to summarised.csv")
