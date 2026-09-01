import pandas as pd

# 1. Cargar el dataset de Scopus
# Se usa 'utf-8-sig' porque los CSV de Scopus a veces incluyen un BOM (Byte Order Mark)
ruta_csv = 'c:\\Users\\yeiso\\Desktop\\PROYECTOS\\2. EMPRENDIMIENTO UNICAFAM\\1. Pipeline Scopus Avaluos a nivel mundial.csv' 
df = pd.read_csv(ruta_csv, encoding='utf-8-sig')

# 2. Identificar y filtrar las columnas más relevantes para tu semillero
# Scopus exporta muchas columnas; aquí conservamos las esenciales para el estado del arte.
columnas_interes = [
    'Authors', 
    'Title', 
    'Year', 
    'Source title', # Nombre de la revista
    'Abstract', 
    'Cited by',     # Número de citas
    'Document Type', 
    'DOI'
]

# Verificar qué columnas existen realmente en tu CSV para evitar errores
columnas_existentes = [col for col in columnas_interes if col in df.columns]
df_limpio = df[columnas_existentes].copy()

# 3. Limpieza y transformación de datos
# Convertir las citas a valores numéricos (reemplazando vacíos con 0)
if 'Cited by' in df_limpio.columns:
    df_limpio['Cited by'] = pd.to_numeric(df_limpio['Cited by'], errors='coerce').fillna(0)

# Rellenar valores nulos en textos para evitar celdas vacías en Excel
df_limpio.fillna('No especificado', inplace=True)

# Ordenar los artículos por año (más recientes primero) y luego por número de citas
df_limpio = df_limpio.sort_values(by=['Year', 'Cited by'], ascending=[False, False])

# 4. AGREGAR EL NÚMERO DE REFERENCIA (Consecutivo)
# .insert(posición_columna, nombre_columna, datos)
# Lo ponemos en la posición 0 para que sea la primera columna en Excel
df_limpio.insert(0, 'N°', range(1, len(df_limpio) + 1))
# 5. Exportar a Excel
ruta_excel = 'estado_del_arte_avaluos.xlsx'
df_limpio.to_excel(ruta_excel, index=False, engine='openpyxl')

print(f"Dataset organizado y exportado con éxito a: {ruta_excel}")