import os
from google.cloud import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument

# Set your Google Cloud credentials (ensure the environment variable is set correctly)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your-service-account-file.json"

# Define the project, agent, and session ID (you can replace these values as needed)
PROJECT_ID = "your-project-id"
AGENT_ID = "your-agent-id"  # For Dialogflow agents
SESSION_ID = "unique-session-id"  # You can use user-specific session IDs for multiple conversations

# Function to send message to Vertex AI (Dialogflow)
def detect_intent_texts(project_id, session_id, text, language_code='en'):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    
    try:
        response = session_client.detect_intent(request={"session": session, "query_input": query_input})
        return response.query_result.fulfillment_text
    except InvalidArgument as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't process your request right now."
