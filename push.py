from notification import NotificationStrategy

class PushNotification(NotificationStrategy):
    def send_notification(self, message: str):
        # Implement push notification logic
        print(f"Sending Push Notification: {message}")
