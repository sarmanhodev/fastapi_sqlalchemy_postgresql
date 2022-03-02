from database import Base, engine
from models import Aluno

print("Creating database...")

Base.metadata.create_all(engine)
