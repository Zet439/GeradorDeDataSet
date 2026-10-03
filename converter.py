"""
Script para converter o checkpoint.json interrompido 
em dataset final (.csv e .jsonl) com validações aplicadas.
Colunas finais: original_sent, reduced_sent, categoria, métricas.
"""
import json
import pandas as pd

CHECKPOINT_FILE = "checkpoint.json"
ARQUIVO_SAIDA_CSV = "dataset_simplificacao.csv"
ARQUIVO_SAIDA_JSONL = "dataset_simplificacao.jsonl"


def main():
    print("⏳ Carregando checkpoint.json...")
    try:
        with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Arquivo checkpoint.json não encontrado na pasta.")
        return

    registros = data.get("registros", [])
    print(f"✅ Encontrados {len(registros)} registros brutos no checkpoint.")

    if not registros:
        print("⚠️ Nenhum registro encontrado para processar.")
        return

    # 1. Converter para DataFrame do Pandas
    df = pd.DataFrame(registros)

    # 2. Aplicar validações (usando os nomes originais das colunas)
    print("⚙️ Aplicando validações e calculando métricas...")
    df['len_original'] = df['texto_original'].str.len()
    df['len_simplificado'] = df['texto_simplificado'].str.len()

    df['reducao_percentual'] = (
        (df['len_original'] - df['len_simplificado'])
        / df['len_original'].replace(0, 1)
    ) * 100

    df['valido_geral'] = (
        (df['len_original'] >= 15)
        & (df['len_simplificado'] > 0)
        & (df['reducao_percentual'] >= 10)
        & (df['texto_original'].str.lower() != df['texto_simplificado'].str.lower())
    )

    # 3. Remover duplicatas exatas
    df = df.drop_duplicates(
        subset=['texto_original', 'texto_simplificado'], keep='first'
    )

    # 4. Filtrar apenas os válidos
    df_final = df[df['valido_geral']].copy()

    # Opcional: cortar exatamente em 30.000 (descomente se quiser)
    # df_final = df_final.head(30000)

    print(f"📊 Registros válidos após filtragem: {len(df_final)}")
    print(f"📉 Redução média de tamanho: {df_final['reducao_percentual'].mean():.1f}%")

    # 5. Renomear colunas para o formato final desejado
    df_final = df_final.rename(columns={
        'texto_original': 'original_sent',
        'texto_simplificado': 'reduced_sent',
    })

    # 6. Reorganizar a ordem das colunas (opcional, mas deixa mais limpo)
    df_final = df_final[[
        'categoria',
        'original_sent',
        'reduced_sent',
        'len_original',
        'len_simplificado',
        'reducao_percentual',
    ]]

    # 7. Salvar nos formatos finais
    print(f"💾 Salvando em {ARQUIVO_SAIDA_CSV} e {ARQUIVO_SAIDA_JSONL}...")
    df_final.to_csv(ARQUIVO_SAIDA_CSV, index=False, encoding="utf-8")
    df_final.to_json(
        ARQUIVO_SAIDA_JSONL,
        orient="records",
        lines=True,
        force_ascii=False,
    )

    print("🎉 Conversão concluída com sucesso!")
    print(f"   - {ARQUIVO_SAIDA_CSV}")
    print(f"   - {ARQUIVO_SAIDA_JSONL}")


if __name__ == "__main__":
    main()