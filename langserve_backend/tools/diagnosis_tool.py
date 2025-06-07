from langchain.tools import tool
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.euri_client import euri_chat_completion


@tool
def ai_diagnosis(symptom_description: str) -> str:
    """Use euri to provide diagnosis suggestions based on symptoms reported by users.

    Args:
        symptom_description: A string describing the patient's symptoms

    Returns:
        A string containing possible diagnoses, next steps, and treatment suggestions
    """
    try:
        message = [
            {
                "role": "user",
                "content": f"A patient reports: {symptom_description}. What are the possible diagnoses, next steps, and suggested treatments for this condition?"
            }
        ]

        return euri_chat_completion(messages=message)
    except Exception as e:
        return f"Error occurred while processing diagnosis request: {str(e)}"