import csv
from openai import OpenAI

PROMPT_TEMPLATE = (
    "Eres un experto en marketing. Genera una descripción atractiva y profesional "
    "para el siguiente producto: {producto}. Asegúrate de que sea clara, "
    "convincente y adecuada para e-commerce."
)

def generar_descripciones(input_csv: str, output_csv: str, api_key: str):
    client = OpenAI(api_key=api_key)
    
    output_rows = []
    
    with open(input_csv, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        header = reader.fieldnames + ['descripcion']
        output_rows.append(header)
        
        for row in reader:
            product_name = row['producto']
            user_prompt = PROMPT_TEMPLATE.format(producto=product_name)
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Eres un asistente de marketing."},
                    {"role": "user", "content": user_prompt}
                ]
            )
            description = response.choices[0].message.content
            
            row['descripcion'] = description
            output_rows.append([row[field] for field in header])
            
    with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(output_rows)
