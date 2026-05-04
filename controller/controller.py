from fastapi import APIRouter
from services.nfeService.Service import Service

router = APIRouter()
nfe_service = Service()

@router.post("/set_nfd")
async def treating_nfe(payload: dict):
    try:
        result = nfe_service.treating_nfe_piso(
            payload.get("files"),
            payload.get("faturamento"),
            payload.get("chegada")
        )

        return result

    except Exception as e:
        return {
            "ok": False,
            "error": str(e)
        }