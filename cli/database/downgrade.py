from alembic import command
from alembic.config import Config


def downgrade_db(steps=1):
    alembic_cfg = Config("alembic.ini")
    command.downgrade(alembic_cfg, f"-{steps}")
