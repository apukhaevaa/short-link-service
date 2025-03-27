from database import engine, Base
from models import URL, User

def init_models():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_models()
    print("Таблицы в MySQL успешно созданы!")