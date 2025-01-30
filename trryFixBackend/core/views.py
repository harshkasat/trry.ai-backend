# from gevent import monkey
# monkey.patch_all()
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pydantic import BaseModel, ValidationError
from typing import Optional
# from suss_file import generate_valid_links, main, capture_screenshots_for_urls, performance_metrics
from core.suss_file import generate_valid_links, capture_screenshots_for_urls, performance_metrics, main
from core.async_locust import load_test_main
import asyncio

import json

class URLModel(BaseModel):
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
            response = main(target_url=target_url.url)
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
                capture_screenshots_for_urls(valid_links)
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
            response = performance_metrics(target_url=target_url.url)
            return Response({
                "message": f"Lighthouse test results for {target_url.url}: {response}"
            })
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
            print(target_url.url)
            valid_links = generate_valid_links(target_url.url)
            
            if isinstance(valid_links, list):
                asyncio.run(load_test_main(target_urls=valid_links))  # ✅ Run async function synchronously
            
            return Response({"message": "Load tests completed"})

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