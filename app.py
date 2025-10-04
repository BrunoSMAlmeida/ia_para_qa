# Importar as funções do Flask que usaremos no projeto #

from flask import Flask, render_template, request
from ia_service import gerar_cenarios_gherkin

# Criar a instância do aplicativo Flask #
# __name__ diz ao Flask onde procurar por arquivos #

app = Flask(__name__)


# Agora vamos definir a rota principal ('/') e o modo de acesso GET #

@app.route('/', methods=['GET'])
def index():
    # 'render_template' busca os arquivos dentro da pasta templates/
    return render_template('index.html')


# Agora vamos gerar uma rota POST, onde iremos inserir algo e ter um retorno confirmando.

"""Vamos usar request.form.get() para acessar o valor do campo de nome "description" no HTML"""


@app.route('/generate', methods=['POST'])
def generate_gherkin():
    feature_description = request.form.get('description')
    """Vamos agora criar uma mensagem de erro básica
    Nessa mensagem, toda vez que o usuário clicar no botão de gerar cenários sem ter preenchido nada
    vai retornar uma mensagem de erro pedindo pra preencher o campo em si com um erro 400"""
    if not feature_description:
        return 'Erro: Nenhuma descrição de funcionalidade fornecida', 400
    return f"""
        <h1> Sucesso! Dado Recebido</h1>
        <p> O Dado recebido foi: </p>
        <pre>{feature_description}</pre>
        <p> A próxima etapa é enviar esse texto para a IA</p>
        <p><a href="/">Voltar</a></p> 
        """

# Aqui criaremos uma condição para rodar o servidor.
# Usaremos também 'debug=true' para reiniciar a cada mudança

if __name__ == '__main__':
    app.run(debug=True);
