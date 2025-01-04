import google.generativeai as genai
from llm import genai_api_key, SAFE_SETTINGS, PROMPT
import asyncio
from typing_extensions import TypedDict
class LlmResponse(TypedDict):
    response : list[str]
# Initialize the API client
class ApiClient():

    def __init__(self):
        genai.configure(api_key=genai_api_key)

    def configure_llm(self, schema=None):
        try:

            llm = genai.GenerativeModel('models/gemini-1.5-flash',
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=list[LlmResponse]
                ))            

            if llm is None:
                raise ValueError("LLM component is None")
            return llm
        except Exception as e:
            print(f"Failed to configure LLM: {e}")
            return None
    
    async def configure_vision_model(self, schema=None):
        try:
            vision_model = genai.GenerativeModel('gemini-pro-vision', 
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=list[LlmResponse]
                )
            )

            if vision_model is None:
                raise ValueError("Vision model component is None")
            return vision_model
        except Exception as e:
            print(f"Failed to configure vision model: {e}")
            return None


    def generate_content(self, contents, schema=None):
        try:
            llm = self.configure_llm(schema=schema)
            response = llm.generate_content(contents=contents,
                safety_settings=SAFE_SETTINGS,
                )
            return response
        except Exception as e:
            print(f"Failed to generate content: {e}")
            return None
    
    async def generate_content_for_image(self, image):
        """Async function to generate content from image."""
        try:
            llm = self.configure_llm()
            response = await asyncio.to_thread(
                llm.generate_content, [PROMPT, image],
                safety_settings=SAFE_SETTINGS,
            )
            return response
        except Exception as e:
            print(f"Failed to generate content: {e}")
            return None