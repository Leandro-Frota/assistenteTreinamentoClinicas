# 📦 Guia de Instalação - MedTrainer

## 🚀 Instalação Rápida

### Opção 1: Instalação Completa (Recomendada)

```bash
# 1. Clone o repositório
git clone <url-do-repositorio>
cd assistenteTreinamentoClinicas

# 2. Crie ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual
# Windows (Git Bash)
source venv/Scripts/activate
# Windows (CMD)
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Configure o .env
cp .env.example .env
# Edite o .env e adicione sua GOOGLE_API_KEY
```

### Opção 2: Instalação Minimalista (Mais Rápida)

Para testes rápidos sem PyTorch pesado:

```bash
pip install -r requirements-minimal.txt
```

## 🔑 Configuração da API Key

1. Acesse: https://aistudio.google.com/apikey
2. Crie uma nova chave API do Google Gemini
3. Adicione no arquivo `.env`:

```env
GOOGLE_API_KEY=sua_chave_aqui
N8N_WEBHOOK_LOG=url_webhook_logs (opcional)
N8N_WEBHOOK_BUSCAR=url_webhook_buscar (opcional)
```

## 📚 Adicionar Documentos PDF

Coloque seus PDFs na pasta `docs/`:

```
docs/
├── 01_Identidade_do_Atendimento_Consultorio.pdf
├── 02_padrao_comunicacao_whatsapp.pdf
└── ... (demais documentos)
```

## ✅ Verificar Instalação

```bash
# Verificar versão do Python
python --version  # Deve ser 3.13+

# Verificar pacotes instalados
pip list

# Testar importações
python -c "import fastapi, google.genai, langchain, faiss; print('✅ Tudo OK!')"
```

## 🎯 Executar o Projeto

### Backend (API FastAPI)
```bash
uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000
```

### Interface Gradio
```bash
python backend/medTrainer.py
```

### Frontend FastHTML
```bash
python frontend/app.py
```

## 🐛 Problemas Comuns

### Erro: "No module named 'torch'"
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Erro: "Microsoft Visual C++ required"
Instale: https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Erro: "Failed building wheel for faiss-cpu"
```bash
pip install faiss-cpu --no-cache-dir
```

### Erro: Memória insuficiente
Use a versão minimal:
```bash
pip install -r requirements-minimal.txt
```

## 📊 Dependências Principais

| Pacote | Versão | Função |
|--------|--------|--------|
| fastapi | 0.128.7 | API REST |
| google-genai | 1.62.0 | IA Gemini |
| langchain | 1.2.10 | Framework LLM |
| faiss-cpu | 1.13.2 | Vector Store |
| gradio | 6.5.1 | Interface Web |
| pypdf | 6.7.0 | Processar PDFs |
| mcp | 1.26.0 | Model Context Protocol |

## 🔄 Atualizar Dependências

```bash
# Atualizar todas
pip install --upgrade -r requirements.txt

# Atualizar específica
pip install --upgrade fastapi
```

## 💾 Gerar requirements.txt do seu ambiente

```bash
pip freeze > requirements-freeze.txt
```

## 🌐 Ambientes Diferentes

### Desenvolvimento
```bash
pip install -r requirements.txt
pip install pytest black flake8
```

### Produção
```bash
pip install -r requirements.txt --no-dev
```

## 📝 Notas

- Python 3.13+ é obrigatório
- Recomendado: 8GB+ RAM
- PyTorch: ~2GB de download
- Tempo de instalação: 5-15 minutos

## 🆘 Suporte

Se encontrar problemas:
1. Verifique a versão do Python
2. Atualize o pip: `pip install --upgrade pip`
3. Limpe o cache: `pip cache purge`
4. Reinstale em ambiente limpo
