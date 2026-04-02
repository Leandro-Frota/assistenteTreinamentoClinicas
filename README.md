# 🏥 MedTrainer - Assistente Virtual de Treinamento para Clínicas Médicas

![Python](https://img.shields.io/badge/Python-3.13-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.128-green)
![Gemini](https://img.shields.io/badge/Google-Gemini%202.5-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

Assistente virtual inteligente baseado em IA Generativa para treinamento, padronização e suporte operacional de equipes em clínicas médicas.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Contribuindo](#contribuindo)

## 🎯 Sobre o Projeto

O **MedTrainer** é um assistente virtual que utiliza IA Generativa (Google Gemini) combinada com RAG (Retrieval-Augmented Generation) para treinar colaboradores de clínicas médicas em tempo real.

### Problema que Resolve

- ⏰ **Alto tempo gasto em treinamentos manuais**
- 📉 **Falta de padronização no atendimento**
- 🔄 **Alto turnover de colaboradores**
- ❓ **Dúvidas frequentes da equipe**
- 📚 **Dificuldade em manter conhecimento atualizado**

### Solução

Um assistente disponível 24/7 que:
- Treina novos colaboradores automaticamente
- Fornece scripts padronizados de atendimento
- Responde dúvidas em tempo real
- Simula cenários reais (roleplay)
- Registra interações para análise

## ✨ Funcionalidades

### 🎓 Treinamento
- Onboarding automatizado de novos funcionários
- Explicação de processos internos passo a passo
- Simulação de situações reais de atendimento
- Correção e orientação em tempo real

### 💬 Atendimento
- Scripts prontos para WhatsApp, telefone e presencial
- Orientação sobre fluxos de primeiro contato
- Gestão de objeções frequentes
- Protocolos de urgência

### 📊 Gestão
- Registro de todas as interações
- Painel de logs e métricas
- Integração com N8N para automações
- Análise de desempenho da equipe

### 🔍 Base de Conhecimento
- 20 documentos PDF com procedimentos
- Busca inteligente com RAG
- Respostas contextualizadas
- Atualização contínua

## 🏗️ Arquitetura

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  Frontend   │─────▶│   Backend    │─────▶│   Gemini    │
│  FastHTML   │      │   FastAPI    │      │  2.5 Flash  │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  MCP Server  │
                     │   RAG + AI   │
                     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │ Vector Store │
                     │    FAISS     │
                     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  20 PDFs     │
                     │  Docs Base   │
                     └──────────────┘
```

### Fluxo de Funcionamento

1. **Usuário** faz uma pergunta no chat
2. **Backend** recebe a mensagem via API
3. **MCP Server** busca contexto relevante nos PDFs usando RAG
4. **FAISS** retorna os trechos mais relevantes (embeddings)
5. **Gemini** gera resposta personalizada com o contexto
6. **Resposta** é enviada ao usuário
7. **Log** é registrado via webhook N8N

## 🛠️ Tecnologias

### Backend
- **Python 3.13** - Linguagem principal
- **FastAPI** - API REST moderna e rápida
- **Google Gemini 2.5 Flash** - Modelo de IA Generativa
- **LangChain** - Framework para aplicações com LLM
- **FAISS** - Vector store para busca semântica
- **HuggingFace** - Embeddings (all-MiniLM-L6-v2)
- **MCP (Model Context Protocol)** - Integração com IA
- **PyPDF** - Processamento de documentos

### Frontend
- **FastHTML** - Framework web moderno em Python
- **CSS3** - Estilização customizada
- **JavaScript** - Interatividade

### Infraestrutura
- **Uvicorn** - ASGI server
- **N8N** - Automação e webhooks
- **python-dotenv** - Gerenciamento de variáveis de ambiente

## 📦 Instalação

### Pré-requisitos

- Python 3.13+
- pip
- Git

### Passo a Passo

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd assistenteTreinamentoClinicas
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**

Windows (Git Bash):
```bash
source venv/Scripts/activate
```

Windows (CMD):
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. **Instale as dependências**

Instalação completa (recomendada):
```bash
pip install -r requirements.txt
```

Ou instalação rápida (sem PyTorch pesado):
```bash
pip install -r requirements-minimal.txt
```

5. **Configure as variáveis de ambiente**

```bash
cp .env.example .env
```

Edite o arquivo `.env` e adicione sua chave:
```env
GOOGLE_API_KEY=sua_chave_google_gemini_aqui
N8N_WEBHOOK_LOG=url_webhook_para_logs (opcional)
N8N_WEBHOOK_BUSCAR=url_webhook_para_buscar_logs (opcional)
```

Para obter a chave do Google Gemini:
- Acesse: https://aistudio.google.com/apikey
- Crie uma nova chave API
- Cole no arquivo `.env`

> 📖 **Guia detalhado**: Veja [INSTALL.md](INSTALL.md) para instruções completas

6. **Adicione os documentos PDF**

Coloque seus documentos de treinamento na pasta `docs/`:
```
docs/
├── 01_Identidade_do_Atendimento_Consultorio.pdf
├── 02_padrao_comunicacao_whatsapp.pdf
├── 03_avaliacao_cognitiva.pdf
└── ... (demais documentos)
```

## 🚀 Como Usar

### Passo 1: Iniciar o Backend (API FastAPI)

```bash
uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em:
- **URL**: http://localhost:8000
- **Documentação**: http://localhost:8000/docs
- **Endpoint**: `POST /chat`

Exemplo de requisição:
```json
{
  "message": "Como atender um paciente novo no WhatsApp?",
  "perfil": "atendente"
}
```

### Passo 2: Iniciar o Frontend (FastHTML)

```bash
python frontend/app.py
```

Interface moderna e responsiva em: http://localhost:5001

> **⚠️ Importante**: O backend (API) precisa estar rodando para o frontend funcionar!

### Opção Alternativa: Interface Gradio (Standalone)

Se preferir usar a interface Gradio com logs integrados:

```bash
python backend/medTrainer.py
```

> **Nota**: Esta opção requer Gradio instalado (descomente no requirements.txt)

## 📁 Estrutura do Projeto

```
assistenteTreinamentoClinicas/
│
├── backend/                      # Backend da aplicação
│   ├── prompts/                  # Instruções do sistema
│   │   └── system_instructions.md
│   ├── api.py                    # API FastAPI
│   ├── medTrainer.py             # Lógica principal
│   ├── mcp_server.py             # Servidor MCP para RAG
│   └── rag_utils.py              # Utilitários RAG
│
├── frontend/                     # Frontend FastHTML
│   └── app.py                    # Interface web
│
├── docs/                         # Base de conhecimento (PDFs)
│   ├── 01_Identidade_do_Atendimento_Consultorio.pdf
│   ├── 02_padrao_comunicacao_whatsapp.pdf
│   └── ... (20 documentos)
│
├── .env                          # Variáveis de ambiente
├── .env.example                  # Template de variáveis
├── .gitignore                    # Arquivos ignorados pelo Git
├── requirements.txt              # Dependências completas
├── requirements-minimal.txt      # Dependências mínimas
├── INSTALL.md                    # Guia de instalação detalhado
├── n8n_workflow.json             # Workflow N8N (opcional)
└── README.md                     # Este arquivo
```

## 🔧 Configuração Avançada

### Ajustar Parâmetros do Modelo

Edite `backend/medTrainer.py`:

```python
config=types.GenerateContentConfig(
    system_instruction=system_instructions,
    temperature=1.0,        # Criatividade (0.0 - 2.0)
    top_p=0.9,             # Nucleus sampling
    top_k=50,              # Top-k sampling
    max_output_tokens=2048, # Tamanho máximo da resposta
)
```

### Ajustar RAG

Edite `backend/rag_utils.py`:

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,      # Tamanho dos chunks
    chunk_overlap=200    # Sobreposição entre chunks
)

retriever = self.vectorstore.as_retriever(
    search_kwargs={"k": 3}  # Número de documentos retornados
)
```

## 📊 Endpoints da API

### POST /chat
Envia mensagem para o assistente

**Request:**
```json
{
  "message": "string",
  "perfil": "atendente" // opcional
}
```

**Response:**
```json
{
  "response": "string"
}
```

## 🧪 Testando a API

### Com curl:
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Como fazer agendamento?", "perfil": "recepcionista"}'
```

### Com Python:
```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={
        "message": "Como atender paciente novo?",
        "perfil": "atendente"
    }
)
print(response.json())
```

## 🎓 Casos de Uso

### 1. Onboarding de Novos Colaboradores
```
Usuário: "Sou novo na clínica, como funciona o primeiro atendimento?"
MedTrainer: [Explica todo o fluxo com scripts prontos]
```

### 2. Dúvidas Operacionais
```
Usuário: "Como remarcar uma consulta?"
MedTrainer: [Fornece procedimento padrão]
```

### 3. Treinamento em Atendimento
```
Usuário: "Simule um atendimento de paciente ansioso"
MedTrainer: [Cria roleplay e orienta respostas]
```

### 4. Scripts Padronizados
```
Usuário: "Preciso de um script para confirmar consulta"
MedTrainer: [Fornece template pronto]
```

## 🔐 Segurança

- ⚠️ **NUNCA** commite o arquivo `.env` com suas chaves
- Use `.gitignore` para proteger credenciais
- Mantenha a `GOOGLE_API_KEY` segura
- Configure CORS adequadamente em produção

## 🐛 Troubleshooting

### Erro: "No module named 'backend'"
```bash
# Solução: Execute do diretório raiz
uvicorn backend.api:app --reload
```

### Erro: "No module named 'medTrainer'"
```bash
# Solução: Já corrigido no código com sys.path
```

### Erro: PDFs não encontrados
```bash
# Verifique se os PDFs estão em docs/
ls docs/
```

### Erro: GOOGLE_API_KEY inválida
```bash
# Verifique o arquivo .env
cat .env
# Gere nova chave em: https://aistudio.google.com/apikey
```

## 📈 Roadmap

- [ ] Dashboard de analytics
- [ ] Gamificação do treinamento
- [ ] App mobile
- [ ] Suporte por voz
- [ ] Multi-idioma
- [ ] Análise de sentimento
- [ ] Integração com CRM
- [ ] Testes automatizados

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

Desenvolvido como projeto do curso de IA Generativa - GeraçãoTech

## 🙏 Agradecimentos

- Google Gemini API
- LangChain Community
- FastAPI Framework
- HuggingFace
- Comunidade Python

---

⭐ Se este projeto foi útil, considere dar uma estrela no repositório!

📧 Dúvidas? Abra uma issue ou entre em contato.
