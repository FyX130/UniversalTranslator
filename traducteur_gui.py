import tkinter as tk
from tkinter import ttk
from deep_translator import GoogleTranslator

STYLE_VARIANTS = {
    'humour': {
        'léger': lambda t: t + " (juste pour rire !)",
        'piquant': lambda t: "Oh là là ! " + t.replace("?", "?!") + " (c'est osé !)"
    },
    'formel': {
        'juridique': lambda t: "Conformément à l'article 1 : " + t,
        'académique': lambda t: "Selon les dernières recherches : " + t
    }
}

TONE_VARIANTS = {
    'professionnel': {
        'sec': lambda t: t + ". Merci.",
        'empathique': lambda t: "Nous comprenons parfaitement. " + t
    },
    'joyeux': {
        'enthousiaste': lambda t: t + " C’est génial !",
        'bienveillant': lambda t: "Pas d'inquiétude ! " + t
    }
}

def apply_variant(text, category, option, table):
    if category in table and option in table[category]:
        return table[category][option](text)
    return text

def change_caps(text, caps):
    if caps == 'upper':
        return text.upper()
    elif caps == 'lower':
        return text.lower()
    elif caps == 'capitalize':
        return text.capitalize()
    return text

def translate():
    src = source_lang.get()
    tgt = target_lang.get()
    text = input_text.get("1.0", tk.END).strip()

    if not text:
        result_text.set("Veuillez entrer un texte.")
        return

    try:
        translated = GoogleTranslator(source=src, target=tgt).translate(text)

        if style_cat.get() and style_opt.get():
            translated = apply_variant(translated, style_cat.get(), style_opt.get(), STYLE_VARIANTS)

        if tone_cat.get() and tone_opt.get():
            translated = apply_variant(translated, tone_cat.get(), tone_opt.get(), TONE_VARIANTS)

        if emoji_var.get():
            translated += " 😊"

        translated = change_caps(translated, caps.get())
        result_text.set(translated)
    except Exception as e:
        result_text.set(f"Erreur : {e}")

# Fenêtre principale
root = tk.Tk()
root.title("Traducteur Universel")

# Champs de saisie
tk.Label(root, text="Texte à traduire :").grid(row=0, column=0, sticky="w")
input_text = tk.Text(root, height=5, width=50)
input_text.grid(row=1, column=0, columnspan=3)

# Langues
source_lang = tk.StringVar(value="fr")
target_lang = tk.StringVar(value="en")

tk.Label(root, text="Langue source :").grid(row=2, column=0, sticky="w")
tk.Entry(root, textvariable=source_lang, width=10).grid(row=2, column=1, sticky="w")
tk.Label(root, text="Langue cible :").grid(row=2, column=2, sticky="w")
tk.Entry(root, textvariable=target_lang, width=10).grid(row=2, column=3, sticky="w")

# Style
style_cat = tk.StringVar()
style_opt = tk.StringVar()

tk.Label(root, text="Style (catégorie:option) :").grid(row=3, column=0, sticky="w")
ttk.Combobox(root, textvariable=style_cat, values=list(STYLE_VARIANTS.keys())).grid(row=3, column=1)
ttk.Combobox(root, textvariable=style_opt, values=["léger", "piquant", "juridique", "académique"]).grid(row=3, column=2)

# Ton
tone_cat = tk.StringVar()
tone_opt = tk.StringVar()

tk.Label(root, text="Ton (catégorie:option) :").grid(row=4, column=0, sticky="w")
ttk.Combobox(root, textvariable=tone_cat, values=list(TONE_VARIANTS.keys())).grid(row=4, column=1)
ttk.Combobox(root, textvariable=tone_opt, values=["sec", "empathique", "enthousiaste", "bienveillant"]).grid(row=4, column=2)

# Autres options
caps = tk.StringVar(value="original")
tk.Label(root, text="Majuscules :").grid(row=5, column=0, sticky="w")
ttk.Combobox(root, textvariable=caps, values=["original", "upper", "lower", "capitalize"]).grid(row=5, column=1)

emoji_var = tk.BooleanVar()
tk.Checkbutton(root, text="Ajouter emoji 😊", variable=emoji_var).grid(row=5, column=2)

# Bouton Traduire
tk.Button(root, text="Traduire", command=translate).grid(row=6, column=1)

# Résultat
result_text = tk.StringVar()
tk.Label(root, text="Résultat :").grid(row=7, column=0, sticky="w")
tk.Label(root, textvariable=result_text, wraplength=400, justify="left", bg="white", anchor="nw", relief="sunken", height=5).grid(row=8, column=0, columnspan=4, sticky="we")

root.mainloop()
