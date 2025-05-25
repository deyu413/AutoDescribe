# AutoDescribe

AutoDescribe is a Python project that uses GPT-4 to generate product descriptions from a CSV file.

**Input:** CSV file with columns such as product, category, etc.
**Output:** CSV file with GPT-4 generated descriptions.
**Usage:** Run from the terminal: `python cli.py input.csv output.csv`

The user needs to provide their own OpenAI API Key.

## Cómo usar

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecuta el script:
   ```bash
   python cli.py --input productos.csv --output descripciones.csv --api_key tu_clave_openai
   ```

3. El archivo `descripciones.csv` tendrá una columna nueva llamada `descripcion`.
