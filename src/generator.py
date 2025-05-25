import pandas as pd
import openai

PROMPT_TEMPLATE = (
    "Eres un experto en marketing. Genera una descripción atractiva y profesional "
    "para el siguiente producto: {producto}. Asegúrate de que sea clara, "
    "convincente y adecuada para e-commerce."
)

def generar_descripciones(input_csv: str, output_csv: str, api_key: str):
    try:
        try:
            df = pd.read_csv(input_csv)
        except FileNotFoundError:
            print(f"Error: El archivo de entrada '{input_csv}' no fue encontrado.")
            return
        except pd.errors.EmptyDataError:
            print(f"Advertencia: El archivo CSV de entrada '{input_csv}' está vacío.")
            # Create an empty DataFrame with 'producto' and 'descripcion' columns 
            # This ensures the output file has the expected basic structure.
            pd.DataFrame(columns=['producto', 'descripcion']).to_csv(output_csv, index=False, encoding='utf-8')
            return
        except Exception as e: # Catch other pandas related errors during read
            print(f"Error al leer el archivo CSV con pandas: {e}")
            return

        if df.empty:
            print("Advertencia: El archivo CSV de entrada no contiene datos (puede que solo tenga encabezados).")
            # Determine output columns: use original columns if they exist, else default. Add 'descripcion'.
            output_columns = list(df.columns) if list(df.columns) else [] # df.columns would be empty if no headers
            if not output_columns and 'producto' not in output_columns: # If CSV was truly empty, ensure 'producto'
                 output_columns.append('producto')
            if 'descripcion' not in output_columns:
                output_columns.append('descripcion')
            
            pd.DataFrame(columns=output_columns).to_csv(output_csv, index=False, encoding='utf-8')
            return

        if 'producto' not in df.columns:
            # This error is critical, so we raise it to be caught by the outer try-except
            raise ValueError("Error: La columna 'producto' no se encuentra en el archivo CSV de entrada.")

        client = openai.OpenAI(api_key=api_key)
        descriptions = []

        for index, row in df.iterrows():
            product_name = row.get('producto') 

            if pd.isna(product_name) or not str(product_name).strip():
                print(f"Advertencia: Fila con índice {index} tiene valor nulo, vacío o solo espacios en la columna 'producto'. Usando placeholder.")
                descriptions.append("Producto no especificado o vacío")
                continue
            
            # Ensure product_name is a string for the prompt
            product_name_str = str(product_name).strip()
            user_prompt = PROMPT_TEMPLATE.format(producto=product_name_str)
            description = ""

            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Eres un asistente de marketing."},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                description = response.choices[0].message.content.strip()
            except openai.APIError as e:
                print(f"Error de API al generar descripción para el producto '{product_name_str}': {e}")
                description = "Error al generar descripción (API)"
            except Exception as e:
                print(f"Un error inesperado ocurrió al procesar el producto '{product_name_str}' con la API: {e}")
                description = "Error inesperado al generar descripción"
            
            descriptions.append(description)

        df['descripcion'] = descriptions
        df.to_csv(output_csv, index=False, encoding='utf-8')
        print(f"Proceso completado. Descripciones generadas guardadas en: {output_csv}")

    except ValueError as ve: # Handles missing 'producto' column
        print(ve)
        # Potentially write an empty file or a file with error message, or just return.
        # For now, consistent with previous behavior, just printing the error.
        return
    except Exception as e:
        print(f"Un error inesperado ocurrió durante el procesamiento general: {e}")
        # Similar to ValueError, decide if an output file should be written.
        return
