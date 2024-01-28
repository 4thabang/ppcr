from typing import List, Protocol 

class BaseModelService(Protocol):
    def config(self, token):
        """
        Config is a factory that initialises a model and its base configuration settings.
        
        Args:
            token(str): the models api key or bearer token.
        """
        ...

    def function_prompt(self, function_name, few_shot) -> str:
        """

        """
        ...

    def call_model(self, model, system_prompt, user_prompt):
        """
        call_model is used to call a model and generate a response based on the provided model variables.
        Args:
            model(str)
            system_prompt(str)
            user_prompt(str)
        """
        ...

    def function_call_model(self, model, system_prompt, user_prompt, functions: List):
        """
        function_call_model is used to call the function call that has been given to it.
        Args:
            model(str)
            system_prompt(str)
            user_prompt(str)
            functions(List)
        """
        ...
