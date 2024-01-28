from urllib.parse import urlparse
from pydantic import Field
from openai_function_call import OpenAISchema

PROMPT = """### Task 
Amazon Product Review ToS Violation Classification and Segmentation

### Description
You are an Amazon terms of service classification model. You will be given a review and the reason that it has been flagged
for violating Amazons reviews terms of service. You are going to check if the review and the reason for it being flagged are in alignment.
You will ensure that the flagged reason discusses buyer side review violations and never seller based violations.

### Notes
- If the review and flagged reason do not align, you will return "False".
- If the review and flagged reason do align but the review discusses the behaviour of the seller, you will return "False"

Otherwise, you will always return "True"
"""


class SellerOrderShippingFeedback(OpenAISchema):
    """Detect whether a review contains feedback about the seller, feedback about the order or feedback about shipping"""
    flagged: bool = Field(
        ..., description="Does this review violate the seller, order and shipping feedback terms of service")
    reason: str = Field(
        ..., description="Why was this review flagged as a violation for this category")

    @staticmethod
    def prompt():
        return """Category: Seller, order, and shipping feedback
    Review: I ordered this product a month ago, and it still hasn't arrived! The seller is unresponsive and doesn't care about their customers.
    Flagged: true
    Flagged Reason: User made negative comments about the seller and shipping experience.

    Category: Seller, order, and shipping feedback
    Review: I ordered this product, and it arrived on time. The seller was helpful in answering my questions.
    Flagged: false
    Flagged Reason: No violation detected.
        """

    @staticmethod
    def function_call(flagged, flagged_reason, review, model, email_client, to_email) -> dict:
        if flagged:
            formatted_prompt = f"Review: {review}\nFlagged Reason: {flagged_reason}"
            response = model.call_model(
                "gpt-3.5-turbo-0613", PROMPT, formatted_prompt)
            validated = response["choices"][0]["message"]["content"]

            url = urlparse(review["URL"])
            split_path = url.path.split("/")
            review_id = split_path[3]  # Return the review ID from URL path

            if validated:
                violation_category = "Seller, order and shipping feedback"
                product_asin = review["Variation"]
                email_subject = email_client.with_subject(violation_category, product_asin)
                email_body = email_client.with_body(
                    product_asin, review["Author"], review["Body"], review_id, flagged_reason, "Miguel @ PPCRoom")
                sg_response = email_client.send(
                    to_email=to_email,
                    subject=email_subject,
                    body=email_body
                )
                return {
                    "response": {
                        "sendgrid_response": sg_response,
                        "email_body": email_body,
                        "violation_category": violation_category
                    }
                }
        return {
            "response": "no violation"
        }


class CommentsPricingAvailability(OpenAISchema):
    """Detect whether a review contains comments about the pricing or the availability of the product"""
    flagged: bool = Field(
        ..., description="Does this review violate the comments about pricing and availability terms of service")
    reason: str = Field(
        ..., description="Why was this review flagged as a violation for this category")

    @staticmethod
    def prompt():
        return """Category: Comments about pricing and availability
    Review: This product is ridiculously overpriced! You can find the same thing for half the price elsewhere.
    Flagged: true
    Flagged Reason: User made negative comments about pricing.

    Category: Comments about pricing and availability
    Review: This product is a bit expensive, but I think the quality justifies the price. I'm satisfied with my purchase.
    Flagged: false
    Flagged Reason: No violation detected.
        """

    @staticmethod
    def function_call(flagged, flagged_reason, review, model, email_client, to_email) -> dict:
        if flagged:
            formatted_prompt = f"Review: {review}\nFlagged Reason: {flagged_reason}"
            response = model.call_model(
                "gpt-3.5-turbo-0613", PROMPT, formatted_prompt)
            validated = response["choices"][0]["message"]["content"]

            url = urlparse(review["URL"])
            split_path = url.path.split("/")
            review_id = split_path[3]  # Return the review ID from URL path

            if validated:
                violation_category = "Comments about pricing and availability"
                product_asin = review["Variation"]
                email_subject = email_client.with_subject(violation_category, product_asin)
                email_body = email_client.with_body(product_asin, review["Author"], review["Body"], review_id, flagged_reason, "Miguel @ PPCRoom")
                sg_response = email_client.send(
                    to_email=to_email,
                    subject=email_subject,
                    body=email_body
                )
                return {
                    "response": {
                        "sendgrid_response": sg_response,
                        "email_body": email_body,
                        "violation_category": violation_category
                    }
                }
        return {
            "response": "no violation"
        }


class UnsupportedLanguage(OpenAISchema):
    """
    Detect whether a review contains unsupported language
    """
    flagged: bool = Field(
        ..., description="Does this review violate the content written in unsupported languages terms of service")
    reason: str = Field(
        ..., description="Why was this review flagged as a violation for this category")

    @staticmethod
    def prompt():
        return """Category: Content written in unsupported languages
    Review: 이 제품은 정말 별로예요. 구매하지 마세요! (Translation: This product is really bad. Do not buy!)
    Flagged: true
    Flagged Reason: User wrote the review in an unsupported language.

    Category: Content written in unsupported languages
    Review: This product is fantastic! I love it, and I highly recommend it to others.
    Flagged: false
    Flagged Reason: No violation detected.
        """

    @staticmethod
    def function_call(flagged, flagged_reason, review, model, email_client, to_email) -> dict:
        if flagged:
            formatted_prompt = f"Review: {review}\nFlagged Reason: {flagged_reason}"
            response = model.call_model(
                "gpt-3.5-turbo-0613", PROMPT, formatted_prompt)
            validated = response["choices"][0]["message"]["content"]

            url = urlparse(review["URL"])
            split_path = url.path.split("/")
            review_id = split_path[3]  # Return the review ID from URL path

            if validated:
                violation_category = "Content written in unsupported languages"
                product_asin = review["Variation"]
                email_subject = email_client.with_subject(violation_category, product_asin)
                email_body = email_client.with_body(
                    product_asin, review["Author"], review["Body"], review_id, flagged_reason, "Miguel @ PPCRoom")
                sg_response = email_client.send(
                    to_email=to_email,
                    subject=email_subject,
                    body=email_body
                )
                return {
                    "response": {
                        "sendgrid_response": sg_response,
                        "email_body": email_body,
                        "violation_category": violation_category
                    }
                }
        return {
            "response": "no violation"
        }


class SpamSymbolsText(OpenAISchema):
    """
    Detect whether a review contains repetitive text, spam, or pictures created with symbols
    """
    flagged: bool = Field(
        ..., description="Does this review violate the repetitive text, spam, pictures created with symbols terms of service")
    reason: str = Field(
        ..., description="Why was this review flagged as a violation for this category")

    @staticmethod
    def prompt():
        return """Category: Repetitive text, spam, pictures created with symbols
    Review: 🌟🌟🌟🌟🌟 Best product ever! 🌟🌟🌟🌟🌟
    Flagged: true
    Flagged Reason: User used repetitive symbols and excessive stars.

    Category: Repetitive text, spam, pictures created with symbols
    Review: The product is good. I'm happy with my purchase.
    Flagged: false
    Flagged Reason: No violation detected.
        """

    @staticmethod
    def function_call(flagged, flagged_reason, review, model, email_client, to_email) -> dict:
        if flagged:
            formatted_prompt = f"Review: {review}\nFlagged Reason: {flagged_reason}"
            response = model.call_model(
                "gpt-3.5-turbo-0613", PROMPT, formatted_prompt)
            validated = response["choices"][0]["message"]["content"]

            url = urlparse(review["URL"])
            split_path = url.path.split("/")
            review_id = split_path[3]  # Return the review ID from URL path

            if validated:
                violation_category = "Repetitive text, spam, pictures created with symbols"
                product_asin = review["Variation"]
                email_subject = email_client.with_subject(violation_category, product_asin)
                email_body = email_client.with_body(
                    product_asin, review["Author"], review["Body"], review_id, flagged_reason, "Miguel @ PPCRoom")
                sg_response = email_client.send(
                    to_email=to_email,
                    subject=email_subject,
                    body=email_body
                )
                return {
                    "response": {
                        "sendgrid_response": sg_response,
                        "email_body": email_body,
                        "violation_category": violation_category
                    }
                }
        return {
            "response": "no violation"
        }


class PrivateInformation(OpenAISchema):
    """
    Detect whether a review container any private information such as emails, phone numbers or addresses
    """
    flagged: bool = Field(
        ..., description="Does this review violate the private information terms of service")
    reason: str = Field(
        ..., description="Why was this review flagged as a violation for this category")

    @staticmethod
    def prompt():
        return """Category: Private information
    Review: I can't believe they shipped the product to my work address, which is 555-1234, instead of my home address!
    Flagged: true
    Flagged Reason: User disclosed private information - phone number.

    Category: Private information
    Review: The product was delivered to the wrong address, but the customer support team was quick to resolve the issue once I provided them with the correct information.
    Flagged: false
    Flagged Reason: No violation detected.
        """

    @staticmethod
    def function_call(flagged, flagged_reason, review, model, email_client, to_email) -> dict:
        if flagged:
            formatted_prompt = f"Review: {review}\nFlagged Reason: {flagged_reason}"
            response = model.call_model(
                "gpt-3.5-turbo-0613", PROMPT, formatted_prompt)
            validated = response["choices"][0]["message"]["content"]

            url = urlparse(review["URL"])
            split_path = url.path.split("/")
            review_id = split_path[3]  # Return the review ID from URL path

            if validated:
                violation_category = "Private information"
                product_asin = review["Variation"]
                email_subject = email_client.with_subject(violation_category, product_asin)
                email_body = email_client.with_body(
                    product_asin, review["Author"], review["Body"], review_id, flagged_reason, "Miguel @ PPCRoom")
                sg_response = email_client.send(
                    to_email=to_email,
                    subject=email_subject,
                    body=email_body
                )
                return {
                    "response": {
                        "sendgrid_response": sg_response,
                        "email_body": email_body,
                        "violation_category": violation_category
                    }
                }
        return {
            "response": "no violation"
        }


class ProfanityHarassmentViolation(OpenAISchema):
    """
    Detect whether a review contains profanity or harassment towards the seller
    """
    flagged: bool = Field(
        ..., description="Does this review violate the profanity and harassment terms of service")
    reason: str = Field(
        ..., description="Why was this review flagged as a violation for this category")

    @staticmethod
    def prompt():
        return """Category: Profanity, harassment
    Review: The customer service of this company is awful! They don't give a damn about their customers' problems!
    Flagged: true
    Flagged Reason: User used profanity - "damn."

    Category: Profanity, harassment
    Review: The customer service representatives were not very helpful, and I had a frustrating experience dealing with them.
    Flagged: false
    Flagged Reason: No violation detected.
        """

    @staticmethod
    def function_call(flagged, flagged_reason, review, model, email_client, to_email) -> dict:
        if flagged:
            formatted_prompt = f"Review: {review}\nFlagged Reason: {flagged_reason}"
            response = model.call_model(
                "gpt-3.5-turbo-0613", PROMPT, formatted_prompt)
            validated = response["choices"][0]["message"]["content"]

            url = urlparse(review["URL"])
            split_path = url.path.split("/")
            review_id = split_path[3]  # Return the review ID from URL path

            if validated:
                violation_category = "Profanity, harassment"
                product_asin = review["Variation"]
                email_subject = email_client.with_subject(violation_category, product_asin)
                email_body = email_client.with_body(
                    product_asin, review["Author"], review["Body"], review_id, flagged_reason, "Miguel @ PPCRoom")
                sg_response = email_client.send(
                    to_email=to_email,
                    subject=email_subject,
                    body=email_body
                )
                return {
                    "response": {
                        "sendgrid_response": sg_response,
                        "email_body": email_body,
                        "violation_category": violation_category
                    }
                }
        return {
            "response": "no violation"
        }


class HateSpeech(OpenAISchema):
    """
    Detect whether a review contains hate speech
    """
    flagged: bool = Field(
        ..., description="Does this review violate the hate speech terms of service")
    reason: str = Field(
        ..., description="Why was this review flagged as a violation for this category")

    @staticmethod
    def prompt():
        return """Category: Hate speech
    Review: This product is trash, just like the people who made it. They should go back to their country and stay there!
    Flagged: true
    Flagged Reason: User used hate speech - xenophobic comment.

    Category: Hate speech
    Review: This product is terrible, and the company should be ashamed of themselves for making such low-quality items.
    Flagged: false
    Flagged Reason: No violation detected.
        """

    @staticmethod
    def function_call(flagged, flagged_reason, review, model, email_client, to_email) -> dict:
        if flagged:
            formatted_prompt = f"Review: {review}\nFlagged Reason: {flagged_reason}"
            response = model.call_model(
                "gpt-3.5-turbo-0613", PROMPT, formatted_prompt)
            validated = response["choices"][0]["message"]["content"]

            url = urlparse(review["URL"])
            split_path = url.path.split("/")
            review_id = split_path[3]  # Return the review ID from URL path

            if validated:
                violation_category = "Hate speech"
                product_asin = review["Variation"]
                email_subject = email_client.with_subject(violation_category, product_asin)
                email_body = email_client.with_body(
                    product_asin, review["Author"], review["Body"], review_id, flagged_reason, "Miguel @ PPCRoom")
                sg_response = email_client.send(
                    to_email=to_email,
                    subject=email_subject,
                    body=email_body
                )
                return {
                    "response": {
                        "sendgrid_response": sg_response,
                        "email_body": email_body,
                        "violation_category": violation_category
                    }
                }
        return {
            "response": "no violation"
        }


class SexualContent(OpenAISchema):
    """
    Detect whether a review contains any sexual content
    """
    flagged: bool = Field(
        ..., description="Does this review violate the sexual content terms of service")
    reason: str = Field(
        ..., description="Why was this review flagged as a violation for this category")

    @staticmethod
    def prompt():
        return """Category: Sexual content
    Review: The product itself is okay, but the images on the packaging are too provocative. Not suitable for all audiences.
    Flagged: true
    Flagged Reason: User mentioned provocative images - sexual content.

    Category: Sexual content
    Review: The packaging of this product is tastefully done and doesn't include any inappropriate images.
    Flagged: false
    Flagged Reason: No violation detected.
        """

    @staticmethod
    def function_call(flagged, flagged_reason, review, model, email_client, to_email) -> dict:
        if flagged:
            formatted_prompt = f"Review: {review}\nFlagged Reason: {flagged_reason}"
            response = model.call_model(
                "gpt-3.5-turbo-0613", PROMPT, formatted_prompt)
            validated = response["choices"][0]["message"]["content"]

            url = urlparse(review["URL"])
            split_path = url.path.split("/")
            review_id = split_path[3]  # Return the review ID from URL path

            if validated:
                violation_category = "Sexual content"
                product_asin = review["Variation"]
                email_subject = email_client.with_subject(violation_category, product_asin)
                email_body = email_client.with_body(
                    product_asin, review["Author"], review["Body"], review_id, flagged_reason, "Miguel @ PPCRoom")
                sg_response = email_client.send(
                    to_email=to_email,
                    subject=email_subject,
                    body=email_body
                )
                return {
                    "response": {
                        "sendgrid_response": sg_response,
                        "email_body": email_body,
                        "violation_category": violation_category
                    }
                }
        return {
            "response": "no violation"
        }


class ExternalLinks(OpenAISchema):
    """
    Detect whether a review contains any links external of Amazon
    """
    flagged: bool = Field(
        ..., description="Does this review violate the external links terms of service")
    reason: str = Field(
        ..., description="Why was this review flagged as a violation for this category")

    @staticmethod
    def prompt():
        return """Category: Links
    Review: Check out my blog post with detailed pictures and a review of this product: www.exampleblog.com/myproductreview
    Flagged: true
    Flagged Reason: User included an external link.

    Category: Links
    Review: I found a great deal on this product at Amazon's website. Just search for the product name, and you'll find it easily.
    Flagged: false
    Flagged Reason: No violation detected.
        """

    @staticmethod
    def function_call(flagged, flagged_reason, review, model, email_client, to_email) -> dict:
        if flagged:
            formatted_prompt = f"Review: {review}\nFlagged Reason: {flagged_reason}"
            response = model.call_model(
                "gpt-3.5-turbo-0613", PROMPT, formatted_prompt)
            validated = response["choices"][0]["message"]["content"]

            url = urlparse(review["URL"])
            split_path = url.path.split("/")
            review_id = split_path[3]  # Return the review ID from URL path

            if validated:
                violation_category = "External links"
                product_asin = review["Variation"]
                email_subject = email_client.with_subject(violation_category, product_asin)
                email_body = email_client.with_body(
                    product_asin, review["Author"], review["Body"], review_id, flagged_reason, "Miguel @ PPCRoom")
                sg_response = email_client.send(
                    to_email=to_email,
                    subject=email_subject,
                    body=email_body
                )
                return {
                    "response": {
                        "sendgrid_response": sg_response,
                        "email_body": email_body,
                        "violation_category": violation_category
                    }
                }
        return {
            "response": "no violation"
        }


class AdsPromotionalContent(OpenAISchema):
    """
    Detect whether a review contains ads, conflicts of interest or promotional content
    """
    flagged: bool = Field(
        ..., description="Does this review violate the ads, conflicts of interest, promotional content terms of service")
    reason: str = Field(
        ..., description="Why was this review flagged as a violation for this category")

    @staticmethod
    def prompt():
        return """Category: Ads, conflicts of interest, promotional content
    Review: I work for the company that makes this product, and I must say it's the best thing on the market! Buy it now!
    Flagged: true
    Flagged Reason: User disclosed a conflict of interest and included promotional content.

    Category: Ads, conflicts of interest, promotional content
    Review: I have no affiliation with the company, but I genuinely love this product. It exceeded my expectations.
    Flagged: false
    Flagged Reason: No violation detected.
        """

    @staticmethod
    def function_call(flagged, flagged_reason, review, model, email_client, to_email) -> dict:
        if flagged:
            formatted_prompt = f"Review: {review}\nFlagged Reason: {flagged_reason}"
            response = model.call_model(
                "gpt-3.5-turbo-0613", PROMPT, formatted_prompt)
            validated = response["choices"][0]["message"]["content"]

            url = urlparse(review["URL"])
            split_path = url.path.split("/")
            review_id = split_path[3]  # Return the review ID from URL path

            if validated:
                violation_category = "Ads, conflicts of interest, promotional content"
                product_asin = review["Variation"]
                email_subject = email_client.with_subject(violation_category, product_asin)
                email_body = email_client.with_body(
                    product_asin, review["Author"], review["Body"], review_id, flagged_reason, "Miguel @ PPCRoom")
                sg_response = email_client.send(
                    to_email=to_email,
                    subject=email_subject,
                    body=email_body
                )
                return {
                    "response": {
                        "sendgrid_response": sg_response,
                        "email_body": email_body,
                        "violation_category": violation_category
                    }
                }
        return {
            "response": "no violation"
        }


class CompensatedReviews(OpenAISchema):
    """
    Detect whether a review may be compensated
    """
    flagged: bool = Field(
        ..., description="Does this review violate the compensated reviews terms of service")
    reason: str = Field(
        ..., description="Why was this review flagged as a violation for this category")

    @staticmethod
    def prompt():
        return """Category: Compensated reviews
    Review: I received a gift card in exchange for writing this review, and honestly, I can't believe they paid me to say good things about this awful product.
    Flagged: true
    Flagged Reason: User mentioned receiving compensation (gift card) for the review.

    Category: Compensated reviews
    Review: I received this product as a gift, and I wanted to share my thoughts about it. It's a great addition to my collection.
    Flagged: false
    Flagged Reason: No violation detected.
        """

    @staticmethod
    def function_call(flagged, flagged_reason, review, model, email_client, to_email) -> dict:
        if flagged:
            formatted_prompt = f"Review: {review}\nFlagged Reason: {flagged_reason}"
            response = model.call_model(
                "gpt-3.5-turbo-0613", PROMPT, formatted_prompt)
            validated = response["choices"][0]["message"]["content"]

            url = urlparse(review["URL"])
            split_path = url.path.split("/")
            review_id = split_path[3]  # Return the review ID from URL path

            if validated:
                violation_category = "Compensated reviews"
                product_asin = review["Variation"]
                email_subject = email_client.with_subject(violation_category, product_asin)
                email_body = email_client.with_body(
                    product_asin, review["Author"], review["Body"], review_id, flagged_reason, "Miguel @ PPCRoom")
                sg_response = email_client.send(
                    to_email=to_email,
                    subject=email_subject,
                    body=email_body
                )
                return {
                    "response": {
                        "sendgrid_response": sg_response,
                        "email_body": email_body,
                        "violation_category": violation_category
                    }
                }
        return {
            "response": "no violation"
        }


class PlagarismInfringementImpersonation(OpenAISchema):
    """
    Detect whether a review contains plagarism, infringement or impersonation
    """
    flagged: bool = Field(
        ..., description="Does this review violate the plagarism, infringement, impersonation terms of service")
    reason: str = Field(
        ..., description="Why was this review flagged as a violation for this category")

    @staticmethod
    def prompt():
        return """Category: Plagiarism, infringement, impersonation
    Review: This is a knockoff product trying to pass as the original. Don't fall for it; it's not the real deal!
    Flagged: true
    Flagged Reason: User accused the product of being a knockoff.

    Category: Plagiarism, infringement, impersonation
    Review: The packaging design of this product resembles a well-known brand, but I believe it's just a coincidence.
    Flagged: false
    Flagged Reason: No violation detected.
        """

    @staticmethod
    def function_call(flagged, flagged_reason, review, model, email_client, to_email) -> dict:
        if flagged:
            formatted_prompt = f"Review: {review}\nFlagged Reason: {flagged_reason}"
            response = model.call_model(
                "gpt-3.5-turbo-0613", PROMPT, formatted_prompt)
            validated = response["choices"][0]["message"]["content"]

            url = urlparse(review["URL"])
            split_path = url.path.split("/")
            review_id = split_path[3]  # Return the review ID from URL path

            if validated:
                violation_category = "Plagiarism, infringement, impersonation"
                product_asin = review["Variation"]
                email_subject = email_client.with_subject(violation_category, product_asin)
                email_body = email_client.with_body(
                    product_asin, review["Author"], review["Body"], review_id, flagged_reason, "Miguel @ PPCRoom")
                sg_response = email_client.send(
                    to_email=to_email,
                    subject=email_subject,
                    body=email_body
                )
                return {
                    "response": {
                        "sendgrid_response": sg_response,
                        "email_body": email_body,
                        "violation_category": violation_category
                    }
                }
        return {
            "response": "no violation"
        }


class IllegalDangerousActivities(OpenAISchema):
    """
    Detect whether a review contains illegal or dangerous activities
    """
    flagged: bool = Field(
        ..., description="Does this review violate the illegal and dangerous activities terms of service")
    reason: str = Field(
        ..., description="Why was this review flagged as a violation for this category")

    @staticmethod
    def prompt():
        return """Category: Illegal and dangerous activities
    Review: This product helped me cheat on my exams, and it's amazing! I aced all my tests without the teacher suspecting a thing.
    Flagged: true
    Flagged Reason: User admitted to using the product for illegal activities (cheating).

    Category: Illegal and dangerous activities
    Review: This knife is extremely sharp, so be cautious while using it in the kitchen.
    Flagged: false
    Flagged Reason: No violation detected.
        """

    @staticmethod
    def function_call(flagged, flagged_reason, review, model, email_client, to_email) -> dict:
        if flagged:
            formatted_prompt = f"Review: {review}\nFlagged Reason: {flagged_reason}"
            response = model.call_model(
                "gpt-3.5-turbo-0613", PROMPT, formatted_prompt)
            validated = response["choices"][0]["message"]["content"]

            url = urlparse(review["URL"])
            split_path = url.path.split("/")
            review_id = split_path[3]  # Return the review ID from URL path

            if validated:
                violation_category = "Illegal and dangerous activities"
                product_asin = review["Variation"]
                email_subject = email_client.with_subject(violation_category, product_asin)
                email_body = email_client.with_body(product_asin, review["Author"], review["Body"], review_id, flagged_reason, "Miguel @ PPCRoom")
                sg_response = email_client.send(
                    to_email=to_email,
                    subject=email_subject,
                    body=email_body
                )
                return {
                    "response": {
                        "sendgrid_response": sg_response,
                        "email_body": email_body,
                        "violation_category": violation_category
                    }
                }
        return {
            "response": "no violation"
        }
