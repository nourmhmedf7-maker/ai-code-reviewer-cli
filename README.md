# AI Code Reviewer CLI

A small command-line tool written in Python that reviews a code file using an AI model.
You give it a file, it sends the code to the model through the Groq API, and prints a short review in your terminal: a rating, the issues it found with solutions, and suggestions for improvement.

## How It Works

1. You run the script and pass the path of a code file.
2. The script reads the file and turns its content into text.
3. It sends the text to the model (`openai/gpt-oss-20b` on Groq) together with review instructions.
4. The response is streamed to your terminal as it is generated.

The model never sees your computer. It only receives the text of the file you pass in.

## Output Format

The review always contains three sections:

- **Rating** out of 10
- **Code Issues and Their Solutions**
- **Improvements**

## Requirements

- Python 3.10 or newer
- A free API key from [Groq](https://console.groq.com)

## Installation

```bash
git clone https://github.com/nourm0hamed/ai-code-reviewer-cli.git
cd ai-code-reviewer-cli
```

Install the dependencies.

Using [`uv`](https://docs.astral.sh/uv/) (recommended, it reads `pyproject.toml` and `uv.lock`):

```bash
uv sync
```

Or using `pip`:

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install openai python-dotenv
```

## Configuration

Copy `.env.example` to `.env` and put your key in it:

```
GROQ_APIKEY=your_api_key_here
```

The `.env` file is listed in `.gitignore`, so your key is never uploaded to GitHub.

## Usage

With `uv`:

```bash
uv run code_reviewer.py path/to/your_file.py
```

Or with `pip` (after activating your virtual environment):

```bash
python code_reviewer.py path/to/your_file.py
```

Example:

```bash
uv run code_reviewer.py test.py
```

Example output:

```
loading....
**Rating:** 7/10

**Code Issues and Their Solutions**
- **Line 6:** The function divides by len(numbers) without checking for an empty list.
  - **Solution:** Add a guard clause that handles an empty list.

**Improvements**
- Use Python's built-in sum() instead of a manual loop.
- Add a docstring and type hints.
```

## Error Handling

The tool prints a clear message instead of a long traceback when:

| Situation | Message |
|---|---|
| No file name given | `please enter your file name` |
| File does not exist | `file not found` |
| File is not a UTF-8 text file | `file is not a valid text file` |
| API key is missing or wrong | `Check your API key or token` |
| No internet connection | `check your network` |

## Project Structure

```
ai-code-reviewer-cli/
├── code_reviewer.py   # the whole program
├── pyproject.toml     # project metadata and dependencies
├── uv.lock            # exact dependency versions
├── .python-version    # Python version used by uv
├── .env.example       # template for your environment variables
├── .gitignore         # keeps .env out of Git
└── README.md
```

## Limitations

- Line numbers in the review are estimated by the model and may not be exact.
- Very large files may exceed the model's input limit.
- The free Groq tier has rate limits, so too many requests in a short time may be rejected.

## What I Learned

- Reading command-line arguments with `sys.argv`
- Working with files and handling errors in Python
- Calling an API with the OpenAI Python SDK and streaming the response
- Storing secrets in a `.env` file
- Writing and improving prompts (prompt engineering)
- Using Git and GitHub

## Possible Improvements

- Add line numbers to the code before sending it, for more accurate references
- Support reviewing a whole folder
- Add options such as `--focus bugs` or `--output report.md`
- Return the review as structured JSON (Structured Outputs)
