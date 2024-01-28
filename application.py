import base64
import os
import csv
from os.path import basename
import dotenv
import openai
import werkzeug
from flask_cors import CORS
from typing import List
from urllib.parse import urlparse
from flask import Flask, jsonify, request
from sendgrid.sendgrid import SendGridAPIClient
from app.service import OpenAI, SendgridClient, CSVParser
from app.domain import ReadWriter, BaseEmailService, BaseModelService
from app.functions.function_schema import ProfanityHarassmentViolation, SellerOrderShippingFeedback, CommentsPricingAvailability, UnsupportedLanguage, SpamSymbolsText, PrivateInformation, HateSpeech, SexualContent, ExternalLinks, AdsPromotionalContent, CompensatedReviews, PlagarismInfringementImpersonation, IllegalDangerousActivities

functions = [
    ProfanityHarassmentViolation,
    SellerOrderShippingFeedback,
    CommentsPricingAvailability,
    UnsupportedLanguage,
    SpamSymbolsText,
    PrivateInformation,
    ProfanityHarassmentViolation,
    HateSpeech,
    SexualContent,
    ExternalLinks,
    AdsPromotionalContent,
    CompensatedReviews,
    PlagarismInfringementImpersonation,
    IllegalDangerousActivities
]

env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    dotenv.load_dotenv(env_path)

openai_token = os.getenv("OPENAI_API_KEY")
sendgrid_token = os.getenv("SENDGRID_API_KEY")
sendgrid_client = SendGridAPIClient()
openai_client = openai.ChatCompletion()

server = Flask(__name__)
server.config["UPLOAD_FOLDER"] = "./upload/csv"
server.config["OUTPUT_FOLDER"] = "./output/csv"
CORS(server)

class ReviewClassification:
    def __init__(self, reader: ReadWriter, model: BaseModelService, email: BaseEmailService, functions):
        self.reader = reader
        self.model = model
        self.email = email
        self.functions = functions

    def save_csv(self, uploaded_file):
        if uploaded_file.filename == "":
            return None

        if uploaded_file:
            file_name = werkzeug.utils.secure_filename(uploaded_file.filename)
            file_path = os.path.join(server.config["UPLOAD_FOLDER"], file_name)
            uploaded_file.save(file_path)
            return file_path
        return None

    def read_reviews(self, file) -> List:
        return self.reader.read(file)

    def write_csv(self, csv_content):
        file_path = os.path.join(server.config["OUTPUT_FOLDER"], "new_output.csv")
        self.reader.write(file_path, csv_content)
        return

    def send_attachment(self, to_email):
        """
        Send the CSV as an attachment at the end of the sequenece
        """
        file_path = os.path.join(server.config["OUTPUT_FOLDER"], "new_output.csv")
        file_name = basename(file_path)
        subject = f"File: {file_name}"
        with open(file_path, "rb") as file:
            data = file.read()
            file.close()
            encoded_csv = base64.b64encode(data).decode()
            self.email.send_with_attachment(to_email, subject, {
                "file_content": encoded_csv,
                "file_name": file_name,
                "file_type": "application/csv",
            })
    
    def ai_function_call(self, reviews, to_email):
        csv_buffer = []
        self.model.config(openai_token)
        self.email.config(sendgrid_token)
        review_template = "Title: {title}\nReview: {body}"
        for function in self.functions:
            few_shot = function.prompt() # Grab few shot prompt relevant to the function call
            function_name = function.openai_schema["name"]
            function_prompt = self.model.function_prompt(function_name, few_shot) # Conctruct the system message prompt by adding in function name to call and few shot prompt
            for review in reviews: # Reviews are of type OrderedDict
                formatted_review = review_template.format(title=review["Title"], body=review["Body"])
                function_args = self.model.function_call_model("gpt-4", function_prompt, formatted_review, [function.openai_schema])
                response = function.from_response(function_args)
                res = function.function_call(response.flagged, response.reason, review, self.model, self.email, to_email)
                if res["response"] == "no violation":
                    continue
                url = urlparse(review["URL"])
                split_path = url.path.split("/")
                review_id = split_path[3] # Return the review ID from URL path
                csv_content = {
                    "review_id": review_id,
                    "review": review["Body"],
                    "violation_category": res["response"]["violation_category"],
                    "flagged_reason": response.reason, 
                    "email_body": res["response"]["email_body"]
                }
                csv_buffer.append(csv_content)
        print(csv_buffer)
        self.write_csv(csv_buffer)
        self.send_attachment(to_email)




openai = OpenAI(openai_client)
sendgrid = SendgridClient(sendgrid_client)
csv_parser = CSVParser(csv)
review_classification = ReviewClassification(csv_parser, openai, sendgrid, functions)

@server.route("/review", methods=["POST", "GET"])
def handle_reviews():
    file = request.files.get("file")
    to_email = request.form.get("email")

    file_path = review_classification.save_csv(file)
    reviews = review_classification.read_reviews(file_path)
    review_classification.ai_function_call(reviews, to_email)

    return jsonify({
        "status_code": 200,
        "task_status": "RUNNING",
        "file_path": file_path
    })


@server.route("/", methods=["GET"])
def handle_route():
    url = request.url
    return jsonify({
        "status": 200,
        "response": {
            "version": "v1.0",
            "location": url
        }
    })

@server.route("/health", methods=["GET"])
def handle_ping():
    return jsonify({
        "status": 200,
        "response": "pong"
    })


if __name__ == "__main__":
    server.run(host="0.0.0.0", debug=True, port=8500)

