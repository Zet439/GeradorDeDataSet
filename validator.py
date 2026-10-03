"""Validações automáticas + deduplicação."""
import pandas as pd
from difflib import SequenceMatcher


class Validador:
    REDUCAO_MINIMA_PERCENTUAL = 10
    TAMANHO_MINIMO_ORIGINAL = 15
    SIMILARIDADE_MAXIMA = 0.85  # frases mais similares que isso são descartadas

    @staticmethod
    def similaridade(a: str, b: str) -> float:
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    @staticmethod
    def validar_linha(row: pd.Series) -> dict:
        original = row["texto_original"]
        simplificado = row["texto_simplificado"]
        len_orig = len(original)
        len_simp = len(simplificado)
        reducao = ((len_orig - len_simp) / len_orig) * 100 if len_orig > 0 else 0.0

        return {
            "len_original": len_orig,
            "len_simplificado": len_simp,
            "reducao_percentual": round(reducao, 2),
            "valido_tamanho_original": len_orig >= Validador.TAMANHO_MINIMO_ORIGINAL,
            "valido_nao_vazio": len_simp > 0,
            "valido_reducao": reducao >= Validador.REDUCAO_MINIMA_PERCENTUAL,
            "valido_nao_identico": original.lower() != simplificado.lower(),
        }

    @staticmethod
    def validar_dataset(df: pd.DataFrame) -> pd.DataFrame:
        validacoes = df.apply(Validador.validar_linha, axis=1, result_type="expand")
        df_validado = pd.concat([df, validacoes], axis=1)
        df_validado["valido_geral"] = (
            df_validado["valido_tamanho_original"]
            & df_validado["valido_nao_vazio"]
            & df_validado["valido_reducao"]
            & df_validado["valido_nao_identico"]
        )
        # Remove duplicatas exatas
        df_validado = df_validado.drop_duplicates(
            subset=["texto_original", "texto_simplificado"], keep="first"
        )
        return df_validado