from agent import ClinicalEscalationAgent, get_patient_context, get_vital_history, get_clinical_protocol

def test_tools():
    print("--- Testing Patient Context Tool ---")
    ctx = get_patient_context("P-003")
    print(ctx)
    
    print("\n--- Testing Vital History Tool ---")
    vit = get_vital_history("P-003")
    print(vit)
    
    print("\n--- Testing Protocol Retrieval Tool ---")
    prot = get_clinical_protocol("spo2_percent respiratory_rate_bpm")
    print(prot)

def test_agent():
    print("\n--- Testing Agent Execution ---")
    agent = ClinicalEscalationAgent()
    if not agent.is_available:
        print("Note: GROQ_API_KEY not set. Testing fallback mode...")
    else:
        print("Note: GROQ_API_KEY found. Testing live agent...")
        
    res = agent.generate_recommendation("P-003", 8.0, ["spo2_percent", "respiratory_rate_bpm"])
    print("\nStructured Response:")
    for key, value in res.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    test_tools()
    test_agent()
