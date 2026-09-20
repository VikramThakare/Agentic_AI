import asyncio
from agent import ClinicalEscalationAgent, get_patient_context, get_vital_history, get_clinical_protocol

async def test_tools():
    print("--- Testing Patient Context Tool ---")
    ctx = get_patient_context("P-003")
    print(ctx)
    
    print("\n--- Testing Vital History Tool ---")
    vit = get_vital_history("P-003")
    print(vit)
    
    print("\n--- Testing Protocol Retrieval Tool ---")
    prot = get_clinical_protocol("spo2_percent respiratory_rate_bpm")
    print(prot)

async def test_agent_fallback():
    print("\n--- Testing Agent Execution ---")
    agent = ClinicalEscalationAgent()
    if not agent.is_available:
        print("Note: Gemini API Key not set. Testing fallback mode...")
    else:
        print("Note: Gemini API Key found. Testing live agent (may take a few seconds)...")
        
    res = await agent.generate_recommendation("P-003", 8.0, ["spo2_percent", "respiratory_rate_bpm"])
    print("\nStructured Response:")
    for key, value in res.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    asyncio.run(test_tools())
    asyncio.run(test_agent_fallback())
