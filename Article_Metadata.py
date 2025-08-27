import mediacloud.api
from importlib.metadata import version
import datetime as dt
import pandas as pd
from urllib.parse import urlparse
from newspaper import Article, ArticleException

MC_API_KEY = #your API key here
search_api = mediacloud.api.SearchApi(MC_API_KEY)

#to only get article data from a specific duration
start_date = dt.date(2019, 1, 1)
end_date = dt.date(2019, 12, 31)

query = '("FSSAI" OR "FSSAI License" OR "FOOD SAFETY" OR "FOODBORNE ILLNESS" OR "FOOD INSPECTIONS" OR "FOOD SAMPLE TESTING" OR "ADULTERATION") AND ("confiscate" OR "contamination" OR "seized")'

all_results = []
more_stories = True
next_token = None 
results, _ = search_api.story_list(
    query, 
    start_date, 
    end_date, 
    source_ids=['39784','56899','20258', '22331','55376', '973649'])
# Times of India: '39784', Indian Express: '56899', Hindustan Times: '20258', Hindu: '22331', Telegraph: '55376', NIE: '973649'
story_data = []

# reused code to get the section from the metadata through the MediaCloudAPI
def get_section (url):
    try:
        path = urlparse(url).path
        parts = [p for p in path.split('/') if p]
        if len(parts) > 1:
            if parts[0].lower() not in ['news', 'article', 'articles', 'india', 'story']:
                return parts[0]
            elif len(parts) > 1:
                return parts[1]
        elif len(parts) == 1:
            return parts[0]
    except Exception:
        pass
    return ''

#removed articles to decrease false positives
exclude_sections = {'lifestyle', 'upsc-current-affairs', 'life-style', 'life-and-style', 'opinion', 'parenting'}

#Newspaper API to extract text
def extract_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        text = article.text.strip()
        text =' '.join(text.split())
        return text
    except ArticleException:
        return ''

for story in results:
    url = story['url']
    section = get_section(url).lower()
    if section in exclude_sections: 
        continue
    #add the relevant metadata to the CSV
    story_data.append({
        'Source': story['media_name'],
        'Section': section,
        'Title': story['title'],
        'Date': story['publish_date'],
        'URL': url,
        'Text': extract_text(url)
    })
df = pd.DataFrame(story_data)
df.to_csv('FoodSafety_2019.csv', index=False)
print("Saved")
print(f"Total results fetched: {len(results)}")
