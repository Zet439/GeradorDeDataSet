"""Pipeline principal com checkpointing para geração em larga escala."""
import json
import os
import pandas as pd
from tqdm import tqdm

from config import (
    CATEGORIAS, QTD_POR_CATEGORIA, ARQUIVO_SAIDA_CSV,
    ARQUIVO_SAIDA_JSONL, CHECKPOINT_FILE,
)
from generator import GeradorFrases
from simplifier import Simplificador
from validator import Validador


def carregar_checkpoint() -> dict:
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"categoria_atual": None, "indice_atual": 0, "registros": []}


def salvar_checkpoint(checkpoint: dict):
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump(checkpoint, f, ensure_ascii=False, indent=2)


def gerar_dataset() -> pd.DataFrame:
    gerador = GeradorFrases()
    simplificador = Simplificador()
    checkpoint = carregar_checkpoint()
    registros = checkpoint["registros"]
    categoria_atual = checkpoint["categoria_atual"]
    indice_atual = checkpoint["indice_atual"]

    total_esperado = len(CATEGORIAS) * QTD_POR_CATEGORIA
    pbar = tqdm(total=total_esperado, initial=len(registros), desc="Gerando dataset")

    for categoria in CATEGORIAS:
        # Pula categorias já processadas
        if categoria_atual is not None and categoria != categoria_atual:
            if categoria_atual != categoria:
                continue
        inicio = indice_atual if categoria == categoria_atual else 0

        for i in range(inicio, QTD_POR_CATEGORIA):
            original = gerador.gerar_uma(categoria)
            if not original:
                continue
            simplificado = simplificador.simplificar(original)
            if not simplificado:
                continue

            registros.append({
                "categoria": categoria,
                "texto_original": original,
                "texto_simplificado": simplificado,
            })

            # Salva checkpoint a cada 50 registros
            if len(registros) % 50 == 0:
                salvar_checkpoint({
                    "categoria_atual": categoria,
                    "indice_atual": i + 1,
                    "registros": registros,
                })

            pbar.update(1)

        categoria_atual = None
        indice_atual = 0

    pbar.close()
    salvar_checkpoint({
        "categoria_atual": None, "indice_atual": 0, "registros": registros,
    })
    return pd.DataFrame(registros)


def main():
    total_previsto = len(CATEGORIAS) * QTD_POR_CATEGORIA
    print(f"🚀 Iniciando geração do dataset (até {total_previsto:,} pares)...")
    print(f"⏱️  Estimativa: {total_previsto:,} pares × ~5s/par")
    print(f"💾 Checkpoint salvo em: {CHECKPOINT_FILE}")
    print(f"🔄 Se o script cair, basta rodar novamente para retomar.\n")

    df = gerar_dataset()

    if df.empty:
        print("❌ Nenhum registro gerado.")
        return

    print(f"\n📊 {len(df)} pares gerados. Validando e deduplicando...")
    df_validado = Validador.validar_dataset(df)

    total = len(df_validado)
    validos = int(df_validado["valido_geral"].sum())
    print(f"\n✅ Válidos: {validos}/{total} ({validos/total*100:.1f}%)")
    print(f"📉 Redução média: {df_validado['reducao_percentual'].mean():.1f}%")

    df_final = df_validado[df_validado["valido_geral"]].copy()
    df_final.to_csv(ARQUIVO_SAIDA_CSV, index=False, encoding="utf-8")
    df_final.to_json(
        ARQUIVO_SAIDA_JSONL, orient="records",
        lines=True, force_ascii=False,
    )

    print(f"\n💾 Dataset salvo em:")
    print(f"   - {ARQUIVO_SAIDA_CSV}")
    print(f"   - {ARQUIVO_SAIDA_JSONL}")
    print(f"\n🧹 Remova o arquivo {CHECKPOINT_FILE} quando terminar.")


if __name__ == "__main__":
    main()