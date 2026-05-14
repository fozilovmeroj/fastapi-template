from cli.database import upgrade_db, downgrade_db, seed_db

COMMANDS = {
    "db": {
        "upgrade": upgrade_db,
        "downgrade": downgrade_db,
        "seed": seed_db
    }
}
