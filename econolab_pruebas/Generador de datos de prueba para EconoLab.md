# Generador de datos de prueba para EconoLab

Este proyecto crea un conjunto reproducible de archivos económicos ficticios para desarrollar y evaluar el futuro sistema de importación, diagnóstico y limpieza de EconoLab. **No implementa el algoritmo de limpieza ni una interfaz gráfica.**

## Requisitos

- Python 3.9 o superior.
- Pandas.
- OpenPyXL para escribir archivos `.xlsx`.

## Instalación y ejecución

Desde la carpeta del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate        # En Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python generador_datos.py
```

Cada ejecución crea o sobrescribe la carpeta `datos_prueba/`; no modifica otros archivos originales.

## Archivos generados

- `datos_prueba/pib.csv`: PIB nominal ficticio por país y periodo, en millones de USD.
- `datos_prueba/inflacion.xlsx`: inflación ficticia por país y periodo, con una hoja de datos y una hoja vacía.
- `datos_prueba/empleo.csv`: desempleo ficticio por país y periodo.
- `datos_prueba/diccionario_variables.xlsx`: nombres estándar, alias observados, unidades, códigos y reglas de revisión.

## Errores intencionados

### `pib.csv`

- Espacios innecesarios en el encabezado ` País `.
- La variable temporal aparece como `year`, con años numéricos, texto y una fecha ISO (`2022-01-01`).
- `PIB_USD_millones` mezcla números, separadores de miles, notación científica, texto y un valor no publicado (`pendiente`).
- `codigo_pais` mezcla números y texto.
- Incluye valores ausentes, una fila completamente vacía y una columna completamente vacía.
- Contiene observaciones duplicadas.
- `notas_internas` es una columna innecesaria para el análisis económico.

### `inflacion.xlsx`

- Los nombres siguen otra convención (`country_name`, `periodo`, `iso3`).
- `periodo` combina años, fechas ISO y fechas con barras.
- `inflacion_pct` combina valores numéricos, coma decimal, punto decimal, símbolo `%` y ausentes.
- Hay una fila de datos con país ausente, un registro duplicado y columnas innecesarias/vacías.
- Contiene una fila inicial vacía por el desplazamiento de la tabla y una hoja adicional vacía.

### `empleo.csv`

- Usa nombres diferentes para las mismas entidades (`Country`, `AÑO `, `country_code`).
- `AÑO ` mezcla años y el periodo trimestral `2022-Q4`.
- `unemployment_rate` mezcla números, coma decimal, símbolo `%`, texto numérico y un valor negativo imposible.
- `country_code` mezcla texto y números.
- Contiene una columna auxiliar innecesaria, una columna y fila completamente vacías y un duplicado.

### `diccionario_variables.xlsx`

- Documenta la correspondencia entre nombres observados y nombres estándar.
- Explica unidades y la interpretación de los códigos numéricos: `724=ESP`, `840=USA`, `276=DEU` y `76=BRA`.
- Incluye reglas de revisión para problemas que no deben resolverse a ciegas.

## Problemas que el futuro sistema debería detectar

1. Encabezados con espacios, mayúsculas o convenciones distintas.
2. Filas y columnas completamente vacías.
3. Tipos de datos inconsistentes y números almacenados como texto.
4. Valores ausentes y textos que representan ausencia o falta de publicación.
5. Fechas, años y trimestres con formatos distintos.
6. Duplicados exactos o potenciales.
7. Columnas auxiliares o innecesarias.
8. Alias de una misma variable entre fuentes.
9. Códigos numéricos que requieren traducción mediante el diccionario.
10. Incompatibilidades entre la granularidad temporal y la unidad de medida.
11. Valores fuera de rango, como una tasa de desempleo negativa.

## Casos que requieren intervención del usuario

- Decidir si `2022-01-01`, `2022/12/31`, `2022` y `2022-Q4` deben convertirse al mismo periodo.
- Confirmar si un duplicado debe eliminarse o si representa una fuente/revisión legítima.
- Decidir cómo tratar `pendiente`, los vacíos y los valores no publicados.
- Confirmar si `notas_internas`, `extra_field`, `comentario` y las columnas vacías deben conservarse.
- Validar si los separadores `1.281.000`, `1,427,000` y `25 462 700` usan la convención numérica esperada.
- Determinar cómo corregir el desempleo negativo; el generador lo deja sin corregir deliberadamente.

El algoritmo futuro debería conservar un registro de cada decisión, permitir deshacerla o modificarla y volver a ejecutar la limpieza mostrando el resultado después de cada cambio.
