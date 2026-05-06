from fastapi import APIRouter
from services.nfeService.Service import NfeService
from services.guideService.Guide import Service

router = APIRouter()

nfe_service = NfeService()
guide_service = Service()

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
            "error": f'Erro de servidor. {str(e)}'
        }
        
        
@router.post("/get_guide")
async def find_guide(payload: dict):
    try:
        result = guide_service.decodePDF(
            payload['files'],
            payload['embarque'])
        
        return result

    except Exception as e:
        return {
            "ok": False,
            "error": f'Erro de servidor. {str(e)}'
        }        