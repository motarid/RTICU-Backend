# api/app/api/routers/hypoxemia.py

from fastapi import APIRouter
from pydantic import BaseModel

from app.core.hypoxemia_ards_engine import hypoxemia_ards_reasoning

router = APIRouter()


class HypoxemiaInput(BaseModel):
    pao2: float
    fio2: float
    peep: float
    bilateral_infiltrates: bool


@router.post("/hypoxemia/ards-analysis")
def analyze_hypoxemia(data: HypoxemiaInput):
    """
    Analyze hypoxemia and ARDS severity
    """
    result = hypoxemia_ards_reasoning(
        pao2=data.pao2,
        fio2=data.fio2,
        peep=data.peep,
        bilateral_infiltrates=data.bilateral_infiltrates
    )

    return result
