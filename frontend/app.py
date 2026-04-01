from fasthtml.common import *
import requests
import re
import html
from datetime import datetime

app, rt = fast_app()

@rt('/')
def home():
    return Div (

         Style("""
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            background: #f5f7fa;
            height: 100vh;
            width: 100vw;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        form {
            width: 100%;
            height: 100vh;
            padding: 20px;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: white;
            padding: 15px 20px;
            border-radius: 8px 8px 0 0;
            border: 1px solid #ddd;
            border-bottom: 2px solid #007bff;
            margin-bottom: 0;
        }
        
        .header h1 {
            margin: 0 0 5px 0;
            font-size: 1.5em;
            color: #333;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .header p {
            margin: 0 0 10px 0;
            color: #666;
            font-size: 0.9em;
        }
        
        .header-info {
            display: flex;
            gap: 15px;
            align-items: center;
            font-size: 0.85em;
            color: #666;
            margin-top: 8px;
            flex-wrap: wrap;
        }
        
        .status-online {
            color: #28a745;
            font-weight: bold;
        }
        
        .perfil-selector {
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px 12px;
            background: #f8f9fa;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        
        #perfil {
            padding: 6px 10px;
            border-radius: 5px;
            border: 1px solid #ccc;
            background: white;
            cursor: pointer;
            font-size: 0.9em;
        }

        .chat-box {
            border-left: 1px solid #ddd;
            border-right: 1px solid #ddd;
            padding: 15px;
            flex: 1;
            overflow-y: auto;
            background: white;
            display: flex;
            flex-direction: column;
        }
        
        .welcome-msg {
            background: #e3f2fd !important;
            border-left: 4px solid #007bff;
            padding: 20px !important;
            margin-bottom: 20px;
        }
        
        .welcome-msg h3 {
            margin: 0 0 10px 0;
            color: #007bff;
        }
        
        .welcome-msg ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        
        .welcome-msg li {
            margin: 5px 0;
        }
        
        .welcome-examples {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
            font-style: italic;
            color: #555;
        }

        .user-msg {
            align-self: flex-end;
            background: #007bff;
            color: white;
            padding: 10px 12px;
            border-radius: 10px;
            max-width: 70%;
            word-wrap: break-word;
            position: relative;
        }
        
        .timestamp {
            font-size: 0.75em;
            opacity: 0.8;
            margin-right: 6px;
        }

        .bot-msg {
            align-self: flex-start;
            background: #e9ecef;
            color: black;
            padding: 15px;
            border-radius: 10px;
            max-width: 70%;
            word-wrap: break-word;
            line-height: 1.6;
            position: relative;
        }
        
        .typing-indicator {
            align-self: flex-start;
            background: #e9ecef;
            padding: 15px 20px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
            max-width: 150px;
        }
        
        .typing-indicator span {
            font-size: 0.9em;
            color: #666;
        }
        
        .typing-dots {
            display: flex;
            gap: 4px;
        }
        
        .typing-dots div {
            width: 8px;
            height: 8px;
            background: #007bff;
            border-radius: 50%;
            animation: typing 1.4s infinite;
        }
        
        .typing-dots div:nth-child(2) {
            animation-delay: 0.2s;
        }
        
        .typing-dots div:nth-child(3) {
            animation-delay: 0.4s;
        }
        
        @keyframes typing {
            0%, 60%, 100% { transform: translateY(0); opacity: 0.7; }
            30% { transform: translateY(-10px); opacity: 1; }
        }
        
        .bot-msg h1, .bot-msg h2, .bot-msg h3 {
            margin: 10px 0 8px 0;
            color: #333;
        }
        
        .bot-msg h1 { font-size: 1.3em; }
        .bot-msg h2 { font-size: 1.2em; }
        .bot-msg h3 { font-size: 1.1em; }
        
        .bot-msg ul, .bot-msg ol {
            margin: 8px 0;
            padding-left: 25px;
        }
        
        .bot-msg li {
            margin: 4px 0;
        }
        
        .bot-msg p {
            margin: 8px 0;
        }
        
        .bot-msg code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            color: #c7254e;
        }
        
        .bot-msg pre {
            background: #f4f4f4;
            padding: 12px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 10px 0;
        }
        
        .bot-msg pre code {
            background: none;
            padding: 0;
            color: #333;
        }
        
        .bot-msg strong {
            font-weight: bold;
            color: #222;
        }
        
        .bot-msg em {
            font-style: italic;
        }
        
        .suggestions-container {
            background: white;
            padding: 10px 15px;
            border-left: 1px solid #ddd;
            border-right: 1px solid #ddd;
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        
        .suggestion-chip {
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            padding: 8px 14px;
            border-radius: 20px;
            font-size: 0.85em;
            color: #007bff;
            cursor: pointer;
            transition: all 0.2s;
            white-space: nowrap;
        }
        
        .suggestion-chip:hover {
            background: #e9ecef;
            border-color: #007bff;
            transform: translateY(-2px);
        }
        
        .input-area {
            background: white;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 0 0 8px 8px;
        }
        
        .input-hint {
            font-size: 0.8em;
            color: #666;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .input-msg {
            flex: 1;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #ccc;
            outline: none;
        }
        
        .input-container {
            gap: 10px;
        }
        
        .btn-enviar {
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            white-space: nowrap;
            min-width: 80px;
            font-weight: 500;
            transition: all 0.3s;
        }
        
        .btn-enviar:hover {
            background-color: #0056b3;
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(0,123,255,0.3);
        }
        
        .btn-enviar:active {
            transform: translateY(0);
        }
        
        .btn-loading {
            background-color: #ffc107 !important;
            cursor: wait;
            position: relative;
        }
        
        .btn-loading::after {
            content: '⏳';
            margin-left: 5px;
        }
        
        .message-group {
            margin-bottom: 15px;
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        """),
    Form(
        Div(
            H1("🏥 MedTrainer - Assistente de Treinamento"),
            P("Assistente virtual para treinamento de profissionais em clínicas geriátricas"),
            Div(
                Span("🟢 Online", cls="status-online"),
                Span("|"),
                Span("📚 14 documentos carregados"),
                Span("|"),
                Div(
                    Span("👤 Perfil:"),
                    Select(
                        Option("Atendente"),
                        Option("Recepcionista"),
                        Option("Supervisor"),
                        id="perfil",
                        name="perfil"
                    ),
                    cls="perfil-selector"
                ),
                cls="header-info"
            ),
            cls="header"
        ),

        Div(
            Div(
                H3("👋 Olá! Sou o MedTrainer"),
                P("Estou aqui para te ajudar com:"),
                Ul(
                    Li("Processos de atendimento"),
                    Li("Dúvidas sobre protocolos"),
                    Li("Treinamento de novos funcionários"),
                    Li("Scripts de comunicação")
                ),
                Div(
                    "💡 Experimente perguntar: \"Como atender um paciente novo?\"",
                    cls="welcome-examples"
                ),
                cls="welcome-msg bot-msg"
            ),
            id="chat-box",
            cls="chat-box"
        ),
        
        Div(
            Button("📋 Fluxo de atendimento", cls="suggestion-chip", type="button",
                   onclick="document.getElementById('user-input').value='Como funciona o fluxo de atendimento?'; document.getElementById('user-input').form.requestSubmit();"),
            Button("💬 Scripts WhatsApp", cls="suggestion-chip", type="button",
                   onclick="document.getElementById('user-input').value='Me mostre scripts prontos para WhatsApp'; document.getElementById('user-input').form.requestSubmit();"),
            Button("📞 Agendamento", cls="suggestion-chip", type="button",
                   onclick="document.getElementById('user-input').value='Como fazer agendamento de consultas?'; document.getElementById('user-input').form.requestSubmit();"),
            Button("❓ Objeções comuns", cls="suggestion-chip", type="button",
                   onclick="document.getElementById('user-input').value='Quais são as objeções mais comuns e como responder?'; document.getElementById('user-input').form.requestSubmit();"),
            cls="suggestions-container"
        ),

        Div(
            Div(
                "💡 Dica: Seja específico sobre sua situação para respostas mais precisas",
                cls="input-hint"
            ),
            Div(
                Input(
                    name="user_input",
                    id="user-input",
                    placeholder="Digite sua dúvida...",
                    cls="input-msg",
                    hx_on="keydown: if(event.key==='Enter'){ this.form.requestSubmit(); event.preventDefault(); }"
                ),

                Button(
                    "Enviar",
                    cls="btn-enviar",
                    id="btn-enviar",
                    type="submit"
                ),
                cls="input-container"
            ),
            cls="input-area"
        ),
        hx_post="/send",
        hx_target="#chat-box",
        hx_swap="beforeend",

        hx_on="""
            htmx:beforeRequest:
                const btn = document.getElementById('btn-enviar');
                btn.classList.add('btn-loading');
                btn.textContent = 'Enviando';
                document.getElementById('user-input').value = '';
                
                const chat = document.getElementById('chat-box');
                const typing = document.createElement('div');
                typing.className = 'typing-indicator';
                typing.id = 'typing-indicator';
                typing.innerHTML = '<span>MedTrainer está digitando</span><div class="typing-dots"><div></div><div></div><div></div></div>';
                chat.appendChild(typing);
                chat.scrollTop = chat.scrollHeight;
            htmx:afterRequest:
                const btn = document.getElementById('btn-enviar');
                btn.classList.remove('btn-loading');
                btn.textContent = 'Enviar';
                
                const typing = document.getElementById('typing-indicator');
                if(typing) typing.remove();
                
                const chat = document.getElementById('chat-box');
                chat.scrollTop = chat.scrollHeight;
            """,

        )
        )
        

def formatar_resposta(texto):
    texto = html.escape(texto)
    
    # Markdown headers
    texto = re.sub(r'###\s*(.+)', r'<h3>\1</h3>', texto)
    texto = re.sub(r'##\s*(.+)', r'<h2>\1</h2>', texto)
    texto = re.sub(r'#\s*(.+)', r'<h1>\1</h1>', texto)
    
    # Bold e Italic
    texto = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', texto)
    texto = re.sub(r'\*(.+?)\*', r'<em>\1</em>', texto)
    
    # Code blocks
    texto = re.sub(r'```([\s\S]+?)```', r'<pre><code>\1</code></pre>', texto)
    texto = re.sub(r'`(.+?)`', r'<code>\1</code>', texto)
    
    # Listas
    texto = re.sub(r'^\s*[-*]\s+(.+)$', r'<li>\1</li>', texto, flags=re.MULTILINE)
    texto = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', texto, flags=re.DOTALL)
    texto = re.sub(r'</ul>\s*<ul>', '', texto)
    
    # Parágrafos
    texto = re.sub(r'\n\n+', '</p><p>', texto)
    if not texto.startswith('<'):
        texto = f'<p>{texto}</p>'
    
    return texto

@rt('/send', methods=["POST"])
def send(user_input: str="", perfil: str=""):
    print(f"DEBUG: Recebido input: {user_input} com perfil: {perfil}")
    if not user_input:
        return Div("Por favor, digite uma mensagem.", cls="bot-msg")
    
    hora_atual = datetime.now().strftime("%H:%M")

    try:
        response = requests.post("http://localhost:8000/chat",
                                json={"message": user_input,
                                        "perfil": perfil,}
                                )

        resposta = response.json().get("response", "Erro ao obter resposta do servidor.")
        resposta_formatada = formatar_resposta(resposta)

        return Div(
                Div(
                    Span(f"[{hora_atual}]", cls="timestamp"),
                    Span(f"Você: {user_input}"),
                    cls="user-msg"
                ),
                Div(
                    Span(f"[{hora_atual}]", cls="timestamp"),
                    NotStr(f"MedTrainer: {resposta_formatada}"),
                    cls="bot-msg"
                ),
                cls="message-group"
        )
    except Exception as e:
        resposta = f"Erro: {str(e)}"

    resposta_formatada = formatar_resposta(resposta)
    return Div(
        Div(
            Span(f"[{hora_atual}]", cls="timestamp"),
            Span(f"Você: {user_input}"),
            cls="user-msg"
        ),
        Div(
            Span(f"[{hora_atual}]", cls="timestamp"),
            NotStr(f"MedTrainer: {resposta_formatada}"),
            cls="bot-msg"
        ),
        cls="message-group"
    )
if __name__ == "__main__":
    serve()
