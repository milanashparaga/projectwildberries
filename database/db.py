import sqlite3


class Database:
    def __init__(self, data):
        self.connect = sqlite3.connect(data)
        self.cursor = self.connect.cursor()
        if self.connect:
            print('Data base connected OK')

    def check_user(self, user_id):
        """Проверка пользователя на наличие в БД"""
        return bool(self.cursor.execute('SELECT * FROM users WHERE tg_id = ?', (user_id,)).fetchone())

    def check_count(self, user_id):
        """Получем количество посещений и имя пользователя"""
        return self.cursor.execute('SELECT count,name FROM users WHERE tg_id = ?', (user_id,)).fetchone()

    async def add_user(self, state):
        """Добавление нового пользователя в БД"""
        async with state.proxy() as data:
            self.cursor.execute('INSERT INTO users VALUES (?,?,?,?)',
                                (data['id'], data['name'], data['count'], data['phone']))
            self.connect.commit()

    def spam(self):
        """Получить id пользователей"""
        return self.cursor.execute('SELECT tg_id FROM users').fetchall()


db = Database('wb_db.db')
