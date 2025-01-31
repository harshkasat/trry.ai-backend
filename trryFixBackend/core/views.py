# from gevent import monkey
# monkey.patch_all()
from django.http import FileResponse
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pydantic import BaseModel, ValidationError
from typing import Optional
# from suss_file import generate_valid_links, main, capture_screenshots_for_urls, performance_metrics
from core.suss_file import generate_valid_links, capture_screenshots_for_urls, performance_metrics, main
from core.utils import zip_file, sanitize_filename
from core.async_locust import load_test_main
import asyncio
import shutil
import json

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

class URLModel(BaseModel):
    flowId: Optional[int] = 1
    name: Optional[str] = "Website Performance"
    url: Optional[str] = "https://www.tryfix.ai/"

class HealthCheckView(APIView):
    def get(self, request):
        return Response({"message": "Server is running Health Check"})

class GreetingView(APIView):
    def get(self, request):
        return Response({"message": "Server start with Django REST framework"})

class TestWebsitesPerformanceView(APIView):
    def post(self, request):
        try:
            if not request.body:
                return Response(
                    {"error": "Request body must be JSON"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            json_data = json.loads(request.body)
            target_url = URLModel(**json_data)
            response = asyncio.run(main(target_url=target_url.url))
            return Response({"message": f"URL {target_url} {response}"})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CaptureScreenshotsView(APIView):
    def post(self, request):
        if not request.body:
            return Response(
                {"error": "Request body must be JSON"},
                status=status.HTTP_400_BAD_REQUEST
            )

        json_data = json.loads(request.body)
        
        target_url = URLModel(**json_data)
        valid_links = generate_valid_links(target_url.url)
        
        try:
            if isinstance(valid_links, list):
                asyncio.run(capture_screenshots_for_urls(valid_links))
                return Response({
                    "message": f"Captured screenshots for {len(valid_links)} URLs done successfully"
                })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            print(target_url)
            # Ensure the directory exists
            os.makedirs("reports", exist_ok=True)
            filename = sanitize_filename(target_url.url) + '.json'
            file_path = os.path.join("reports", filename)
            response = asyncio.run(performance_metrics(target_url=target_url.url, dynamic_file_path=file_path))
            # Return the JSON file as a downloadable response
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=file_path)
            return response
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        # finally:
        #     # Clean up the JSON file
        #     if os.path.exists(file_path):
        #         os.remove(file_path)

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
            print(target_url.url)
            valid_links = generate_valid_links(target_url.url)
                       
            if isinstance(valid_links, list):
                asyncio.run(load_test_main(target_urls=valid_links))  # ✅ Run async function synchronously
            source_path = 'Z:/trryfix.ai/trryfix-backend/trryFixBackend/performance_tests'
            filename = zip_file(url=target_url.url, source_path=source_path)
            
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
            # Cleanup source_path (if needed)
            try:
                if 'source_path' in locals() and os.path.exists(source_path):
                    shutil.rmtree(source_path)
            except Exception as e:
                print(f"Error deleting source directory: {e}")

            # Fallback cleanup for filename (if not already deleted by response)
            try:
                if filename and os.path.exists(filename):
                    os.remove(filename)
            except Exception as e:
                print(f"Error deleting file: {e}")

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