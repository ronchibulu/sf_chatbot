"""FastAPI dependencies for authentication."""

from typing import Annotated, Optional
from datetime import datetime

from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import text

from app.db.database import get_db


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Validate session from cookie or Next.js proxy headers.
    
    Queries the shared PostgreSQL database to validate the session.
    """
    # Check if request is proxied from Next.js (has X-User-Id header)
    user_id_header = request.headers.get("X-User-Id")
    user_email_header = request.headers.get("X-User-Email")
    
    if user_id_header:
        # Request is from Next.js proxy - trust the headers
        # Next.js already validated the session
        return {
            "id": user_id_header,
            "email": user_email_header or "",
            "name": request.headers.get("X-User-Name") or ""
        }
    
    # Direct request - validate session cookie
    session_token = (
        request.cookies.get("session") or 
        request.cookies.get("better-auth.session_token") or
        request.cookies.get("better_auth.session_token")
    )
    
    if not session_token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    
    # Query session from BetterAuth's session table
    result = await db.execute(
        text("""
            SELECT s.id, s."expiresAt", s."userId", u.id as user_id, u.email, u.name
            FROM session s
            JOIN "user" u ON s."userId" = u.id
            WHERE s.token = :token
        """),
        {"token": session_token}
    )
    
    session_row = result.fetchone()
    
    if not session_row:
        raise HTTPException(
            status_code=401,
            detail="Invalid session"
        )
    
    # Check if session has expired
    expires_at = session_row[1]  # expiresAt is index 1
    if expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=401,
            detail="Session expired"
        )
    
    # Return user info
    return {
        "id": session_row[3],  # user_id
        "email": session_row[4],  # email
        "name": session_row[5]  # name
    }


# Type alias for dependency injection
CurrentUser = Annotated[dict, Depends(get_current_user)]
