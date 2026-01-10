from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

# =========================
# Input Schema
# =========================
class HypoxemiaInput(BaseModel):
    pao2: float        # mmHg
    fio2: float        # decimal (e.g. 0.21, 0.5)
    peep: float | None = None


# =========================
# Hypoxemia & ARDS Engine
# =========================
@router.post("/hypoxemia/ards")
def hypoxemia_ards_engine(data: HypoxemiaInput):
    pf_ratio = data.pao2 / data.fio2

    if pf_ratio > 300:
        severity = "No ARDS"
        interpretation = "Normal oxygenation"
    elif 200 < pf_ratio <= 300:
        severity = "Mild ARDS"
        interpretation = "Mild hypoxemia"
    elif 100 < pf_ratio <= 200:
        severity = "Moderate ARDS"
        interpretation = "Moderate hypoxemia"
    else:
        severity = "Severe ARDS"
        interpretation = "Severe hypoxemia"

    return {
        "PaO2": data.pao2,
        "FiO2": data.fio2,
        "PF_ratio": round(pf_ratio, 1),
        "ARDS_severity": severity,
        "clinical_interpretation": interpretation
    }
