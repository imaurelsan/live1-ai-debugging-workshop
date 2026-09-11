# N1 · Exercice 1 — Le tri

## L'énoncé

`etudiants.json` contient une promotion. Trie-la sur **deux critères** :

1. note **décroissante**
2. à note égale, nom **croissant** (A → Z)

Affiche le classement. C'est tout.

## Ce qu'on te donne

| Fichier | Contenu |
|---|---|
| `etudiants.json` | 68 entrées, dont une quinzaine de cas limites |
| `etudiants-vide.json` | tableau vide |
| `etudiants-un-seul.json` | une seule entrée |

## Les questions qui vont se poser

Le fichier n'est pas propre. Tu vas devoir **décider**, pas deviner :

- Certaines entrées n'ont pas de note exploitable. Elles sortent du classement,
  ou elles vont à la fin ? Ton code doit-il planter, ou les ignorer en silence ?
- Une note est stockée en chaîne de caractères. Tu la convertis, ou tu la rejettes ?
- Une note vaut `21.5`. Le barème est sur 20.
- Il y a des accents dans les noms. `Écuyer` se trie-t-il avant ou après `Espinosa` ?
  Réponse courte : ça dépend de la locale, et le tri par défaut te donnera quelque
  chose de faux si tu n'y penses pas.
- `de Souza` et `De Souza` sont deux personnes différentes. Le tri par défaut met
  les majuscules avant les minuscules.
- Un nom est vide.
- Une entrée est un doublon strict.

## Ce que tu demandes à l'IA

Commence **sans** lui parler des cas limites. Regarde ce qu'elle produit.
Puis regarde ce qui casse. Puis re-prompte.

C'est l'exercice : mesurer l'écart entre la première réponse et la réponse utilisable.

## Réussi si…

- Tu sais expliquer la complexité de ta solution
- Le tri est **stable** (à note et nom égaux, l'ordre d'entrée est conservé)
- Liste vide et liste à un élément passent sans cas particulier dans le code
- Tu as pris une décision **explicite** sur chaque cas limite, et tu peux la défendre
