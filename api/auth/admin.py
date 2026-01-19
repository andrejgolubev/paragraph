from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from api.auth.helpers import get_refreshed_access_token
from api.auth.utils import verify_admin_api_key
from api.auth.validation import get_refresh_token_payload
from api.db.database import get_db
from api.db.models import User
from api.db.schemas import FullUserResponse
from api.settings import settings


router = APIRouter(
    tags=['admin'],
    prefix='/admin', 
    dependencies=[Depends(verify_admin_api_key)]
)


@router.post("/make-admin/")
async def make_admin(
    email: str = Query(alias="почта того, кого сделать админом"),
    groups_to_admin: str = Query(
        alias="Например: 543, 5413. Можно указать несколько через запятую."
    ),
    db: AsyncSession = Depends(get_db),
):
    """делает админом :O"""

    user_result = await db.scalars(select(User).where(User.email == email))
    user = user_result.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="пользователя с такой почтой не существует.",
        )

    user.role = "admin." + ".".join(set(
        [gr.strip() for gr in groups_to_admin.split(",")]
    ))

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {
        "message": f"{user.name}`s role is now: {user.role}",
        "role": user.role,
    }


@router.get(
    '/get-full-info', 
    response_model=FullUserResponse, 
)
async def get_full_user_info(
    user_email: str, 
    db: AsyncSession = Depends(get_db), 
) -> FullUserResponse:
    """can be mostly used to check if user agrees with terms of use etc."""
    result = await db.scalars(select(User).where(User.email == user_email)
    .options(selectinload(User.consents)))

    if (user := result.first()):  
        user_response = FullUserResponse( 
            email=user.email, 
            name=user.name, 
            group_id=user.group_id if user.group_id else None, 
            role=user.role,
            active=user.active, 
            sign_up_date=user.sign_up_date,
            consents = [
                {
                    'consent_type': consent.consent_type, 
                    'accepted_at': consent.accepted_at,
                }
                for consent in user.consents
            ]
        )
        return user_response
        
    else: 
        raise HTTPException(
            status_code=404,
            detail='пользователь не найден'
        )


@router.post(
    '/delete', 
)
async def delete_user_by_email(email: str, db: AsyncSession = Depends(get_db)): 
    result = await db.scalars(select(User).where(User.email == email))
    if not (user := result.first()) : 
        raise HTTPException(
            status_code=404,
            detail='пользователь с таким email не найден'
        )
    db.delete(user)
    await db.commit()
    return {'message': 'удаление успешно'}




# @router.post(
#     "/refresh-token",
# )
# async def refresh_token(
#     response: Response,
#     payload: dict = Depends(get_refresh_token_payload), 
#     db: AsyncSession = Depends(get_db)):
#     """
#     Обновляет access_token с помощью refresh_token.
#     """

#     access_token = await get_refreshed_access_token(payload=payload, db=db)

#     response.set_cookie(
#             key='access_token',
#             value=access_token,
#             httponly=True,
#             secure=True,  # для htpps
#             samesite='none', # обязательно 'lax' для продакшна  
#             max_age=settings.auth_jwt.access_token_expire_minutes*60
#         )  

#     return {"message": 'токен успешно обновлен'}