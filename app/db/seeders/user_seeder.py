import datetime

from app.logic.repositories.user_repository import UserRepository


async def run():
    await UserRepository.create({
        "email": "admin@gmail.com",
        "name": "admin",
        "password": "Qwerty123$",
        "gender": "male",
        "date_of_birth": datetime.datetime(2000, 1, 1),
    })