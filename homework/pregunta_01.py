"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """
    import pandas as pd
    import re
    
    with open('files/input/clusters_report.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    
    lines = content.strip().split('\n')
    
    data_start = -1
    for i, line in enumerate(lines):
        if '---' in line:
            data_start = i + 1
            break
    
    data = []
    current_cluster = None
    current_cantidad = None
    current_porcentaje = None
    current_keywords = []
    
    for i in range(data_start, len(lines)):
        line = lines[i].strip()
        if not line:  # Línea vacía
            continue
            
        match = re.match(r'^\s*(\d+)\s+(\d+)\s+([\d,]+\s*%)\s+(.+)', line)
        if match:
            if current_cluster is not None:
                keywords_str = ' '.join(current_keywords)
                keywords_str = re.sub(r'\s+', ' ', keywords_str.strip())
                keywords_str = re.sub(r'\s*,\s*', ', ', keywords_str)
                keywords_str = keywords_str.replace('.','')
                data.append([current_cluster, current_cantidad, current_porcentaje, keywords_str])
            
            current_cluster = int(match.group(1))
            current_cantidad = int(match.group(2))
            porcentaje_str = match.group(3).replace(',', '.').replace('%', '').strip()
            current_porcentaje = float(porcentaje_str)
            current_keywords = [match.group(4)]
        else:
            if current_cluster is not None:
                current_keywords.append(line)
    
    if current_cluster is not None:
        keywords_str = ' '.join(current_keywords)
        keywords_str = re.sub(r'\s+', ' ', keywords_str.strip())
        keywords_str = re.sub(r'\s*,\s*', ', ', keywords_str)
        keywords_str = keywords_str.replace('.','')
        data.append([current_cluster, current_cantidad, current_porcentaje, keywords_str])
    
    df = pd.DataFrame(data, columns=['cluster', 'cantidad_de_palabras_clave', 'porcentaje_de_palabras_clave', 'principales_palabras_clave'])
    
    return df