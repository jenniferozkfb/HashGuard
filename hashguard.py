import tkinter as tk
from tkinter import filedialog, messagebox
import hashlib

class HashGuard:
    def __init__(self, root):
        self.root = root
        self.root.title("HashGuard - File Integrity Checker")
        self.root.geometry("500x400")

        # File selection label
        self.file_label = tk.Label(root, text="Selected File: None", wraplength=400)
        self.file_label.pack(pady=10)

        # Select file button
        self.select_file_button = tk.Button(root, text="Select File", command=self.select_file)
        self.select_file_button.pack(pady=5)

        # Algorithm selection
        self.algorithm_label = tk.Label(root, text="Choose Hash Algorithm:")
        self.algorithm_label.pack(pady=5)
        self.algorithm_var = tk.StringVar(value="sha256")
        self.algorithm_menu = tk.OptionMenu(root, self.algorithm_var, "md5", "sha1", "sha256")
        self.algorithm_menu.pack(pady=5)

        # Hash generation
        self.generate_hash_button = tk.Button(root, text="Generate Hash", command=self.generate_hash)
        self.generate_hash_button.pack(pady=5)

        # Display hash result
        self.hash_result_label = tk.Label(root, text="Generated Hash: None", wraplength=400)
        self.hash_result_label.pack(pady=10)

        # Reference hash input
        self.ref_hash_label = tk.Label(root, text="Enter Reference Hash:")
        self.ref_hash_label.pack(pady=5)
        self.ref_hash_entry = tk.Entry(root, width=50)
        self.ref_hash_entry.pack(pady=5)

        # Compare hashes button
        self.compare_button = tk.Button(root, text="Compare Hashes", command=self.compare_hashes)
        self.compare_button.pack(pady=5)

        # Comparison result
        self.comparison_result_label = tk.Label(root, text="Comparison Result: None", wraplength=400)
        self.comparison_result_label.pack(pady=10)

    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.file_label.config(text=f"Selected File: {self.file_path}")
        else:
            self.file_label.config(text="Selected File: None")

    def generate_hash(self):
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("Error", "Please select a file first.")
            return

        algorithm = self.algorithm_var.get()
        try:
            hasher = hashlib.new(algorithm)
            with open(self.file_path, 'rb') as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
            file_hash = hasher.hexdigest()
            self.hash_result_label.config(text=f"Generated Hash ({algorithm}): {file_hash}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating the hash: {e}")

    def compare_hashes(self):
        generated_hash = self.hash_result_label.cget("text").split(": ")[-1]
        reference_hash = self.ref_hash_entry.get().strip()

        if "None" in generated_hash:
            messagebox.showerror("Error", "Please generate a hash first.")
            return

        if not reference_hash:
            messagebox.showerror("Error", "Please enter a reference hash.")
            return

        if generated_hash == reference_hash:
            self.comparison_result_label.config(text="Comparison Result: Hashes match!", fg="green")
        else:
            self.comparison_result_label.config(text="Comparison Result: Hashes do not match.", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = HashGuard(root)
    root.mainloop()
