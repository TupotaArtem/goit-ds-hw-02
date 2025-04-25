from faker import Faker
import sqlite3
import random

fake = Faker()
conn = sqlite3.connect("task_manager.db")
cur = conn.cursor()

# Додаємо статуси
statuses = ['new', 'in progress', 'completed']
cur.executemany("INSERT OR IGNORE INTO status(name) VALUES (?)", [(s,) for s in statuses])

# Додаємо користувачів
users = [(fake.name(), fake.unique.email()) for _ in range(5)]
cur.executemany("INSERT INTO users(fullname, email) VALUES (?, ?)", users)

# Отримуємо id статусів та користувачів
cur.execute("SELECT id FROM status")
status_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT id FROM users")
user_ids = [row[0] for row in cur.fetchall()]

# Додаємо завдання
tasks = [(fake.sentence(), fake.text(), random.choice(status_ids), random.choice(user_ids)) for _ in range(10)]
cur.executemany("INSERT INTO tasks(title, description, status_id, user_id) VALUES (?, ?, ?, ?)", tasks)

conn.commit()
conn.close()
