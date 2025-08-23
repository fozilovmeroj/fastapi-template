from sqlalchemy.ext.asyncio.session import AsyncSession


class Service:
    def __init__(self, session: AsyncSession):
        self.session = session
