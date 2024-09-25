import openai
import os

class OpenAIModel:
    def __init__(self, api_key=None, model="dall-e-2"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=openai.api_key)
        self.model = model

    def generate_image(self, prompt):
        response = self.client.images.generate(
            prompt=prompt,
            n=1,
            model=self.model,
            size="1024x1024",
            quality="standard"
        )
        return response.data[0].url
