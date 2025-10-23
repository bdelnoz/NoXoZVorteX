#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module d'analyse via API
Gère les appels à l'API Mistral pour l'analyse des conversations
"""

import time
import random
import re
from typing import Dict, List, Any, Optional
import uuid
import requests

from config import API_URL, MAX_TOKENS
from utils import ecrire_log, compter_tokens
from analyzers import analyser_sujets_local


def nettoyer_competences_api(texte_brut: str) -> Dict[str, List[str]]:
    """Nettoie et extrait les compétences organisées par domaines d'une réponse API."""
    from categories import categoriser_competence_automatique
    
    competences_par_domaine = {}
    lignes = texte_brut.strip().split('\n')

    for ligne in lignes:
        ligne = ligne.strip()
        if not ligne or ligne.startswith(('#', '*', '-', '>')):
            continue
        if ':' in ligne:
            parties = ligne.split(':', 1)
            if len(parties) == 2:
                domaine = re.sub(r'\*\*|__|\d+\.\s*', '', parties[0].strip())
                if len(domaine) < 3:
                    continue
                competences = []
                for comp in re.split(r'[,;]', parties[1]):
                    comp = re.sub(r'\([^)]+\)', '', comp).strip()
                    if len(comp) >= 3 and comp.lower() not in {'etc', 'et', 'ou'}:
                        competences.append(comp.capitalize() if not comp[0].isupper() else comp)
                if competences:
                    competences_par_domaine.setdefault(domaine, []).extend(competences)

    if not competences_par_domaine:
        competences = [s.strip() for s in re.sub(r'[*#_-]', '', texte_brut).split(',')
                      if s.strip() and len(s.strip()) > 2]
        for comp in competences:
            domaine = categoriser_competence_automatique(comp)
            competences_par_domaine.setdefault(domaine, []).append(
                comp.capitalize() if not comp[0].isupper() else comp
            )

    return competences_par_domaine


def decouper_conversation(conversation: Dict[str, Any], messages: List[str]) -> List[Dict[str, Any]]:
    """Découpe une conversation si > MAX_TOKENS."""
    titre = conversation.get("title", "Sans titre")

    if not messages:
        return [{"title": titre, "messages": [], "partie": "1/1"}]

    texte_complet = "\n".join(messages)
    token_count = compter_tokens(texte_complet)

    if token_count <= MAX_TOKENS:
        return [{
            "title": titre,
            "messages": messages,
            "partie": "1/1",
            "titre_original": titre
        }]

    conv_id = str(uuid.uuid4())
    moitie = len(messages) // 2

    return [
        {
            "title": f"{titre} (Partie 1/2)",
            "messages": messages[:moitie],
            "conversation_id": conv_id,
            "partie": "1/2",
            "titre_original": titre
        },
        {
            "title": f"{titre} (Partie 2/2)",
            "messages": messages[moitie:],
            "conversation_id": conv_id,
            "partie": "2/2",
            "titre_original": titre
        }
    ]


def analyser_conversation(
    conversation: Dict[str, Any],
    api_key: Optional[str],
    model: str,
    simulate: bool = False,
    mode_local: bool = False,
    avec_contexte: bool = False,
    delay: float = 0.5
) -> Dict[str, Any]:
    """Analyse une conversation."""
    titre = conversation.get("title", "Sans titre")
    messages = conversation.get("messages", [])
    source_file = conversation.get("_source_file", "inconnu")

    base_result = {
        "conversation_id": conversation.get("conversation_id", str(uuid.uuid4())),
        "titre_original": conversation.get("titre_original", titre),
        "titre": titre,
        "partie": conversation.get("partie", "1/1"),
        "_source_file": source_file
    }

    if not messages:
        return {
            **base_result,
            "sujets": "[VIDE]",
            "nombre_sujets": 0,
            "token_count": 0,
            "statut": "Vide"
        }

    texte_complet = "\n".join(messages)
    token_count = compter_tokens(texte_complet)

    if mode_local:
        time.sleep(0.05)
        sujets = analyser_sujets_local(messages, nb_sujets=8, avec_contexte=avec_contexte)
        ecrire_log(f"Analyse locale: {titre} ({len(sujets)} sujets)", "INFO")
        return {
            **base_result,
            "sujets": "; ".join(sujets),
            "nombre_sujets": len(sujets),
            "token_count": token_count,
            "statut": "Analysée (Local)"
        }

    if simulate:
        time.sleep(random.uniform(0.1, 0.3))
        sujets_fictifs = [
            "IA et ChatGPT", "Limites des modèles", "Contextualisation",
            "Mémoire conversationnelle", "GPT-5 vs GPT-4", "Paramètres"
        ]
        nb_sujets = random.randint(2, 5)
        sujets = random.sample(sujets_fictifs, min(nb_sujets, len(sujets_fictifs)))
        return {
            **base_result,
            "sujets": "; ".join(sujets),
            "nombre_sujets": len(sujets),
            "token_count": token_count,
            "statut": "Simulée"
        }

    time.sleep(delay)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    texte_extrait = texte_complet[:4000] if len(texte_complet) > 4000 else texte_complet

    system_prompt = (
        "Tu es un expert RH et coach carrière spécialisé dans l'identification de compétences professionnelles, "
        "avec une expertise particulière en Intelligence Artificielle et technologies émergentes. "
        "Analyse cette conversation et identifie UNIQUEMENT les compétences techniques, méthodologiques et professionnelles "
        "qui peuvent enrichir un CV ou un profil LinkedIn.\n\n"

        "⚠️ PRIORITÉ ABSOLUE: COMPÉTENCES IA ET TECHNOLOGIES ÉMERGENTES\n"
        "Accorde une attention MAXIMALE à toute compétence liée à:\n"
        "- Intelligence Artificielle (IA/AI)\n"
        "- Machine Learning et Deep Learning\n"
        "- Modèles de langage (LLM, GPT, Claude, etc.)\n"
        "- Génération d'images (DALL-E, Midjourney, Stable Diffusion)\n"
        "- Prompt Engineering et optimisation\n"
        "- Fine-tuning et RAG\n"
        "- Traitement du langage naturel (NLP)\n"
        "- Computer Vision\n"
        "- Frameworks ML (TensorFlow, PyTorch, Hugging Face)\n"
        "- Déploiement de modèles IA\n"
        "- Éthique et gouvernance de l'IA\n\n"

        "INSTRUCTIONS CRITIQUES:\n"
        "- Organise les compétences par DOMAINES\n"
        "- Format: DOMAINE: compétence1, compétence2, compétence3\n"
        "- Un domaine par ligne\n"
        "- PAS de markdown (pas de **, ###, -, etc.)\n"
        "- PAS de numérotation\n"
        "- Place TOUJOURS 'Intelligence artificielle et ML' EN PREMIER si des compétences IA sont détectées\n"
        "- Sois EXHAUSTIF sur les compétences IA (même les mentions indirectes)\n"
        "- Utilise des termes standards du marché du travail\n"
        "- Sois précis et concret\n\n"
    )

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"Conversation:\n\n{texte_extrait}"
            }
        ],
        "temperature": 0.5,
        "max_tokens": 16000
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()["choices"][0]["message"]["content"]

            competences_par_domaine = nettoyer_competences_api(result)
            sujets_list = []
            for domaine, competences in competences_par_domaine.items():
                for comp in competences:
                    sujets_list.append(f"[{domaine}] {comp}")

            ecrire_log(f"Analysée: {titre} ({len(sujets_list)} compétences, {len(competences_par_domaine)} domaines)", "INFO")

            return {
                **base_result,
                "sujets": "; ".join(sujets_list),
                "competences_par_domaine": competences_par_domaine,
                "nombre_sujets": len(sujets_list),
                "nombre_domaines": len(competences_par_domaine),
                "token_count": token_count,
                "statut": "Analysée (API)"
            }

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response else "Unknown"

            if attempt < max_retries - 1 and (status_code == 429 or status_code >= 500):
                wait_time = 5 * (2 ** attempt) if status_code == 429 else (attempt + 1) * 2
                ecrire_log(f"Tentative {attempt + 1}/{max_retries} échouée. Retry dans {wait_time}s", "WARNING")
                time.sleep(wait_time)
                continue

            error_msg = str(e)
            try:
                error_msg = e.response.json().get("message", str(e))
            except:
                pass

            ecrire_log(f"Erreur HTTP {status_code}: {titre} - {error_msg}", "ERROR")

            return {
                **base_result,
                "sujets": f"[ERREUR HTTP {status_code}]",
                "nombre_sujets": 0,
                "token_count": token_count,
                "statut": f"Erreur HTTP {status_code}"
            }

        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                ecrire_log(f"Timeout tentative {attempt + 1}/{max_retries}. Retry...", "WARNING")
                time.sleep((attempt + 1) * 2)
                continue

            ecrire_log(f"Timeout après {max_retries} tentatives: {titre}", "ERROR")
            return {
                **base_result,
                "sujets": "[ERREUR: Timeout]",
                "nombre_sujets": 0,
                "token_count": token_count,
                "statut": "Erreur Timeout"
            }

        except Exception as e:
            ecrire_log(f"Erreur: {titre} - {type(e).__name__}: {str(e)}", "ERROR")
            return {
                **base_result,
                "sujets": f"[ERREUR: {type(e).__name__}]",
                "nombre_sujets": 0,
                "token_count": token_count,
                "statut": f"Erreur {type(e).__name__}"
            }

    return {
        **base_result,
        "sujets": "[ERREUR: Échec après retry]",
        "nombre_sujets": 0,
        "token_count": token_count,
        "statut": "Erreur"
    }
