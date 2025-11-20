import streamlit as st

st.set_page_config(page_title="Persona-Critic", layout="wide")

st.title("Persona-Critic (MVP)")
st.write("AI Persona-based Creative Evaluation")


import json
from modules.generator import generate_personas
from modules.evaluator import evaluate_creative

# Sidebar for configuration (optional, maybe for API keys later)
with st.sidebar:
    st.header("Configuration")
    st.info("Using Vertex AI (Gemini 1.5 Pro)")

# --- Input Module ---
st.header("1. Campaign Input")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Product Info")
    product_name = st.text_input("Product Name", placeholder="e.g. Super Energy Drink")
    product_price = st.text_input("Product Price", placeholder="e.g. 300 JPY")
    product_features = st.text_area("Product Features", placeholder="e.g. Zero sugar, 200mg caffeine, organic ingredients")
    
with col2:
    st.subheader("Target Audience")
    target_definition = st.text_area("Target Definition", placeholder="e.g. Office workers in Tokyo, 30s, health-conscious, income > 6M JPY")

st.subheader("Creative Assets")
creative_image = st.file_uploader("Upload Creative Image (Banner/LP)", type=["jpg", "png", "jpeg"])
creative_text = st.text_area("Creative Text (Copy/Message)", placeholder="e.g. Boost your energy without the crash!")

if st.button("Generate Personas & Evaluate"):
    if not product_name or not target_definition or not (creative_image or creative_text):
        st.error("Please fill in all required fields (Product Name, Target, and at least one Creative).")
    else:
        # Combine features and price for the model
        full_product_info = f"{product_features}\nPrice: {product_price}" if product_price else product_features

        with st.spinner("Generating Personas..."):
            personas = generate_personas(product_name, full_product_info, target_definition)
            
        if not personas:
            st.error("Failed to generate personas. Please try again.")
        else:
            st.success(f"Generated {len(personas)} personas!")
            
            # Display Personas (Expandable)
            with st.expander("View Generated Personas", expanded=False):
                st.json(personas)

            with st.spinner("Evaluating Creative..."):
                # Prepare image data if uploaded
                image_bytes = None
                mime_type = None
                if creative_image:
                    image_bytes = creative_image.getvalue()
                    mime_type = creative_image.type
                
                evaluations = evaluate_creative(
                    product_name, 
                    full_product_info, 
                    personas, 
                    image_bytes, 
                    mime_type, 
                    creative_text
                )
            
            if not evaluations:
                st.error("Failed to evaluate creative.")
            else:
                st.header("2. Evaluation Results")
                
                # --- Summary Metrics ---
                yes_count = sum(1 for e in evaluations if e.get("decision") == "YES")
                avg_score = sum(e.get("score", 0) for e in evaluations) / len(evaluations)
                
                m1, m2 = st.columns(2)
                m1.metric("Pseudo-CTR (Buy/Click)", f"{yes_count}/{len(evaluations)}")
                m2.metric("Average Attractiveness Score", f"{avg_score:.1f}/10")
                
                # --- Detailed Feedback ---
                st.subheader("Persona Feedback")
                
                # Create a mapping of persona_id to persona details for easy lookup
                persona_map = {p["persona_id"]: p for p in personas}
                
                for eval_item in evaluations:
                    p_id = eval_item.get("persona_id")
                    persona = persona_map.get(p_id, {})
                    p_name = persona.get("demographics", {}).get("name", "Unknown")
                    p_job = persona.get("demographics", {}).get("occupation", "")
                    
                    with st.container():
                        st.markdown(f"**{p_name}** ({p_job})")
                        c1, c2 = st.columns([1, 3])
                        with c1:
                            decision = eval_item.get("decision")
                            score = eval_item.get("score")
                            color = "green" if decision == "YES" else "red"
                            st.markdown(f":{color}[{decision}] (Score: {score})")
                        with c2:
                            st.markdown(f"_{eval_item.get('reasoning')}_")
                            st.info(f"💡 {eval_item.get('feedback')}")
                        st.divider()
                
                # --- Export Results ---
                import pandas as pd
                
                # Prepare data for export
                export_data = []
                for eval_item in evaluations:
                    p_id = eval_item.get("persona_id")
                    persona = persona_map.get(p_id, {})
                    export_data.append({
                        "Persona Name": persona.get("demographics", {}).get("name"),
                        "Age": persona.get("demographics", {}).get("age"),
                        "Occupation": persona.get("demographics", {}).get("occupation"),
                        "Decision": eval_item.get("decision"),
                        "Score": eval_item.get("score"),
                        "Reasoning": eval_item.get("reasoning"),
                        "Feedback": eval_item.get("feedback")
                    })
                
                df = pd.DataFrame(export_data)
                csv = df.to_csv(index=False).encode('utf-8')
                
                st.download_button(
                    label="📥 Download Report (CSV)",
                    data=csv,
                    file_name="persona_critic_report.csv",
                    mime="text/csv",
                )

