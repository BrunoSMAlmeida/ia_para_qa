import os
# Importa o SDK principal do Google para interagir com o Gemini
from google import genai
# Importa o tipo de erro específico do SDK, essencial para tratamento de falhas
from google.genai.errors import APIError 

# ==============================================================================
# 1. INICIALIZAÇÃO E SEGURANÇA (PRÁTICA DEVOPS/SRE)
# ==============================================================================

# O SDK do Gemini automaticamente procura a chave na variável de ambiente.
# Este é o método mais seguro, pois a chave não fica no código-fonte.
try:
    # Tenta criar o cliente Gemini. Se a chave não estiver na variável de ambiente
    # (GEMINI_API_KEY), este bloco falhará, o que será capturado pelo 'except'.
    client = genai.Client()
except Exception as e:
    # Se falhar, registra o erro (como um log de SRE) e define o cliente como None.
    print(f"ERRO DE CONFIGURAÇÃO: Falha ao inicializar o cliente Gemini. Verifique a variável GEMINI_API_KEY: {e}")
    client = None


# ==============================================================================
# 2. FUNÇÃO PRINCIPAL PARA GERAÇÃO DE GHERKIN
# ==============================================================================

def gerar_cenarios_gherkin(feature_description):
    """
    Envia uma descrição de funcionalidade para o Gemini e retorna o texto Gherkin.
    
    Args:
        feature_description (str): A descrição da funcionalidade em linguagem natural.
        
    Returns:
        str: O texto Gherkin gerado ou uma mensagem de erro Gherkin formatada.
    """
    
    # 2.1. TRATAMENTO DE ERRO DE CONFIGURAÇÃO (RESILIÊNCIA)
    # Verifica se o cliente foi inicializado corretamente no bloco acima.
    if client is None:
        return """Feature: Erro de Configuração da API
  Scenario: Chave da API Ausente ou Inválida
    Dado que a variável de ambiente GEMINI_API_KEY não foi configurada
    Então o serviço de IA deve falhar na inicialização."""
    
    # 2.2. DEFINIÇÃO DO PROMPT
    # Instrução detalhada para a IA. Quanto mais clara, melhor o resultado.
    prompt = f"""
    Aja como um especialista em BDD para um time de QA.
    Gere cenários de teste Gherkin (Dado/Quando/Então)
    para a seguinte funcionalidade: {feature_description}
    Inclua um cenário positivo (sucesso) e pelo menos um negativo (erro/falha).
    Retorne APENAS o texto Gherkin completo, sem nenhuma saudação ou explicação adicional.
    Use a linguagem Gherkin em Português.
    """
    
    # 2.3. CHAMADA À API E TRATAMENTO DE EXCEÇÕES (SRE)
    try:
        # Usa o método 'generate_content' para enviar o prompt ao modelo.
        # O modelo 'gemini-2.5-flash' é rápido e ideal para tarefas de texto estruturado.
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                temperature=0.7 # Define a criatividade da IA (0.0=conservador, 1.0=criativo)
            )
        )
        
        # O resultado do texto gerado fica no atributo '.text' da resposta.
        return response.text
        
    except APIError as e:
        # Trata erros específicos da API (ex: excedeu o limite de uso, erro no token).
        print(f"ERRO DE API: Falha ao chamar a API Gemini: {e}")
        return f"""Feature: Erro de Comunicação com a IA
  Scenario: Falha no Serviço Gemini
    Dado que a chamada da API Gemini falhou
    Então deve retornar o erro de API: {e}"""
    
    except Exception as e:
        # Captura qualquer outro erro inesperado (ex: erro de rede).
        print(f"ERRO INESPERADO: {e}")
        return f"""Feature: Erro Inesperado
  Scenario: Falha Interna
    Dado que ocorreu um erro inesperado
    Então deve retornar o erro: {e}"""
