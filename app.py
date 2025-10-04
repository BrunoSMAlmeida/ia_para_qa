# 🐍 app.py

from flask import Flask, render_template, request
from ia_service import gerar_cenarios_gherkin # Importa a função que comunica com o Gemini

app = Flask(__name__) 

@app.route('/', methods=['GET'])
def index():
    # Retorna o template 'index.html'. Na primeira visita, resultado=None.
    return render_template('index.html', resultado=None)

@app.route('/generate', methods=['POST'])
def generate_gherkin():
    
    # 1. CAPTURA O DADO
    feature_description = request.form.get('description') 

    # 2. TRATAMENTO DE ERRO BÁSICO (Se o campo estiver vazio)
    if not feature_description:
        return "Erro: Nenhuma descrição da funcionalidade fornecida.", 400 

    # 3. CHAMA A FUNÇÃO DE IA
    # Esta linha executa o código no ia_service.py, que se conecta ao Gemini.
    gherkin_output = gerar_cenarios_gherkin(feature_description) 
    
    # 4. RENDERIZAÇÃO
    # Retorna o template, passando o texto gerado ou a mensagem de erro formatada.
    return render_template('index.html', resultado=gherkin_output)

if __name__ == '__main__':
    # Roda o servidor. debug=True faz ele reiniciar a cada mudança.
    app.run(debug=True)
