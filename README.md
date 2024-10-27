# Lyrics Interpreter

## Overview
Lyrics Interpreter is your guide in understanding lyrics. Integrating the power of LLMs and Urban Dictionary, with this app you can really understand what Kanye meant in that latest song. 

## Installation

### Prerequisites
- Python 3.8 or higher
- Pip for Python package management

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/tomas-salgado/lyrics_interpreter.git
   ```
2. Navigate to the project directory:
   ```bash
   cd path/to/lyrics_interpreter
   ```
3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables
Create a `.env` file in the root directory of the project and add the following environment variable:
```bash
CLAUDE_API_KEY='your_anthropic_api_key_here'
```

## Usage
Run the script from the command line:
```bash
python backend/lyrics_interpreter.py
```

## Code Structure
- **LyricsInterpreter Class**: Implements core functionalities including text filtering, slang detection, and text interpretation. See `backend/lyrics_interpreter.py` lines 10-72.
- **UrbanDictionary Integration**: Fetches slang definitions from Urban Dictionary. See `backend/urban_dictionary.py` lines 1-41.
- **Command-line Interface Loop**: Manages user input and displays results. See `backend/lyrics_interpreter.py` lines 89-99.