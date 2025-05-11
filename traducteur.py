import argparse
from deep_translator import GoogleTranslator

# Sous-styles et tons personnalisés
STYLE_VARIANTS = {
    'humour': {
        'léger': lambda t: t + " (juste pour rire !)",
        'piquant': lambda t: "Oh là là ! " + t.replace("?", "?!") + " (c'est osé !)",
        'absurde': lambda t: t + " avec une licorne en costume.",
        'noir': lambda t: t + " (mais vous ne dormirez plus ensuite...)"
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

def apply_variant(text, category, option):
    if category in STYLE_VARIANTS and option in STYLE_VARIANTS[category]:
        return STYLE_VARIANTS[category][option](text)
    if category in TONE_VARIANTS and option in TONE_VARIANTS[category]:
        return TONE_VARIANTS[category][option](text)
    return text

def change_caps(text, caps):
    if caps == 'upper':
        return text.upper()
    elif caps == 'lower':
        return text.lower()
    elif caps == 'capitalize':
        return text.capitalize()
    return text

def main():
    parser = argparse.ArgumentParser(description="Traducteur universel", add_help=False)
    parser.add_argument('-t', action='store_true', help='Activer la traduction')
    parser.add_argument('-from', dest='source_lang', default='auto', help='Langue source (ex: fr)')
    parser.add_argument('-to', '-en', dest='to', default='en', help='Langue cible (ex: en)')
    parser.add_argument('-style', help='Style:option (ex: humour:piquant)')
    parser.add_argument('-tone', help='Tone:option (ex: professionnel:sec)')
    parser.add_argument('-emoji', choices=['on', 'off'], help='Ajoute ou retire les emojis')
    parser.add_argument('-caps', choices=['upper', 'lower', 'capitalize', 'original'], default='original')
    parser.add_argument('--help', action='store_true')
    parser.add_argument('text', nargs='*')

    args = parser.parse_args()

    if args.help or not args.text:
        print("""USAGE :
  -t                        : Traduction
  -from fr                 : Langue source
  -to de                   : Langue cible
  -style humour:piquant    : Style (catégorie:sous-option)
  -tone professionnel:sec  : Ton (catégorie:sous-option)
  -emoji on/off            : Emojis
  -caps capitalize          : Majuscules
  : Texte à traduire       : Suivi des options
        """)
        return

    full_text = " ".join(args.text)
    translated = GoogleTranslator(source=args.source_lang, target=args.to).translate(full_text)

    # Application des sous-options
    if args.style and ':' in args.style:
        cat, opt = args.style.split(':', 1)
        translated = apply_variant(translated, cat, opt)

    if args.tone and ':' in args.tone:
        cat, opt = args.tone.split(':', 1)
        translated = apply_variant(translated, cat, opt)

    if args.emoji == 'on':
        translated += " 😊"
    elif args.emoji == 'off':
        for em in ['😊', '🙂', '😂', '😢']:
            translated = translated.replace(em, '')

    translated = change_caps(translated, args.caps)
    print(translated)

if __name__ == "__main__":
    main()
