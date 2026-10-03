# Dataset de simplificação de frases cotidianas em português

Projeto em Python que gera frases em português brasileiro e versões
simplificadas usando um modelo local servido pelo [Ollama](https://ollama.com/).
O pipeline valida e remove pares duplicados antes de exportar os resultados.

## Requisitos

- Python 3.11
- [Ollama](https://ollama.com/) instalado e em execução
- Modelo `llama3.1:8b` disponível no Ollama

## Contexto e decisão do projeto

Esse projeto surgiu com a necessidade de criar um dataset específico de simplificação de mensagens de maneira extrativa se mantendo o contexto, visto que datasets públicos existentes não satisfaziam a necessidade conversacional, sendo a maioria de teor jornalístico.

### LLM local via Ollama

Em vez de depender de chaves da OpenAI/Anthropic, optamos por rodar a LLM localmente com Ollama, sendo motivado pela privacidade total, sem limites de requisição e execução offline.


### Implementação do checkpoint

Gerar dezenas de milhares de pares em CPU pode levar dezenas de horas. Para evitar perda total em caso de interrupção, implementamos um checkpoint automático a cada 50 registros, permitindo retomar exatamente de onde parou.

### Validação e deduplicação automáticas

Após a geração, um validador aplica filtros de qualidade:
- Tamanho mínimo da frase original (≥ 15 caracteres);
- Redução mínima de 10% no tamanho;
- Frase simplificada não vazia;
- Frase simplificada diferente da original;
- Remoção de duplicatas exatas.

### Conversor separado

Para se adaptar a outro projeto, um conversor específico para a compatibilidade com ele foi gerado, ele lê o checkpoint.json e produz os arquivos finais em csv e .jsonl com as colunas renomeadas para "original_sent" e "reduced_sent".

## Instalação

Clone o repositório e entre na pasta do projeto. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

No Windows (PowerShell), ative-o com:

```powershell
.venv\Scripts\Activate.ps1
```

Instale as dependências e baixe o modelo:

```bash
python -m pip install -r requirements.txt
ollama pull llama3.1:8b
```

O padrão do projeto conecta ao serviço Ollama em `http://localhost:11434`.
Se necessário, altere `OLLAMA_HOST` e `MODEL_NAME` em `config.py`.
Não é necessária uma chave de API nem um arquivo `.env`.

## Uso

Com o Ollama em execução, inicie a geração:

```bash
python main.py
```

O pipeline está configurado para gerar 1.000 pares em cada uma das 32
categorias (até 32.000 pares antes da validação). Ele salva o progresso em
`checkpoint.json` a cada 50 registros e pode continuar desse ponto se for
executado novamente após uma interrupção. O checkpoint é um arquivo local
intermediário e não deve ser publicado.

Ao concluir, os pares aprovados são gravados em:

- `dataset_simplificacao.csv`
- `dataset_simplificacao.jsonl`

Para validar e exportar os registros de um checkpoint existente sem executar
novamente a geração, use:

```bash
python converter.py
```

## Estrutura

- `main.py`: coordena geração, checkpoint, validação e exportação.
- `generator.py`: gera as frases originais usando o Ollama.
- `simplifier.py`: produz as versões simplificadas.
- `validator.py`: calcula métricas, valida e remove duplicatas.
- `config.py`: categorias, prompts, modelo e configurações do pipeline.
- `converter.py`: converte um checkpoint existente em arquivos de dados.
