import os
from google import genai
from google.genai.errors import APIError

"""O cliente do Gemini, sempre procura a chave na variável de ambiente.
É o método mais seguro, pois não fica no código fonte."""

"""Tenta criar o cliente Gemini. Se a chave não estiver na váriavel de ambiente
(GEMINI_API_KEY), este bloco falhará e cairá no except"""
try:
    client = genai.Client()
except Exception as e:
    """Se falhar, gera um log e define o client como none"""
    print(f'ERRO DE INICIALIZAÇÃO: Falha ao inicializar o cliente Gemini. Verifique a variável GEMINI_API_KEY: {e}')
    client = None


def gerar_cenarios_gherkin(feature_description):
    """
    Envia uma descrição da funcionalidade para o Gemini e retorna o texto em Gherkin
    Args:
        feature_description(str): A descrição da funcionalidade em linguagem natural
    Returns:
        str: O texto Gherkin gerado ou uma mensagem de erro Gherkin formatada.
    """
    # Verifica se o client foi inicializado lá no bloco acima
    if client is None:
        return """Feature: Erro de configuração da API
        Scenario: Chave da API ausente ou inválida:
        Dado que a variável de ambiente GEMINI_API_KEY não foi configurada
        Então o serviço de IA deve falhar na inicialização.
    """

    # Instrução detalhada para a IA. Quanto mais clara, melhor.

    prompt=f""" 
    Aja como um especialista em BDD para um time de QA
    Gere cenários de testes em Gherkin (Dado/Quando/Então)
    para a seguinte funcionalidade {feature_description}
    Inclua um cenário positivo e pelo menos um negativo (erro ou falha)
    Retorne os testes em Gherkin e explicando o que cada testes irá cobrir.
    Use a linguagem Gherkin em Português"""


try:
    response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                temperature=0.7
        )
    )


