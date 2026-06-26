from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

_tarefas: dict[int, dict] = {}
_next_id = 1


class TarefaIn(BaseModel):
    titulo: str
    concluida: bool = False


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tarefas", status_code=201)
def criar_tarefa(payload: TarefaIn):
    global _next_id
    tarefa = {"id": _next_id, "titulo": payload.titulo, "concluida": payload.concluida}
    _tarefas[_next_id] = tarefa
    _next_id += 1
    return tarefa


@app.get("/tarefas")
def listar_tarefas():
    return list(_tarefas.values())


@app.get("/tarefas/{tarefa_id}")
def obter_tarefa(tarefa_id: int):
    tarefa = _tarefas.get(tarefa_id)
    if tarefa is None:
        raise HTTPException(status_code=404, detail="tarefa nao encontrada")
    return tarefa


@app.put("/tarefas/{tarefa_id}")
def atualizar_tarefa(tarefa_id: int, payload: TarefaIn):
    if tarefa_id not in _tarefas:
        raise HTTPException(status_code=404, detail="tarefa nao encontrada")
    tarefa = {"id": tarefa_id, "titulo": payload.titulo, "concluida": payload.concluida}
    _tarefas[tarefa_id] = tarefa
    return tarefa
