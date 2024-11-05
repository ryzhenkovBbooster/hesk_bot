from sqlalchemy import Column, BigInteger, Text, Boolean

from db.database import Base


class Auth(Base):
    __tablename__ = 'tg_auth'
    id = Column(BigInteger, unique=True, primary_key=True, autoincrement=True)

    user_id = Column(BigInteger, unique=True)
    username = Column(Text, unique=False, nullable=True)
    email = Column(Text, unique=False, nullable=False)




    def __str__(self) -> str:
        return f"<USER: {self.user_id, self.username, self.email}>"