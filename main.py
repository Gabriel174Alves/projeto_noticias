import os
import requests
import json
from flask import Flask, jsonify, send_from_directory
from dotenv import load_dotenv
from google import genai

# Carrega as chaves do arquivo .env
load_dotenv()

app = Flask(__name__, static_folder='static')

# Configuração dos Clientes (Usa a nova SDK google-genai instalada globalmente)
# Certifique-se de que as chaves no seu .env estão corretas
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

@app.route('/')
def index():
    # Serve o arquivo HTML da pasta static
    return send_from_directory('static', 'index.html')

@app.route('/api/noticias/<tema>')
def buscar_noticias(tema):
    # 1. Busca notícias reais na NewsAPI
    url = f"https://newsapi.org/v2/everything?q={tema}&language=pt&pageSize=5&apiKey={NEWS_API_KEY}"
    try:
        res = requests.get(url).json()
        artigos = res.get('articles', [])
    except Exception as e:
        print(f"❌ Erro NewsAPI: {e}")
        return jsonify({"erro": "Falha ao buscar notícias"}), 500

    resultados = []
    for art in artigos:
        # 2. IA analisa com Prompt Rigoroso para evitar apenas resultados 'Neutros'
        prompt = (
            f"Analise criticamente a notícia: '{art['title']}'.\n"
            f"Classifique o impacto como POSITIVO, NEGATIVO ou NEUTRO.\n"
            f"Seja rigoroso e tome uma decisão. Dê uma nota de relevância de 0 a 10.\n"
            f"Responda APENAS o JSON puro: {{'sentimento': 'VALOR', 'relevancia': NOTA}}"
        )
        
        try:
            # Chama o modelo Gemini 2.0 Flash
            response = client.models.generate_content(
                model="gemini-2.0-flash", 
                contents=prompt
            )
            
            # Limpa e converte a resposta da IA
            texto_ia = response.text.replace('```json', '').replace('```', '').strip()
            analise = json.loads(texto_ia)
            
            # Força o sentimento para maiúsculas para bater com o filtro do JS
            sentimento_final = analise.get('sentimento', 'NEUTRO').upper()
            
            print(f"✅ IA analisou: {art['title'][:30]}... -> {sentimento_final}")
            
        except Exception as e:
            # Se a IA falhar (Quota 429), define como NEUTRO para não travar o site
            print(f"⚠️ Erro na IA (provável limite de quota): {e}")
            sentimento_final = "NEUTRO"
            analise = {"relevancia": 5}

        resultados.append({
            "titulo": art['title'],
            "url": art['url'],
            "sentimento": sentimento_final,
            "relevancia": analise.get('relevancia', 5)
        })

    # Retorna o Top 3 organizado por relevância (nota da IA)
    top_3 = sorted(resultados, key=lambda x: x['relevancia'], reverse=True)[:3]
    return jsonify(top_3)

if __name__ == "__main__":
    print("🚀 Servidor Monitor de IA rodando em http://127.0.0.1:5000")
    # debug=True permite que o servidor reinicie sozinho ao salvar o arquivo
    app.run(debug=True, port=5000)