"""
Plus court chemin dans un reseau de transport, par Dijkstra.

Ce code est volontairement tres "pythonique" : dictionnaires partout,
exceptions pour les cas d'erreur, retours None, typage implicite,
et quelques raccourcis qui n'ont pas d'equivalent direct en Rust.

C'est le point de depart de l'exercice N3. Le but n'est pas de le
traduire ligne a ligne, mais de le reecrire en Rust idiomatique.
"""

import heapq
import json
from collections import defaultdict


class ReseauIntrouvable(Exception):
    pass


class StationInconnue(Exception):
    def __init__(self, nom):
        super().__init__("Station inconnue : %s" % nom)
        self.nom = nom


def charger_reseau(chemin):
    """Charge le reseau et construit la liste d'adjacence."""
    try:
        with open(chemin, encoding="utf-8") as f:
            brut = json.load(f)
    except FileNotFoundError:
        raise ReseauIntrouvable(chemin)

    graphe = defaultdict(list)
    for arete in brut["aretes"]:
        a, b, duree = arete["de"], arete["vers"], arete["duree_min"]
        graphe[a].append((b, duree))
        if not arete.get("sens_unique", False):
            graphe[b].append((a, duree))

    return graphe, brut["stations"]


def plus_court_chemin(graphe, depart, arrivee):
    """Renvoie (duree_totale, [stations]) ou None s'il n'y a pas de chemin."""
    if depart not in graphe:
        raise StationInconnue(depart)

    distances = {depart: 0}
    precedent = {}
    visites = set()
    file = [(0, depart)]

    while file:
        d, courant = heapq.heappop(file)
        if courant in visites:
            continue
        visites.add(courant)

        if courant == arrivee:
            chemin = []
            noeud = arrivee
            while noeud is not None:
                chemin.append(noeud)
                noeud = precedent.get(noeud)
            return d, list(reversed(chemin))

        for voisin, poids in graphe[courant]:
            if voisin in visites:
                continue
            nouvelle = d + poids
            if nouvelle < distances.get(voisin, float("inf")):
                distances[voisin] = nouvelle
                precedent[voisin] = courant
                heapq.heappush(file, (nouvelle, voisin))

    return None


def formater(resultat, stations):
    if resultat is None:
        return "Aucun itineraire."
    duree, chemin = resultat
    noms = [stations.get(code, code) for code in chemin]
    return "%d min : %s" % (duree, " -> ".join(noms))


if __name__ == "__main__":
    graphe, stations = charger_reseau("reseau.json")
    for depart, arrivee in [("A1", "F2"), ("B3", "E1"), ("A1", "Z9"), ("D2", "D2")]:
        try:
            print("%s -> %s  %s" % (
                depart, arrivee, formater(plus_court_chemin(graphe, depart, arrivee), stations)))
        except StationInconnue as e:
            print("%s -> %s  erreur : %s" % (depart, arrivee, e))
