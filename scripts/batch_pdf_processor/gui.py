#!/usr/bin/env python3
"""
Simple GUI for Batch PDF Processing
Provides easy file/folder selection and progress tracking
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from pathlib import Path
import threading
import queue
from typing import Optional
import json

from batch_processor import FabricBatchProcessor, ProcessingResult

class PDFProcessorGUI:
    """Simple GUI for batch PDF processing"""

    def __init__(self, root):
        self.root = root
        self.root.title("Fabric PDF Teaching Pattern Extractor")
        self.root.geometry("900x700")

        # Processing queue for thread communication
        self.message_queue = queue.Queue()
        self.is_processing = False

        # Configuration
        self.config = self.load_config()

        self.setup_ui()
        self.check_queue()

    def load_config(self) -> dict:
        """Load saved configuration"""
        config_path = Path.home() / '.config' / 'fabric' / 'batch_processor_config.json'
        if config_path.exists():
            with open(config_path) as f:
                return json.load(f)
        return {}

    def save_config(self):
        """Save configuration"""
        config_path = Path.home() / '.config' / 'fabric' / 'batch_processor_config.json'
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def setup_ui(self):
        """Setup the user interface"""

        # Configure grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(3, weight=1)

        # Title
        title_label = ttk.Label(
            self.root,
            text="📚 PDF Teaching Pattern Extractor",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, pady=10)

        # Configuration Frame
        config_frame = ttk.LabelFrame(self.root, text="Configuration", padding=10)
        config_frame.grid(row=1, column=0, padx=10, pady=5, sticky='ew')
        config_frame.columnconfigure(1, weight=1)

        # Gemini API Key
        ttk.Label(config_frame, text="Gemini API Key:").grid(row=0, column=0, sticky='w', pady=5)
        self.api_key_var = tk.StringVar(value=self.config.get('gemini_api_key', ''))
        api_key_entry = ttk.Entry(config_frame, textvariable=self.api_key_var, show='*', width=50)
        api_key_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

        ttk.Button(config_frame, text="Save", command=self.save_api_key).grid(row=0, column=2, padx=5)

        # Pattern Selection
        ttk.Label(config_frame, text="Pattern:").grid(row=1, column=0, sticky='w', pady=5)
        self.pattern_var = tk.StringVar(value=self.config.get('pattern', 'extract_teaching_content'))
        pattern_combo = ttk.Combobox(
            config_frame,
            textvariable=self.pattern_var,
            values=['extract_teaching_content', 'create_teaching_pattern'],
            state='readonly',
            width=47
        )
        pattern_combo.grid(row=1, column=1, sticky='ew', padx=5, pady=5)

        # Vision Intelligence Toggle
        self.use_vision_var = tk.BooleanVar(value=self.config.get('use_vision', True))
        vision_check = ttk.Checkbutton(
            config_frame,
            text="Enable Vision Intelligence (analyze diagrams, charts, equations)",
            variable=self.use_vision_var
        )
        vision_check.grid(row=2, column=0, columnspan=3, sticky='w', pady=5)

        # File Selection Frame
        file_frame = ttk.LabelFrame(self.root, text="Input Selection", padding=10)
        file_frame.grid(row=2, column=0, padx=10, pady=5, sticky='ew')
        file_frame.columnconfigure(1, weight=1)

        # Input path display
        ttk.Label(file_frame, text="Selected:").grid(row=0, column=0, sticky='w', pady=5)
        self.input_path_var = tk.StringVar(value="No files selected")
        input_label = ttk.Label(file_frame, textvariable=self.input_path_var, foreground='blue')
        input_label.grid(row=0, column=1, sticky='w', padx=5, pady=5)

        # Buttons
        button_frame = ttk.Frame(file_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=5)

        ttk.Button(button_frame, text="📁 Select Folder", command=self.select_folder).pack(side='left', padx=5)
        ttk.Button(button_frame, text="📄 Select Files", command=self.select_files).pack(side='left', padx=5)

        # Output directory
        ttk.Label(file_frame, text="Output:").grid(row=2, column=0, sticky='w', pady=5)
        self.output_path_var = tk.StringVar(value=self.config.get('last_output_dir', str(Path.home() / 'fabric_output')))
        output_entry = ttk.Entry(file_frame, textvariable=self.output_path_var, width=50)
        output_entry.grid(row=2, column=1, sticky='ew', padx=5, pady=5)
        ttk.Button(file_frame, text="Browse", command=self.select_output).grid(row=2, column=2, padx=5)

        # Progress Frame
        progress_frame = ttk.LabelFrame(self.root, text="Progress", padding=10)
        progress_frame.grid(row=3, column=0, padx=10, pady=5, sticky='nsew')
        progress_frame.columnconfigure(0, weight=1)
        progress_frame.rowconfigure(1, weight=1)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.grid(row=0, column=0, sticky='ew', pady=5)

        # Log output
        self.log_text = scrolledtext.ScrolledText(
            progress_frame,
            height=15,
            wrap=tk.WORD,
            font=('Courier', 9)
        )
        self.log_text.grid(row=1, column=0, sticky='nsew', pady=5)

        # Control Frame
        control_frame = ttk.Frame(self.root)
        control_frame.grid(row=4, column=0, padx=10, pady=10)

        self.process_button = ttk.Button(
            control_frame,
            text="🚀 Process PDFs",
            command=self.start_processing,
            style='Accent.TButton'
        )
        self.process_button.pack(side='left', padx=5)

        self.cancel_button = ttk.Button(
            control_frame,
            text="❌ Cancel",
            command=self.cancel_processing,
            state='disabled'
        )
        self.cancel_button.pack(side='left', padx=5)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor='w'
        )
        status_bar.grid(row=5, column=0, sticky='ew')

        # Initialize
        self.selected_path = None

    def save_api_key(self):
        """Save Gemini API key to config"""
        self.config['gemini_api_key'] = self.api_key_var.get()
        self.save_config()
        messagebox.showinfo("Success", "API key saved successfully!")

    def select_folder(self):
        """Select a folder containing PDFs"""
        folder = filedialog.askdirectory(title="Select folder containing PDFs")
        if folder:
            self.selected_path = Path(folder)
            pdf_count = len(list(self.selected_path.rglob('*.pdf')))
            self.input_path_var.set(f"{folder} ({pdf_count} PDFs found)")
            self.log(f"📁 Selected folder: {folder}")
            self.log(f"   Found {pdf_count} PDF files")

    def select_files(self):
        """Select individual PDF files"""
        files = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[("PDF files", "*.pdf")]
        )
        if files:
            # Create temporary file list
            self.selected_files = [Path(f) for f in files]
            self.selected_path = self.selected_files[0].parent  # Use first file's directory
            self.input_path_var.set(f"{len(files)} PDF files selected")
            self.log(f"📄 Selected {len(files)} PDF files")

    def select_output(self):
        """Select output directory"""
        folder = filedialog.askdirectory(title="Select output directory")
        if folder:
            self.output_path_var.set(folder)
            self.config['last_output_dir'] = folder
            self.save_config()

    def log(self, message: str):
        """Add message to log"""
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def check_queue(self):
        """Check message queue for updates from processing thread"""
        try:
            while True:
                msg = self.message_queue.get_nowait()

                if msg['type'] == 'log':
                    self.log(msg['message'])
                elif msg['type'] == 'progress':
                    self.progress_var.set(msg['value'])
                elif msg['type'] == 'status':
                    self.status_var.set(msg['message'])
                elif msg['type'] == 'complete':
                    self.processing_complete(msg['results'])
                elif msg['type'] == 'error':
                    self.processing_error(msg['error'])

        except queue.Empty:
            pass

        # Check again in 100ms
        self.root.after(100, self.check_queue)

    def start_processing(self):
        """Start processing PDFs in background thread"""
        if not self.selected_path:
            messagebox.showwarning("Warning", "Please select PDF files or folder first!")
            return

        if not self.api_key_var.get() and self.use_vision_var.get():
            response = messagebox.askyesno(
                "No API Key",
                "No Gemini API key provided. Continue with text-only extraction?"
            )
            if not response:
                return

        # Disable controls
        self.is_processing = True
        self.process_button.config(state='disabled')
        self.cancel_button.config(state='normal')

        # Clear log
        self.log_text.delete(1.0, tk.END)
        self.progress_var.set(0)

        # Start processing thread
        thread = threading.Thread(target=self.process_pdfs, daemon=True)
        thread.start()

    def process_pdfs(self):
        """Process PDFs (runs in background thread)"""
        try:
            self.message_queue.put({
                'type': 'status',
                'message': 'Processing...'
            })

            # Create processor
            processor = FabricBatchProcessor(
                gemini_api_key=self.api_key_var.get() if self.use_vision_var.get() else None,
                pattern=self.pattern_var.get(),
                use_vision=self.use_vision_var.get(),
                max_workers=3
            )

            # Get input and output paths
            input_path = self.selected_path
            output_path = Path(self.output_path_var.get())

            # Process
            self.message_queue.put({
                'type': 'log',
                'message': f'\n🚀 Starting batch processing...\n'
            })

            results = processor.process_batch(
                input_path=input_path,
                output_dir=output_path,
                parallel=True
            )

            self.message_queue.put({
                'type': 'complete',
                'results': results
            })

        except Exception as e:
            self.message_queue.put({
                'type': 'error',
                'error': str(e)
            })

    def processing_complete(self, results):
        """Handle processing completion"""
        self.is_processing = False
        self.process_button.config(state='normal')
        self.cancel_button.config(state='disabled')

        successful = sum(1 for r in results if r.success)
        total = len(results)

        self.status_var.set(f'Complete: {successful}/{total} successful')
        self.progress_var.set(100)

        messagebox.showinfo(
            "Processing Complete",
            f"Successfully processed {successful} out of {total} PDF files.\n\n"
            f"Results saved to:\n{self.output_path_var.get()}"
        )

    def processing_error(self, error: str):
        """Handle processing error"""
        self.is_processing = False
        self.process_button.config(state='normal')
        self.cancel_button.config(state='disabled')
        self.status_var.set('Error occurred')

        messagebox.showerror("Error", f"Processing failed:\n{error}")

    def cancel_processing(self):
        """Cancel processing (placeholder - actual cancellation needs implementation)"""
        messagebox.showinfo("Cancel", "Processing will stop after current file completes")

def main():
    """Main entry point"""
    root = tk.Tk()

    # Set style
    style = ttk.Style()
    style.theme_use('clam')

    app = PDFProcessorGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
