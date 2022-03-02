from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ValidationError
from typing import List
from database import SessionLocal
import models



app = FastAPI()
templates = Jinja2Templates(directory="templates")


class Aluno(BaseModel):
    id:int
    nome:str
    email:str

    class Config:
        orm_mode=True


db = SessionLocal()



@app.get("/")
async def hello(request:Request):
    ola=str("Seja bem-vindo ao cadastro de alunos!")
    
    return templates.TemplateResponse("home.html",{"request":request,"ola":ola})



@app.get("/alunos/", response_model=List[Aluno], status_code=200)
async def list_all(request:Request):
    """
    Lista todos os registros contidos no banco
    """
    aluno = db.query(models.Aluno).all()
    
    total="Total de alunos cadastrados: "+str(len(aluno))
   
    print("\n"+str(total)+"\n")
    return aluno
    
   
    

@app.get("/alunos/{id}", response_model=Aluno, response_model_exclude_unset=True, status_code=status.HTTP_200_OK)
async def busca_aluno(id:int):
    """
    Função que realiza a busca de um determinado aluno através de seu Id
    """
         
    aluno = db.query(models.Aluno).filter(models.Aluno.id==id).first() #busca pelo ID
    data=aluno

    print("\nid: "+str(data.id))
    print("nome: "+str(data.nome))
    print("email: "+str(data.email)+"\n")
     
    return aluno



@app.post("/alunos/", response_model=Aluno, status_code=status.HTTP_201_CREATED)
async def novo_registro(aluno: Aluno):
    """
    Cria novo registro
    """
    novo_aluno=models.Aluno(nome = aluno.nome, email = aluno.email)
    db.add(novo_aluno)
    db.commit()
    
    print("\nid: "+str(novo_aluno.id))
    print("nome: "+str(novo_aluno.nome))
    print("email: "+str(novo_aluno.email)+"\n")
    print("\nAluno cadastrado com sucesso\n")

    return novo_aluno

@app.put("/alunos/{id}",response_model=Aluno,status_code=status.HTTP_200_OK)
async def atualiza_registro(id:int,aluno:Aluno):
    """
    Atualiza registro existente no banco
    """
    aluno_update = db.query(models.Aluno).filter(models.Aluno.id==id).first()
    aluno_update.name=aluno.nome
    aluno_update.email=aluno.email

    db.commit()

    print("\nid: "+str(aluno_update.id))
    print("nome: "+str(aluno_update.nome))
    print("email: "+str(aluno_update.email)+"\n")
    print("\nDados atualizados com sucesso!")
    return aluno_update

    

@app.delete("/alunos/{id}", response_model=Aluno, status_code=status.HTTP_200_OK)
async def deleta_registro(id:int):
    """
    Apaga registro existente no banco
    """

    aluno_delete = db.query(models.Aluno).filter(models.Aluno.id==id).first()

    if aluno_delete is None:
        print("\nRegistro não encontrado\n")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Registro não encontrado')
    
    db.delete(aluno_delete)
    db.commit()

    print("REGISTRO EXCLUIDO")
    return aluno_delete
