from sqlalchemy import Update, Select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Auth


async def update_email_to_user(user_id: int, session: AsyncSession, email: str):

    await session.execute(Update(Auth).where(Auth.user_id == user_id).values(email=email))
    await session.commit()


async def get_email_to_user(user_id: int, session: AsyncSession):
    result = await session.execute(Select(Auth).where(Auth.user_id == user_id))
    result: ScalarResult
    email: Auth = result.one_or_none()
    if email is None:
        return  False
    # print(f'email: {type(email[0])}')
    return email[0].email