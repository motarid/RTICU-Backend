# Hypoxemia & ARDS Reasoning Engine
# Medical logic based on Berlin Definition

def calculate_pf_ratio(pa_o2: float, fio2: float) -> float:
    """
    Calculate PaO2 / FiO2 ratio
    FiO2 must be entered as percentage (e.g. 60 for 60%)
    """
    if fio2 <= 0:
        raise ValueError("FiO2 must be greater than 0")

    return pa_o2 / (fio2 / 100)


def classify_hypoxemia(pf_ratio: float) -> str:
    if pf_ratio >= 300:
        return "Normal oxygenation"
    elif 200 <= pf_ratio < 300:
        return "Mild hypoxemia"
    elif 100 <= pf_ratio < 200:
        return "Moderate hypoxemia"
    else:
        return "Severe hypoxemia"


def classify_ards(pf_ratio: float, peep: float) -> dict:
    """
    ARDS classification based on Berlin definition
    Requires PEEP >= 5 cmH2O
    """
    if peep < 5:
        return {
            "ards": False,
            "message": "PEEP < 5 cmH2O — ARDS criteria not met"
        }

    if 200 < pf_ratio <= 300:
        return {"ards": True, "severity": "Mild ARDS"}
    elif 100 < pf_ratio <= 200:
        return {"ards": True, "severity": "Moderate ARDS"}
    elif pf_ratio <= 100:
        return {"ards": True, "severity": "Severe ARDS"}
    else:
        return {"ards": False, "message": "No ARDS"}


def hypoxemia_reasoning_engine(
    pa_o2: float,
    fio2: float,
    peep: float
) -> dict:
    """
    Full clinical reasoning output
    """
    pf_ratio = calculate_pf_ratio(pa_o2, fio2)

    hypoxemia_status = classify_hypoxemia(pf_ratio)
    ards_status = classify_ards(pf_ratio, peep)

    return {
        "pa_o2": pa_o2,
        "fio2": fio2,
        "peep": peep,
        "pf_ratio": round(pf_ratio, 1),
        "hypoxemia": hypoxemia_status,
        "ards_assessment": ards_status
    }
