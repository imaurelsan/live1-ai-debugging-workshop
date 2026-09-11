# N1 · Exercice 3 — La regex

## L'énoncé

Les références produit suivent ce format :

```
PP-AAAA-NNNNN-V
```

| Champ | Règle |
|---|---|
| `PP` | deux lettres **majuscules** |
| `AAAA` | année sur 4 chiffres, entre **2015 et 2030** |
| `NNNNN` | séquence sur **exactement** 5 chiffres |
| `V` | **une seule** lettre majuscule |

Écris une regex qui valide une référence. Puis une seconde qui les **extrait**
d'un texte libre. Ce ne sont pas les mêmes.

## Ce qu'on te donne

`references.txt` — un cas par ligne, regroupés par famille, commentés.

## La consigne de prompting

Deux temps, dans cet ordre :

1. Demande la regex **et l'explication de chaque groupe**. Si tu ne peux pas
   expliquer chaque morceau, tu ne peux pas la maintenir.
2. Demande à l'IA de **casser sa propre regex** : « trouve-moi trois chaînes qui
   passent alors qu'elles ne devraient pas ». C'est le moment le plus utile de
   l'exercice.

## Les pièges du fichier

- Casse : `fr-2026-00412-a`, `Fr-2026-00412-A`
- Longueurs : 4 chiffres au lieu de 5, code pays à 1 ou 3 lettres, variante à 2 lettres
- Bornes d'année : `1899`, `2014`, `2031` — la contrainte 2015-2030 ne se fait pas
  avec `\d{4}`
- Séparateurs : `/`, `_`, espace, tiret cadratin
- Caractères qui se ressemblent : `O` majuscule au lieu de `0`
- **Faux positifs sans ancrage** : `XFR-2026-00412-AX` passe si ta regex n'a ni
  `^$` ni `\b`
- Unicode : chiffres arabes-indiens `٢٠٢٦` — `\d` les matche en Python
- Espace insécable et espace de largeur nulle en fin de ligne

## Réussi si…

- Tu peux expliquer chaque groupe de ta regex à voix haute
- Tu as trouvé **au moins un faux positif** que ta première version laissait passer
- Tu as compris pourquoi validation et extraction demandent deux regex différentes
- Tu sais ce que `\d` matche vraiment en Python
