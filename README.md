# 🧑‍🔬 PubMed Paper Extractor 📄

This Python program fetches research papers from the PubMed API based on a user-specified query. It identifies papers with at least one author affiliated with a pharmaceutical or biotech company and returns the results in a CSV format.

## 🌟 Features

- 🔍 Fetches papers using the PubMed API with full query syntax support.
- 🏥 Filters papers based on authors affiliated with pharmaceutical or biotech companies.
- 📑 Outputs the results to a CSV file, including:
  - PubMed ID
  - Title
  - Publication Date
  - Non-academic Author(s)
  - Company Affiliation(s)
  - Corresponding Author Email
- ⚙️ Command-line interface (CLI) to interact with the program.
- ⚡ Accepts the following command-line options:
  - `-h` or `--help`: Display usage instructions.
  - `-d` or `--debug`: Print debug information during execution.
  - `-f` or `--file`: Specify the filename to save the results as a CSV. If this option is not provided, the output will be printed to the console.

## 📦 Requirements

- Python 3.x 🐍
- Poetry (for dependency management) 📜
- Git (for version control) 🧑‍💻

## 🔧 Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/username/pubmed-paperfetcher-and-cli.git
    cd pubmed-paperfetcher-and-cli
    ```

2. Install dependencies using Poetry:

    ```bash
    poetry install
    ```

3. Run the program:

    ```bash
    poetry run get-papers-list "<your-query>"
    ```

   If you want to save the results to a file:

    ```bash
    poetry run get-papers-list "<your-query>" -f results.csv
    ```

4. To enable debugging (for development purposes), use:

    ```bash
    poetry run get-papers-list "<your-query>" -d
    ```

## 📝 How It Works

- The program sends a query to the PubMed API, parses the response, and filters the results based on authors affiliated with pharmaceutical or biotech companies.
- It identifies non-academic authors based on heuristics like email addresses containing domains such as `gmail.com`, `yahoo.com`, or words like `university` or `lab`.
- The results are saved in a CSV file or printed to the console.

## 💡 Example Usage

```bash
poetry run get-papers-list "cancer treatment" -f cancer_papers.csv
This will search for papers related to "cancer treatment" and save the filtered results to cancer_papers.csv.
```

## 📂 Code Structure

- **get_papers.py**: Contains the logic to interact with the PubMed API, filter the results, and save them to a CSV file.
- **cli.py**: Contains the command-line interface logic for accepting user inputs and calling `get_papers.py`.
- **requirements.txt**: Lists the dependencies for the project.
- **README.md**: Provides documentation for the project (this file).

## 📋 Dependencies

The project uses the following libraries:
- **requests**: For making HTTP requests to the PubMed API.
- **argparse**: For handling command-line arguments.
- **csv**: For saving the results in a CSV file.
- **Poetry**: For managing project dependencies and packaging.

## 🚀 Publishing the Module

The module has been published to TestPyPI for testing and distribution.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔧 External Tools Used

- **PubMed API** for fetching research papers.
- **Poetry** for dependency management.
- **requests** for making API calls.

### Usage

```bash
poetry run get-papers-list "cancer treatment" -f cancer_papers.csv
```




