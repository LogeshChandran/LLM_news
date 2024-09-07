import concurrent.futures
import requests
from bs4 import BeautifulSoup
import pandas as pd
from huggingface_hub import login
import os
from datasets import Dataset,load_dataset
from datetime import datetime

os.environ['HUGGING_FACE_WRITE_KEY'] = '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'

def download_existing_dataset(repo_id):
    try:
        existing_dataset = load_dataset(repo_id)
        existing_df = existing_dataset['train'].to_pandas()
        return existing_df
    except Exception as e:
        print(f"Error downloading existing dataset: {e}")
        return pd.DataFrame()

def merge_datasets(existing_df, new_df):
    if not existing_df.empty:
        # merged_df = pd.merge(existing_df, new_df, on='URL')
        # merged_df = pd.concat([existing_df, new_df]).reset_index(drop=True)
        merged_df = pd.concat([existing_df, new_df], ignore_index=True) \
                            .reset_index(drop=True) \
                            .drop_duplicates(subset='URL')
        return merged_df
    else:
        return new_df
    
def pageURL_to_articleURLs(url):
    print("Processing URL:", url)
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all <a> tags (links) within the category
        soup = soup.find("ul", {"id": "cagetory"})
        links = soup.find_all('a')

        # Extract the href attribute from each link
        urls = []
        for link in links:
            href = link.get('href')
            if href:
                urls.append(href)
        return list(set(urls))  # Return unique URLs
    except Exception as e:
        print(f"Error processing page URL {url}: {e}")
        return []  # Return empty list on error

# Function to extract news from article URLs
def articleURL_to_news(url):
    print("Processing article:", url)
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Try to find the content div
        content_data = soup.find("div", {"id": "contentdata"})
        
        # Check if content_data exists
        if content_data is None:
            print(f"Warning: 'contentdata' div not found for URL: {url}")
            return None  # Skip this article

        # Extract title
        title_tag = soup.find("h1", class_="article_title artTitle")
        title = title_tag.get_text(strip=True) if title_tag else "No title available"

        # Extract the article schedule (date and time)
        article_schedule = soup.find("div", class_="article_schedule")
        article_time = article_schedule.get_text(strip=True) if article_schedule else "No date available"

        news = {'URL': url, 'title': title, 'subtitle': "", 'content': "", 'article time': article_time}

        # Extract paragraphs while excluding disclaimers
        for tag in content_data.find_all(['h2', 'p']):
            if tag.name == 'h2':
                news['subtitle'] += tag.get_text(strip=True) + "."
            elif tag.name == 'p':
                p_text = tag.get_text(strip=True)
                if 'Disclaimer:' not in p_text:
                    news['content'] += p_text + " "

        return news
    except Exception as e:
        print(f"Error processing article URL {url}: {e}")
        return None  # Return None on error

# Function to handle both tasks in sequence
def moneycontrol_task(page_url):
    articleURLs = pageURL_to_articleURLs(page_url)[0:5]  # Extract article URLs from the page
    if not articleURLs:
        return []  # If no articles, return empty list

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(articleURL_to_news, articleURL) for articleURL in articleURLs]
        news_data = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                news_data.append(result)
        return news_data

# Function to manage multi-threaded execution
def multi_threaded_execution(page_urls):
    final_results = []  # To store all results
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(moneycontrol_task, page_url) for page_url in page_urls]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                final_results.extend(result)  # Collect the results from each page
    return final_results  # Return the complete set of results

if __name__ == "__main__":

    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')

    page_urls = []
    for page_index in range(0, 31):
        page_url = f"https://www.moneycontrol.com/news/business/markets/page-{page_index}/"
        page_urls.append(page_url)

    # Start the multi-threaded execution and store the result
    news_data = multi_threaded_execution(page_urls)

    # Convert the scraped news data into a Pandas DataFrame
    if news_data:
        news_data_df = pd.DataFrame(news_data)
        news_data_df = news_data_df.reset_index() \
                        # .rename(columns={'index': 'Index'}) \
                        # .set_index("Index")

        column_order = ['URL', 'title', 'subtitle', 'content', 'article time']
        news_data_df = news_data_df[column_order]
        news_data_df.to_csv("today_news_data.csv")

        login(token=os.environ['HUGGING_FACE_WRITE_KEY'])

        repo_id = "Logeshkc/money_control_news"
        existing_data_df = download_existing_dataset(repo_id)
        merged_data_df = merge_datasets(existing_data_df, news_data_df)
        merged_data_df.reset_index() \
                    # .rename(columns={'index': 'Index'}) \
                    # .set_index("Index")
        
        merged_data_df = merged_data_df[column_order]
        merged_data_df.to_csv("merged_news_data.csv", index=False)

        merged_dataset = Dataset.from_pandas(merged_data_df)
        news_data = Dataset.from_pandas(news_data_df)
        
        merged_dataset.push_to_hub("Logeshkc/money_control_news")
        news_data.push_to_hub("Logeshkc/news_data_sep_07")