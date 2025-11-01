import csv
import re
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# ---------------------- MODEL ----------------------
class Place(Base):
    __tablename__ = "places"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    tags = Column(String)
    image_link = Column(String)  # local path hoặc cloud URL
    description = Column(Text)


# ---------------------- DATABASE SETUP ----------------------
engine = create_engine("sqlite:///places.db")
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

# ---------------------- LINK CONVERTER ----------------------
def convert_drive_or_dropbox_link(url: str) -> str:
    """
    Tự động chuyển link Google Drive hoặc Dropbox thành direct download link.
    - Google Drive: https://drive.google.com/file/d/<FILE_ID>/view?usp=sharing
      → https://drive.google.com/uc?export=view&id=<FILE_ID>
    - Dropbox: https://www.dropbox.com/s/<FILE_ID>/tenfile.jpg?dl=0
      → https://www.dropbox.com/s/<FILE_ID>/tenfile.jpg?dl=1
    """
    if not url:
        return url



# ---------------------- CSV HELPER FUNCTIONS ----------------------
def read_csv(file_path: str):
    rows = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)  # bo dong tieu de 
        for row in reader:
            rows.append(row)
    return rows


def add_single(data_row, session):
    try:
        raw_link = data_row[3]
        clean_link = convert_drive_or_dropbox_link(raw_link)  #ham convert 

        place = Place(
            id=int(data_row[0]) if data_row[0].isdigit() else None,
            name=data_row[1],
            tags=data_row[2],
            image_link=clean_link,  # link da convert 
            description=data_row[4],
        )
        session.add(place)
        session.commit()
        print(f"Da them thanh cong: {place.name}")
    except Exception as e:
        session.rollback()
        print(f"Loi khi them {data_row}: {e}")


def add_data(file_csv: str):
    session = Session()
    rows = read_csv(file_csv)
    for row in rows:
        add_single(row, session)
    session.close()
    print("Database done.")


# ---------------------- MAIN EXECUTION ----------------------
if __name__ == "__main__":
    print("Kiem tra hoac tao moi...")
    Base.metadata.create_all(engine)

    csv_path = "data.csv"  # Đặt file CSV cùng thư mục
    print(f"Doc du lieu tu '{csv_path}' ...")
    add_data(csv_path)
