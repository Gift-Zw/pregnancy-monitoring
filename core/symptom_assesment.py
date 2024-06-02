import google.generativeai as genai
import certifi

genai.configure(api_key="AIzaSyDqMzdjSvbYtwsSu6zR1Yrg8PbEhJE91L0",)


def get_assessment(symptoms):
    model = genai.GenerativeModel("gemini-pro")
    chat = model.start_chat()
    response = chat.send_message( "I am pregnant and have the following sysmptoms: {0}. The response should be one paragraph".format(symptoms))
    # Extract necessary data from response
    response_data = {
        "text": response.text,  # Assuming response.text contains the relevant response data
        # Add other relevant data from response if needed
    }
    return response_data
