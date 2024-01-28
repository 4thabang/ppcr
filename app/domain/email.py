from typing import Dict, Protocol

class BaseEmailService(Protocol):
    def config(self, token):
        """
        Set the configuration values for the email service.

        Args:
            token(str)
        """
        ...

    def with_body(self, asin, reviewer, review, review_id, flag_reason, sender) -> str:
        """
        Add the email body.

        Args:
            product_id(str|int)
            reviewer(str)
            review(str)
            flag_reason(str)
            sender(str)

        Return:
            str: return the formatted email body.
        """
        ...

    def send_with_attachment(self, to_email, subject, attachment_contents: dict) -> Dict:
        """
        Send an email with an attachment.

        Args:
            to_email(str)
            subject(str)
            attachment(dict)

        Return:
            dict: sendgrid email response
        """
        ...

    def send(self, to_email, subject, body) -> Dict:
        """
        Send an email.

        Args:
            to_email(str)
            subject(str)
            body(str)

        Return:
            dict: sendgrid email response 
        """
        ...
