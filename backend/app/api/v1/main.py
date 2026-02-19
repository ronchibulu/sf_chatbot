"""FastAPI v1 router."""
from fastapi import APIRouter

from app.api.deps import CurrentUser
from app.api.v1.endpoints import lists

router = APIRouter(prefix="/api/v1")

# Include endpoint routers
router.include_router(lists.router)


@router.get("/health")
async def api_health():
    """API v1 health check."""
    return {"status": "ok", "version": "1.0.0"}


@router.get("/auth/validate")
async def validate_session(
    current_user: CurrentUser
):
    """
    Validate session for API access.
    
    Returns user info if session is valid.
    """
    return {
        "valid": True,
        "user": current_user
    }


@router.get("/auth/me")
async def get_current_user_info(
    current_user: CurrentUser
):
    """Get current authenticated user info."""
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "name": current_user["name"]
    }
