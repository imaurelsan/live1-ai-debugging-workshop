# Live 1 — Jeux de données des ateliers

Trois niveaux, cinq jeux de données. Chaque dossier contient les fichiers et un
`ENONCE.md` avec la consigne, les pièges attendus et les critères de réussite.

| Dossier | Niveau | Exercice |
|---|---|---|
| `n1-tri/` | N1 | Tri multi-critères sur données sales |
| `n1-parsing/` | N1 | Extraction depuis un log au format maison |
| `n1-regex/` | N1 | Validation et extraction de références produit |
| `n2-api/` | N2 | Mini API REST de gestion de tâches |
| `n3-rust/` | N3 | Portage d'un Dijkstra Python vers Rust |

## Le principe

Ces jeux de données ne sont pas propres. Chaque fichier contient des cas limites
placés volontairement : valeurs nulles, doublons, encodages exotiques, lignes
malformées, faux positifs.

C'est le cœur de l'exercice. Une IA qui reçoit une consigne vague produit du code
qui marche sur les données nominales et casse sur le reste. L'objectif du live
n'est pas de faire tourner un script, c'est de voir **où** ça casse et **pourquoi**.

## Règle commune aux trois niveaux

1. `git init` et premier commit avant de lancer quoi que ce soit.
2. Tu lis le diff avant d'accepter. Toujours.
3. Tout nom que l'IA te sort — méthode, paquet, option — se vérifie dans la doc.

## Ce qu'on attend en restitution

Pas un code qui marche. Une réponse à ces quatre questions :

- Quel prompt t'a débloqué ?
- Où l'IA t'a menti ?
- Qu'as-tu accepté sans lire ?
- Temps gagné, ou temps perdu ?

## Note

Les données sont entièrement fictives et générées pour l'exercice. Aucune n'est
issue d'un système réel.

Le fichier `CORRECTION-animateur.md` contient les résultats de référence et la
liste complète des pièges. À ne pas distribuer aux participants avant la
restitution.
