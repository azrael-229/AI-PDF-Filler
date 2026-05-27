# Contributing to AI PDF Filler

Thank you for your interest in contributing! This document covers how to get started.

## How to Contribute

1. **Fork** this repository on GitHub
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/ai-pdf-filler.git
   cd ai-pdf-filler
   ```
3. **Install dependencies**:
   ```bash
   python src/install.py
   ```
4. **Create a branch** for your feature or fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
5. **Make changes** and commit with clear messages:
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```
6. **Push** to your fork and open a Pull Request

## Development Setup

- Python 3.7+ required
- Tesseract OCR must be installed on the system (see README.md)
- Run `python src/gui.py` to test the application

## Code Style

- Follow PEP 8 conventions
- Use meaningful variable and function names
- Add docstrings to new functions and classes
- Keep functions focused and under ~50 lines when possible

## Reporting Issues

Use GitHub Issues to report bugs or request features. Include:
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Your OS, Python version, and AI provider configuration
