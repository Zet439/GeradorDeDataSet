"""Configurações para geração em larga escala (32.000 linhas)."""

OLLAMA_HOST = "http://localhost:11434"
MODEL_NAME = "llama3.1:8b"

# 32 categorias × 1.000 frases = 32.000 linhas
CATEGORIAS = [
    # Saudações e despedidas
    "saudacao_formal", "saudacao_informal", "saudacao_telefonica",
    "saudacao_escrita", "despedida_formal", "despedida_informal",
    # Estado e sentimentos
    "pergunta_estado", "resposta_estado_positivo", "resposta_estado_negativo",
    "pergunta_saude", "pergunta_bem_estar",
    # Pedidos e instruções
    "pedido_educado", "instrucao_tecnica", "instrucao_rotina",
    "solicitacao_esclarecimento", "pedido_desculpa",
    # Social
    "convite_formal", "convite_informal", "agradecimento_formal",
    "agradecimento_informal", "elogio", "consolo",
    # Trabalho e atendimento
    "atendimento_cliente", "reclamacao educada", "negociacao",
    "agendamento", "confirmacao", "cancelamento",
    # Opinião e justificativa
    "opinia_positiva", "opinia_negativa", "justificativa_ausencia",
    "explicacao_situacao",
]

QTD_POR_CATEGORIA = 1000  # 30 × 1000 = 30.000

# Prompts com variação para aumentar diversidade
PROMPT_GERAR_FRASE = """
Gere UMA frase cotidiana em português brasileiro, natural e conversacional,
na categoria "{categoria}".

Contexto: {contexto}

A frase deve ser um pouco prolixa ou formal demais, como alguém falaria
em um contexto levemente polido. Retorne APENAS a frase, sem aspas ou
explicações. Varie bastante o vocabulário e a estrutura.
"""

PROMPT_SIMPLIFICAR = """
Simplifique a frase a seguir para soar mais natural, direta e cotidiana em
português brasileiro. Mantenha o sentido original e a cordialidade.
Regras:
- Elimine redundâncias.
- Prefira verbos diretos a construções longas.
- Reduza o tamanho em pelo menos 20% sem perder o sentido.

Frase original: "{frase}"

Retorne APENAS a frase simplificada, sem aspas ou explicações.
"""

# Contextos específicos para cada categoria (aumenta diversidade)
CONTEXTOS = {
    "saudacao_formal": "reunião de trabalho com alguém que você vê pela primeira vez",
    "saudacao_informal": "encontro casual com um amigo próximo no fim de semana",
    "saudacao_telefonica": "atendendo uma ligação de um conhecido",
    "saudacao_escrita": "abrindo um e-mail profissional",
    "despedida_formal": "encerrando uma reunião com clientes",
    "despedida_informal": "saindo de um bar com amigos",
    "pergunta_estado": "conversa com um colega de trabalho no café",
    "resposta_estado_positivo": "respondendo a um amigo próximo",
    "resposta_estado_negativo": "desabafando com alguém de confiança",
    "pergunta_saude": "ligando para um parente idoso",
    "pergunta_bem_estar": "conversando com um vizinho",
    "pedido_educado": "pedindo um favor a um colega",
    "instrucao_tecnica": "explicando como usar um aplicativo",
    "instrucao_rotina": "dando instruções domésticas",
    "solicitacao_esclarecimento": "não entendeu uma orientação no trabalho",
    "pedido_desculpa": "atrasou para um compromisso",
    "convite_formal": "convidando para um evento corporativo",
    "convite_informal": "convidando para um churrasco",
    "agradecimento_formal": "após uma entrevista de emprego",
    "agradecimento_informal": "após receber um presente de amigo",
    "elogio": "parabéns pelo trabalho bem feito",
    "consolo": "amigo passando por momento difícil",
    "atendimento_cliente": "vendedor falando com cliente na loja",
    "reclamacao educada": "cliente insatisfeito falando com gerente",
    "negociacao": "discutindo preço de um serviço",
    "agendamento": "marcando consulta médica por telefone",
    "confirmacao": "confirmando presença em evento",
    "cancelamento": "cancelando um serviço contratado",
    "opinia_positiva": "recomendando um restaurante",
    "opinia_negativa": "criticando um filme educadamente",
    "justificativa_ausencia": "explicando por que faltou a uma reunião",
    "explicacao_situacao": "contando o motivo de um atraso",
}

ARQUIVO_SAIDA_CSV = "dataset_simplificacao.csv"
ARQUIVO_SAIDA_JSONL = "dataset_simplificacao.jsonl"
CHECKPOINT_FILE = "checkpoint.json"  # para retomar em caso de queda