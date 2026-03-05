# 🔍 Monitor de Sentimentos com IA (Gemini 2.0 Flash)

Este projeto é um dashboard em Flask que monitora notícias em tempo real via **NewsAPI** e utiliza a inteligência artificial do **Google (Gemini)** para classificar o impacto das manchetes como Positivo, Negativo ou Neutro.

## 🛠️ Tecnologias
- **Python 3.14**
- **Flask** (Servidor Web)
- **Google GenAI SDK** (IA de processamento de linguagem)
- **NewsAPI** (Fonte de dados em tempo real)

## ⚡ Desafios Superados
Durante o desenvolvimento, lidei com conflitos de dependências no Windows (Erro: ResolutionImpossible) e superei a necessidade de compiladores externos (Rust/C++) utilizando instalações de pacotes puramente binários (`--only-binary`). 

## ⚙️ Como rodar
1. Instale as dependências: `pip install flask requests python-dotenv google-genai`
2. Configure suas chaves no arquivo `.env`
3. Execute: `python main.py`