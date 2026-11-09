"""Mini-RAG : base vectorielle locale de runbooks IT (Semaine 9).

Utilise sentence-transformers pour les embeddings et ChromaDB comme
base vectorielle locale. Aucun modèle génératif n'est utilisé : la
réponse est toujours extraite d'un document source cité (approche RAG
conforme à l'arbre de décision du cours : ML puis RAG, jamais
génératif seul).

Le dossier des runbooks peut être surchargé par la variable
d'environnement ``INCIDENTS_RUNBOOKS`` (utile hors dépôt / en conteneur).

Exemple :
    python -m incidents_app.rag --indexer   # indexe data/runbooks/
    python -m incidents_app.rag --rechercher Hardware "ecran noir"
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any

import chromadb
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

# Modèle d'embedding léger (turn-around rapide, portable, pas de GPU requis)
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DEFAULT_PERSIST_DIR = "chroma_db"
DEFAULT_COLLECTION = "runbooks_it"
DEFAULT_RUNBOOKS_DIR = "data/runbooks"
ENV_RUNBOOKS = "INCIDENTS_RUNBOOKS"


def _dossier_runbooks(dossier: str | None = None) -> str:
    """Résout le dossier des runbooks : argument > variable d'env > défaut."""
    if dossier:
        return dossier
    env = os.environ.get(ENV_RUNBOOKS)
    if env:
        return env
    return DEFAULT_RUNBOOKS_DIR


class MiniRAG:
    """Base vectorielle de runbooks IT avec recherche par similarité."""

    def __init__(
        self,
        persist_directory: str = DEFAULT_PERSIST_DIR,
        collection_name: str = DEFAULT_COLLECTION,
        embedding_model: str = EMBEDDING_MODEL,
    ) -> None:
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embedding_model_name = embedding_model
        self._model: SentenceTransformer | None = None
        # chromadb n'a pas de stubs de typage : on utilise Any pour éviter les erreurs mypy
        self._client: Any = None
        self._collection: Any = None

    @property
    def model(self) -> SentenceTransformer:
        """Charge le modèle d'embedding à la demande (lazy loading)."""
        if self._model is None:
            self._model = SentenceTransformer(self.embedding_model_name)
        return self._model

    @property
    def client(self) -> Any:
        if self._client is None:
            Path(self.persist_directory).mkdir(parents=True, exist_ok=True)
            self._client = chromadb.PersistentClient(path=self.persist_directory)
        return self._client

    @property
    def collection(self) -> Any:
        if self._collection is None:
            self._collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"},
            )
        return self._collection

    def _charger_runbooks(self, runbooks_dir: str | None = None) -> list[dict[str, Any]]:
        """Lit tous les fichiers .md du dossier des runbooks.

        Retourne une liste de dicts : {id, categorie, titre, contenu, chemin}.
        L'identifiant est construit à partir du nom de fichier (sans extension).
        """
        runbooks_dir_path = Path(_dossier_runbooks(runbooks_dir))
        if not runbooks_dir_path.exists():
            return []

        runbooks: list[dict[str, Any]] = []
        for fichier in sorted(runbooks_dir_path.glob("*.md")):
            # Le README documente la base mais n'est pas une procédure.
            if fichier.stem.lower() == "readme":
                continue
            categorie = fichier.stem  # nom du fichier sans extension = catégorie ML
            contenu = fichier.read_text(encoding="utf-8")
            # Première ligne après le titre # comme titre du runbook
            lignes = contenu.strip().splitlines()
            titre = lignes[0].lstrip("# ").strip() if lignes else categorie
            runbooks.append(
                {
                    "id": f"runbook_{categorie}",
                    "categorie": categorie,
                    "titre": titre,
                    "contenu": contenu,
                    "chemin": str(fichier),
                }
            )
        return runbooks

    def indexer_runbooks(self, runbooks_dir: str | None = None) -> dict[str, int]:
        """Indexe tous les runbooks dans la base vectorielle Chroma.

        Retourne un dict {categorie: nombre_de_chunks_indexes}.
        """
        runbooks = self._charger_runbooks(runbooks_dir)
        if not runbooks:
            return {}

        # Supprimer l'ancienne collection pour éviter les doublons en cas de ré-indexation
        try:
            self.client.delete_collection(name=self.collection_name)
        except ValueError:
            # Collection absente : ce n'est pas une erreur, on recrée.
            logger.debug("Collection %s absente, création en cours", self.collection_name)
        self._collection = None  # forcer la recréation
        _ = self.collection  # recrée la collection

        documents: list[str] = []
        metadatas: list[dict[str, Any]] = []
        ids: list[str] = []

        for rb in runbooks:
            documents.append(rb["contenu"])
            metadatas.append(
                {
                    "categorie": rb["categorie"],
                    "titre": rb["titre"],
                    "chemin": rb["chemin"],
                }
            )
            ids.append(rb["id"])

        # Calcul des embeddings
        embeddings = self.model.encode(documents, convert_to_numpy=True).tolist()

        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings,
        )

        return {rb["categorie"]: 1 for rb in runbooks}

    def rechercher(
        self,
        categorie: str,
        requete: str,
        k: int = 3,
    ) -> list[dict[str, Any]]:
        """Recherche les runbooks les plus pertinents pour une catégorie.

        Retourne une liste de dicts : {categorie, titre, contenu, chemin, score, distance}.
        Les résultats sont filtrés par catégorie (where) pour ne retourner
        que le runbook pertinent à la catégorie qualifiée par le ML.
        """
        if self.compter() == 0:
            return []

        query_embedding = self.model.encode([requete], convert_to_numpy=True).tolist()[0]

        resultats = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(k, self.compter()),
            where={"categorie": categorie},
            include=["documents", "metadatas", "distances"],
        )

        documents = (resultats.get("documents") or [[]])[0]
        metadatas = (resultats.get("metadatas") or [[]])[0]
        distances = (resultats.get("distances") or [[]])[0]

        sorties: list[dict[str, Any]] = []
        for doc, meta, dist in zip(documents, metadatas, distances):
            # Conversion distance cosinus en score de similarité (1 - distance)
            score = max(0.0, 1.0 - float(dist))
            sorties.append(
                {
                    "categorie": meta.get("categorie", categorie),
                    "titre": meta.get("titre", categorie),
                    "contenu": doc,
                    "chemin": meta.get("chemin", ""),
                    "score": round(score, 4),
                    "distance": round(float(dist), 4),
                }
            )

        # Trier par score décroissant
        sorties.sort(key=lambda x: x["score"], reverse=True)
        return sorties

    def compter(self) -> int:
        """Retourne le nombre de documents indexés (0 si collection non ouverte)."""
        if self._collection is None:
            # Ne pas ouvrir/ créer la collection juste pour compter.
            try:
                return int(self.client.get_collection(self.collection_name).count())
            except Exception:  # noqa: BLE001 - collection absente ou backend non initialisé
                return 0
        return int(self._collection.count())

    def charger_ou_indexer(self, runbooks_dir: str | None = None) -> MiniRAG:
        """Charge la base existante ou indexe les runbooks si absente."""
        if self.compter() == 0:
            self.indexer_runbooks(runbooks_dir)
        return self


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--indexer", action="store_true", help="indexe les runbooks")
    parser.add_argument(
        "--rechercher",
        nargs=2,
        metavar=("CATEGORIE", "REQUETE"),
        help="recherche dans le RAG : categorie requete",
    )
    parser.add_argument("--runbooks-dir", default=None)
    args = parser.parse_args()

    rag = MiniRAG()

    if args.indexer:
        index_resultats = rag.indexer_runbooks(args.runbooks_dir)
        print(f"Runbooks indexés : {len(index_resultats)}")
        for cat, nb in index_resultats.items():
            print(f"  - {cat}: {nb}")
        return 0

    if args.rechercher:
        categorie, requete = args.rechercher
        recherche_resultats = rag.rechercher(categorie, requete)
        if not recherche_resultats:
            print(f"Aucun runbook trouvé pour la catégorie '{categorie}'.")
            return 1
        print(f"Résultats pour '{categorie}' / '{requete}' :")
        for i, r in enumerate(recherche_resultats, 1):
            print(f"\n[{i}] {r['titre']} (score={r['score']})")
            print(f"    Source : {r['chemin']}")
            print(f"    Aperçu : {r['contenu'][:200]}...")
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
