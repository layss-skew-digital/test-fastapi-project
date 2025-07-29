from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
from schamas import CustomerMessageRequest, MainResponse
from services.gbt_service import CustomerSupportAIService

load_dotenv()


app = FastAPI(
    title="Customer Support AI Service",
    description="AI-powered customer support message classification and response generation",
    version="1.0.0",
)


@app.get("/")
def read_root():
    return {"message": "Customer Support AI Service", "status": "running"}


@app.post("/process-customer-message", response_model=MainResponse)
def process_customer_message(request: CustomerMessageRequest):
    try:
        # Check if OpenAI API key exists
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required. Please add it to your .env file."
            )

        # Initialize AI service and process the message
        ai_service = CustomerSupportAIService()
        response = ai_service.classify_and_generate_response(request)

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    """
    Health check endpoint to verify the application is running properly
    """
    return {
        "status": "healthy",
        "message": "Application is running successfully",
        "openai_key_configured": bool(os.getenv("OPENAI_API_KEY")),
    }
