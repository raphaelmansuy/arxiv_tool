# ArXiv Article Extractor

This Python script is designed to extract and compile a list of articles from the arXiv repository within a specified date range. It specifically targets articles related to artificial intelligence in the Computer Science (cs) category. The script generates a Markdown file containing a table of articles with details such as the arXiv ID, submission date, title, authors, and a full abstract.

## Features

- Extracts articles from arXiv using BeautifulSoup4 for HTML parsing.
- Filters articles based on a date range provided by the user.
- Outputs a Markdown file with a table of articles.
- Each article entry includes metadata such as the title, authors, arXiv ID, URL, tags, and abstracts.
- Offers command-line interface options to specify the date range and output directory.

## Requirements

Before running the script, ensure that you have the following packages installed:

- `requests`
- `bs4` (BeautifulSoup4)
- `pydantic`
- `rich`
- `click`

You can install the required packages using pip:

```bash
pip install requests beautifulsoup4 pydantic rich click
```

## Usage

To use the script, execute it from the command line with the following options:

```bash
python arxiv_extractor.py extract --from-date YYYY-MM-DD --to-date YYYY-MM-DD --target-dir /path/to/directory
```

- `--from-date`: The start date for the articles to be extracted. (format: YYYY-MM-DD)
- `--to-date`: The end date for the articles. (format: YYYY-MM-DD)
- `--target-dir`: The directory where the Markdown file will be saved.

## Example

```bash
python arxiv_extractor.py extract --from-date 2023-03-01 --to-date 2023-03-31 --target-dir ./articles
```

This will extract articles from March 1, 2023, to March 31, 2023, and save the Markdown file in the `./articles` directory.

## Installation with pipx

```bash
pipx install git+https://github.com/raphaelmansuy/arxiv_tool.git --force --include-dep
```

## Output

The script creates a Markdown file named with the date range of the articles, for example, "2023-03-01_to_2023-03-31-arxiv.md". The file contains a table with the following columns:

- Arxiv Number
- Submitted
- Title
- Authors
- Abstract

Each row corresponds to an article, and the Arxiv Number is linked to the article's page on arXiv.org.

## Contributing

Contributions are welcome! Feel free to submit pull requests or create issues for bugs and feature requests.

## License

This script is provided as-is, with no warranty. You are free to use, modify, and distribute it under the terms of your choosing. Please check with the arXiv terms of service regarding the use of their data.

Keep in mind that this `README.md` is a template and should be modified to fit your project's specifics and additional details as needed. If you have any particular sections or details you'd like to add or modify, please let me know, and I can assist you further.