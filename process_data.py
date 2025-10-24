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
    # (Esta parte se mantiene igual)
    es_cloud_id = os.environ.get('ES_CLOUD_ID')
    es_api_key = os.environ.get('ES_API_KEY')

    if es_cloud_id and es_api_key:
        print("Conectando a Elasticsearch...")
        try:
            es = Elasticsearch(cloud_id=es_cloud_id, api_key=es_api_key)
            es.info()
            print("Conexión a Elasticsearch exitosa.")
            
            actions = []
            for _, row in df.iterrows():
                doc = row.to_dict()
                doc['fecha'] = doc['fecha'].isoformat()
                actions.append({"index": {"_index": "indice-calidad"}})
                actions.append(doc)
            
            if actions:
                print(f"Cargando {len(df)} documentos a Elasticsearch...")
                es.bulk(index="indice-calidad", operations=actions, refresh=True)
                print("Datos cargados exitosamente a Elasticsearch.")

        except Exception as e:
            print(f"Error al conectar o cargar datos en Elasticsearch: {e}")
            print("Continuando solo con la generación del gráfico local...")
    else:
        print("No se encontraron credenciales de Elasticsearch, omitiendo la carga de datos.")

    # --- 3. Generar AMBOS Gráficos ---
    print("Generando gráficos...")

    # --- NUEVO: Gráfico 1 (Barras) ---
    # Primero, agregamos los datos por línea
    df_agg = df.groupby('linea').agg(
        total_fallas=('fallas_detectadas', 'sum'),
        total_inspecciones=('inspecciones', 'sum')
    ).reset_index()
    
    chart_bar = alt.Chart(df_agg).mark_bar().encode(
        x=alt.X('linea', title='Línea', sort='-y'), # Ordenar de mayor a menor
        y=alt.Y('total_fallas', title='Total de Fallas Detectadas'),
        tooltip=['linea', 'total_fallas', 'total_inspecciones']
    ).properties(
        title='Total de Fallas por Línea de Producción'
    )

    # --- Gráfico 2 (Líneas) ---
    # (Este es el que ya tenías)
    chart_time = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('fecha', title='Fecha', axis=alt.Axis(format="%Y-%m-%d")),
        y=alt.Y('fallas_detectadas', title='Fallas Diarias'),
        color=alt.Color('linea', title='Línea'),
        tooltip=[alt.Tooltip('fecha', format="%Y-%m-%d"), 'linea', 'fallas_detectadas', 'inspecciones']
    ).properties(
        title='Evolución de Fallas Detectadas en el Tiempo'
    ).interactive()

    # --- 4. NUEVO: Combinar y Guardar Gráficos ---
    print("Combinando gráficos...")
    
    # Combinar los dos gráficos verticalmente (uno encima del otro)
    # Usamos el operador '&' de Altair
    combined_chart = chart_bar & chart_time
    
    # Guardar el gráfico combinado como un archivo HTML
    combined_chart.save('index.html')
    print("Gráfico combinado guardado como 'index.html'.")

if __name__ == "__main__":
    main()
