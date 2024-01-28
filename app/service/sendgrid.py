from typing import Dict
from retry import retry
from sendgrid.helpers.mail import FileContent, FileName, FileType, Disposition, To, Email, Content, Mail, Attachment


class SendgridClient:
    def __init__(self, sendgrid):
        self.sendgrid = sendgrid

    def config(self, token):
        if token == "" or token is None:
            raise Exception("empty api key")
        self.sendgrid.api_key = token

    def with_subject(self, violation_reason, asin) -> str:
        return f"Request for Review Removal - ASIN: {asin} - Violated Policy: {violation_reason}"

    def with_body(self, asin, reviewer, review, review_id, flag_reason, sender) -> str:
        return f"""Dear Community Help,

I am reaching out to you today concerning a product review that may breach Amazon's Customer Review Policy.

The review in question can be located under ASIN: {asin}, and it was posted by a user with the username {reviewer}.

Here’s the content of the review:

Review ID: {review_id}
Review: "{review}"

Upon careful examination, this review infringes upon your review policies for the reasons listed below:

{flag_reason}

I would like to request your assistance in reviewing this case and, if appropriate, removing the review to maintain a fair and unbiased review environment for our customers.

We place immense value on the authenticity of customer feedback and fully comprehend the significance of sincere reviews for our enterprise and prospective customers. While we have no intention of suppressing negative feedback, we firmly stand by the notion that all reviews should strictly conform to Amazon's established policies.

I appreciate your attention to this matter.

Best regards,

{sender}"""

    @retry(tries=5, delay=1, backoff=2, max_delay=32)
    def send_with_attachment(self, to_email, subject, attachment_contents: dict):
        _from = Email(email="tsomkanda@gmail.com", name="Thabang @ MorningSide")
        _to = To(to_email)
        _body = Content("text/plain", "Find your attached CSV below.")
        _attachment = Attachment(
             FileContent(attachment_contents["file_content"]),
             FileName(attachment_contents["file_name"]),
             FileType(attachment_contents["file_type"]),
             Disposition("attachment")
         )
        _mail = Mail(_from, _to, subject, _body)
        _mail.add_attachment(_attachment)
        try:
            response = self.sendgrid.client.mail.send.post(
                request_body=_mail.get())
            if response.status_code < 300:
                return {
                "status_code": response.status_code,
                "message:": response.body
            }
            return {
                "status_code": response.status_code,
                "message:": "message did not send"
            }
        except Exception as e:
            raise ValueError("Sendgrid Client error:", e)

    @retry(tries=5, delay=1, backoff=2, max_delay=32)
    def send(self, to_email, subject, body) -> Dict:
        _from = Email(email="tsomkanda@gmail.com", name="Thabang @ MorningSide")
        _to = To(to_email)
        _body = Content("text/plain", body)
        _mail = Mail(_from, _to, subject, _body)
        try:
            response = self.sendgrid.client.mail.send.post(
                request_body=_mail.get())
            if response.status_code < 300:
                return {
                "status_code": response.status_code,
                "message:": response.body
            }
            return {
                "status_code": response.status_code,
                "message:": "message did not send"
            }
        except Exception as e:
            raise ValueError("Sendgrid Client error:", e)
