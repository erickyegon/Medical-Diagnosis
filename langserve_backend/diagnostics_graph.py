from langchain_core.runnables import RunnableLambda
from tools.diagnosis_tool import ai_diagnosis
from tools.symptom_checker import check_symptom


def build_graph():
    """Build a simple medical diagnosis chain"""

    def medical_diagnosis_chain(input_data):
        """Process medical diagnosis request"""

        # Extract input text
        if isinstance(input_data, dict):
            user_input = input_data.get("input", "")
        else:
            user_input = str(input_data)

        # Validate input
        if not user_input or user_input.strip() == "":
            return {
                "input": user_input,
                "symptom_area": "No input provided",
                "diagnosis": "Please provide symptom description for diagnosis"
            }

        # Step 1: Get symptom category
        try:
            symptom_area = check_symptom.invoke(user_input)
        except Exception as e:
            symptom_area = f"Error categorizing symptoms: {str(e)}"

        # Step 2: Get AI diagnosis
        try:
            diagnosis = ai_diagnosis.invoke(user_input)
        except Exception as e:
            diagnosis = f"Error getting diagnosis: {str(e)}"

        # Return structured result
        return {
            "input": user_input,
            "symptom_area": symptom_area,
            "diagnosis": diagnosis
        }

    return RunnableLambda(medical_diagnosis_chain)