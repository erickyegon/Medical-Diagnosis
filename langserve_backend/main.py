from fastapi import FastAPI
from langserve import add_routes
from pydantic import BaseModel
from diagnostics_graph import build_graph

# Define explicit input/output schemas
class DiagnosisRequest(BaseModel):
    input: str

class DiagnosisResponse(BaseModel):
    input: str
    symptom_area: str
    diagnosis: str

app = FastAPI(
    title="Medical Diagnostics API",
    description="AI-powered medical diagnosis support system",
    version="1.0.0"
)

# Add a simple health check endpoint
@app.get("/")
async def root():
    return {"message": "Medical Diagnostics API is running", "status": "healthy"}

# Add a simple test endpoint
@app.post("/test", response_model=DiagnosisResponse)
async def test_diagnosis(request: DiagnosisRequest):
    """Simple test endpoint for diagnosis"""
    try:
        diagnosis_chain = build_graph()
        result = diagnosis_chain.invoke({"input": request.input})
        return DiagnosisResponse(**result)
    except Exception as e:
        return DiagnosisResponse(
            input=request.input,
            symptom_area="Error",
            diagnosis=f"Error: {str(e)}"
        )

# Build and add the diagnosis chain with explicit schemas
try:
    diagnosis_chain = build_graph()

    add_routes(
        app,
        diagnosis_chain,
        path="/diagnose"
    )
    print("✅ Diagnosis chain added successfully")
except Exception as e:
    print(f"❌ Error building diagnosis chain: {e}")

    # Add a fallback endpoint if the main chain fails
    @app.post("/diagnose/fallback")
    async def diagnose_fallback(input_data: DiagnosisRequest):
        return DiagnosisResponse(
            input=input_data.input,
            symptom_area="Service Error",
            diagnosis=f"Diagnosis service unavailable: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
