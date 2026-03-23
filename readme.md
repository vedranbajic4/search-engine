# PDF Search Engine

## Table of context 📑
1. [Description](#description)
2. [Overview](#overview)
3. [Technologies](#technologies)
4. [Usage](#usage)
5. [How to Run](#how-to-run)
6. [Project Structure](#project-structure)
7. [License](#license)
8. [Contact](#contact)

## Description 📌
A custom PDF search engine built in Python that parses a PDF document, indexes its contents using a **Trie** data structure, and allows users to search for keywords. It features advanced query operations such as Boolean searches (AND, OR, NOT), wildcard queries (autocomplete), and spelling suggestions ("did you mean"). The engine ranks search results based on word occurrence frequency and a "PageRank"-style algorithm that utilizes a **Graph** of referenced pages.

## Overview 📖
This project was developed to demonstrate advanced knowledge of data structures and algorithms. The application extracts text page-by-page from a PDF (*Data Structures and Algorithms in Python*) and builds internal structures to facilitate fast, optimized searching. 

**Key Features:**
- **Efficient Indexing:** Uses a **Trie** data structure to index words on every page for fast retrieval.
- **Page Ranking Algorithm:** Ranks results based on term frequency and page references. It parses text for phrases like *"See page X"* to build a **Graph**, giving higher rank weight to heavily referenced pages.
- **Advanced Query Parser:** Supports logical operators (`AND`, `OR`, `NOT`) and grouping via parentheses to create complex search expressions.
- **Autocomplete & Wildcards:** Entering a query ending in `*` (e.g., `fun*`) prompts the engine to suggest popular completions like *function* or *functionality*.
- **"Did you mean?" Suggestions:** Suggests alternative, popular search terms if a query yields zero or very few results.
- **Serialization:** Saves parsed structures (Tries, Graph, and Dictionaries) using Python's `pickle` to drastically speed up startup times on subsequent runs.
- **Highlighted Output:** Highlights the searched terms directly in the console using `colorama` and generates a new PDF (`res.pdf`) with the found text visually highlighted using `reportlab`.

## Technologies ⚙️
- **Python 3.x**
- **PDFMiner (`pdfminer.high_level`, `pdfminer.pdfpage`)**: For accurate text extraction from the source PDF.
- **ReportLab / FPDF**: Used for generating the resulting PDF (`res.pdf`) and drawing highlighted text context.
- **Colorama**: For terminal text coloring and highlighting.
- **Pickle**: Standard Python library for serializing/deserializing Python object structures.
- **RegEx (`re`)**: For pattern matching page references and tokenizing expressions.

## Usage 💡
Upon running the script, the engine will quickly load the serialized data (if previously generated) and open a command-line interface. 

You can enter various types of search queries:
- **Single Keyword:** `python`
- **Boolean Expression:** `python AND sequence` or `(python OR java) NOT word`
- **Autocomplete/Wildcard:** `algo*#` (Prompts the system to suggest matching words)
- **Exit:** Type `-1` to exit the program.

The results will be paginated in the console, showing the page number, ranked score, and a text snippet with the searched words highlighted in yellow. A visual `res.pdf` file is concurrently generated.

## How to Run 🚀
1. **Clone the repository** and navigate to the project directory.
2. **Install dependencies:**
   ```bash
   pip install pdfminer.six reportlab fpdf colorama
   ```
3. **First-Time Execution (Data Parsing & Serialization)**
Before you can search, the engine needs to parse the PDF and build the indexing structures.

 - Open the Python script and scroll to the bottom (`if __name__ == '__main__'`: block).
  - Uncomment the `extract_text_by_page()` line.
 - Run the script: `python your_script_name.py`
 - The script will read the PDF page by page, build the structures, save them to the `data/` folder, and automatically exit.
 - **Important**: Once this is done, comment `extract_text_by_page()` back out.

4. **Running the Search Engine**

- Run the script again: `python your_script_name.py`
- The engine will quickly load the saved data and prompt you: `Unesite izraz za pretragu:`
- Enter your queries (e.g., `python AND java`, `func*`, or `(data OR struct) NOT list`).
- Type `-1` to exit the program.
- Check the generated `res.pdf` file in your directory to see visually highlighted results!


## Project Structure 🗂️

### Data Structures & Classes 🧱

 - `Result`

   Represents the search outcome for a single page. It stores the page index, the calculated rank (`_weight`), and the text snippets containing the found words. It implements comparison methods (`__lt__`, `__eq__`) to allow easy sorting of results from highest to lowest rank. It also handles the terminal output (`ispisi_rez`), using `colorama` to highlight the queried terms in yellow.

 - `TrieNode` & `Trie`

   A custom Trie (Prefix Tree) implementation used to index words for every single page.
    - `TrieNode stores` children characters and an `is_end_of_word` counter that tracks how many times a word appears.

    - `Trie` handles the `insert` logic and includes a specialized `search` method. If a wildcard `*` is detected in the search, it triggers a `recursive` function that sums up the occurrences of all words sharing that prefix.

### Core Global Variables 💾
 - `tries`: A list where the i-th element is the `Trie` corresponding to the i-th page of the PDF.
 - `graf`: A dictionary acting as an adjacency list. It maps pages to the pages they reference (extracted via Regex patterns like "see page X"), used for PageRank-style weight distribution.
 - `didumean`: A frequency dictionary of all words in the document, used to power the spelling correction and autocomplete features.

 ### Key Functions 🔧
 - `extract_text_by_page()`

    The initialization engine. It iterates through `book.pdf`, cleans the text, populates the `Trie` for each page, uses Regular Expressions to find page references for the `graf`, and finally serializes everything into `.pickle` files to save loading time on future runs.

 - `sredi_izraz(exp)`

   Parses the user's raw input. It uses Regex to separate valid keywords from Boolean operators (`AND`, `OR`, `NOT`) and parentheses. It also detects if the user is asking for autocomplete (indicated by `#` at the end of the query) and dynamically fetches suggestions from the `didumean` dictionary.

 - `sredi_rezultate()`

   The core evaluator. It iterates through all pages and evaluates the parsed Boolean expression using a custom Stack-based evaluator (`izracunaj`). If a page satisfies the Boolean logic, it calculates a base rank based on term frequency. Finally, it applies the graph logic: if Page A references Page B, Page B receives bonus weight, prioritizing highly referenced pages.

 - `nadji_tekst(pg)`

   Whenever a page is flagged as a valid result, this function re-reads the specific page to extract short text snippets (context windows of a few words before and after the matched keyword) to display to the user.

- `draw_highlighted_text(...)`

  Utilizes the `reportlab` canvas library to write the extracted text snippets to a physical output file (`res.pdf`), calculating string widths to draw yellow highlight rectangles exactly behind the matched search terms.

## License 🧾

This project is for educational purposes within the DSA course.
You are free to use or modify it for learning and research.

## Contact 📬

If you have any questions, suggestions, or would like to collaborate — feel free to reach out!

👤 Author: Vedran Bajić

📧 Email: bajic196@gmail.com