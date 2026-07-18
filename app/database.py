from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .configs import settings
# an Engine, which the Session will use for connection resources
#print(settings.model_dump())
engine = create_engine(f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}?sslmode=require&channel_binding=require")
#?sslmode=require&channel_binding=require add for neon
class Base(DeclarativeBase):
    pass

SessionLocal=sessionmaker(engine)

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# THIS IS FOR WHEN UR WRITING SQL CODE USING PSYCOPG
# while True:
#     try:
#         conn = psycopg.connect(
#             host="localhost",
#             dbname="fastapi",
#             user="postgres",
#             password="admin123",
#             row_factory=dict_row

#         )
#         print("Connection sucessfully established")
#         break
#     except Exception as error:
#         print("Error:",error)
#         time.sleep(2)