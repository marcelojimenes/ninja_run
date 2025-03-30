from core.app.game import Game
from core.database.sqlite import SQLiteDatabase

if __name__ == "__main__":
    db = SQLiteDatabase()
    game = Game(db)
    game.run()

