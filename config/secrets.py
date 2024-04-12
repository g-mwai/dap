# config/secrets.py

from google.cloud import secretmanager
import os

# Initialize the Secret Manager client
client = secretmanager.SecretManagerServiceClient()

def get_secret(secret_id, project_id):
    # Construct the secret name
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    # Retrieve the secret
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# Example usage:
# DATABASE_PASSWORD = get_secret("database-password", "your-project-id")
# SECRET_KEY = get_secret("django-secret-key", "your-project-id")
