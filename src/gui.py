import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from testingcode import process_pdf

# Language translations for UI elements
LANGUAGES = {
    'pol': {
        'title': "AI Wypełnianie Formularzy - AI PDF Filler",
        'lang_label': "Język (Language):",
        'model_label': "Model AI:",
        'provider_label': "Dostawca AI / AI Provider:",
        'api_key_label': "Klucz API (opcjonalny) / API Key (optional):",
        'base_url_label': "Adres URL API / Base URL:",
        'pdf_label': "Wybierz plik PDF:",
        'context_label': "Wybierz plik kontekstu:",
        'output_label': "Wybierz katalog wyjściowy:",
        'browse_button': "Przeglądaj",
        'start_button': "Rozpocznij Przetwarzanie",
        'processing_status': "Rozpoczęto przetwarzanie...",
        'completion_status': "Przetwarzanie zakończone!",
        'error_message': "Wystąpił błąd.",
        'success_message': "Przetwarzanie PDF zakończone pomyślnie.",
        'pdf_error': "Proszę wybrać poprawny plik PDF.",
        'context_error': "Proszę wybrać poprawny plik kontekstu.",
        'output_error': "Proszę wybrać poprawny katalog wyjściowy.",
        'file_types': [("Pliki PDF", "*.pdf"), ("Wszystkie pliki", "*.*")],
        'context_file_types': [("Pliki Tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")]
    },
    'eng': {
        'title': "AI Form Filler - AI PDF Filler",
        'lang_label': "Language:",
        'model_label': "AI Model:",
        'provider_label': "AI Provider:",
        'api_key_label': "API Key (optional):",
        'base_url_label': "Base URL:",
        'pdf_label': "Select PDF file:",
        'context_label': "Select context file:",
        'output_label': "Select output directory:",
        'browse_button': "Browse",
        'start_button': "Start Processing",
        'processing_status': "Processing started...",
        'completion_status': "Processing complete!",
        'error_message': "An error occurred.",
        'success_message': "PDF processing completed successfully.",
        'pdf_error': "Please select a valid PDF file.",
        'context_error': "Please select a valid context file.",
        'output_error': "Please select a valid output directory.",
        'file_types': [("PDF Files", "*.pdf"), ("All files", "*.*")],
        'context_file_types': [("Text Files", "*.txt"), ("All files", "*.*")]
    }
}

class PDFProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.lang_var = tk.StringVar(value='pol')  # Default to Polish
        self.model_var = tk.StringVar(value="gemma4:E4b")  # Default AI model
        self.provider_var = tk.StringVar(value="Ollama")  # Default provider
        self.api_key_var = tk.StringVar()  # Empty by default
        self.base_url_var = tk.StringVar()  # Empty by default (uses defaults)
        
        # Initialize with Polish UI
        self.root.title(LANGUAGES['pol']['title'])
        self.root.geometry("700x650")  # Taller to accommodate more fields
        
        self.create_widgets()

    def update_ui_language(self, lang):
        """Update all UI elements based on selected language"""
        translations = LANGUAGES[lang]
        
        # Update window title
        self.root.title(translations['title'])
        
        # Update labels
        self.lang_label.config(text=translations['lang_label'])
        self.model_label.config(text=translations['model_label'])
        self.provider_label.config(text=translations['provider_label'])
        self.api_key_label.config(text=translations['api_key_label'])
        self.base_url_label.config(text=translations['base_url_label'])
        self.pdf_label.config(text=translations['pdf_label'])
        self.context_label.config(text=translations['context_label'])
        self.output_label.config(text=translations['output_label'])
        
        # Update buttons
        self.pdf_button.config(text=translations['browse_button'])
        self.context_button.config(text=translations['browse_button'])
        self.output_button.config(text=translations['browse_button'])
        self.start_button.config(text=translations['start_button'])

    def create_widgets(self):
        padding = {'padx': 10, 'pady': 5}

        # Language Selection
        self.lang_label = tk.Label(self.root, text="Język (Language):")
        self.lang_label.grid(row=0, column=0, sticky='e', **padding)

        self.lang_combo = ttk.Combobox(self.root, textvariable=self.lang_var, width=20, state='readonly')
        self.lang_combo['values'] = ('pol', 'eng')
        self.lang_combo.grid(row=0, column=1, **padding)
        
        # Bind language change event
        self.lang_combo.bind('<<ComboboxSelected>>', self.on_language_change)

        # AI Provider Selection
        self.provider_label = tk.Label(self.root, text="Dostawca AI / AI Provider:")
        self.provider_label.grid(row=1, column=0, sticky='e', **padding)

        self.provider_combo = ttk.Combobox(self.root, textvariable=self.provider_var, width=20, state='readonly')
        self.provider_combo['values'] = ('Ollama', 'LM Studio', 'OpenAI Compatible', 'Custom')
        self.provider_combo.grid(row=1, column=1, **padding)
        
        # Bind provider change event to update URL suggestions
        self.provider_combo.bind('<<ComboboxSelected>>', self.on_provider_change)

        # API Key (optional)
        self.api_key_label = tk.Label(self.root, text="Klucz API / API Key:")
        self.api_key_label.grid(row=2, column=0, sticky='e', **padding)

        self.api_key_entry = tk.Entry(self.root, textvariable=self.api_key_var, width=50)
        self.api_key_entry.grid(row=2, column=1, **padding)

        # Base URL
        self.base_url_label = tk.Label(self.root, text="Adres URL / Base URL:")
        self.base_url_label.grid(row=3, column=0, sticky='e', **padding)

        self.base_url_entry = tk.Entry(self.root, textvariable=self.base_url_var, width=50)
        self.base_url_entry.grid(row=3, column=1, **padding)

        # Model Selection
        self.model_label = tk.Label(self.root, text="Model AI:")
        self.model_label.grid(row=4, column=0, sticky='e', **padding)

        self.model_entry = tk.Entry(self.root, textvariable=self.model_var, width=50)
        self.model_entry.grid(row=4, column=1, **padding)

        # Input PDF Selection
        self.pdf_label = tk.Label(self.root, text="Wybierz plik PDF:")
        self.pdf_label.grid(row=5, column=0, sticky='e', **padding)

        self.pdf_path = tk.StringVar()
        self.pdf_entry = tk.Entry(self.root, textvariable=self.pdf_path, width=50)
        self.pdf_entry.grid(row=5, column=1, **padding)

        self.pdf_button = tk.Button(self.root, text="Przeglądaj", command=self.browse_pdf)
        self.pdf_button.grid(row=5, column=2, **padding)

        # Context File Selection
        self.context_label = tk.Label(self.root, text="Wybierz plik kontekstu:")
        self.context_label.grid(row=6, column=0, sticky='e', **padding)

        self.context_path = tk.StringVar()
        self.context_entry = tk.Entry(self.root, textvariable=self.context_path, width=50)
        self.context_entry.grid(row=6, column=1, **padding)

        self.context_button = tk.Button(self.root, text="Przeglądaj", command=self.browse_context)
        self.context_button.grid(row=6, column=2, **padding)

        # Output Directory Selection
        self.output_label = tk.Label(self.root, text="Wybierz katalog wyjściowy:")
        self.output_label.grid(row=7, column=0, sticky='e', **padding)

        self.output_path = tk.StringVar()
        self.output_entry = tk.Entry(self.root, textvariable=self.output_path, width=50)
        self.output_entry.grid(row=7, column=1, **padding)

        self.output_button = tk.Button(self.root, text="Przeglądaj", command=self.browse_output)
        self.output_button.grid(row=7, column=2, **padding)

        # Start Button
        self.start_button = tk.Button(self.root, text="Rozpocznij Przetwarzanie", 
                                     command=self.start_processing, bg='green', fg='white')
        self.start_button.grid(row=8, column=1, **padding)

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, orient='horizontal', length=400, mode='determinate')
        self.progress.grid(row=9, column=0, columnspan=3, **padding)

        # Status Message
        self.status_message = tk.StringVar()
        self.status_label = tk.Label(self.root, textvariable=self.status_message, fg='blue')
        self.status_label.grid(row=10, column=0, columnspan=3, **padding)

    def on_language_change(self, event):
        """Handle language selection change"""
        lang = self.lang_var.get()
        self.update_ui_language(lang)

    def on_provider_change(self, event):
        """Update base URL based on selected provider"""
        provider = self.provider_var.get()
        
        # Set default URLs for known providers
        if provider == "Ollama":
            self.base_url_var.set("")  # Empty means use Ollama defaults
        elif provider == "LM Studio":
            self.base_url_var.set("http://localhost:1234")
        elif provider == "OpenAI Compatible":
            self.base_url_var.set("https://api.openai.com/v1")
        # For "Custom", user can enter their own URL

    def browse_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=LANGUAGES[self.lang_var.get()]['file_types'])
        if file_path:
            self.pdf_path.set(file_path)

    def browse_context(self):
        file_path = filedialog.askopenfilename(filetypes=LANGUAGES[self.lang_var.get()]['context_file_types'])
        if file_path:
            self.context_path.set(file_path)

    def browse_output(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_path.set(directory)

    def start_processing(self):
        pdf = self.pdf_path.get()
        context = self.context_path.get()
        output = self.output_path.get()
        lang = self.lang_var.get()
        model = self.model_var.get().strip()  # Get selected/entered model
        
        # Get provider settings
        api_key = self.api_key_var.get().strip() or None
        base_url = self.base_url_var.get().strip() or None

        # Get translations for current language
        translations = LANGUAGES[lang]

        if not pdf or not os.path.isfile(pdf):
            messagebox.showerror("Błąd" if lang == 'pol' else "Error", translations['pdf_error'])
            return

        if not context or not os.path.isfile(context):
            messagebox.showerror("Błąd" if lang == 'pol' else "Error", translations['context_error'])
            return

        if not output or not os.path.isdir(output):
            messagebox.showerror("Błąd" if lang == 'pol' else "Error", translations['output_error'])
            return

        self.start_button.config(state='disabled')
        self.status_message.set(translations['processing_status'])
        self.progress['value'] = 0

        threading.Thread(target=self.run_processing, args=(pdf, context, output, lang, model, api_key, base_url)).start()

    def run_processing(self, pdf, context, output, lang, model, api_key=None, base_url=None):
        try:
            process_pdf(pdf, output, context, lang, model, api_key=api_key, base_url=base_url)
            self.progress['value'] = 100
            
            # Get translations for current language
            translations = LANGUAGES[lang]
            
            self.status_message.set(translations['completion_status'])
            messagebox.showinfo("Sukces" if lang == 'pol' else "Success", translations['success_message'])
        except Exception as e:
            translations = LANGUAGES[lang]
            self.status_message.set(translations['error_message'])
            messagebox.showerror("Błąd" if lang == 'pol' else "Error", f"{translations['error_message']}: {str(e)}")
        finally:
            self.start_button.config(state='normal')

def main():
    root = tk.Tk()
    app = PDFProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
