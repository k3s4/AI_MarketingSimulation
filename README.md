# Persona-Critic (MVP)

**Persona-Critic** is an AI agent that automates the "focus group" process for ad creatives.
Leveraging Google Cloud Vertex AI (Gemini 2.5 Pro), it generates diverse AI personas based on your target audience and has them evaluate your creative assets.

## Features

- **Automated Persona Generation**: Generates 5 diverse personas with specific values, pain points, and budgets based on your product and target description.
- **Creative Evaluation**: Personas analyze your image or text creative, deciding whether to "Buy" or "Skip" based on their unique attributes.
- **Pseudo-CTR Calculation**: Calculates a potential Click-Through Rate based on the persona decisions.
- **Actionable Feedback**: Provides specific reasoning and improvement suggestions from each persona's perspective.
- **Exportable Reports**: Download the evaluation results as a CSV file for further analysis.

## Setup

### Prerequisites
- Python 3.10+
- Google Cloud Project (Vertex AI API enabled)

### Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Google Cloud Authentication
You must authenticate with Google Cloud to use Vertex AI.
```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

## Usage

Start the Streamlit application:

```bash
streamlit run app.py
```

The app will open in your browser (usually `http://localhost:8501`).

1. **Input Campaign Info**: Enter Product Name, Price, Features, and Target Audience.
2. **Upload Creative**: Upload an image (Banner/LP) or enter copy text.
3. **Generate & Evaluate**: Click the button to generate personas and get their feedback.
4. **Download Report**: Use the "Download Report (CSV)" button to save the results.

## Tech Stack
- **Frontend**: Streamlit
- **AI Model**: Google Vertex AI (Gemini 2.5 Pro)
- **Language**: Python
