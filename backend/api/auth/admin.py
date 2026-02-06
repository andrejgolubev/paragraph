from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ...api.logger import log
from ..auth.utils import verify_admin_api_key
from ..db.database import get_db
from ..db.models import User
from ..db.schemas import FullUserResponse


router = APIRouter(
    tags=['admin'],
    prefix='/admin', 
    dependencies=[Depends(verify_admin_api_key)]
)


@router.post("/make-admin/")
async def make_admin(
    user_email: str,
    groups_to_admin: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """
    Дает права администратора - возможность редактировать ДЗ. Не добавляет 
    вводмиые группы к существующим администрируемым группам, а перезаписывает 
    старый список администрируемых групп. 

    Чтобы указать несколько групп, перечислите их через запятую.

    Для лишения пользователя прав администратора оставьте groups_to_admin пустой строкой. 
    """
        

    user_result = await db.scalars(select(User).where(User.email == user_email))
    user = user_result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="пользователя с такой почтой не существует.",
        )

    log.debug('groups_to_admin: %s', groups_to_admin)

    if not groups_to_admin: 
        if 'admin' in user.role: 
            user.role = 'student'
        return {
            "message": f"{user.name}`s role is now: {user.role}",
            "role": user.role,
        }

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
    """
    Возвращает полную информацию по пользователю (email, имя, группа, роль,
    активность, дата регистрации, подтверждённые соглашения) по переданному email.
    HTTP 404 если пользователь не найден.
    """
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


@router.patch('/set-user-activeness')
async def set_user_activeness(
    user_email: str, 
    user_activeness: bool, 
    db: AsyncSession = Depends(get_db)
): 
    """
    Управляет активностью пользователя по email. Если запись найдена — возвращает
    подтверждение, иначе бросает 404.
    """
    result = await db.scalars(select(User).where(User.email == user_email))
    if not (user := result.first()) : 
        raise HTTPException(
            status_code=404,
            detail='пользователь с таким email не найден'
        )

    user.active = user_activeness
    await db.commit()
    return {
        "user_activeness": user_activeness,
        "id": user.id,
        "email": user.email,
        "name": user.name,
    }


@router.post('/delete-user')
async def delete_user(
    user_email: str, 
    db: AsyncSession = Depends(get_db)
): 
    """
    Удаляет пользователя по email. Если запись найдена — удаляет и возвращает
    подтверждение, иначе бросает 404.
    """
    result = await db.scalars(select(User).where(User.email == user_email))
    if not (user := result.first()) : 
        raise HTTPException(
            status_code=404,
            detail='пользователь с таким email не найден'
        )

    await db.delete(user)
    await db.commit()
    return {'deleted': {'id': user.id, 'email': user.email, 'name': user.name}}
