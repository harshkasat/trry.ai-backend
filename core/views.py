# from gevent import monkey
# monkey.patch_all()
from django.http import FileResponse
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pydantic import BaseModel, ValidationError
from typing import Optional
from core.suss_file import generate_valid_links, capture_screenshots_for_urls, performance_metrics, main
from core.pydantic_model import URLModel
from core.load_test import load_test_main
from core.utils import zip_file
import asyncio
import shutil
import json

# authentication and permision classes
from rest_framework.permissions import AllowAny

# Custom FileResponse to delete the file after sending
class DeleteOnCloseFileResponse(FileResponse):
    def __init__(self, *args, **kwargs):
        self._file_to_delete = kwargs.pop('file_to_delete', None)
        super().__init__(*args, **kwargs)

    def close(self):
        super().close()
        if self._file_to_delete and os.path.exists(self._file_to_delete):
            try:
                os.remove(self._file_to_delete)
            except Exception as e:
                print(f"Error deleting file on close: {e}")


class HealthCheckView(APIView):
    def get(self, request):
        return Response({"message": "Server is running Health Check"})

class GreetingView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def get(self, request):
        return Response({"message": "Server start with Django REST framework"})

class WebsitesPerformanceView(APIView):
    def post(self, request):
        try:
            if not request.body:
                return Response(
                    {"error": "Request body must be JSON"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            json_data = json.loads(request.body)
            target_url = URLModel(**json_data)
            print("Running Main file")
            asyncio.run(main(target_url=target_url))
            filename = zip_file()
            file_obj = open(filename, 'rb')
            response = DeleteOnCloseFileResponse(
                file_obj,
                as_attachment=True,
                filename=os.path.basename(filename),
                file_to_delete=filename
            )
            return response
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            # Clean up the reports directory
            if os.path.exists("reports"):
                shutil.rmtree("reports")
                print("Deleted reports directory")

class CaptureScreenshotsView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        if not request.body:
            return Response(
                {"error": "Request body must be JSON"},
                status=status.HTTP_400_BAD_REQUEST
            )

        json_data = json.loads(request.body)
        
        target_url = URLModel(**json_data)
        
        try:
            asyncio.run(capture_screenshots_for_urls(target_url=target_url))
            filename = zip_file()
            file_obj = open(filename, 'rb')
            response = DeleteOnCloseFileResponse(
                file_obj,
                as_attachment=True,
                filename=os.path.basename(filename),
                file_to_delete=filename
            )
            return response

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            # Clean up the reports directory
            if os.path.exists("reports"):
                shutil.rmtree("reports")
                print("Deleted reports directory")

class LighthouseTestView(APIView):
    def post(self, request):
        try:
            if not request.body:
                return Response(
                    {"error": "Request body must be JSON"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            json_data = json.loads(request.body)
            target_url = URLModel(**json_data)
            
            file_path = asyncio.run(performance_metrics(target_url=target_url))
            # Return the JSON file as a downloadable response
            file_obj = open(file_path, 'rb')
            response = DeleteOnCloseFileResponse(
                file_obj,
                as_attachment=True,
                filename=os.path.basename(file_path),
                file_to_delete=file_path
            )
            return response
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
       

class LoadTestsView(APIView):
    def post(self, request):
        try:
            if not request.body:
                return Response(
                    {"error": "Request body must be JSON"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            json_data = json.loads(request.body)  # Convert bytes to dictionary

            # Validate JSON with Pydantic
            target_url = URLModel(**json_data)

            asyncio.run(load_test_main(target_url=target_url))  # ✅ Run async function synchronously

            filename = zip_file()
            # Create response with auto-cleanup
            file_obj = open(filename, 'rb')
            response = DeleteOnCloseFileResponse(
                file_obj,
                as_attachment=True,
                filename=os.path.basename(filename),
                file_to_delete=filename
            )
            return response

        except json.JSONDecodeError:
            return Response(
                {"error": "Invalid JSON format"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValidationError as ve:
            return Response(
                {"error": ve.errors()},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            # Clean up the reports directory
            if os.path.exists("reports"):
                shutil.rmtree("reports")
                print("Deleted reports directory")


class GenerateValidLinksView(APIView):
    def post(self, request):
        try:
            if not request.body:
                return Response(
                    {"error": "Request body must be JSON"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            json_data = json.loads(request.body)
            target_url = URLModel(**json_data)
            response = generate_valid_links(target_url=target_url.url)
            return Response({
                "message": f"Valid links for {target_url.url}: {response}"
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ImageReview(APIView):
    
    def get(self, request):
        from PIL import Image
        from core.llm.config import ApiClient
        import requests
        from io import BytesIO
        import asyncio
        try:
            if not request.body:
                return Response(
                    {"error": "Request body must be JSON"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Process the image (if needed, move this logic to another function for clarity)
            try:
                refined_url = requests.get('https://plus.unsplash.com/premium_photo-1666672388644-2d99f3feb9f1?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8anBnfGVufDB8fDB8fHww')
                image = Image.open(BytesIO(refined_url.content))
            except Exception as e:
                return Response({
                    "message": f"Error opening image: {e}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            issue_identify_by_llm = asyncio.run(ApiClient().generate_content_for_image(image=image))
            llm_response = json.loads(issue_identify_by_llm.text)[0]['response']
            return Response({
                "message": f"Response: {llm_response}"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            # Clean up the reports directory
            if os.path.exists("reports"):
                shutil.rmtree("reports")
                print("Deleted reports directory")