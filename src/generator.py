import csv
from openai import OpenAI

def generar_descripciones(input_csv: str, output_csv: str, api_key: str):
    client = OpenAI(api_key=api_key)
    
    output_rows = []
    
    with open(input_csv, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        header = reader.fieldnames + ['descripcion']
        output_rows.append(header)
        
        for row in reader:
            product_name = row['producto']
            prompt = f"Genera una descripción para el producto: {product_name}"
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Eres un asistente de marketing."},
                    {"role": "user", "content": prompt}
                ]
            )
            description = response.choices[0].message.content
            
            row['descripcion'] = description
            output_rows.append([row[field] for field in header])
            
    with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(output_rows)
