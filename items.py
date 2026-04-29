import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

def add_item(title, description, servings, user_id, classes):
    sql = "INSERT INTO items (title, description, servings, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, description, servings, user_id])

    item_id = db.last_insert_id()

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [item_id, title, value])

def add_enrollment(item_id, user_id):
    check_sql = "SELECT 1 FROM enrolled WHERE item_id = ? AND user_id = ?"
    result = db.query(check_sql, [item_id, user_id])

    if result:
        return False

    item = get_item(item_id)
    if item["servings"] <= 0:
        return False

    sql_enroll = "INSERT INTO enrolled (item_id, user_id) VALUES (?, ?)"
    db.execute(sql_enroll, [item_id, user_id])

    sql_update = "UPDATE items SET servings = servings - 1 WHERE id = ?"
    db.execute(sql_update, [item_id])

    return True

def get_enrollments(item_id):
    sql = "SELECT users.id user_id, users.username FROM enrolled, users WHERE enrolled.item_id = ? AND enrolled.user_id = users.id ORDER BY enrolled.id"
    return db.query(sql, [item_id])

def remove_enrollment(item_id, user_id):
    sql_delete = "DELETE FROM enrolled WHERE item_id = ? AND user_id = ?"
    db.execute(sql_delete, [item_id, user_id])

    sql_update = "UPDATE items SET servings = servings + 1 WHERE id = ?"
    db.execute(sql_update, [item_id])

def get_classes(item_id):
    sql = "SELECT title, value FROM item_classes WHERE item_id = ?"
    return db.query(sql, [item_id])

def get_items():
    sql = "SELECT id, title, servings FROM items ORDER BY id DESC"
    return db.query(sql)

def get_item(item_id):
    sql = "SELECT items.id, items.title, items.description, items.servings, users.id user_id, users.username FROM items, users WHERE items.user_id = users.id AND items.id = ?"
    result = db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, title, description, servings, classes):
    sql = "UPDATE items SET title = ?, description = ?, servings = ? WHERE id = ?"
    db.execute(sql, [title, description, servings, item_id])

    sql = "DELETE FROM item_classes WHERE item_id = ?"
    db.execute(sql, [item_id])

    sql = "INSERT INTO item_classes (item_id, title, value) VALUES (?, ?, ?)"
    for title, value in classes:
        db.execute(sql, [item_id, title, value])

def remove_item(item_id):
    sql_enrolled = "DELETE FROM enrolled WHERE item_id = ?"
    db.execute(sql_enrolled, [item_id])

    sql_classes = "DELETE FROM item_classes WHERE item_id = ?"
    db.execute(sql_classes, [item_id])

    sql_item = "DELETE FROM items WHERE id = ?"
    db.execute(sql_item, [item_id])

def find_items(query):
    sql = "SELECT id, title, servings FROM items WHERE title LIKE ? OR description LIKE ? ORDER BY id DESC"
    like = "%" + query + "%"
    return db.query(sql, [like, like])