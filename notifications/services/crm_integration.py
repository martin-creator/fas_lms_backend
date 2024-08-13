# notifications/services/crm_integration.py
import requests

def send_crm_alert(user_id, event_type, event_data):
    crm_endpoint = "https://crm.example.com/api/alerts"
    payload = {
        "user_id": user_id,
        "event_type": event_type,
        "event_data": event_data
    }
    response = requests.post(crm_endpoint, json=payload)
    response.raise_for_status()
