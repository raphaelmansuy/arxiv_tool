import os
from typing import List
from datetime import datetime, timedelta
import requests
from pydantic import BaseModel
# pylint: disable=W0622
from rich import print
from bs4 import BeautifulSoup
import click


class Article(BaseModel):
    """_summary_


    Args:
        BaseModel (_type_): _description_
    """

    title: str
    authors: List[str]
    arxiv_id: str
    arxiv_url: str
    tags: List[str]
    abstract_short: str
    abstract_full: str
    submited_date: datetime


def parse_date(date_string: str) -> datetime:
    """Parse a date string into a datetime object"""
    # Define the date format
    date_format = "%d %B, %Y"
    try:
        # Parse the date string into a datetime object
        parsed_date = datetime.strptime(date_string, date_format)
        return parsed_date
    except ValueError as _e:
        # Handle the error if the date_string is not in the expected format
        return None


def extract_date_submitted(article) -> datetime:
    """
    Extract the date the article was submitted from the article's HTML
    """
    # Find the <p> tag that contains the submission date
    submission_info = article.find("p", class_="is-size-7")

    # Extract the text and clean it up
    if submission_info:
        submission_text = submission_info.text.strip()
        # Split the text to get the different dates
        submission_parts = submission_text.split(";")
        # Extract the most recent submission date (assuming it's the first one mentioned)
        submitted_date = submission_parts[0].replace("Submitted", "").strip()
        return parse_date(submitted_date)
    else:
        return None


def extract_article_detail(article) -> Article:  # Removed 'soup' parameter
    """
    Extract the details of an article from the article's HTML
    """
    # Directly use 'article' parameter
    title = article.find("p", class_="title is-5 mathjax").get_text(strip=True)
    authors = [
        a.get_text(strip=True)
        for a in article.find_all(
            "a",
            href=lambda href: href and href.startswith("/search/cs?searchtype=author"),
        )
    ]
    arxiv_id = article.find(
        "a", href=lambda href: href and href.startswith("https://arxiv.org/abs/")
    )["href"].split("/")[-1]
    arxiv_url = article.find(
        "a", href=lambda href: href and href.startswith("https://arxiv.org/abs/")
    )["href"]
    tags = [
        tag.get_text(strip=True)
        for tag in article.find_all(
            "span", class_="tag is-small is-link tooltip is-tooltip-top"
        )
    ]
    abstract_short = article.find(
        "span", class_="abstract-short has-text-grey-dark mathjax"
    ).get_text(strip=True)
    abstract_full = article.find(
        "span", class_="abstract-full has-text-grey-dark mathjax"
    ).get_text(strip=True)

    submited_date = extract_date_submitted(article)

    return Article(
        title=title,
        authors=authors,
        arxiv_id=arxiv_id,
        arxiv_url=arxiv_url,
        tags=tags,
        abstract_short=abstract_short,
        abstract_full=abstract_full,
        submited_date=submited_date,
    )


def get_articles(query: str, from_date: datetime, to_date_time: datetime) -> List[Article]:
    """
    Get the articles from arXiv
    """
    print("Sending request to arXiv...")
    search_from_date = from_date.strftime("%Y-%m-%d")
    search_to_date = to_date_time.strftime("%Y-%m-%d")
    ## URL encode the query
    encoded_query = query.replace(" ", "+")
    url = f"https://arxiv.org/search/cs?query={encoded_query}&searchtype=all&abstracts=show&order=-submitted_date&size=200"
    url += f"&date-filter_by=date_range&from_date={search_from_date}&to_date={search_to_date}"
    url += "&date-date_type=submitted_date"

    response = requests.get(url, timeout=12000)
    print(f"Request sent to {url}")
    soup = BeautifulSoup(response.text, "html.parser")
    print("Response received.")

    articles = soup.find_all(class_="arxiv-result")
    if not articles:
        print("No articles found.")
        return None

    result_list = list(extract_article_detail(article) for article in articles)
    return result_list


def format_article_to_markdown(articles: List[Article]) -> str:
    """
    Format the articles into a markdown table
    """
    markdown_table = """
| Arxiv Number | Submitted | Title | Authors | Abstract |
|--------------|-----------|-------|---------|----------|
"""
    for _index, article in enumerate(articles):
        row =  f"""| [{article.arxiv_id}]({article.arxiv_url}) """
        row += f"""| {article.submited_date.strftime('%Y-%m-%d')} """
        row += f"""| {article.title} """
        row += f"""| {', '.join(article.authors)} """
        row += f"""| {article.abstract_full} """
        row += """ |"""

        markdown_table += row + "\n"

    return markdown_table


def extract_articles(
    query: str,
    from_date: datetime, to_date: datetime, target_dir: str = None
) -> None:
    """
    Extract articles from arXiv within a specified date range.
    """
    articles = get_articles(query,from_date=from_date, to_date_time=to_date)
    if articles is not None and len(articles) > 0:
        from_date_display = from_date.strftime("%Y-%m-%d")
        to_date_display = to_date.strftime("%Y-%m-%d")
        print(
            f"Found {len(articles)} articles from {from_date_display} to {to_date_display}."
        )
        markdown_content = format_article_to_markdown(articles)
        filename = f"{from_date_display}_to_{to_date_display}-arxiv.md"
        
        if target_dir: 
            # use os.path.join to join the target_dir and filename
            filename = os.path.join(target_dir, filename)

        with open(filename, "w", encoding="utf-8") as file:
            file.write(markdown_content)
        print(f"Article saved to {filename}")
    else:
        print("No article to save.")




@click.command("extract", help="Extract articles from arXiv within a specified date range.")
@click.option(
    '--query', 'query', 
    type=str, 
    required=True, 
    help='Search query for the articles. ex: "quantum computing" or "quantum+computing"',
    default="Artificial Intelligence"
)
@click.option(
    '--from-date', 'from_date', 
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=datetime.now(), 
    help='Start date for the articles. ex: 2024-03-31'
)
@click.option(
    '--to-date', 'to_date', 
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=datetime.now() - timedelta(days=1), 
    help='End date for the articles. ex: 2024-04-01'
)
@click.option(
    '--target-dir', 'target_dir', 
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True), 
    help='Directory to save the articles.'
)
def main(query: str,from_date: datetime, to_date: datetime, target_dir: str = None):
    """
    Extract articles from arXiv within a specified date range.

    :param from_date: Start date for the articles.
    :param to_date: End date for the articles.
    """
    # Your function logic here
    print(f"Extracting articles from arXiv for '{query}' ...")
    extract_articles(query,from_date, to_date, target_dir)

if __name__ == "__main__":
    # ignore Pylint error E1120
    # pylint: disable=no-value-for-parameter
    main()