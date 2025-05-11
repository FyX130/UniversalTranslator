# 🧾 CHANGELOG - Traducteur GUI V1

## [1.1.0] - 2025-05-10
### Ajouté
- Interface graphique (GUI) de base avec Tkinter
- Sélecteurs de langue, style, humeur et champ de texte
- Bouton de traduction et affichage du résultat

## [1.0.1] - 2025-05-09
### Corrigé
- Gestion des erreurs si le texte est vide
- Correction du comportement de `:` mal placé
- Nettoyage du parsing des arguments
- Traductions plus stables en cas d'entrée complexe

## [1.0.0] - 2025-05-08
### Ajouté
- Fonction de traduction CLI `-t`
- Argument `-langue` (langue cible)
- Support des styles (`-style`) : formel, familier, soutenu...
- Support des humeurs (`-humeur`) : neutre, piquant, dramatique...
- Commande `-t --help` pour afficher toutes les options
- Générateur de prompt intelligent avec structure en `:` pour détecter le texte
