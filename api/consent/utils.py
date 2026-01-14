from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select
from api.db.models import UserConsent


async def user_has_all_consents(user_id: int, db: AsyncSession) -> bool:
    result = await db.execute(
        select(UserConsent.consent_type)
        .where(UserConsent.user_id == user_id)
        .distinct()
    )
    
    user_consent_types = {row[0] for row in result.all()}
    
    # Проверяем наличие обоих типов
    return {"pd", "terms_and_privacy"}.issubset(user_consent_types)