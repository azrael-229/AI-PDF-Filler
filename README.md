# AI PDF Filler

AI PDF Filler is a Python application that automatically fills out PDF forms using AI-powered text generation. It detects empty fields in PDF documents and fills them with contextually appropriate responses based on provided information. The application supports **bilingual operation (Polish & English)** through an intuitive language selector, along with **multi-provider AI model selection** via the GUI.

## Features

- Bilingual Support: Full Polish and English functionality with dynamic UI translation
- Multi-Provider AI Support: Use any OpenAI-compatible API provider including:
  - Ollama (local)
  - LM Studio (local)
  - vLLM (local/cloud)
  - OpenAI (cloud)
  - Any other OpenAI-compatible endpoint
- GUI Interface: Easy file selection and processing via Tkinter-based interface
- Automated Field Detection: Intelligent detection of empty form fields using image processing
- AI-Powered Generation: Context-aware text generation for filling out forms
- Multi-cell Input Handling: Support for handling multiple-cell inputs efficiently
- Q&A Section Processing: Automatic question and answer section handling
- PDF/Image Conversion: Seamless conversion between PDF and high-resolution images

## Prerequisites

Before running the application, ensure you have:

1. Python 3.7 or higher installed
2. Tesseract OCR installed on your system (with language packs)
3. An AI provider set up (see [AI Provider Configuration](#ai-provider-configuration))

### Installing Tesseract OCR

#### Windows

1. Download the installer from the [UB-Mannheim Tesseract page](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer
3. Add the Tesseract installation directory to your system PATH
4. Update the Tesseract path in `src/testingcode.py`:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

#### macOS

```bash
brew install tesseract
```

#### Linux

```bash
sudo apt-get install tesseract-ocr
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/ai-pdf-filler.git
cd ai-pdf-filler
```

2. Install Python dependencies:

```bash
python src/install.py
```

This will install the following packages:

- opencv-python
- numpy
- PyMuPDF
- pytesseract
- Pillow
- transformers
- torch
- setuptools
- requests (for AI API calls)

Or install manually from `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the GUI application:

```bash
python src/gui.py
```

2. Using the GUI:

   - Select your preferred language from the dropdown menu (Polish or English)
   - Choose an AI provider from the dropdown (Ollama, LM Studio, OpenAI Compatible, or Custom)
   - Enter your API key if required by your chosen provider (optional for local providers)
   - The Base URL will auto-fill based on your provider selection, but you can customize it
   - Enter your preferred AI model name in the "Model AI" field
   - Select your input PDF file
   - Choose the context text file containing relevant information
   - Select an output directory for the processed files
   - Click "Start Processing" to begin

## Project Structure

```
AI-PDF-Filler/
├── README.md          # Documentation (this file)
├── CHANGELOG.md       # Version history
├── CONTRIBUTING.md    # Contribution guidelines
├── requirements.txt   # Python dependencies
├── data/              # Input and sample files
│   ├── Dummy_Questionnaire.pdf
│   └── Dummy_data.txt
├── output/            # Generated output files (created at runtime)
└── src/               # Application source code
    ├── gui.py         # Main GUI application with bilingual & multi-provider support
    ├── testingcode.py # Core processing logic and AI integration
    ├── ai_provider.py # Unified AI provider abstraction layer
    └── install.py     # Package installation script
```

## How It Works

1. The application converts PDF pages to high-resolution images
2. It detects empty form fields using image processing techniques
3. For each empty field:
   - Identifies the field name using OCR
   - Generates appropriate text using AI based on selected language prompts and configurable model
   - Fills the field with the generated text
4. Processes Q&A sections similarly with language-specific prompt templates
5. Converts the processed images back to PDF format

## Language Support

The application supports two languages:

| Code | Language | UI Translation | AI Prompts | OCR Support |
|------|----------|----------------|------------|-------------|
| `pol` | Polish   | Yes            | Yes        | Built-in    |
| `eng` | English  | Yes            | Yes        | Built-in    |

### Prompt Templates

The application uses language-specific prompt templates for AI generation:

- **Single Field**: Concise answers (1-3 words) with date/number handling
- **Multi-field**: Comma-separated lists with item count specification
- **Q&A Section**: Contextual responses (~20-25 words) with current date awareness

## Configuration

### AI Provider Configuration

The application supports multiple AI providers through a unified abstraction layer. You can configure your preferred provider in the GUI or programmatically:

#### Using the GUI

1. Open the "AI Provider" dropdown and select your provider type
2. If using a cloud provider (e.g., OpenAI), enter your API key in the "API Key" field
3. The "Base URL" will auto-fill based on your selection, but you can customize it:
   - **Ollama**: Leave empty or use `http://localhost:11434`
   - **LM Studio**: Uses `http://localhost:1234/v1` by default
   - **OpenAI Compatible**: Uses `https://api.openai.com/v1` by default
   - **Custom**: Enter your own URL

#### Programmatic Configuration

In `src/testingcode.py`, you can set global defaults:

```python
# AI Provider Configuration
AI_API_KEY = None  # Set to your API key for cloud providers (e.g., OpenAI)
AI_BASE_URL = None  # Leave as None for Ollama default, or set custom URL
```

#### Example Configurations

**Ollama (Local)**

```python
# No API key needed
AI_API_KEY = None
AI_BASE_URL = None  # Uses http://localhost:11434 by default
DEFAULT_MODEL = "gemma4:E4b"  # Or any Ollama model
```

**LM Studio (Local)**

```python
# LM Studio doesn't require an API key for local use
AI_API_KEY = None
AI_BASE_URL = "http://localhost:1234/v1"
DEFAULT_MODEL = "your-model-name"  # Any model loaded in LM Studio
```

**OpenAI (Cloud)**

```python
# Set your OpenAI API key
AI_API_KEY = "sk-you...here"
AI_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-3.5-turbo"  # Or gpt-4, etc.
```

**Custom Provider (e.g., vLLM)**

```python
# For any OpenAI-compatible endpoint
AI_API_KEY = None  # If authentication is not required
AI_BASE_URL = "http://localhost:8000/v1"  # Your custom endpoint
DEFAULT_MODEL = "your-model-name"
```

### Tesseract Configuration

Update the Tesseract path in `src/testingcode.py` to match your system installation.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Tesseract OCR for text recognition
- OpenCV for image processing
- PyMuPDF for PDF handling
- Requests library for HTTP API calls
- Pillow for image manipulation
- All AI providers that make this possible!
