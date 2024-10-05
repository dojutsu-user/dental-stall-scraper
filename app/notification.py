from app.logger import logger


class Notification:
    def notify(self, new_count: int, updated_count: int):
        """Send notification - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses should implement this method.")


class LoggingNotification(Notification):
    def notify(self, new_count: int, updated_count: int):
        """Log the notification result"""
        logger.info(f"SENDING_NOTIFICATION: {new_count} new products scraped and {
                    updated_count} products updated.")


class EmailNotification(Notification):
    def notify(self, new_count: int, updated_count: int, recipient_email: str):
        """Send email notification"""
        # Implement email sending logic here
        logger.info(f"""Sending email to {recipient_email}: {
                    new_count} new products scraped and {updated_count} products updated.""")


class SMSNotification(Notification):
    def notify(self, new_count: int, updated_count: int, recipient_phone: str):
        """Send SMS notification"""
        # Implement SMS sending logic here
        logger.info(f"""Sending SMS to {recipient_phone}: {
                    new_count} new products scraped and {updated_count} products updated.""")
