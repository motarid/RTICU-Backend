# api/app/core/hypoxemia_ards_engine.py

from typing import Dict, List


def calculate_pafi(pao2: float, fio2: float) -> float:
    """
    Calculate PaO2 / FiO2 ratio
    """
    if fio2 <= 0:
        raise ValueError("FiO2 must be greater than 0")

    return pao2 / fio2


def classify_ards(pafi: float) -> str:
    """
    Classify ARDS severity using Berlin Definition
    """
    if pafi > 300:
        return "No ARDS"
    elif 200 < pafi <= 300:
        return "Mild ARDS"
    elif 100 < pafi <= 200:
        return "Moderate ARDS"
    else:
        return "Severe ARDS"


def hypoxemia_ards_reasoning(
    pao2: float,
    fio2: float,
    peep: float,
    bilateral_infiltrates: bool
) -> Dict:
    """
    Hypoxemia & ARDS clinical reasoning engine
    """

    pafi = calculate_pafi(pao2, fio2)
    ards_severity = classify_ards(pafi)

    reasoning: List[str] = []

    reasoning.append(f"PaO2/FiO2 ratio calculated: {round(pafi, 1)}")

    if pafi < 300:
        reasoning.append("Hypoxemia detected based on PaO2/FiO2 < 300")

    if bilateral_infiltrates:
        reasoning.append("Chest imaging shows bilateral infiltrates")

    if peep >= 5:
        reasoning.append("PEEP ≥ 5 cmH2O supports ARDS criteria")

    if ards_severity != "No ARDS":
        reasoning.append(f"Meets Berlin Definition for {ards_severity}")

    return {
        "pafi_ratio": round(pafi, 1),
        "ards_severity": ards_severity,
        "clinical_reasoning": reasoning
    }
