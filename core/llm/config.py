import google.generativeai as genai
from core.llm import genai_api_key, SAFE_SETTINGS, PROMPT
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

            llm = genai.GenerativeModel('models/gemini-2.0-flash',
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

    def generate_valdi_urls(self, contents, schema=None):
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
            import time
            start = time.time()
            llm = self.configure_llm()
            response = await asyncio.to_thread(
                llm.generate_content, [PROMPT, image],
                safety_settings=SAFE_SETTINGS,
            )
            print(f"Time taken to generate content: {time.time() - start}")
            return response
        except Exception as e:
            print(f"Failed to generate content: {e}")
            return None

# if __name__ == '__main__':
#     from PIL import Image
#     import json
#     api = ApiClient()
#     image = Image.open('reports/capture_screenshots/desktop_drive.google.com.png')
#     response = asyncio.run(api.generate_content_for_image(image))
#     print(type(json.loads(response.text)[0]['response'][0]))