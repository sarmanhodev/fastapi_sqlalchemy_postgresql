from database import Base
from sqlalchemy import String,Integer, Column



class Aluno(Base):
    __tablename__='alunos'
    id=Column(Integer, primary_key=True)
    nome = Column(String(256), nullable= False, unique = True)
    email = Column(String(256), nullable= False, unique = True)

