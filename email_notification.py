from notification import NotificationStrategy
class EmailNotification(NotificationStrategy):
    def __init__(self, smtp_server, port, login, password, from_addr):
        self.smtp_server = smtp_server
        self.port = port
        self.login = login
        self.password = password
        self.from_addr = from_addr

    def send_notification(self, message: str):
        print(f"Sending Email Notification: {message}")
