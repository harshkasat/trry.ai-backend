from django.urls import path
from .views import (
    HealthCheckView, 
    GreetingView,
    TestWebsitesPerformanceView,
    CaptureScreenshotsView,
    LighthouseTestView,
    LoadTestsView,
    GenerateValidLinksView
)

urlpatterns = [
    path('health/', HealthCheckView.as_view(), name='health-check'),
    path('', GreetingView.as_view(), name='greeting'),
    path('test_websites_performance/', TestWebsitesPerformanceView.as_view(), name='test-websites-performance'),
    path('capture_screenshots_websites/', CaptureScreenshotsView.as_view(), name='capture-screenshots'),
    path('lighthouse_test/', LighthouseTestView.as_view(), name='lighthouse-test'),
    path('load_tests/', LoadTestsView.as_view(), name='load-tests'),
    path('generate_valid_links/', GenerateValidLinksView.as_view(), name='generate-valid-links'),
]