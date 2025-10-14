from sqlalchemy.ext.asyncio.session import AsyncSession


class WithSession:
    def __init__(self, session: AsyncSession):
        self.session = session
