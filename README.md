
# News Relevance Filter Script

## Overview

This Python script is designed to evaluate the relevance of news articles in a JSON feed based on specific criteria for a business-oriented platform. Using a set of AI models, it analyzes each article to determine whether it aligns with the company's economic, legal, financial, or strategic activity. The script processes each article using multiple AI models and saves the responses into a CSV file for further review and analysis.

## Purpose

The primary goal of this script is to streamline the process of filtering news articles, ensuring that only relevant articles appear in the company's platform. The relevance criteria focus on articles that provide insights into business activities, legal developments, or market trends directly affecting the company in question.

### Key Relevance Criteria
The script is designed to identify articles that:
- Concern the company’s business or operational activities in France or Europe.
- Provide insights into market shifts, such as increases or decreases in activity.
- Have legal, strategic, or regulatory implications that might impact the company.

By utilizing these criteria, the script assists in automating news relevance checks, ensuring that only pertinent articles are retained for display or analysis.

## How It Works

The script reads a JSON file containing news articles, then:
1. Uses a defined prompt template to query three AI models (`mistral-nemo:latest`, `llama3.2:latest`, and `gemma2:9b`) for each article's relevance.
2. Records each model’s response in a CSV file.
3. Outputs the article title, description, URL, and the models' responses ("Yes" or "No") indicating relevance.

### AI Models and Responses
The script queries three different models, which provide independent assessments of each article. Each model's response is recorded separately in the output CSV, allowing for comparison and evaluation of consistency.

## Prerequisites

### 1. Python 3.x
Ensure that you have Python 3.x installed on your machine.

### 2. Dependencies
Install the required packages using:
```bash
pip install tqdm
```

### 3. `ollama` CLI
This script uses `ollama` to interact with the AI models. Ensure that `ollama` is installed and properly configured.

### 4. Input JSON File
Prepare a JSON file containing the news articles, structured as follows:
```json
[
  {
    "name": "Article title",
    "description": "Brief article description",
    "url": "https://example.com/article-url"
  },
  ...
]
```

### 5. Output CSV File
Define a path for the output CSV file, where the results will be stored.

## Usage

### Running the Script
To run the script, simply execute:

```bash
python news_relevance_filter.py
```

The script will:
1. Load the JSON data from the specified input file.
2. Process each article by querying each AI model with a standardized prompt.
3. Write the results into a CSV file, which includes:
   - `name`: Article title.
   - `description`: Article description.
   - `url`: URL of the article.
   - `mistral_nemo_response`: Relevance assessment by the Mistral-Nemo model.
   - `llama32_response`: Relevance assessment by the Llama model.
   - `gemma2_response`: Relevance assessment by the Gemma model.

### Output Example
An example row in the output CSV will look like:
```
name,description,url,mistral_nemo_response,llama32_response,gemma2_response
"Orange fined for network issues","The Council of State confirmed a fine against Orange for failure to meet network obligations.","https://example.com/article","Yes","Yes","No"
```

### Debugging
To assist with debugging, the script outputs each model’s prompt and response in the console. This allows you to review and assess each AI model's interpretation of the prompt.

## Customization

You can customize the script by modifying the `prompt_template` to adjust the relevance criteria based on specific needs or add additional models if required. 

## Model Comparison and Relevance Analysis

### Objective
The purpose of this analysis is to determine which AI model (`mistral-nemo`, `llama32`, or `gemma2`) provides the most consistent and accurate relevance assessment for articles related to a company’s economic, legal, financial, and strategic activity. Each model’s performance was evaluated based on its ability to identify relevant news articles while excluding unrelated content.

### Analysis Results

After testing the models, **`gemma2:9b` emerged as the most reliable and consistent model** for this use case, based on the following observations:

1. **Relevance to Economic and Strategic Activity**  
   `gemma2:9b` consistently marked articles relevant to business activities, such as those about regulatory fines or major strategic partnerships (e.g., *"Supercomputing for French Military AI"* and *"Orange fined for network obligations"*). These articles align well with the platform's economic and strategic relevance criteria.  
   In comparison, `llama32` often returned "No" even for articles directly related to economic and strategic developments, making it less aligned with the platform's objectives.

2. **Accurate Identification of Non-Relevant Articles**  
   In cases where "Orange" was mentioned as a location rather than the company (e.g., *"PHOTOS - In Orange, winemakers protest supermarket prices"*), `gemma2:9b` reliably responded with "No," demonstrating its ability to distinguish between contextually irrelevant mentions and relevant brand references.  
   Both `mistral-nemo` and `llama32` showed some inconsistency, occasionally misclassifying irrelevant articles as relevant.

3. **Broad Coverage of Pertinent Topics**  
   `gemma2:9b` accurately captured relevance for articles about partnerships, investments, and legal issues, showing strong alignment with the platform's financial and strategic news requirements.  
   This model was also adept at recognizing the significance of regulatory and legal news, consistently returning "Yes" for articles with regulatory implications, while `llama32` displayed a conservative bias, with many "No" responses that excluded relevant articles.

### Summary of Model Performance

- **`gemma2:9b`**: Demonstrated the strongest alignment with the defined criteria for economic, legal, and strategic relevance, making it the most suitable model for this purpose.
- **`mistral-nemo`**: Provided correct classifications for some articles but displayed less consistency, occasionally missing key strategic articles.
- **`llama32`**: Showed a tendency toward overly conservative responses, frequently marking articles as irrelevant, even when they aligned with business-oriented criteria.

### Conclusion

Based on these observations, **`gemma2:9b` is recommended as the primary model** for evaluating article relevance. Its performance is well-suited to the platform's focus on business, financial, and regulatory news, ensuring that pertinent articles are consistently identified while irrelevant mentions are effectively filtered out.



## License
This project is open for educational and non-commercial use. For commercial applications, please consult your organization’s compliance guidelines.

## Contact
For questions or feedback, please reach out to our development team.
