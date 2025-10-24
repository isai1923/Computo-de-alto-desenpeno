import pandas as pd
import altair as alt
import os
from elasticsearch import Elasticsearch

def main():
    # --- 1. Cargar y Procesar Datos Locales ---
    try:
        df = pd.read_csv("calidad (1).csv")
        df['fecha'] = pd.to_datetime(df['fecha'])
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'calidad (1).csv'.")
        return
    except Exception as e:
        print(f"Error al leer el CSV: {e}")
        return

    # --- 2. (Opcional) Cargar Datos en Elasticsearch ---
    # Las credenciales se leen de forma segura desde las variables de entorno
    # (que configurarás como GitHub Secrets)
    es_cloud_id = os.environ.get('ES_CLOUD_ID')
    es_api_key = os.environ.get('ES_API_KEY')

    if es_cloud_id and es_api_key:
        print("Conectando a Elasticsearch...")
        try:
            es = Elasticsearch(cloud_id=es_cloud_id, api_key=es_api_key)
            es.info() # Probar conexión
            print("Conexión a Elasticsearch exitosa.")

            # Convertir DataFrame a formato de bulk de Elasticsearch
            actions = []
            for _, row in df.iterrows():
                doc = row.to_dict()
                # Convertir Timestamp a string ISO 8601 para JSON
                doc['fecha'] = doc['fecha'].isoformat()
                actions.append({"index": {"_index": "indice-calidad"}})
                actions.append(doc)
            
            # Enviar datos en bloque
            if actions:
                print(f"Cargando {len(df)} documentos a Elasticsearch...")
                es.bulk(index="indice-calidad", operations=actions, refresh=True)
                print("Datos cargados exitosamente a Elasticsearch.")

        except Exception as e:
            print(f"Error al conectar o cargar datos en Elasticsearch: {e}")
            print("Continuando solo con la generación del gráfico local...")
    else:
        print("No se encontraron credenciales de Elasticsearch, omitiendo la carga de datos.")

    # --- 3. Generar el Gráfico Interactivo ---
    print("Generando gráfico interactivo...")
    
    # Gráfico de líneas de fallas en el tiempo
    chart_time = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('fecha', title='Fecha', axis=alt.Axis(format="%Y-%m-%d")),
        y=alt.Y('fallas_detectadas', title='Fallas Diarias'),
        color=alt.Color('linea', title='Línea'), # Añadir color por línea
        tooltip=[alt.Tooltip('fecha', format="%Y-%m-%d"), 'linea', 'fallas_detectadas', 'inspecciones']
    ).properties(
        title='Evolución de Fallas Detectadas en el Tiempo'
    ).interactive() # Permite zoom y paneo

    # Guardar el gráfico como un archivo HTML independiente
    chart_time.save('index.html')
    print("Gráfico guardado como 'index.html'.")

if __name__ == "__main__":
    main()