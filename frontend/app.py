from fasthtml.common import *
import requests
import re
import html

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
            font-family: Arial;
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
            max-width: 1200px;
            height: 100vh;
            padding: 20px;
            display: flex;
            flex-direction: column;
        }
        
        h1 {
            margin-bottom: 10px;
        }
        
        p {
            margin-bottom: 10px;
        }
        
        #perfil {
            margin-bottom: 15px;
            padding: 8px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }

        .chat-box {
            border: 1px solid #ddd;
            padding: 15px;
            flex: 1;
            overflow-y: auto;
            background: white;
            display: flex;
            flex-direction: column;
            margin-bottom: 10px;
        }

        .user-msg {
            align-self: flex-end;
            background: #007bff;
            color: white;
            padding: 10px;
            border-radius: 10px;
            max-width: 70%;
            word-wrap: break-word;
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
        .input-msg {
            flex: 1;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #ccc;
            outline: none;
        }
        .btn-enviar:hover {
            background-color: #0056b3;
        }
        .btn-enviar:active {
            background-color: #28a745;
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
        }
        .btn-loading {
            background-color: #ffc107 !important;
        }
        .message-group {
            margin-bottom: 15px;
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        """),
    Form(
        H1 ( "MedTrainer - Assistente de Treinamento para Clínicas Geriátricas" ),

        P("Treinamento para profissionais de clínicas médicas geriátricas"),

        Select(
            Option("Atendente"),
            Option("Recepcionista"),
            Option("Supervisor"),
            id="perfil",
            name = "perfil"
        ),

        Div(id="chat-box",cls="chat-box"),

        Div(
            Input(
                name="user_input",
                id="user-input",
                placeholder="Digite sua mensagem...",
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
        hx_post="/send",
        hx_target="#chat-box",
        hx_swap="beforeend",

        hx_on="""
            htmx:beforeRequest:
                document.getElementById('user-input').value = '';
                document.getElementById('btn-enviar').classList.add('btn-loading');
            htmx:afterRequest:
                document.getElementById('btn-enviar').classList.remove('btn-loading');
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
    

    try:
        response = requests.post("http://localhost:8000/chat",
                                json={"message": user_input,
                                        "perfil": perfil,}
                                )

        resposta = response.json().get("response", "Erro ao obter resposta do servidor.")
        resposta_formatada = formatar_resposta(resposta)

        return Div(
                Div(f"Você: {user_input}", cls="user-msg"),
                Div(NotStr(f"MedTrainer: {resposta_formatada}"), cls="bot-msg"),
                cls="message-group"
        )
    except Exception as e:
        resposta = f"Erro: {str(e)}"

    resposta_formatada = formatar_resposta(resposta)
    return Div(
        Div(
            Div(f"Você: {user_input}", cls="user-msg"),
            Div(NotStr(f"MedTrainer: {resposta_formatada}"), cls="bot-msg"),
            cls="message-group"
        )
    )
if __name__ == "__main__":
    serve()