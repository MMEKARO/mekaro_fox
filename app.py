from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import speech_recognition as sr
import os

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar o app Flask
app = Flask(__name__)
CORS(app)

# Inicializando o cliente Groq com a chave de API
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Configurando o template da conversa
template = """Você é um assistente de aprendizado de inglês.
Responda em inglês, corrija erros e explique de maneira amigável.

Input: {input}
"""
base_prompt = PromptTemplate(input_variables=["input"], template=template)

# Configurando a memória de conversação
memory = ConversationBufferMemory(memory_key="chat_history", input_key='input')

# Rota principal para carregar o frontend
@app.route('/')
def index():
    return render_template('index.html')

# Rota para transcrição de áudio
@app.route('/transcrever_audio', methods=['POST'])
def transcrever_audio():
    try:
        recognizer = sr.Recognizer()
        audio_file = request.files['file']

        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='en-US')

        return jsonify({"transcricao": text})

    except Exception as e:
        return jsonify({"error": str(e)})

# Rota para interação com a IA (Groq)
@app.route('/conversar', methods=['POST'])
def conversar():
    data = request.json
    user_input = data.get("message")

    try:
        # Prepara as mensagens para a API do Groq
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": user_input}],
            model="gemma2-9b-it"
        )

        resposta_ia = response.choices[0].message.content
        return jsonify({"resposta": resposta_ia})

    except Exception as e:
        return jsonify({"error": str(e)})

# Executar o app
if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
