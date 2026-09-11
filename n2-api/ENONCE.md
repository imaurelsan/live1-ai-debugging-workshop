# N2 · Mini API REST

## L'énoncé

Une API de gestion de tâches. FastAPI ou Express, au choix. Stockage en mémoire,
pas de base de données.

## La spec

| Méthode | Route | Renvoie |
|---|---|---|
| `GET` | `/taches` | 200 + tableau (vide = 200, pas 404) |
| `GET` | `/taches/{id}` | 200, ou 404 si inconnu |
| `POST` | `/taches` | 201 + la tâche créée, ou 400 |
| `PATCH` | `/taches/{id}` | 200 + la tâche à jour, ou 400 / 404 |
| `DELETE` | `/taches/{id}` | 204, ou 404 |

**Modèle**

```json
{
  "id": 1,
  "titre": "string, 1 à 200 caractères, non vide après trim",
  "description": "string, optionnel, 0 à 1000 caractères",
  "statut": "a_faire | en_cours | terminee",
  "priorite": 1 | 2 | 3,
  "creee_le": "ISO 8601, généré par le serveur",
  "etiquettes": ["string"]
}
```

**Règles non négociables**

- L'`id` est généré par le serveur. Un `id` envoyé par le client est ignoré.
- Aucune stack trace ne sort de l'API. Jamais.
- Un test par endpoint, écrit **avant** de passer au suivant.

## Ce qu'on te donne

| Fichier | Contenu |
|---|---|
| `taches-seed.json` | 16 tâches pour amorcer |
| `payloads-invalides.json` | 12 corps de requête que ton API doit rejeter proprement |

Chaque payload invalide porte un champ `_pourquoi` qui dit ce qui cloche. Ton API
doit renvoyer un 400 explicite sur chacun, sans planter.

## La méthode, dans cet ordre

1. **Écris ta spec** avant d'ouvrir le chat. Cinq lignes suffisent.
2. **Demande le plan, pas le code.** Tu valides, ensuite il code.
3. **Un endpoint à la fois.** Généré, lu, testé. Puis le suivant.
4. **Commit à chaque endpoint qui marche.**

La tentation sera de demander l'API complète en un prompt. Essaie, regarde le
diff, et compte les fichiers touchés. C'est instructif.

## Les pièges des payloads

Titre vide, titre absent, titre de 512 caractères, titre en espaces uniquement,
statut inconnu, priorité hors bornes, priorité en chaîne, champ inconnu en plus,
`id` imposé par le client, balise `<script>` dans le titre, `etiquettes` qui n'est
pas un tableau, corps vide.

Regarde en particulier ce que l'IA fait du champ inconnu et du `<script>`. Par
défaut, beaucoup de code généré accepte l'un et stocke l'autre tel quel.

## Réussi si…

- Les 5 endpoints répondent avec les bons codes
- Les 12 payloads invalides renvoient un 400 avec un message utile
- Aucune stack trace dans une réponse
- Un test par endpoint, et ils passent
- Ton historique Git montre un commit par endpoint
