"""Contrats d'entrée et de sortie de l'API (Pydantic v2).
Adapté pour la classification d'incidents IT.
"""
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator


class PredictRequest(BaseModel):
    """Requête de prédiction pour un incident."""
    text: str = Field(..., min_length=1, max_length=2000, description="Description de l'incident IT",
                      examples=["My laptop screen is flickering", "Cannot access the VPN"])

    @field_validator("text")
    @classmethod
    def valider_texte_non_vide(cls, v: str) -> str:
        """Refuse un texte fait uniquement de blancs."""
        if not v.strip():
            raise ValueError("texte vide")
        return v

class PredictResponse(BaseModel):
    """Réponse de classification d'incident."""
    label: str = Field(..., description="Catégorie d'incident (ex: Hardware, Access...)")
    score: float = Field(..., ge=0, le=1, description="Confiance du modèle")
    text: str = Field(..., description="Aperçu de la description analysée")
    status: Literal["VALIDE", "A_VERIFIER"] = Field(..., description="Statut basé sur le seuil d'incertitude")

class HealthResponse(BaseModel):
    """État de santé de l'API."""
    status: str = Field(..., description="OK si le service est opérationnel")
    model: str = Field(..., description="Nom du modèle chargé")


class ResolveRequest(BaseModel):
    """Requête de résolution d'incident par l'agent autonome."""
    text: str = Field(..., min_length=1, max_length=2000, description="Description de l'incident IT",
                      examples=["Cannot access the VPN", "Screen flickering and turning black"])

    @field_validator("text")
    @classmethod
    def valider_texte_non_vide(cls, v: str) -> str:
        """Refuse un texte fait uniquement de blancs."""
        if not v.strip():
            raise ValueError("texte vide")
        return v


class ResolveResponse(BaseModel):
    """Réponse de résolution par l'agent autonome (RAG + sources citées)."""
    categorie: str = Field(..., description="Catégorie prédite par le modèle ML")
    score: float = Field(..., ge=0, le=1, description="Confiance du modèle ML")
    statut: Literal["VALIDE", "A_VERIFIER"] = Field(..., description="Statut basé sur le seuil d'incertitude")
    runbook: str | None = Field(None, description="Titre du runbook RAG utilisé (None si A_VERIFIER)")
    resolution: str = Field(..., description="Procédure de résolution (procédure RAG ou message d'escalade humaine)")
    sources: list[dict[str, Any]] = Field(..., description="Sources citées (chemin, score, titre)")
    action_humaine: bool = Field(..., description="True si une intervention humaine est requise")
    message_humain: str | None = Field(None, description="Message pour l'opérateur humain si action_humaine True")
