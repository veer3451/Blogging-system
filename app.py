from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("blog.db")

@app.route("/")
def index():
    db = get_db()
    blogs = db.execute("SELECT * FROM blogs ORDER BY id DESC").fetchall()
    return render_template("index.html", blogs=blogs)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        db = get_db()
        db.execute("INSERT INTO blogs (title, content, likes) VALUES (?, ?, 0)", 
                   (title, content))
        db.commit()
        return redirect("/")
    return render_template("create.html")

@app.route("/blog/<int:id>")
def blog(id):
    db = get_db()
    blog = db.execute("SELECT * FROM blogs WHERE id=?", (id,)).fetchone()
    comments = db.execute("SELECT * FROM comments WHERE blog_id=?", (id,)).fetchall()
    return render_template("blog.html", blog=blog, comments=comments)

@app.route("/like/<int:id>")
def like(id):
    db = get_db()
    db.execute("UPDATE blogs SET likes = likes + 1 WHERE id=?", (id,))
    db.commit()
    return redirect(f"/blog/{id}")

@app.route("/comment/<int:id>", methods=["POST"])
def comment(id):
    text = request.form["comment"]
    db = get_db()
    db.execute("INSERT INTO comments (blog_id, text) VALUES (?, ?)", (id, text))
    db.commit()
    return redirect(f"/blog/{id}")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    db = get_db()
    blog = db.execute("SELECT * FROM blogs WHERE id=?", (id,)).fetchone()

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        db.execute("UPDATE blogs SET title=?, content=? WHERE id=?", 
                   (title, content, id))
        db.commit()
        return redirect("/")
    return render_template("edit.html", blog=blog)

@app.route("/delete/<int:id>")
def delete(id):
    db = get_db()
    db.execute("DELETE FROM blogs WHERE id=?", (id,))
    db.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
