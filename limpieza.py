import pandas as pd
import re

# Leer el archivo CSV
data = pd.read_csv("Lenguas_COL_denger_2.csv")

# Función para extraer el contenido entre corchetes
def extract_content(s):
    match = re.search(r'\[también conocido como(.*?)\]', s, re.DOTALL)
    return match.group(1).strip() if match else ""

# Función para limpiar la columna 'lengua'
def clean_lengua(s):
    return re.sub(r'\[también conocido como.*?\]', '', s, flags=re.DOTALL).strip()

# Aplicar las funciones
data['también conocido como'] = data['lengua'].apply(extract_content)
data['lengua'] = data['lengua'].apply(clean_lengua)

# Reordenar las columnas para poner 'también conocido como' justo después de 'lengua'
columns_order = data.columns.tolist()
index_lengua = columns_order.index('lengua')
columns_order.insert(index_lengua + 1, columns_order.pop())
data = data[columns_order]

# Guardar el DataFrame actualizado de nuevo en el CSV
data.to_csv("Lenguas_COL_denger_2_updated.csv", index=False)

print("Archivo CSV actualizado!")
