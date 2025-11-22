# Agent

A multi-functional AI agent powered by Google's Gemini API that can execute various tasks based on natural language instructions. The agent can read files, write content, explore directory structures, and run Python code dynamically.

## Installation

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager

### Setup

1. Clone the repository and navigate to the project directory:

```bash
cd agent
```

2. Create a virtual environment and install dependencies using uv:

```bash
uv sync
```

3. Create a `.env` file in the root directory with your Gemini API key:

```
GEMINI_API_KEY=your_api_key_here
```

Get your API key from [Google AI Studio](https://aistudio.google.com/).

## Usage

Run the agent with a message using uv:

```bash
uv run main.py "your message here"
```

For verbose output:

```bash
uv run main.py "your message here" -v
```

### Example

```bash
uv run main.py "List all files in the current directory"
uv run main.py "Create a Python calculator and test it"
```

## Project Structure

- `main.py` - Entry point for the agent
- `call_function.py` - Function calling logic and function dispatch
- `prompts.py` - System prompts and prompt management
- `config.py` - Configuration settings
- `functions/` - Available functions the agent can call:
  - `get_file_content.py` - Read file contents
  - `get_files_info.py` - List files and directories
  - `write_file.py` - Create and write to files
  - `run_python_file.py` - Execute Python scripts
- `calculator/` - Example module with a Calculator class that evaluates mathematical expressions

## Available Functions

The agent can call the following functions:

### get_files_info
Lists files in a specified directory along with their sizes.

**Parameters:**
- `directory` - The directory to list files from (relative to working directory)

### get_file_content
Reads and returns the content of a file.

**Parameters:**
- `file_path` - The path to the file to read

### write_file
Creates or overwrites a file with specified content.

**Parameters:**
- `file_path` - The file path to create/write to
- `content` - The content to write to the file

### run_python_file
Executes a Python script within the working directory.

**Parameters:**
- `file_path` - The Python file to execute
- `args` - Optional arguments to pass to the script


## Testing

Run tests with uv:

```bash
uv run tests.py
```

## Requirements

- google-genai==1.12.1
- python-dotenv==1.1.0

## License

See LICENSE file for details.
