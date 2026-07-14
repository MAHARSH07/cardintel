from fastapi import APIRouter

router = APIRouter(tags=["system"])


@router.get("/health")
def health_check() -> dict[str, str]:
    """Confirm that the API process is responding."""
    return {"status": "ok"}
