# msal_config.py
 
import os
 
# MSAL Configuration (client_id, authority, and redirect_uri are from Azure AD app registration)
msal_config = {
    "client_id": "72354d86-fbcf-492c-a7cc-78a924bb3fc9",  # Replace with your app's client ID
    "authority": "https://login.microsoftonline.com/05d75c05-fa1a-42e7-9cf1-eb416c396f2d",  # Replace with your tenant ID
    "client_secret": "QFn8Q~0K9nw6Gs4z7Muh5295BPNMoafw-V.pVbdt",  # Optional for confidential client
    "redirect_uri": "http://localhost:8000",  # Replace with your app's redirect URI
    "scopes": ["User.Read"],  # Define the API permissions (e.g., Microsoft Graph API)
}