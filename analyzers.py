#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module d'analyse locale
Analyse les sujets sans appel API
"""

import re
from typing import List, Tuple, Optional
from collections import Counter
from config import STOPWORDS
from utils import nettoyer_texte


def extraire_ngrammes(mots: List[str], n: int, min_freq: int = 2) -> List[Tuple[str, int]]:
    """Extrait les n-grammes significatifs avec leur fréquence."""
    ngrammes = []
    for i in range(len(mots) - n + 1):
        segment = mots[i:i+n]
        if all(mot not in STOPWORDS and len(mot) > 2 for mot in segment):
            ngrammes.append(' '.join(segment))
    freq = Counter(ngrammes)
    return [(ng, count) for ng, count in freq.most_common() if count >= min_freq]


def extraire_contexte_sujet(messages: List[str], mots_cles: str, max_chars: int = 150) -> Optional[str]:
    """Extrait un contexte/exemple pour un sujet donné."""
    mots_lower = [m.lower() for m in mots_cles.split()]
    for message in messages:
        message_lower = message.lower()
        if all(mot in message_lower for mot in mots_lower):
            contexte = ' '.join(message.split())
            if len(contexte) > max_chars:
                contexte = contexte[:max_chars]
                dernier_point = max(
                    contexte.rfind('.'),
                    contexte.rfind('!'),
                    contexte.rfind('?')
                )
                if dernier_point > max_chars * 0.6:
                    contexte = contexte[:dernier_point + 1]
                else:
                    contexte += "..."
            return contexte
    return None


def calculer_score_pertinence(mot: str, freq: int, doc_length: int) -> float:
    """Calcule un score de pertinence pour un terme."""
    tf = freq / doc_length if doc_length > 0 else 0
    length_bonus = min(len(mot) / 10, 1.5)
    return tf * length_bonus


def analyser_sujets_local(messages: List[str], nb_sujets: int = 8, avec_contexte: bool = False) -> List[str]:
    """Analyse locale des sujets sans API."""
    if not messages:
        return []

    texte_complet = ' '.join(messages)
    texte_propre = nettoyer_texte(texte_complet)
    mots = texte_propre.split()
    mots_filtres = [
        mot for mot in mots
        if len(mot) > 3 and mot not in STOPWORDS and mot.isalpha()
    ]

    if not mots_filtres:
        return ["Conversation générale"]

    freq_mots = Counter(mots_filtres)
    doc_length = len(mots_filtres)
    trigrammes = extraire_ngrammes(mots, 3, min_freq=2)
    bigrammes = extraire_ngrammes(mots, 2, min_freq=3)

    sujets = []

    for trigramme, count in trigrammes[:3]:
        titre = trigramme.title()
        if avec_contexte:
            contexte = extraire_contexte_sujet(messages, trigramme, 120)
            if contexte:
                sujets.append(f"{titre} - {contexte}")
            else:
                sujets.append(f"{titre} (mentionné {count}× dans la conversation)")
        else:
            sujets.append(titre)

    for bigramme, count in bigrammes:
        if len(sujets) >= nb_sujets:
            break
        if not any(bigramme.lower() in s.lower() for s in sujets):
            titre = bigramme.title()
            if avec_contexte:
                contexte = extraire_contexte_sujet(messages, bigramme, 120)
                if contexte:
                    sujets.append(f"{titre} - {contexte}")
                else:
                    sujets.append(f"{titre} (fréquence: {count})")
            else:
                sujets.append(titre)

    mots_scores = [
        (mot, calculer_score_pertinence(mot, freq, doc_length))
        for mot, freq in freq_mots.items()
        if freq >= 5 and len(mot) > 4
    ]
    mots_scores.sort(key=lambda x: x[1], reverse=True)

    for mot, score in mots_scores[:20]:
        if len(sujets) >= nb_sujets:
            break
        if not any(mot in s.lower() for s in sujets):
            titre = mot.capitalize()
            if avec_contexte:
                contexte = extraire_contexte_sujet(messages, mot, 100)
                if contexte:
                    sujets.append(f"{titre} - {contexte}")
                else:
                    freq = freq_mots[mot]
                    sujets.append(f"{titre} (apparitions: {freq})")
            else:
                sujets.append(titre)

    return sujets[:nb_sujets] if sujets else ["Conversation générale"]
