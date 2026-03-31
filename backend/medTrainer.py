import os
import sys
import requests
import gradio as gr
from google import genai
from dotenv import load_dotenv
from google.genai import types
from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters
from datetime import datetime

load_dotenv()

N8N_WEBHOOK_LOG    = os.getenv("N8N_WEBHOOK_LOG", "")
N8N_WEBHOOK_BUSCAR = os.getenv("N8N_WEBHOOK_BUSCAR", "")

client = genai.Client()

# Inicializar servidor MCP uma única vez
mcp_session = None
mcp_read = None
mcp_write = None

server_params = StdioServerParameters(
    command="python",
    args=["mcp_server.py"],
    env=os.environ
)

with open("backend/prompts/system_instructions.md", "r", encoding="utf-8") as f:
    system_instructions = f.read()

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_instructions,
        temperature=1.0,
        top_p=0.9,
        top_k=50,
        max_output_tokens=2048,
    )
)


def enviar_log(mensagem: str, request: gr.Request):
    if not N8N_WEBHOOK_LOG:
        return
    try:
        ip = request.client.host if request and request.client else "desconhecido"
        user_agent = request.headers.get("user-agent", "desconhecido") if request else "desconhecido"
        payload = {
            "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "mensagem": mensagem,
            "ip": ip,
            "dispositivo": user_agent,
        }
        requests.post(N8N_WEBHOOK_LOG, json=payload, timeout=5)
    except Exception:
        pass


async def inicializar_mcp():
    global mcp_session, mcp_read, mcp_write
    if mcp_session is None:
        print("Inicializando servidor MCP...", file=sys.stderr)
        mcp_read, mcp_write = await stdio_client(server_params).__aenter__()
        mcp_session = ClientSession(mcp_read, mcp_write)
        await mcp_session.__aenter__()
        await mcp_session.initialize()
        print("Servidor MCP inicializado com sucesso!", file=sys.stderr)


async def consultar_servidor_mcp(pergunta: str):
    await inicializar_mcp()
    result = await mcp_session.call_tool("consultar_documentacao", arguments={"pergunta": pergunta})
    if result.content and len(result.content) > 0:
        return result.content[0].text
    return "Desculpe, não encontrei informações relevantes para sua pergunta."


async def gerar_resposta(user_message, chat_history,perfil=None, request=None):
    if request:
        enviar_log(user_message, request)
    try:
        enviar_log(user_message, request)
        
        try:
            contexto_encontrado = await consultar_servidor_mcp(user_message)
        except Exception:
            contexto_encontrado = "Erro ao buscar contexto."
        
        mensagem_com_contexto = f"""

        Perfil do usuário: {perfil}
        
        Mensagem do usuário:
        {user_message}

        Contexto relevante:
        {contexto_encontrado}

        Responda à mensagem do usuário utilizando o contexto encontrado, se necessário.
        """
        response = chat.send_message(mensagem_com_contexto)
        return response.text
    except Exception as e:
        return f"Erro ao gerar resposta: {str(e)}"


def buscar_logs():
    if not N8N_WEBHOOK_BUSCAR:
        return [["N8N_WEBHOOK_BUSCAR não configurado no .env", "", "", ""]]
    try:
        resp = requests.get(N8N_WEBHOOK_BUSCAR, timeout=10)
        resp.raise_for_status()
        dados = resp.json()
        if not isinstance(dados, list) or len(dados) == 0:
            return [["Nenhum log encontrado.", "", "", ""]]
        return [
            [
                row.get("data_hora", ""),
                row.get("mensagem", ""),
                row.get("dispositivo", ""),
                row.get("ip", ""),
            ]
            for row in dados
        ]
    except Exception as e:
        return [[f"Erro ao buscar logs: {str(e)}", "", "", ""]]


with gr.Blocks(title="GeriCare — Assistente Virtual") as demo:
    gr.Markdown("# GeriCare — Assistente Virtual de Atendimento em Geriatria")
    gr.Markdown("Assistente virtual desenvolvido para realizar o primeiro atendimento de pacientes e familiares, oferecendo acolhimento, informações claras sobre o atendimento geriátrico e apoio no agendamento de consultas.")

    with gr.Tabs():
        with gr.Tab("💬 Chat"):
            gr.ChatInterface(
                fn=gerar_resposta,
            )

        with gr.Tab("📋 Logs"):
            gr.Markdown("### Histórico de mensagens registradas na planilha")
            tabela_logs = gr.Dataframe(
                headers=["Data e Hora", "Mensagem", "Dispositivo", "IP"],
                datatype=["str", "str", "str", "str"],
                interactive=False,
                wrap=True,
            )
            btn_atualizar = gr.Button("🔄 Atualizar Logs")
            btn_atualizar.click(fn=buscar_logs, outputs=tabela_logs)


if __name__ == "__main__":
    demo.launch(share=True)
