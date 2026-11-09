"""IA Agentique autonome de résolution d'incidents IT (Semaine 10).

L'agent suit l'architecture exigée par le prof Larhlimi :
1. **Qualification ML** : le modèle classique (TF-IDF + LogisticRegression)
   qualifie la catégorie du ticket avec un score de confiance.
2. **Seuil d'incertitude** : si le score < 0.60, le ticket est `A_VERIFIER`
   et l'agent ne résout pas automatiquement (renvoie à un opérateur humain).
3. **Résolution RAG** : sinon, l'agent interroge le Mini-RAG pour récupérer
   le runbook de la catégorie prédite et retourne la procédure avec sources citées.

L'agent n'utilise JAMAIS un modèle génératif seul : il qualifie avec ML puis
résout avec des documents sources citables (arbre de décision : ML → RAG).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from incidents_app.predict import SEUIL_ABSTENTION, charger_modele, predire
from incidents_app.rag import MiniRAG

#: Statuts renvoyés par l'agent.
STATUT_VALIDE = "VALIDE"
STATUT_A_VERIFIER = "A_VERIFIER"


class IncidentAgent:
    """Agent autonome : qualifie un ticket ML puis résout via RAG."""

    def __init__(
        self,
        rag: MiniRAG | None = None,
        seuil_confiance: float = SEUIL_ABSTENTION,
        modele_path: Path | None = None,
    ) -> None:
        self.rag = rag if rag is not None else MiniRAG()
        self.seuil_confiance = seuil_confiance
        self.modele_path = modele_path
        self._modele: Any = None  # chargé à la demande

    def _charger_modele(self) -> Any:
        if self._modele is None:
            self._modele = charger_modele(chemin=self.modele_path)
        return self._modele

    def qualifier(self, texte: str) -> dict[str, Any]:
        """Qualifie le ticket avec le modèle ML existant.

        Retourne {'categorie', 'score', 'statut'}.
        """
        modele = self._charger_modele()
        resultat = predire(texte, modele=modele, seuil=self.seuil_confiance)
        return {
            "categorie": resultat["label"],
            "score": resultat["score"],
            "statut": resultat["status"],  # VALIDE ou A_VERIFIER
        }

    def resoudre(self, texte_ticket: str) -> dict[str, Any]:
        """Résout un incident de bout en bout.

        Étapes :
        1. Qualification ML (catégorie + score + statut).
        2. Si statut == A_VERIFIER : pas de résolution automatique,
           recommande une intervention humaine.
        3. Sinon : recherche RAG du runbook pour la catégorie prédite,
           retourne la procédure de résolution avec sources citées.

        Retourne un dict :
            {
                'categorie': str,
                'score': float,
                'statut': 'VALIDE' | 'A_VERIFIER',
                'runbook': str | None,        # titre du runbook trouvé
                'resolution': str,            # procédure de résolution
                'sources': list[dict],        # sources citées (chemin, score)
                'action_humaine': bool,       # True si renvoi vers un humain
                'message_humain': str | None, # message si action humaine requise
            }
        """
        qualification = self.qualifier(texte_ticket)
        categorie = qualification["categorie"]
        score = qualification["score"]
        statut = qualification["statut"]

        # Seuil d'incertitude : le modèle hésite -> pas de résolution auto
        if statut == STATUT_A_VERIFIER or categorie == "INDETERMINE":
            return {
                "categorie": categorie,
                "score": score,
                "statut": STATUT_A_VERIFIER,
                "runbook": None,
                "resolution": (
                    "Le modèle n'est pas suffisamment confiant pour qualifier ce ticket "
                    f"(score {score:.2%} < seuil {self.seuil_confiance:.0%}). "
                    "Une vérification humaine est requise avant toute résolution."
                ),
                "sources": [],
                "action_humaine": True,
                "message_humain": (
                    "Ticket à vérifier par un opérateur humain. "
                    f"Catégorie pressentie : {categorie} (confiance {score:.2%})."
                ),
            }

        # Résolution via RAG : recherche du runbook pour la catégorie qualifiée
        self.rag.charger_ou_indexer()
        resultats_rag = self.rag.rechercher(categorie, texte_ticket, k=1)

        if not resultats_rag:
            return {
                "categorie": categorie,
                "score": score,
                "statut": STATUT_A_VERIFIER,
                "runbook": None,
                "resolution": (
                    f"Aucune procédure de dépannage trouvée pour la catégorie '{categorie}'. "
                    "Une vérification humaine est requise."
                ),
                "sources": [],
                "action_humaine": True,
                "message_humain": (
                    f"Aucun runbook disponible pour '{categorie}'. "
                    "Transférer à un opérateur humain."
                ),
            }

        meilleur = resultats_rag[0]
        return {
            "categorie": categorie,
            "score": score,
            "statut": STATUT_VALIDE,
            "runbook": meilleur["titre"],
            "resolution": meilleur["contenu"],
            "sources": [
                {
                    "chemin": meilleur["chemin"],
                    "score": meilleur["score"],
                    "titre": meilleur["titre"],
                }
            ],
            "action_humaine": False,
            "message_humain": None,
        }


def main() -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("texte", nargs="?", help="Description de l'incident à résoudre")
    parser.add_argument(
        "--indexer",
        action="store_true",
        help="indexe les runbooks avant la résolution",
    )
    args = parser.parse_args()

    agent = IncidentAgent()

    if args.indexer:
        agent.rag.indexer_runbooks()
        print("Runbooks indexés pour l'agent.")
        return 0

    if not args.texte:
        parser.print_help()
        return 1

    resultat = agent.resoudre(args.texte)
    print(json.dumps(resultat, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
