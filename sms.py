from notification import NotificationStrategy

class SMSNotification(NotificationStrategy):
    def __init__(self, sms_gateway, auth_token, from_number):
        self.sms_gateway = sms_gateway
        self.auth_token = auth_token
        self.from_number = from_number

    def send_notification(self, message: str):
        # Implement SMS sending logic using an SMS gateway API
        print(f"Sending SMS: {message}")