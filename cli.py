import argparse
from src.generator import generar_descripciones

def main():
    parser = argparse.ArgumentParser(description='Genera descripciones de productos utilizando OpenAI GPT-4.')
    parser.add_argument('--input', required=True, help='Ruta al archivo CSV de entrada')
    parser.add_argument('--output', required=True, help='Ruta al archivo CSV de salida')
    parser.add_argument('--api_key', required=True, help='Clave de API de OpenAI')

    args = parser.parse_args()

    generar_descripciones(args.input, args.output, args.api_key)
    print(f"Proceso completado. Descripciones generadas guardadas en: {args.output}")

if __name__ == "__main__":
    main()
