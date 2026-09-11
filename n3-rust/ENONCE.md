# N3 · Porter un algo Python vers Rust

## L'énoncé

`dijkstra.py` calcule le plus court chemin dans un réseau de transport. Porte-le
en **Rust idiomatique**.

Pas en Python déguisé. C'est toute la difficulté.

## Ce qu'on te donne

| Fichier | Contenu |
|---|---|
| `dijkstra.py` | la source, volontairement très pythonique |
| `reseau.json` | 20 stations, 28 arêtes |
| `reseau-degrade.json` | même réseau + composante isolée + arête de poids négatif |

## Pourquoi cet exercice

L'IA connaît très bien les deux langages. Elle traduit quand même ligne à ligne,
parce que c'est ce que la consigne « porte ce code » suggère statistiquement.

Le résultat compile rarement du premier coup, et quand il compile, il n'est pas
idiomatique. C'est exactement ce qu'on veut observer.

## Sortie de référence

```
A1 -> F2  28 min : Gare Centrale -> Marche -> Universite -> Parc Nord
                   -> Quartier Latin -> Colline -> Belvedere
B3 -> E1  5 min  : Parc Nord -> Quartier Latin
A1 -> Z9  Aucun itineraire.
D2 -> D2  0 min  : Terminus Ouest
```

Ton portage doit produire les mêmes résultats.

## Où l'IA va te mentir

| Piège | Ce que tu verras |
|---|---|
| Ownership et emprunts | `.clone()` partout pour faire taire le compilateur |
| `unwrap()` | port direct des exceptions Python, y compris sur le chemin nominal |
| Durées de vie | annotations inventées qui ne compilent pas |
| `Option` / `Result` | confondus, ou mélangés dans la même fonction |
| Boucles `for` | là où un itérateur serait idiomatique |
| Crates hallucinées | vérifie **chaque** nom sur crates.io |
| `BinaryHeap` | c'est un tas **max** en Rust, pas un tas min comme `heapq` |
| `f64` dans le tas | `f64` n'implémente pas `Ord`. Le portage naïf ne compile pas |
| `defaultdict` | n'existe pas. `entry().or_default()` est l'équivalent |

Les deux dernières lignes sont les plus intéressantes : ce sont des différences
**structurelles** entre les deux langages, pas des questions de syntaxe. Une
traduction ligne à ligne ne peut pas les résoudre.

## Cas limites du réseau

- Une arête de poids `0` entre `E2` et `E1`
- Deux arêtes `A1 -> A2` de poids différents — le plus court doit gagner
- Deux arêtes à sens unique (`C2 -> G1`, `G1 -> G2`) — le portage doit les conserver
- Départ = arrivée
- Station inconnue au départ (erreur) vs à l'arrivée (pas de chemin) — ce ne sont
  pas les mêmes cas, et le Python les traite différemment
- `reseau-degrade.json` contient une arête de poids négatif. Dijkstra n'est pas
  fait pour ça. Que fait ton code ?

## Réussi si…

- `cargo build` passe
- Aucun `unwrap()` dans le chemin nominal
- Les erreurs passent par `Result`, pas par des `panic!`
- `cargo clippy` ne dit rien
- La sortie correspond à la référence
- Tu peux expliquer pourquoi ton portage n'est pas une traduction ligne à ligne
