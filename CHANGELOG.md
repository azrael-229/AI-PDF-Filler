# Changelog

All notable changes to this project will be documented in this file.

## [2.2.0] - 2026-05-27

### Added
- Multi-provider AI support via unified abstraction layer (`src/ai_provider.py`)
  - Ollama (local)
  - LM Studio (local)
  - vLLM / any OpenAI-compatible endpoint (cloud or local)
  - OpenAI (cloud)
- GUI provider selector with auto-fill for known providers
- API key input field in the GUI
- Base URL configuration per provider

### Changed
- Consolidated project from multiple versioned directories into a single clean repository
- Restructured source code to use `ai_provider.py` abstraction instead of direct Ollama calls
- Improved bilingual UI with dynamic language switching (Polish/English)

## [2.1.0] - Previous iteration

### Added
- Bilingual support (Polish and English) for UI labels and AI prompts
- Q&A section processing in PDFs

## [2.0.0] - Previous iteration

### Changed
- Improved cell detection and marking logic
- Better multi-cell input handling

## [1.0.0] - Initial version

### Added
- Basic PDF form filling with Ollama AI
- Tkinter-based GUI
- Field detection using OpenCV image processing
- Tesseract OCR for field name recognition
