import os
import sys
from dotenv import load_dotenv
from rag_utils import RAGUtils
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("servidor de mcp para geriCare")

arquivos_pdf = [
                "docs/01_Identidade_do_Atendimento_Consultorio.pdf",
                "docs/02_padrao_comunicacao_whatsapp.pdf",
                "docs/03_avaliacao_cognitiva.pdf",
                "docs/04_valores_e_pagamento.pdf",
                "docs/05_fluxo_primeiro_contato.pdf",
                "docs/06_fluxo_followup.pdf",
                "docs/07_situacoes_de_urgencia.pdf",
                "docs/09_followup_e_resgate_pacientes.pdf",
                "docs/08_objecoes_frequentes.pdf",
                "docs/10_servico_consulta_geriatrica.pdf",
                "docs/11_beneficios_geriatria.pdf",
                "docs/12_objecoes_comuns.pdf",
                "docs/13_agendamento_consultas.pdf",
                "docs/14_limites_atendimento_whatsapp.pdf",]

print('Carrgegando documentos e criando RAGUtils...', file=sys.stderr)
rag_engine = RAGUtils(pdf_paths=arquivos_pdf)
print('RAGUtils criado com sucesso.', file=sys.stderr)

@mcp.tool()
def consultar_documentacao(pergunta:str)->str:
    try:
        contexto = rag_engine.buscar_contexto(pergunta)
        if not contexto:
            return "Desculpe, não encontrei informações relevantes para sua pergunta."
        return contexto
    except Exception as e:
        return f"Erro ao consultar documentação: {str(e)}"

if __name__ == "__main__":
    mcp.run()

