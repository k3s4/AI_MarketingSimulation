import json
from modules.generator import generate_personas
from modules.evaluator import evaluate_creative

def test_flow():
    print("--- Starting Verification Flow ---")
    
    product_name = "Eco-Friendly Water Bottle"
    product_features = "Keeps water cold for 24h, made from recycled ocean plastic, lifetime warranty."
    product_price = "4500 JPY"
    full_product_info = f"{product_features}\nPrice: {product_price}"
    target_definition = "Environmentally conscious millennials, outdoor enthusiasts."
    creative_text = "Save the planet, one sip at a time. The last water bottle you'll ever need."
    
    print(f"Product: {product_name}")
    print(f"Price: {product_price}")
    print(f"Target: {target_definition}")
    
    # 1. Generate Personas
    print("\n1. Generating Personas...")
    personas = generate_personas(product_name, full_product_info, target_definition, count=3)
    
    if not personas:
        print("FAILED: No personas generated.")
        return
        
    print(f"SUCCESS: Generated {len(personas)} personas.")
    print(json.dumps(personas, indent=2, ensure_ascii=False))
    
    # 2. Evaluate Creative
    print("\n2. Evaluating Creative...")
    evaluations = evaluate_creative(
        product_name,
        full_product_info,
        personas,
        creative_text=creative_text
    )
    
    if not evaluations:
        print("FAILED: No evaluations returned.")
        return
        
    print(f"SUCCESS: Received {len(evaluations)} evaluations.")
    print(json.dumps(evaluations, indent=2, ensure_ascii=False))
    
    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    test_flow()
