"""Geração das versões simplificadas via LLM local (Ollama)."""
import ollama
from config import MODEL_NAME, OLLAMA_HOST, PROMPT_SIMPLIFICAR


class Simplificador:
    def __init__(self):
        self.client = ollama.Client(host=OLLAMA_HOST)

    def simplificar(self, frase_original: str, max_tentativas: int = 3) -> str:
        prompt = PROMPT_SIMPLIFICAR.format(frase=frase_original)
        for tentativa in range(max_tentativas):
            try:
                resposta = self.client.chat(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    options={"temperature": 0.3, "num_predict": 150},
                )
                frase = resposta["message"]["content"].strip()
                frase = frase.strip('"').strip("'").strip()
                return frase
            except Exception as e:
                print(f"  [erro tentativa {tentativa+1}] {e}")
        return ""