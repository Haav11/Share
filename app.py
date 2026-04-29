import sqlite3
from flask import Flask, flash
from flask import abort, redirect, render_template, request, session
import config
import db
import items
import re
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_items = items.get_items()
    return render_template("index.html", items = all_items)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    items = users.get_items(user_id)
    return render_template("show_user.html", user = user, items = items)

@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if query:
        results = items.find_items(query)
    else:
        query = ""
        results = []
    return render_template("find_item.html", query = query, results = results)

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)

    raw_classes = items.get_classes(item_id)
    grouped_classes = {}

    for entry in raw_classes:
        title = entry["title"]
        value = entry["value"]
        if title not in grouped_classes:
            grouped_classes[title] = []
        grouped_classes[title].append(value)

    enrollments = items.get_enrollments(item_id)

    is_enrolled = False
    if "user_id" in session:
        for enrollment in enrollments:
            if enrollment["user_id"] == session["user_id"]:
                is_enrolled = True
                break

    return render_template("show_item.html", item = item, classes = grouped_classes, enrollments = enrollments, is_enrolled = is_enrolled)

@app.route("/new_item")
def new_item():
    require_login()
    classes = items.get_all_classes()
    return render_template("new_item.html", classes = classes)

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    servings = request.form["servings"]
    if not re.search("^[1-9][0-9]{0,3}$", servings):
        abort(403)
    user_id = session["user_id"]

    classes = []

    selected_diets = request.form.getlist("diet[]")
    for diet in selected_diets:
        if diet:
            classes.append(("Ruokavalio", diet))

    dish = request.form["dish"]
    if dish:
        classes.append(("Laji", dish))

    items.add_item(title, description, servings, user_id, classes)

    return redirect("/")

@app.route("/enroll", methods=["POST"])
def enroll():
    require_login()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)

    user_id = session["user_id"]

    success = items.add_enrollment(item_id, user_id)

    if not success:
        return "Ilmoittautuminen epäonnistui"

    return redirect("/item/" + str(item_id))

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    all_classes = items.get_all_classes()
    classes = {}

    for my_class in all_classes:
        if my_class == "Ruokavalio":
            classes[my_class] = []
        else:
            classes[my_class] = ""

    for entry in items.get_classes(item_id):
        category = entry["title"]
        value = entry["value"]

        if category == "Ruokavalio":
            classes[category].append(value)
        else:
            classes[category] = value

    return render_template("edit_item.html", item = item, all_classes = all_classes, classes = classes)

@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()
    item_id = request.form["item_id"]

    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    servings = request.form["servings"]
    if not re.search("^[1-9][0-9]{0,3}$", servings):
        abort(403)

    all_classes = items.get_all_classes()

    classes = []

    selected_diets = request.form.getlist("diet[]")
    for diet in selected_diets:
        if diet:
            if "Ruokavalio" not in all_classes:
                abort(403)
            if diet not in all_classes["Ruokavalio"]:
                abort(403)

            classes.append(("Ruokavalio", diet))

    dish = request.form.get("dish")
    if dish:
        parts = dish.split(":")

        if len(parts) == 2:
            category = parts[0]
            value = parts[1]

            if category not in all_classes:
                abort(403)
            if value not in all_classes[category]:
                abort(403)

            classes.append((category, value))

    items.update_item(item_id, title, description, servings, classes)

    return redirect("/item/" + str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if item["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_item.html", item = item)

    if request.method == "POST":
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat", "error")
        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu", "error")
        return redirect("/register")

    flash("Tunnus luotu", "success")

    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")