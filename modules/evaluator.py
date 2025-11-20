import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig, Part
import json
from typing import List, Optional
from pydantic import BaseModel, Field

class EvaluationResult(BaseModel):
    persona_id: str = Field(description="ID of the persona giving the evaluation")
    decision: str = Field(description="YES (Buy/Click) or NO (Skip)")
    score: int = Field(description="Attractiveness score out of 10")
    reasoning: str = Field(description="Reasoning for the decision from the persona's perspective")
    feedback: str = Field(description="Specific feedback or improvement suggestion")

class EvaluationList(BaseModel):
    evaluations: List[EvaluationResult]

def evaluate_creative(
    product_name: str,
    product_features: str,
    personas: List[dict],
    creative_image_data: Optional[bytes] = None,
    creative_image_mime_type: Optional[str] = None,
    creative_text: Optional[str] = None
) -> List[dict]:
    """
    Evaluates the creative using the generated personas and Vertex AI.
    """
    
    model = GenerativeModel("gemini-1.5-pro")
    
    # Construct the prompt context
    personas_str = json.dumps(personas, ensure_ascii=False, indent=2)
    
    prompt_text = f"""
    You are simulating a focus group consisting of the following personas:
    {personas_str}
    
    Product: {product_name}
    Features: {product_features}
    
    Please evaluate the provided creative content (image and/or text) from the perspective of EACH persona.
    
    For each persona:
    1. Analyze the creative visually (if image provided) and textually.
    2. Determine if it appeals to their specific values and needs.
    3. Decide if they would click/buy (YES/NO).
    4. Give a score (1-10).
    5. Provide reasoning in their voice.
    6. Suggest improvements.
    
    Output the result strictly in JSON format following the schema provided.
    """
    
    parts = [prompt_text]
    
    if creative_text:
        parts.append(f"Creative Text/Copy: {creative_text}")
        
    if creative_image_data and creative_image_mime_type:
        image_part = Part.from_data(data=creative_image_data, mime_type=creative_image_mime_type)
        parts.append(image_part)
        
    generation_config = GenerationConfig(
        response_mime_type="application/json",
        response_schema=EvaluationList.model_json_schema()
    )
    
    try:
        response = model.generate_content(
            parts,
            generation_config=generation_config,
        )
        
        json_response = json.loads(response.text)
        return json_response.get("evaluations", [])
        
    except Exception as e:
        print(f"Error evaluating creative: {e}")
        return []
