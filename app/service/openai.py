from retry import retry

class OpenAI:
    def __init__(self, openai):
        self.openai = openai

    def config(self, token):
        if token == "" or token is None:
            raise Exception("empty api key")
        self.openai.api_key = token

    def function_prompt(self, function_name, few_shot) -> str:
        return f"""### Task
    Product Review TOS Violation Identification

    ### Description
    You are an Amazon Terms of Service classification system used to flag product reviews for potential reviewer Terms of Service (TOS) violations.
    Your task is to identify which of the following TOS have been violated by the reviewer for a provided review, as well as a reason as to why it has been flagged. 
    You should attempt to flag as many reviews under these TOS violations as possible, within reason.
    The reviews you will see are from buyers. You are acting on behalf of the seller, and should only flag the review if the reviewer (not the product or seller) has violated the TOS.
    DO NOT flag reviews where the seller violates a term of service, only flag a review if the buyer/reviewer has violated the terms of service within the context of the task.

    ### Examples
    {few_shot}

    ### Notes
    - Never flag reviews where the seller has violated the Terms of Service
    - Only flag reviews where the reviewer has violated the Terms of Service in the content of their review
    - Always use {function_name} to parse the output.
    - Always call the function.
    """

    @retry(tries=5, delay=1, backoff=2, max_delay=32)
    def call_model(self, model, system_prompt, user_prompt):
        try:
            response = self.openai.create(
                model=model,
                temperature=0.7,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response
        except Exception as e:
            raise ValueError("Error chatting with OpenAI model:", e)

    @retry(tries=5, delay=1, backoff=2, max_delay=32)
    def function_call_model(self, model, system_prompt, user_prompt, functions):
        try:
            response = self.openai.create(
                model=model,
                functions=functions,
                temperature=0.2,
                function_call={"name": functions[0]["name"]},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response
        except Exception as e:
            raise ValueError("Error calling OpenAI function call model:", e)
