# N1 · Exercice 2 — Le parsing

## L'énoncé

`app.log` est un journal applicatif au format maison. Sors le **nombre d'erreurs
par heure**.

Une erreur = niveau `ERROR` ou `FATAL`.

## Le format

```
2026-09-11T11:04:12|INFO |api-gateway|req=a71c3e04|Requete traitee en 142ms
horodatage         |niv  |service    |requête   |message
```

Cinq champs séparés par des `|`. Enfin, en théorie.

## Ce qu'on te donne

| Fichier | Contenu |
|---|---|
| `app.log` | 847 lignes, de 11h à 18h |
| `extrait-3-lignes.log` | trois lignes propres |

## La consigne de prompting

**Ne décris pas le format à l'IA. Donne-lui `extrait-3-lignes.log`.**

C'est du few-shot : trois exemples valent mieux qu'un paragraphe de description.
Compare avec ce que tu obtiens en décrivant le format en mots — c'est la vraie
leçon de l'exercice.

## Les questions qui vont se poser

Le fichier contient une dizaine de lignes qui ne rentrent pas dans le moule :

- une ligne vide
- une ligne tronquée à trois champs
- un message qui contient lui-même un `|` — un `split("|")` naïf casse dessus
- une stack trace sur quatre lignes, les continuations sont indentées
- un horodatage au format epoch
- un niveau inconnu (`CRIT`)
- un niveau en minuscules
- un niveau entouré d'espaces
- une ligne du jour précédent
- un message vide
- une ligne dupliquée à l'identique
- une ligne séparée par des tabulations
- des accents dans un message

Aucune ne doit faire planter ton script. Toutes doivent faire l'objet d'une décision.

## Réussi si…

- Le script ne plante sur aucune ligne
- Tu peux dire combien de lignes ont été écartées, et pourquoi
- Tu repères le pic horaire (il est net, c'est un incident)
- Tu as testé en cassant volontairement une ligne de plus
