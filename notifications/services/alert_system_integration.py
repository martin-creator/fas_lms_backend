import requests

def send_external_alert(user_id, alert_type, message):
    alert_endpoint = "https://alerts.example.com/api/notify"
    payload = {
        "user_id": user_id,
        "alert_type": alert_type,
        "message": message
    }
    response = requests.post(alert_endpoint, json=payload)
    response.raise_for_status()