# Vérification de la disponibilité de tkinter
try:
    import tkinter as tk
    from tkinter import ttk, messagebox
except ModuleNotFoundError:
    print("Erreur : le module 'tkinter' n'est pas disponible dans cet environnement.")
    exit(1)

from deep_translator import GoogleTranslator

class TranslatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Traducteur Universel")
        self.root.geometry("600x400")

        self.setup_widgets()

    def setup_widgets(self):
        self.text_input = tk.Text(self.root, height=8)
        self.text_input.pack(fill="x", padx=10, pady=10)

        options_frame = ttk.Frame(self.root)
        options_frame.pack(fill="x", padx=10)

        ttk.Label(options_frame, text="Langue source :").grid(row=0, column=0, padx=5, pady=5)
        self.source_lang = ttk.Combobox(options_frame, values=self.get_languages())
        self.source_lang.set("auto")
        self.source_lang.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(options_frame, text="Langue cible :").grid(row=0, column=2, padx=5, pady=5)
        self.target_lang = ttk.Combobox(options_frame, values=self.get_languages())
        self.target_lang.set("en")
        self.target_lang.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(options_frame, text="Style :").grid(row=1, column=0, padx=5, pady=5)
        self.style = ttk.Combobox(options_frame, values=["neutre", "formel", "familier", "humour", "piquant"])
        self.style.set("neutre")
        self.style.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.root, text="Traduire", command=self.translate).pack(pady=10)

        self.result_output = tk.Text(self.root, height=8)
        self.result_output.pack(fill="x", padx=10, pady=10)

    def get_languages(self):
        return ["auto", "fr", "en", "de", "es", "it", "pt", "nl", "pl", "ru", "ja", "zh"]

    def translate(self):
        original_text = self.text_input.get("1.0", tk.END).strip()
        source = self.source_lang.get()
        target = self.target_lang.get()
        style = self.style.get()

        if not original_text:
            messagebox.showwarning("Attention", "Veuillez entrer un texte à traduire.")
            return

        try:
            translated = GoogleTranslator(source=source, target=target).translate(original_text)
            if style == "humour":
                translated += " 😄"
            elif style == "piquant":
                translated += " 🔥"
            elif style == "formel":
                translated = "Veuillez noter que : " + translated
            elif style == "familier":
                translated = "Tu sais quoi ? " + translated

            self.result_output.delete("1.0", tk.END)
            self.result_output.insert(tk.END, translated)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorGUI(root)
    root.mainloop()
