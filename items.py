import db

def add_item(title, description, servings, user_id):
    sql = "INSERT INTO items (title, description, servings, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, description, servings, user_id])