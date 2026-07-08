"""Exceptions du domaine — types d'erreurs métier, indépendants de toute infrastructure."""

from __future__ import annotations


class ErreurParsing(Exception):
    """Levée quand un parseur ne peut pas garantir l'intégrité du document extrait
    (ex. pages non traitées faute de ressources système). Ne jamais retourner un
    DocumentBrut silencieusement incomplet — mieux vaut échouer bruyamment.
    """
class ErreurExtraction(Exception):
    """Levée quand l'extraction métier ne peut garantir un niveau de confiance
    minimal (ex. aucun tableau ne correspond au motif attendu). Même principe
    que ErreurParsing : mieux vaut échouer bruyamment qu'extraire silencieusement
    une donnée fausse ou vide.
    """