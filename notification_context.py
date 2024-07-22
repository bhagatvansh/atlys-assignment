from notification import NotificationStrategy

class NotificationContext:
    def __init__(self, strategy: NotificationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: NotificationStrategy):
        self._strategy = strategy

    def notify(self, products):
        for product in products:
            self._strategy.send_notification(f"Product {product['product_title']} price updated to {product['product_price']}")
