from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///lesson.db"
db = SQLAlchemy(app)

class Lessons(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String)
    content: Mapped[str] = mapped_column(db.String)

admin = Admin(app)
admin.add_view(ModelView(Lessons, db.session))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/lessons/add", methods=["GET", "POST"])
def add_lesson():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        lesson = Lessons(title=title, content=content)
        db.session.add(lesson)
        db.session.commit()
        return redirect(url_for("view_lesson", id=lesson.id))
    
    return render_template("add_lesson.html")

@app.route("/lessons/view/<int:id>")
def view_lesson(id):
    lesson = db.get_or_404(Lessons, id)
    return render_template("view_lessons.html", lessons=[lesson])

@app.route("/lessons/view-all")
def view_lessons():
    lessons = Lessons.query.all()
    return render_template("view_lessons.html", lessons=lessons)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
