#!/usr/bin/env python3
"""Generador de datos económicos ficticios para probar EconoLab.

Cada ejecución sobrescribe únicamente los archivos de salida dentro de
``datos_prueba``. Los datos son deliberadamente imperfectos: el objetivo es
probar importación, detección y limpieza asistida, no representar estadísticas
oficiales.
"""

from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "datos_prueba"


def crear_pib() -> None:
    """Genera PIB con nombres heterogéneos, textos, vacíos y duplicados."""
    filas = [
        {" País ": "España", "year": 2020, "PIB_USD_millones": "1.281.000", "codigo_pais": 724, "fuente": "simulada"},
        {" País ": "España", "year": "2021", "PIB_USD_millones": "1,427,000", "codigo_pais": "724", "fuente": "simulada"},
        {" País ": "España", "year": "2022-01-01", "PIB_USD_millones": 1_476_000, "codigo_pais": 724, "fuente": "simulada"},
        {" País ": "España", "year": "2022-01-01", "PIB_USD_millones": 1_476_000, "codigo_pais": 724, "fuente": "simulada"},  # duplicado
        {" País ": "España", "year": 2023, "PIB_USD_millones": "1.62e6", "codigo_pais": 724, "fuente": "simulada"},
        {" País ": "Estados Unidos", "year": 2020, "PIB_USD_millones": "21,060,000", "codigo_pais": 840, "fuente": "simulada"},
        {" País ": "Estados Unidos", "year": "2021", "PIB_USD_millones": 23_315_000, "codigo_pais": 840, "fuente": "simulada"},
        {" País ": "Estados Unidos", "year": 2022, "PIB_USD_millones": "25 462 700", "codigo_pais": 840, "fuente": "simulada"},
        {" País ": "Alemania", "year": 2020, "PIB_USD_millones": "3.85e6", "codigo_pais": 276, "fuente": "simulada"},
        {" País ": "Alemania", "year": 2021, "PIB_USD_millones": "4.26e6", "codigo_pais": 276, "fuente": "simulada"},
        {" País ": "Alemania", "year": 2022, "PIB_USD_millones": None, "codigo_pais": 276, "fuente": "simulada"},
        {" País ": "Brasil", "year": "2023", "PIB_USD_millones": "2.17e6", "codigo_pais": 76, "fuente": "simulada"},
        {" País ": "Brasil", "year": 2024, "PIB_USD_millones": "pendiente", "codigo_pais": 76, "fuente": "simulada"},
    ]
    df = pd.DataFrame(filas)
    # Columna innecesaria y columna completamente vacía para probar su detección.
    df["notas_internas"] = ["ok", "ok", "revisar", "revisar", "ok", "ok", "ok", "ok", "ok", "ok", "faltante", "ok", "revisar"]
    df["columna_vacia"] = np.nan
    # Fila completamente vacía (se conserva en el CSV mediante una fila de NaN).
    df.loc[len(df)] = [np.nan] * len(df.columns)
    df.to_csv(OUTPUT_DIR / "pib.csv", index=False, encoding="utf-8-sig")


def crear_inflacion() -> None:
    """Genera un Excel con formatos de periodo y separadores decimales mixtos."""
    filas = [
        {"country_name": "España", "periodo": "2020", "inflacion_pct": "-0,3", "iso3": "ESP", "codigo_pais": 724, "comentario": "dato anual simulado"},
        {"country_name": "España", "periodo": "2021-12-31", "inflacion_pct": "3.1", "iso3": "ESP", "codigo_pais": 724, "comentario": "dato anual simulado"},
        {"country_name": "España", "periodo": "2022", "inflacion_pct": 8.4, "iso3": "ESP", "codigo_pais": 724, "comentario": "dato anual simulado"},
        {"country_name": "Estados Unidos", "periodo": 2020, "inflacion_pct": 1.2, "iso3": "USA", "codigo_pais": 840, "comentario": "dato anual simulado"},
        {"country_name": "Estados Unidos", "periodo": "2021", "inflacion_pct": "4.7%", "iso3": "USA", "codigo_pais": 840, "comentario": "incluye símbolo"},
        {"country_name": "Alemania", "periodo": "2022/12/31", "inflacion_pct": "6,9", "iso3": "DEU", "codigo_pais": 276, "comentario": "dato anual simulado"},
        {"country_name": "Brasil", "periodo": "2023", "inflacion_pct": None, "iso3": "BRA", "codigo_pais": 76, "comentario": "sin publicar"},
        {"country_name": "Brasil", "periodo": "2023", "inflacion_pct": None, "iso3": "BRA", "codigo_pais": 76, "comentario": "sin publicar"},  # duplicado
    ]
    df = pd.DataFrame(filas)
    df[" columna_innecesaria "] = "eliminar"
    df["columna_totalmente_vacia"] = np.nan
    # Excel conserva una fila vacía intermedia y otra al final.
    df.loc[3, "country_name"] = np.nan
    with pd.ExcelWriter(OUTPUT_DIR / "inflacion.xlsx", engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="inflacion", index=False, startrow=1)
        pd.DataFrame({"hoja_vacia": []}).to_excel(writer, sheet_name="hoja_vacia", index=False)


def crear_empleo() -> None:
    """Genera desempleo con convenciones de nombres y valores ambiguos."""
    filas = [
        {"Country": "España", "AÑO ": "2020", "unemployment_rate": "15.5", "country_code": "724", "period_type": "annual"},
        {"Country": "España", "AÑO ": 2021, "unemployment_rate": "14,8", "country_code": 724, "period_type": "annual"},
        {"Country": "España", "AÑO ": "2022-Q4", "unemployment_rate": 12.9, "country_code": 724, "period_type": "quarterly"},
        {"Country": "Estados Unidos", "AÑO ": 2020, "unemployment_rate": "8.1%", "country_code": 840, "period_type": "annual"},
        {"Country": "Estados Unidos", "AÑO ": 2021, "unemployment_rate": 5.4, "country_code": 840, "period_type": "annual"},
        {"Country": "Alemania", "AÑO ": 2022, "unemployment_rate": "3,1", "country_code": 276, "period_type": "annual"},
        {"Country": "Brasil", "AÑO ": 2023, "unemployment_rate": "12.4", "country_code": 76, "period_type": "annual"},
        {"Country": "Brasil", "AÑO ": 2023, "unemployment_rate": "12.4", "country_code": 76, "period_type": "annual"},  # duplicado
        {"Country": "España", "AÑO ": 2024, "unemployment_rate": "-2.0", "country_code": 724, "period_type": "annual"},  # inconsistencia no corregible automáticamente
    ]
    df = pd.DataFrame(filas)
    df["extra_field"] = ["x", "x", "q4", "x", "x", "x", "x", "x", "revisar"]
    df["all_blank"] = np.nan
    df.loc[len(df)] = [np.nan] * len(df.columns)
    df.to_csv(OUTPUT_DIR / "empleo.csv", index=False, encoding="utf-8-sig")


def crear_diccionario() -> None:
    """Genera el diccionario que documenta variables y códigos numéricos."""
    variables = pd.DataFrame([
        {"Nombre estándar": "pais", "Nombres observados": "País; country_name; Country", "Unidad": "texto", "Código": "", "Descripción": "País de la observación"},
        {"Nombre estándar": "anio", "Nombres observados": "year; periodo; AÑO", "Unidad": "año o periodo", "Código": "", "Descripción": "Año o trimestre de referencia; requiere decisión si hay granularidades mezcladas"},
        {"Nombre estándar": "pib_usd_millones", "Nombres observados": "PIB_USD_millones", "Unidad": "millones de USD", "Código": "", "Descripción": "Producto interior bruto nominal ficticio"},
        {"Nombre estándar": "inflacion_pct", "Nombres observados": "inflacion_pct", "Unidad": "%", "Código": "", "Descripción": "Variación anual de precios"},
        {"Nombre estándar": "desempleo_pct", "Nombres observados": "unemployment_rate", "Unidad": "% de población activa", "Código": "", "Descripción": "Tasa de desempleo"},
        {"Nombre estándar": "codigo_pais", "Nombres observados": "codigo_pais; country_code", "Unidad": "código numérico ISO 3166-1 alpha-3 numérico", "Código": "724=ESP; 840=USA; 276=DEU; 76=BRA", "Descripción": "Código numérico que debe traducirse o validarse"},
        {"Nombre estándar": "period_type", "Nombres observados": "period_type", "Unidad": "annual/quarterly", "Código": "annual=anual; quarterly=trimestral", "Descripción": "Granularidad temporal; no debe mezclarse sin decisión del usuario"},
    ])
    notas = pd.DataFrame([
        {"Regla": "Valores negativos", "Acción sugerida": "Revisar manualmente; un desempleo negativo no es económicamente válido y no debe imputarse automáticamente."},
        {"Regla": "Periodos mixtos", "Acción sugerida": "Decidir si se convierten fechas y trimestres a una granularidad común."},
        {"Regla": "Duplicados", "Acción sugerida": "Confirmar si son copias exactas o registros legítimos repetidos antes de eliminarlos."},
    ])
    with pd.ExcelWriter(OUTPUT_DIR / "diccionario_variables.xlsx", engine="openpyxl") as writer:
        variables.to_excel(writer, sheet_name="variables", index=False)
        notas.to_excel(writer, sheet_name="reglas_revision", index=False)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    crear_pib()
    crear_inflacion()
    crear_empleo()
    crear_diccionario()
    print(f"Archivos de prueba generados en: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
