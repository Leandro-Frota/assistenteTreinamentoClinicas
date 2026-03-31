from fastapi import FastAPI
from pydantic import BaseModel
import os
from backend.medTrainer import gerar_resposta


app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    perfil: str = "atendente"  # Valor padrão para o perfil

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        print(f"DEBUG API -> mensagem: {request.message} | perfil: {request.perfil}")

        resposta = await gerar_resposta(
            request.message,
            [],
            request.perfil,
            None
        )

        return {"response": resposta}

    except Exception as e:
        return {"response": f"Erro interno: {str(e)}"}

    resposta = await gerar_resposta(request.message, [],request.perfil, None)
    return {"response": resposta}