# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.ext.asyncio import AsyncSession
# from api.auth.validation import get_current_active_auth_user_data
# from api.db.models import UserConsent, User
# from api.db.database import get_db
# from sqlalchemy import select

# consent_router = router = APIRouter() 

# @router.get('/check-user-consents') 
# async def get_user_consents(
#     user: User = Depends(get_current_active_auth_user_data), 
#     db: AsyncSession = Depends(get_db)
# ): 
#     result = await db.scalars(select(UserConsent).where(UserConsent.user_id == user.id)) 
#     consents = result.all() 
#     return consents 
