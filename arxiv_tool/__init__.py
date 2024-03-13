import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

# Function to get the latest article
def get_latest_article():
    url = "https://arxiv.org/search/cs?query=artificial+intelligence&searchtype=all&abstracts=show&order=-submitted_date&size=200"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the latest article
    articles = soup.find_all('div', class_='meta')
    latest_article = articles[0] # Assuming the first article is the latest
    
    # Extract details
    arxiv_number = latest_article.find('a').text
    arxiv_link = latest_article.find('a')['href']
    title = latest_article.find('div', class_='list-title mathjax').text.strip()
    authors = [a.text for a in latest_article.find_all('a', class_='meta-link')]
    abstract = latest_article.find('dd', class_='abstract').text.strip()
    submitted_date = latest_article.find('dd', class_='is-size-7').text.strip()
    
    return {
        'arxiv_number': arxiv_number,
        'arxiv_link': arxiv_link,
        'title': title,
        'authors': authors,
        'abstract': abstract,
        'submitted_date': submitted_date
    }

# Function to format the article details into a markdown table
def format_article_to_markdown(article):
    markdown_table = f"""
| Arxiv Number | Link | Title | Authors | Abstract | Submitted Date |
|--------------|------|-------|---------|----------|----------------|
| {article['arxiv_number']} | [Link](https://arxiv.org{article['arxiv_link']}) | {article['title']} | {', '.join(article['authors'])} | {article['abstract']} | {article['submitted_date']} |
"""
    return markdown_table

# Main function to download and save the article
def main():
    article = get_latest_article()
    markdown_content = format_article_to_markdown(article)
    
    # Save the markdown content to a file
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"{today}-arxiv.md"
    with open(filename, 'w') as file:
        file.write(markdown_content)
    
    print(f"Article saved to {filename}")

if __name__ == "__main__":
    main()
