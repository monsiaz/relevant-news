import json
import csv
import subprocess
import os
from tqdm import tqdm

# Input JSON file path
input_json_path = "/Users/simonazoulay/Clean_news/orange.json"
# Output CSV file path
output_csv_path = "/Users/simonazoulay/Clean_news/resultats_articles.csv"

# Template for the model prompt (in French for consistency in responses)
prompt_template = (
    "En lisant/analysant \"{name}\" et \"{description}\", je veux que tu me répondes par \"Oui\" ou \"Non\" en français. "
    "Tu dois seulement répondre par \"Oui\" ou \"Non\", sans commentaire supplémentaire. "
    "La question est la suivante : je suis un site de données financières et légales sur les entreprises, et je souhaite savoir si cette information est pertinente pour l'associer en tant qu'information récente sur la fiche entreprise dédiée. "
    "\"Oui\" si l'information est pertinente -> Cela signifie : "
    "- elle concerne l'entreprise et son activité en France ou en Europe "
    "- elle peut être intéressante pour comprendre des hausses ou baisses d'activités "
    "- elle peut être intéressante si elle impacte l'entreprise sur le plan juridique/stratégique ou réglementaire. "
    "Exemples d'informations pertinentes pour \"Orange\" : "
    "\"name\": \"Fibre optique : le Conseil d'État confirme une amende record de 26 millions d'euros pour Orange\", "
    "\"description\": \"L'Arcep impose une sanction financière à Orange pour avoir manqué à ses obligations de déploiement dans des zones où l'accès au très haut débit reste un enjeu majeur. Cette décision fait suite à une procédure entamée depuis 2022.\", "
    "\"Non\" si l'information est non pertinente -> Cela signifie : "
    "- elle n'est pas relative à l'entreprise (c'est un synonyme ou homonyme). "
    "- elle relate une information de type général (qui n'intéressera pas nos lecteurs). "
    "Exemples d'informations non pertinentes pour \"Orange\" : "
    "\"name\": \"PHOTOS - À Orange, les viticulteurs brisent des bouteilles de vin pour dénoncer des prix trop bas en grande surface\", "
    "\"description\": \"Nouvelle mobilisation des producteurs de vin du Vaucluse contre les prix trop bas pratiqués par les grandes surfaces. Ils ont brisé des bouteilles de Côtes du Rhône pour demander une juste rémunération.\""
)

def query_model_with_ollama(model_name, prompt):
    try:
        print(f"[DEBUG] Full prompt for {model_name}: {prompt}")
        result = subprocess.run(
            ["ollama", "run", model_name],
            input=prompt,
            text=True,
            capture_output=True
        )
        if result.returncode != 0:
            print(f"[ERROR] Model {model_name} failed with return code {result.returncode}: {result.stderr}")
        
        # Print the full response for debugging
        response = result.stdout.strip()
        print(f"[DEBUG] Full response from {model_name}: {response}")
        
        # Return the full response in French
        return response
    except Exception as e:
        print(f"[ERROR] Exception occurred while running model {model_name}: {str(e)}")
        return f"Erreur: {str(e)}"

def process_article(article):
    name = article.get("name", "")
    description = article.get("description", "")
    url = article.get("url", "")

    # Generate dynamic prompts
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

    # Create the output CSV with headers
    print("[DEBUG] Creating output CSV with headers...")
    with open(output_csv_path, "w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["name", "description", "url", "mistral_nemo_response", "llama32_response", "gemma2_response"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()  # Write headers

        # Process each article and write results to the CSV
        for article in tqdm(data, desc="Analyzing articles"):
            result = process_article(article)
            writer.writerow(result)
            csv_file.flush()  # Ensure each row is immediately written to the file
            print(f"[INFO] Processed article: {result['name']}")

if __name__ == "__main__":
    main()
