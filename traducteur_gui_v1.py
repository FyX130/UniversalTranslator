import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
from gtts import gTTS
import pygame
import json
import os
import tempfile

HISTORY_FILE = "translation_history.json"

class TranslatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Traducteur Universel")
        self.root.geometry("800x600")
        self.history = []

        self.load_history()
        self.setup_widgets()

    def setup_widgets(self):
        # Onglets
        self.tab_control = ttk.Notebook(self.root)

        # Tab Traduction
        self.tab_translate = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_translate, text='Traduction')

        # Tab Historique
        self.tab_history = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_history, text='Historique')

        self.tab_control.pack(expand=1, fill="both")

        # Widgets de la tab Traduction
        self.text_input = tk.Text(self.tab_translate, height=6)
        self.text_input.pack(fill="x", padx=10, pady=10)

        options_frame = ttk.Frame(self.tab_translate)
        options_frame.pack(fill="x", padx=10)

        ttk.Label(options_frame, text="Langue source :").grid(row=0, column=0)
        self.source_lang = ttk.Combobox(options_frame, values=self.get_languages())
        self.source_lang.set("auto")
        self.source_lang.grid(row=0, column=1)

        ttk.Label(options_frame, text="Langue cible :").grid(row=0, column=2)
        self.target_lang = ttk.Combobox(options_frame, values=self.get_languages())
        self.target_lang.set("en")
        self.target_lang.grid(row=0, column=3)

        ttk.Label(options_frame, text="Style :").grid(row=1, column=0)
        self.style = ttk.Combobox(options_frame, values=[
            "neutre", "formel", "familier", "humour", "piquant", "sérieux", "poétique", "sarcastique", "émotionnel"
        ])
        self.style.set("neutre")
        self.style.grid(row=1, column=1)

        ttk.Label(options_frame, text="Formalité :").grid(row=2, column=0)
        self.formality = ttk.Scale(options_frame, from_=0, to=4, orient='horizontal')
        self.formality.grid(row=2, column=1)

        ttk.Label(options_frame, text="Émotion :").grid(row=2, column=2)
        self.emotion = ttk.Scale(options_frame, from_=-1, to=1, orient='horizontal')
        self.emotion.grid(row=2, column=3)

        control_frame = ttk.Frame(self.tab_translate)
        control_frame.pack(pady=10)

        ttk.Button(control_frame, text="Traduire", command=self.translate).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Lire", command=self.read_translation).grid(row=0, column=1, padx=5)

        self.result_output = tk.Text(self.tab_translate, height=6)
        self.result_output.pack(fill="x", padx=10, pady=10)

        # Historique
        self.history_listbox = tk.Listbox(self.tab_history)
        self.history_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.update_history_display()

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

            # Préformatage simple selon style
            if style == "humour":
                translated += " 😄"
            elif style == "piquant":
                translated += " 🔥"
            elif style == "formel":
                translated = "Veuillez noter que : " + translated
            elif style == "familier":
                translated = "Tu sais quoi ? " + translated
            elif style == "poétique":
                translated = "🌸 " + translated + " 🌙"
            elif style == "sarcastique":
                translated = "Oh, vraiment ? " + translated
            elif style == "émotionnel":
                emotion_val = self.emotion.get()
                if emotion_val > 0.5:
                    translated = "Quelle joie ! " + translated
                elif emotion_val < -0.5:
                    translated = "Quel malheur... " + translated

            self.result_output.delete("1.0", tk.END)
            self.result_output.insert(tk.END, translated)

            # Ajout à l’historique
            self.history.append({
                "source": original_text,
                "result": translated,
                "source_lang": source,
                "target_lang": target,
                "style": style
            })
            self.save_history()
            self.update_history_display()

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")

    def read_translation(self):
        text = self.result_output.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Attention", "Aucun texte à lire.")
            return
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_path = fp.name
                tts = gTTS(text=text, lang=self.target_lang.get())
                tts.save(temp_path)

            pygame.mixer.init()
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            pygame.mixer.music.stop()
            pygame.mixer.quit()
            os.remove(temp_path)
        except Exception as e:
            messagebox.showerror("Erreur audio", f"Impossible de lire l'audio : {e}")

    def save_history(self):
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("Erreur de sauvegarde historique :", e)

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    self.history = json.load(f)
            except:
                self.history = []

    def update_history_display(self):
        self.history_listbox.delete(0, tk.END)
        for item in self.history[::-1]:
            try:
                display = f"{item['source'][:30]}... => {item['result'][:30]}..."
                self.history_listbox.insert(tk.END, display)
            except:
                continue

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorGUI(root)
    root.mainloop()
