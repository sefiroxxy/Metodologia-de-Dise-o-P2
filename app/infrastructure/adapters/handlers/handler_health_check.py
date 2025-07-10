from fastapi import APIRouter, status, Response

router = APIRouter()

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok", "message": "La aplicación está funcionando correctamente."}