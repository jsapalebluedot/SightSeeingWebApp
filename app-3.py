from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
from createDataBase import Place

app = Flask(__name__)

engine = create_engine("sqlite:///places.db")
Session = sessionmaker(bind=engine)
session = Session()

@app.route("/")
def index():
    keyword = request.args.get("q", "").strip().lower()  # ép về chữ thường
    if keyword:
        # dùng ilike nếu DB hỗ trợ, còn SQLite thì convert chuỗi sang lower để so sánh
        places = session.query(Place).filter(
            or_(
                Place.name.ilike(f"%{keyword}%"),
                Place.tags.ilike(f"%{keyword}%"),
                Place.description.ilike(f"%{keyword}%")
            )
        ).all()
    else:
        places = session.query(Place).all()
    return render_template("index.html", places=places, keyword=keyword)

if __name__ == "__main__":
    app.run(debug=True)
