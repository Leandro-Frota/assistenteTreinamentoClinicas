from fasthtml.common import *
import requests
import re
import html
from datetime import datetime

app, rt = fast_app()

@rt('/')
def home():
    return Div(
        Style("""
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background: #f7f7f8;
            height: 100vh;
            width: 100vw;
            overflow: hidden;
        }
        
        .app-container {
            display: flex;
            height: 100vh;
            width: 100vw;
        }
        
        /* ========== SIDEBAR ========== */
        .sidebar {
            width: 260px;
            background: #202123;
            color: #ececf1;
            display: flex;
            flex-direction: column;
            border-right: 1px solid #4d4d4f;
            flex-shrink: 0;
        }
        
        .sidebar-header {
            padding: 16px 12px;
            border-bottom: 1px solid #4d4d4f;
        }
        
        .sidebar-header h2 {
            font-size: 1.1em;
            font-weight: 600;
            color: #ececf1;
            margin-bottom: 4px;
        }
        
        .sidebar-header p {
            font-size: 0.75em;
            color: #8e8ea0;
        }
        
        .sidebar-content {
            flex: 1;
            overflow-y: auto;
            padding: 12px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        
        .new-chat-btn {
            width: 100%;
            padding: 12px 16px;
            background: transparent;
            border: 1px solid #4d4d4f;
            color: #ececf1;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9em;
            font-weight: 500;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 16px;
        }
        
        .new-chat-btn:hover {
            background: #2a2b32;
        }
        
        .conversations-section {
            margin-top: 8px;
        }
        
        .conversations-section h3 {
            font-size: 0.75em;
            color: #8e8ea0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            margin-top: 16px;
            padding: 0 8px;
        }
        
        .empty-state {
            font-size: 0.85em;
            color: #8e8ea0;
            padding: 12px 8px;
            text-align: center;
            font-style: italic;
        }
        
        .sidebar-footer {
            padding: 12px;
            border-top: 1px solid #4d4d4f;
        }
        
        .feature-btn {
            width: 100%;
            padding: 10px 16px;
            background: transparent;
            border: 1px solid #4d4d4f;
            color: #ececf1;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85em;
            font-weight: 500;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 10px;
            text-align: left;
        }
        
        .feature-btn:hover {
            background: #2a2b32;
            border-color: #10a37f;
        }
        
        .feature-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .feature-btn:disabled:hover {
            background: transparent;
            border-color: #4d4d4f;
        }
        
        .features-section {
            margin-top: 8px;
        }
        
        .features-section h3 {
            font-size: 0.75em;
            color: #8e8ea0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            padding: 0 8px;
        }
        
        .user-profile {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 12px;
            background: #2a2b32;
            border-radius: 6px;
            border: 1px solid #4d4d4f;
        }
        
        .user-avatar {
            width: 36px;
            height: 36px;
            background: #10a37f;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1em;
            font-weight: 600;
            color: white;
            flex-shrink: 0;
        }
        
        .user-info {
            flex: 1;
            min-width: 0;
        }
        
        .user-name {
            font-size: 0.9em;
            font-weight: 600;
            color: #ececf1;
            margin-bottom: 2px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        .user-role {
            font-size: 0.75em;
            color: #8e8ea0;
        }
        
        .perfil-selector {
            width: 100%;
            padding: 10px 12px;
            background: #2a2b32;
            border: 1px solid #4d4d4f;
            border-radius: 6px;
            margin-bottom: 10px;
        }
        
        .perfil-selector label {
            display: block;
            font-size: 0.75em;
            color: #8e8ea0;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        #perfil {
            width: 100%;
            padding: 8px;
            background: #40414f;
            border: 1px solid #4d4d4f;
            border-radius: 4px;
            color: #ececf1;
            font-size: 0.9em;
            cursor: pointer;
        }
        
        #perfil option {
            background: #40414f;
            color: #ececf1;
        }
        
        .status-info {
            display: flex;
            flex-direction: column;
            gap: 6px;
            font-size: 0.8em;
            color: #8e8ea0;
            margin-bottom: 12px;
        }
        
        .status-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .status-online {
            color: #10a37f;
            font-weight: 600;
        }
        
        /* ========== CHAT AREA ========== */
        .chat-area {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: #f7f7f8;
            position: relative;
            height: 100vh;
            width: 100%;
            overflow: hidden;
        }
        
        .messages-container {
            flex: 1;
            overflow-y: auto;
            overflow-x: hidden;
            padding: 20px;
            padding-bottom: 200px;
            display: flex;
            flex-direction: column;
            min-height: 0;
        }
        
        .messages-container::-webkit-scrollbar {
            width: 8px;
        }
        
        .messages-container::-webkit-scrollbar-track {
            background: transparent;
        }
        
        .messages-container::-webkit-scrollbar-thumb {
            background: #d1d5db;
            border-radius: 4px;
        }
        
        .messages-container::-webkit-scrollbar-thumb:hover {
            background: #9ca3af;
        }
        
        /* ========== MESSAGES ========== */
        .message-group {
            margin-bottom: 20px;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        
        .user-msg-wrapper {
            display: flex;
            justify-content: flex-end;
        }
        
        .user-msg {
            background: #f7f7f8;
            color: #353740;
            padding: 12px 16px;
            border-radius: 12px;
            max-width: 90%;
            word-wrap: break-word;
            border: 1px solid #e5e5e5;
        }
        
        .bot-msg-wrapper {
            display: flex;
            justify-content: flex-start;
        }
        
        .bot-msg {
            background: #ffffff;
            color: #353740;
            padding: 16px 20px;
            border-radius: 12px;
            max-width: 90%;
            word-wrap: break-word;
            line-height: 1.6;
            border: 1px solid #e5e5e5;
        }
        
        .timestamp {
            font-size: 0.7em;
            color: #8e8ea0;
            margin-bottom: 4px;
            display: block;
        }
        
        .welcome-msg {
            background: #ffffff !important;
            border: 1px solid #e5e5e5 !important;
            padding: 24px !important;
            margin-bottom: 24px;
            max-width: 100% !important;
        }
        
        .welcome-msg h3 {
            margin: 0 0 12px 0;
            color: #353740;
            font-size: 1.3em;
        }
        
        .welcome-msg p {
            margin: 8px 0;
            color: #565869;
        }
        
        .welcome-msg ul {
            margin: 12px 0;
            padding-left: 24px;
        }
        
        .welcome-msg li {
            margin: 6px 0;
            color: #565869;
        }
        
        .welcome-examples {
            background: #f7f7f8;
            padding: 12px;
            border-radius: 6px;
            margin-top: 12px;
            font-style: italic;
            color: #8e8ea0;
            font-size: 0.9em;
        }
        
        .typing-indicator {
            display: flex;
            align-items: center;
            gap: 8px;
            background: #ffffff;
            padding: 12px 16px;
            border-radius: 12px;
            max-width: 150px;
            border: 1px solid #e5e5e5;
        }
        
        .typing-indicator span {
            font-size: 0.85em;
            color: #8e8ea0;
        }
        
        .typing-dots {
            display: flex;
            gap: 4px;
        }
        
        .typing-dots div {
            width: 6px;
            height: 6px;
            background: #10a37f;
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
            0%, 60%, 100% { transform: translateY(0); opacity: 0.5; }
            30% { transform: translateY(-8px); opacity: 1; }
        }
        
        /* ========== MESSAGE FORMATTING ========== */
        .bot-msg h1, .bot-msg h2, .bot-msg h3 {
            margin: 12px 0 8px 0;
            color: #353740;
        }
        
        .bot-msg h1 { font-size: 1.3em; }
        .bot-msg h2 { font-size: 1.2em; }
        .bot-msg h3 { font-size: 1.1em; }
        
        .bot-msg ul, .bot-msg ol {
            margin: 8px 0;
            padding-left: 24px;
        }
        
        .bot-msg li {
            margin: 4px 0;
        }
        
        .bot-msg p {
            margin: 8px 0;
        }
        
        .bot-msg code {
            background: #f7f7f8;
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            color: #eb5757;
        }
        
        .bot-msg pre {
            background: #f7f7f8;
            padding: 12px;
            border-radius: 6px;
            overflow-x: auto;
            margin: 10px 0;
        }
        
        .bot-msg pre code {
            background: none;
            padding: 0;
            color: #353740;
        }
        
        .bot-msg strong {
            font-weight: 600;
            color: #353740;
        }
        
        .bot-msg em {
            font-style: italic;
        }
        
        /* ========== INPUT AREA ========== */
        .input-area {
            background: #f7f7f8;
            padding: 10px 20px;
            border-top: 1px solid #e5e5e5;
            flex-shrink: 0;
            position: fixed;
            bottom: 0;
            left: 260px;
            right: 0;
            z-index: 100;
        }
        
        .input-container-wrapper {
            max-width: 100%;
            margin: 0 auto;
        }
        
        .suggestions-container {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 6px;
        }
        
        .suggestion-chip {
            background: #ffffff;
            border: 1px solid #e5e5e5;
            padding: 8px 14px;
            border-radius: 20px;
            font-size: 0.85em;
            cursor: pointer;
            transition: all 0.2s;
            white-space: nowrap;
            color: #353740;
        }
        
        .suggestion-chip:hover {
            background: #f7f7f8;
            border-color: #10a37f;
            transform: translateY(-1px);
        }
        
        .input-hint {
            font-size: 0.75em;
            color: #8e8ea0;
            margin-bottom: 6px;
        }
        
        .input-wrapper {
            display: flex;
            gap: 8px;
            align-items: center;
            background: #ffffff;
            border: 1px solid #e5e5e5;
            border-radius: 12px;
            padding: 8px 12px;
            transition: border-color 0.2s;
        }
        
        .input-wrapper:focus-within {
            border-color: #10a37f;
            box-shadow: 0 0 0 3px rgba(16, 163, 127, 0.1);
        }
        
        .input-msg {
            flex: 1;
            border: none;
            outline: none;
            font-size: 1em;
            color: #353740;
            background: transparent;
            resize: none;
            font-family: inherit;
            min-height: 24px;
            max-height: 120px;
        }
        
        .input-msg::placeholder {
            color: #8e8ea0;
        }
        
        .btn-enviar {
            flex:0;
            background: #10a37f;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 500;
            font-size: 0.9em;
            transition: all 0.2s;
            white-space: nowrap;
            flex-shrink: 0;
        }
        
        .btn-enviar:hover {
            background: #0d8c6a;
        }
        
        .btn-enviar:disabled {
            background: #d1d5db;
            cursor: not-allowed;
        }
        
        .btn-loading {
            background: #fbbf24 !important;
            cursor: wait;
        }
        
        .btn-loading::after {
            content: '...';
            animation: dots 1.5s infinite;
        }
        
        @keyframes dots {
            0%, 20% { content: '.'; }
            40% { content: '..'; }
            60%, 100% { content: '...'; }
        }
        
        /* ========== RESPONSIVE ========== */
        @media (max-width: 768px) {
            .sidebar {
                position: fixed;
                left: -260px;
                top: 0;
                height: 100vh;
                z-index: 1000;
                transition: left 0.3s;
            }
            
            .input-area {
                left: 0;
            }
            
            .user-msg, .bot-msg {
                max-width: 90%;
            }
            
            .input-container-wrapper {
                max-width: 100%;
            }
        }
        """),
        
        Div(
            # ========== SIDEBAR ==========
            Div(
                Div(
                    H2("MedTrainer"),
                    P("Assistente de Treinamento"),
                    cls="sidebar-header"
                ),
                
                Div(
                    Button(
                        "✚ Novo Chat",
                        cls="new-chat-btn",
                        type="button",
                        onclick="window.location.reload();"
                    ),
                    
                    Div(
                        # H3("Funcionalidades"),
                        Button(
                            Span("📊"),
                            Span("Avaliação de Desempenho"),
                            cls="feature-btn",
                            type="button",
                            disabled=True,
                            title="Em breve"
                        ),
                        Button(
                            Span("📽️"),
                            Span("Gerar Apresentação"),
                            cls="feature-btn",
                            type="button",
                            disabled=True,
                            title="Em breve"
                        ),
                        cls="features-section"
                    ),
                    
                    # Div(
                    #     H3("Conversas"),
                    #     P("Nenhuma conversa salva ainda", cls="empty-state"),
                    #     cls="conversations-section"
                    # ),
                    
                    cls="sidebar-content"
                ),
                
                Div(
                    Div(
                        Div(
                            Span("●", cls="status-online"),
                            Span("Online"),
                            cls="status-item"
                        ),
                        cls="status-info"
                    ),
                    
                    Div(
                        Label("Perfil do Usuário", **{"for": "perfil"}),
                        Select(
                            Option("Atendente"),
                            Option("Recepcionista"),
                            Option("Supervisor"),
                            id="perfil",
                            name="perfil"
                        ),
                        cls="perfil-selector"
                    ),
                    
                    Div(
                        Div(
                            Span("A"),
                            cls="user-avatar"
                        ),
                        Div(
                            Div("Leandro Frota", cls="user-name", id="user-display-name"),
                            Div("Usuário logado", cls="user-role"),
                            cls="user-info"
                        ),
                        cls="user-profile"
                    ),
                    
                    cls="sidebar-footer"
                ),
                
                cls="sidebar"
            ),
            
            # ========== CHAT AREA ==========
            Form(
                Div(
                    Div(
                        Div(
                            H3("Olá! Sou o MedTrainer"),
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
                        cls="messages-container"
                    ),
                    
                    Div(
                        Div(
                            Div(
                                Button(
                                    "📋 Fluxo de atendimento",
                                    cls="suggestion-chip",
                                    type="button",
                                    onclick="document.getElementById('user-input').value='Como funciona o fluxo de atendimento?'; document.getElementById('user-input').form.requestSubmit();"
                                ),
                                Button(
                                    "💬 Scripts WhatsApp",
                                    cls="suggestion-chip",
                                    type="button",
                                    onclick="document.getElementById('user-input').value='Me mostre scripts prontos para WhatsApp'; document.getElementById('user-input').form.requestSubmit();"
                                ),
                                Button(
                                    "📞 Agendamento",
                                    cls="suggestion-chip",
                                    type="button",
                                    onclick="document.getElementById('user-input').value='Como fazer agendamento de consultas?'; document.getElementById('user-input').form.requestSubmit();"
                                ),
                                Button(
                                    "❓ Objeções comuns",
                                    cls="suggestion-chip",
                                    type="button",
                                    onclick="document.getElementById('user-input').value='Quais são as objeções mais comuns e como responder?'; document.getElementById('user-input').form.requestSubmit();"
                                ),
                                cls="suggestions-container"
                            ),
                            
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
                                    hx_on="keydown: if(event.key==='Enter' && !event.shiftKey){ this.form.requestSubmit(); event.preventDefault(); }"
                                ),
                                Button(
                                    "Enviar",
                                    cls="btn-enviar",
                                    id="btn-enviar",
                                    type="submit"
                                ),
                                cls="input-wrapper"
                            ),
                            
                            cls="input-container-wrapper"
                        ),
                        cls="input-area"
                    ),
                    
                    cls="chat-area"
                ),
                
                hx_post="/send",
                hx_target="#chat-box",
                hx_swap="beforeend",
                hx_on="""
                    htmx:beforeRequest:
                        const btn = document.getElementById('btn-enviar');
                        btn.classList.add('btn-loading');
                        btn.textContent = 'Enviando';
                        btn.disabled = true;
                        document.getElementById('user-input').value = '';
                        
                        const chat = document.getElementById('chat-box');
                        const typing = document.createElement('div');
                        typing.className = 'typing-indicator';
                        typing.id = 'typing-indicator';
                        typing.innerHTML = '<span>Digitando</span><div class="typing-dots"><div></div><div></div><div></div></div>';
                        chat.appendChild(typing);
                        chat.scrollTop = chat.scrollHeight;
                    htmx:afterRequest:
                        const btn = document.getElementById('btn-enviar');
                        btn.classList.remove('btn-loading');
                        btn.textContent = 'Enviar';
                        btn.disabled = false;
                        
                        const typing = document.getElementById('typing-indicator');
                        if(typing) typing.remove();
                        
                        const chat = document.getElementById('chat-box');
                        chat.scrollTop = chat.scrollHeight;
                """
            ),
            
            cls="app-container"
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
        return Div(
            Div(
                Span("Por favor, digite uma mensagem."),
                cls="bot-msg"
            ),
            cls="bot-msg-wrapper"
        )
    
    hora_atual = datetime.now().strftime("%H:%M")

    try:
        response = requests.post("http://localhost:8000/chat",
                                json={"message": user_input,
                                        "perfil": perfil}
                                )

        resposta = response.json().get("response", "Erro ao obter resposta do servidor.")
        resposta_formatada = formatar_resposta(resposta)

        return Div(
            Div(
                Div(
                    Span(f"[{hora_atual}]", cls="timestamp"),
                    Span(f"Você: {user_input}"),
                    cls="user-msg"
                ),
                cls="user-msg-wrapper"
            ),
            Div(
                Div(
                    Span(f"[{hora_atual}]", cls="timestamp"),
                    NotStr(f"MedTrainer: {resposta_formatada}"),
                    cls="bot-msg"
                ),
                cls="bot-msg-wrapper"
            ),
            cls="message-group"
        )
    except Exception as e:
        resposta = f"Erro: {str(e)}"
        resposta_formatada = formatar_resposta(resposta)
        
        return Div(
            Div(
                Div(
                    Span(f"[{hora_atual}]", cls="timestamp"),
                    Span(f"Você: {user_input}"),
                    cls="user-msg"
                ),
                cls="user-msg-wrapper"
            ),
            Div(
                Div(
                    Span(f"[{hora_atual}]", cls="timestamp"),
                    NotStr(f"MedTrainer: {resposta_formatada}"),
                    cls="bot-msg"
                ),
                cls="bot-msg-wrapper"
            ),
            cls="message-group"
        )


if __name__ == "__main__":
    serve()
