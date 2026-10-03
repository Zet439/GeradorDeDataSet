"""Geração de frases originais via LLM local (Ollama)."""
import ollama
from config import MODEL_NAME, OLLAMA_HOST, PROMPT_GERAR_FRASE, CONTEXTOS


class GeradorFrases:
    def __init__(self):
        self.client = ollama.Client(host=OLLAMA_HOST)

    def gerar_uma(self, categoria: str, max_tentativas: int = 3) -> str:
        contexto = CONTEXTOS.get(categoria, "conversa cotidiana comum")
        prompt = PROMPT_GERAR_FRASE.format(categoria=categoria, contexto=contexto)
        for tentativa in range(max_tentativas):
            try:
                resposta = self.client.chat(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    options={"temperature": 0.95, "num_predict": 150},
                )
                frase = resposta["message"]["content"].strip()
                frase = frase.strip('"').strip("'").strip()
                return frase
            except Exception as e:
                print(f"  [erro tentativa {tentativa+1}] {e}")
        return ""