import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
import json
from typing import List
from pydantic import BaseModel, Field

# Initialize Vertex AI (You might need to set project and location explicitly if not in env)
# vertexai.init(project="your-project-id", location="us-central1")
# For now, we assume the environment is configured or we'll handle it in app.py

class Demographics(BaseModel):
    name: str = Field(description="Name of the persona")
    age: int = Field(description="Age of the persona")
    occupation: str = Field(description="Occupation of the persona")


class Psychographics(BaseModel):
    core_value: str = Field(description="Core value (e.g., Efficiency, Cost-performance)")
    spending_habit: str = Field(description="Spending habit (e.g., Cautious, Impulsive)")
    current_worry: str = Field(description="Current worry or pain point")
    budget_sensitivity: str = Field(description="Budget sensitivity (High/Medium/Low)")
    personality: str = Field(description="Personality traits (e.g., Impulsive buyer, Careful planner)")

class Persona(BaseModel):
    persona_id: str = Field(description="Unique ID for the persona (e.g., p_001)")
    demographics: Demographics
    psychographics: Psychographics

class PersonaList(BaseModel):
    personas: List[Persona]

def generate_personas(product_name: str, product_features: str, target_definition: str, count: int = 5) -> List[dict]:
    """
    Generates a list of personas based on product info and target definition using Vertex AI.
    """
    
    model = GenerativeModel("gemini-1.5-pro")
    
    prompt = f"""
    You are a professional marketing strategist.
    Your task is to generate {count} detailed and diverse user personas for a specific product.
    
    Product Name: {product_name}
    Product Features: {product_features}
    Target Audience Definition: {target_definition}
    
    Please generate {count} personas that fit within this target audience but have different backgrounds, values, and personalities to ensure a wide range of feedback.
    
    Output the result strictly in JSON format following the schema provided.
    """
    
    generation_config = GenerationConfig(
        response_mime_type="application/json",
        response_schema=PersonaList.model_json_schema()
    )
    
    try:
        response = model.generate_content(
            prompt,
            generation_config=generation_config,
        )
        
        # Parse the response
        json_response = json.loads(response.text)
        return json_response.get("personas", [])
        
    except Exception as e:
        print(f"Error generating personas: {e}")
        # Return empty list or handle error appropriately
        return []

if __name__ == "__main__":
    # Test run
    personas = generate_personas(
        "Super Energy Drink", 
        "Zero sugar, 200mg caffeine", 
        "Office workers in Tokyo, 30s"
    )
    print(json.dumps(personas, indent=2, ensure_ascii=False))
