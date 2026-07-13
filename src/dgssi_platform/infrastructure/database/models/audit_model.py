"""Modèles SQLAlchemy — tables Postgres pour les audits extraits."""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class AuditModel(Base):
    __tablename__ = "audits"

    id: Mapped[int] = mapped_column(primary_key=True)
    iiv_nom: Mapped[str] = mapped_column(String(200))
    iiv_secteur: Mapped[str] = mapped_column(String(200))
    prestataire_audit: Mapped[str] = mapped_column(String(200))
    classification: Mapped[str] = mapped_column(String(100))
    taux_conformite_global: Mapped[float | None] = mapped_column(Float, nullable=True)
    date_extraction: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    confiance_extraction: Mapped[float] = mapped_column(Float)

    historique_versions: Mapped[list["HistoriqueVersionModel"]] = relationship(
        back_populates="audit", cascade="all, delete-orphan"
    )
    resultats_techniques: Mapped[list["ResultatTechniqueModel"]] = relationship(
        back_populates="audit", cascade="all, delete-orphan"
    )


class HistoriqueVersionModel(Base):
    __tablename__ = "historique_versions"

    id: Mapped[int] = mapped_column(primary_key=True)
    audit_id: Mapped[int] = mapped_column(ForeignKey("audits.id"))
    version: Mapped[str] = mapped_column(String(20))
    date: Mapped[date] = mapped_column(Date)
    commentaire: Mapped[str] = mapped_column(String(500))

    audit: Mapped[AuditModel] = relationship(back_populates="historique_versions")


class ResultatTechniqueModel(Base):
    __tablename__ = "resultats_techniques"

    id: Mapped[int] = mapped_column(primary_key=True)
    audit_id: Mapped[int] = mapped_column(ForeignKey("audits.id"))
    element_audite: Mapped[str] = mapped_column(String(200))
    critique: Mapped[int] = mapped_column(Integer)
    elevee: Mapped[int] = mapped_column(Integer)
    moyenne: Mapped[int] = mapped_column(Integer)
    faible: Mapped[int] = mapped_column(Integer)

    audit: Mapped[AuditModel] = relationship(back_populates="resultats_techniques")
class EvaluationConformiteModel(Base):
    __tablename__ = "evaluations_conformite"

    id: Mapped[int] = mapped_column(primary_key=True)
    audit_id: Mapped[int] = mapped_column(ForeignKey("audits.id"))
    statut: Mapped[str] = mapped_column(String(20))
    seuil_applique: Mapped[float] = mapped_column(Float)
    nb_ecarts_critiques: Mapped[int] = mapped_column(Integer)
    element_le_plus_expose: Mapped[str] = mapped_column(String(200))
    date_evaluation: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)