import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import json
import tempfile

class TranslatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Traducteur Universel")
        self.root.geometry("800x600")

        self.history = []
        self.history_file = "translation_history.json"
        self.load_history()

        self.setup_widgets()

    def setup_widgets(self):
        notebook = ttk.Notebook(self.root)
        self.main_frame = ttk.Frame(notebook)
        self.history_frame = ttk.Frame(notebook)
        notebook.add(self.main_frame, text="Traduction")
        notebook.add(self.history_frame, text="Historique")
        notebook.pack(fill="both", expand=True)

        # Zone de saisie
        self.text_input = tk.Text(self.main_frame, height=8)
        self.text_input.pack(fill="x", padx=10, pady=10)

        # Options
        options_frame = ttk.Frame(self.main_frame)
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

        # Curseur de formalité
        ttk.Label(options_frame, text="Formalité :").grid(row=2, column=0, padx=5, pady=5)
        self.formality = ttk.Scale(options_frame, from_=0, to=4, orient="horizontal")
        self.formality.grid(row=2, column=1, padx=5, pady=5)

        # Curseur émotionnel
        ttk.Label(options_frame, text="Émotion :").grid(row=2, column=2, padx=5, pady=5)
        self.emotion = ttk.Scale(options_frame, from_=-1, to=1, orient="horizontal")
        self.emotion.grid(row=2, column=3, padx=5, pady=5)

        # Boutons
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Traduire", command=self.translate).grid(row=0, column=0, padx=10)
        ttk.Button(btn_frame, text="Lire", command=self.read_translation).grid(row=0, column=1, padx=10)

        # Résultat
        self.result_output = tk.Text(self.main_frame, height=8)
        self.result_output.pack(fill="x", padx=10, pady=10)

        # Historique
        self.history_listbox = tk.Listbox(self.history_frame)
        self.history_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.update_history_display()

    def get_languages(self):
        return ["auto", "fr", "en", "de", "es", "it", "pt", "nl", "pl", "ru", "ja", "zh"]

    def translate(self):
        original_text = self.text_input.get("1.0", tk.END).strip()
        source = self.source_lang.get()
        target = self.target_lang.get()
        style = self.style.get()

        formality_levels = ["très formel", "formel", "neutre", "informel", "très informel"]
        formality_text = formality_levels[int(self.formality.get())]

        emotion_level = float(self.emotion.get())
        if emotion_level < -0.3:
            emotion_text = "négatif"
        elif emotion_level > 0.3:
            emotion_text = "positif"
        else:
            emotion_text = "neutre"

        if not original_text:
            messagebox.showwarning("Attention", "Veuillez entrer un texte à traduire.")
            return

        try:
            translated = GoogleTranslator(source=source, target=target).translate(original_text)
            translated = f"[{style} | {formality_text} | {emotion_text}] {translated}"

            self.result_output.delete("1.0", tk.END)
            self.result_output.insert(tk.END, translated)

            self.save_to_history(original_text, translated)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

    def save_to_history(self, source, result):
        self.history.append({"source": source, "result": result})
        with open(self.history_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
        self.update_history_display()

    def update_history_display(self):
        self.history_listbox.delete(0, tk.END)
        for item in self.history:
            display = f"{item['source'][:30]}... => {item['result'][:30]}..."
            self.history_listbox.insert(tk.END, display)

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r", encoding="utf-8") as f:
                self.history = json.load(f)

    def read_translation(self):
        text = self.result_output.get("1.0", tk.END).strip()
        if not text:
            messagebox.showinfo("Info", "Aucune traduction à lire.")
            return
        try:
            tts = gTTS(text=text, lang=self.target_lang.get())
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(temp_audio.name)
            os.system(f'start {temp_audio.name}')  # Windows only. For Linux/Mac, replace accordingly.
        except Exception as e:
            messagebox.showerror("Erreur audio", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorGUI(root)
    root.mainloop()
