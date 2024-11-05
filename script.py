import json
import csv
import subprocess
import os
from tqdm import tqdm

# File paths
input_json_path = "/Users/simonazoulay/Clean_news/orange.json"
output_csv_path = "/Users/simonazoulay/Clean_news/resultats_articles.csv"

# Improved prompt with examples
prompt_template = (
    'En lisant/analysant "{name}" et "{description}", je veux que tu répondes par "Oui" ou "Non". Réponds uniquement par "Oui" ou "Non" sans commenter. La question est la suivante : je suis un site dédié aux données économiques, juridiques, financières et stratégiques des entreprises, et je veux savoir si cette information est pertinente pour un public cherchant à comprendre l\'évolution de l\'entreprise Orange dans un contexte économique et stratégique.\n\n'
    'Réponds "Oui" si l\'information est pertinente, c’est-à-dire si :\n'
    '- Elle concerne directement les activités économiques, financières ou stratégiques d\'Orange.\n'
    '- Elle a un impact significatif sur la performance, la réglementation, ou les décisions stratégiques de l\'entreprise.\n'
    '- Elle porte sur des partenariats, des investissements, des innovations technologiques, des initiatives de développement ou des sanctions réglementaires affectant l’entreprise.\n\n'
    'Exemples d\'informations pertinentes pour "Orange" :\n'
    '1. "Orange se retire de Wall Street après 27 ans de cotation"\n'
    '   Impact financier et stratégique pour l\'entreprise.\n'
    '2. "Orange et Mastercard s\'allient pour développer des services financiers en Afrique"\n'
    '   Partenariat stratégique visant l\'expansion internationale et le développement de nouveaux services financiers.\n'
    '3. "Le Conseil d\'État confirme une amende de 26 millions d\'euros pour Orange"\n'
    '   Décision réglementaire ayant des implications économiques pour l\'entreprise.\n'
    '4. "Orange choisit HPE pour construire un supercalculateur IA pour l\'armée française"\n'
    '   Partenariat stratégique renforçant la position d\'Orange dans les services de haute technologie.\n\n'
    'Réponds "Non" si l\'information est non pertinente, c’est-à-dire si :\n'
    '- Elle concerne un homonyme ou un sujet sans lien direct avec Orange en tant qu’entreprise.\n'
    '- Elle porte sur des événements locaux ou des offres commerciales sans impact stratégique, économique ou financier significatif pour l\'entreprise.\n\n'
    'Exemples d\'informations non pertinentes pour "Orange" :\n'
    '1. "Orange propose deux mois gratuits sur sa fibre pour la rentrée"\n'
    '   Offre commerciale sans impact direct sur la stratégie d\'entreprise.\n'
    '2. "Concert de Francis Cabrel écourté au Théâtre Antique d\'Orange à cause du froid"\n'
    '   Information locale sans lien avec l\'entreprise Orange.\n'
    '3. "En partenariat avec Orange, Midi Libre organise un atelier pour éviter les arnaques en ligne"\n'
    '   Partenariat promotionnel sans portée stratégique pour l\'entreprise.\n'
    '4. "Sosh et YouPrice se battent pour offrir les meilleurs forfaits sur le réseau d\'Orange"\n'
    '   Comparaison de forfaits sans impact sur la stratégie ou la performance économique d\'Orange.\n'
)

def query_model_with_ollama(model_name, prompt):
    try:
        print(f"[DEBUG] Running model: {model_name} with prompt: {prompt[:100]}...")
        result = subprocess.run(
            ["ollama", "run", model_name],
            input=prompt,
            text=True,
            capture_output=True
        )
        if result.returncode != 0:
            print(f"[ERROR] Model {model_name} failed with return code {result.returncode}: {result.stderr}")
        response = result.stdout.strip()  # Capture the full response for debugging
        print(f"[DEBUG] Full response from {model_name}: {response}")  # Print the full response
        return response  # Return the full response for analysis
    except Exception as e:
        print(f"[ERROR] Exception occurred while running model {model_name}: {str(e)}")
        return f"Erreur: {str(e)}"

def process_article(article):
    name = article.get("name", "")
    description = article.get("description", "")
    url = article.get("url", "")

    # Generate dynamic prompt
    prompt = prompt_template.format(name=name, description=description)
    mistral_nemo_response = query_model_with_ollama("mistral-nemo:latest", prompt)
    llama32_response = query_model_with_ollama("llama3.2:latest", prompt)
    gemma2_response = query_model_with_ollama("gemma2:9b", prompt)

    return {
        "name": name,
        "description": description,
        "url": url,
        "mistral_nemo_response": mistral_nemo_response,
        "llama32_response": llama32_response,
        "gemma2_response": gemma2_response
    }

def main():
    # Load JSON data
    print("[DEBUG] Loading JSON data...")
    with open(input_json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    print(f"[DEBUG] Loaded {len(data)} articles from JSON.")

    # Create or open the output CSV
    with open(output_csv_path, "w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["name", "description", "url", "mistral_nemo_response", "llama32_response", "gemma2_response"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()  # Ensure headers are included in the CSV
        for article in tqdm(data, desc="Processing articles"):
            result = process_article(article)
            writer.writerow(result)
            csv_file.flush()  # Ensure each line is written immediately
            print(f"[INFO] Processed article: {result['name']}")

if __name__ == "__main__":
    main()
