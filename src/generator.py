import csv
import openai # Ensure this is at the top

PROMPT_TEMPLATE = (
    "Eres un experto en marketing. Genera una descripción atractiva y profesional "
    "para el siguiente producto: {producto}. Asegúrate de que sea clara, "
    "convincente y adecuada para e-commerce."
)

def generar_descripciones(input_csv: str, output_csv: str, api_key: str):
    output_rows = []

    try:
        with open(input_csv, mode='r', encoding='utf-8', newline='') as infile:
            reader = csv.DictReader(infile)
            header = reader.fieldnames
            
            if not header: # Handles case of totally empty file
                print("Advertencia: El archivo CSV de entrada está completamente vacío.")
                return

            if 'producto' not in header:
                raise ValueError("Error: La columna 'producto' no se encuentra en el archivo CSV de entrada.")

            # Prepare data for writing, including new header
            output_header = header + ['descripcion']
            output_rows.append(output_header) # Add header to output list

            # Check for empty data after header
            try:
                first_row = next(reader)
            except StopIteration: # No rows after header
                print("Advertencia: El archivo CSV de entrada solo contiene encabezados.")
                # Still write the header to the output file
                with open(output_csv, mode='w', encoding='utf-8', newline='') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerows(output_rows)
                return
            
            # Process the first row and subsequent rows
            rows_to_process = [first_row] + list(reader)

        client = OpenAI(api_key=api_key)
        
        for product_row in rows_to_process:
            product_name = product_row.get('producto', '').strip() # Get product name, ensure it's a string and strip whitespace
            description = ""

            if not product_name:
                print(f"Advertencia: Fila encontrada sin valor en la columna 'producto' o con valor vacío. Fila: {product_row}. Saltando generación de descripción.")
                description = "Producto no especificado"
            else:
                user_prompt = PROMPT_TEMPLATE.format(producto=product_name)
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
                    print(f"Error de API al generar descripción para el producto '{product_name}': {e}")
                    description = "Error al generar descripción (API)"
                except Exception as e: # Catch any other unexpected errors during API interaction
                    print(f"Un error inesperado ocurrió al procesar el producto '{product_name}' con la API: {e}")
                    description = "Error inesperado al generar descripción"
            
            # Construct current_output_row as a list of values in the order of output_header
            current_output_values = []
            for col_name in header: # original header
                current_output_values.append(product_row.get(col_name, ''))
            current_output_values.append(description)
            output_rows.append(current_output_values)

    except FileNotFoundError:
        print(f"Error: El archivo de entrada '{input_csv}' no fue encontrado.")
        return 
    except ValueError as ve: # Catch the ValueError from missing 'producto'
        print(ve)
        # If 'producto' is missing, we might not have output_rows initialized with header yet,
        # or we might not want to write an empty file.
        # For now, just print and return. If an output file with only headers is desired,
        # that logic would need to be more complex here.
        return
    except Exception as e: # Catch any other unexpected errors during file processing or other operations
        print(f"Un error inesperado ocurrió durante el procesamiento general: {e}")
        return

    # Write all collected rows to output_csv
    try:
        with open(output_csv, mode='w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(output_rows)
    except Exception as e:
        print(f"Error al escribir el archivo de salida '{output_csv}': {e}")
