from gevent import monkey
monkey.patch_all()
from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
from typing import Optional
from main import generate_valid_links, main, capture_screenshots_for_urls, performance_metrics
from async_locust import load_test_main

app = Flask(__name__)
app.config["DEBUG"] = True  # Enable debug mode


class URLModel(BaseModel):
    url: Optional[str] = "https://www.tryfix.ai/"

@app.route("/health/", methods=['GET'])
async def health_check():
    return {"message": "Server is running Health Check"}

@app.route("/", methods=['GET'])
async def greeting():
    return {"message": "Server start with Flask 3.1.0"}


@app.route("/test_websites_performance/", methods=["POST"])
async def add_url_to_fix():
    try:
        # Parse and validate the input
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "Request body must be JSON"}), 400

        # Validate using Pydantic
        target_url = URLModel(**json_data)
        response = await main(target_url=target_url.url)
        return {"message": f"URL {target_url} {response}"}
    except Exception as e:
        return f'<h1> {str(e)} </h1>', 500

@app.route("/capture_screenshots_websites/", methods=["POST"])
async def add_urls_to_fix():
    # Parse and validate the input
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Validate using Pydantic
    target_url = URLModel(**json_data)
    # Step 1: Scrape and validate links
    valid_links = generate_valid_links(target_url.url)
    
    try:
        if isinstance(valid_links, list):
            # Step 2: Run all tasks asynchronously
            await capture_screenshots_for_urls(valid_links)
            return f"<h1> Captured screenshots for {len(valid_links)} URLs done successfully</h1>"
    except Exception as e:
        return f'<h1> {str(e)} </h1>', 500

@app.route("/lighthouse_test/", methods=["POST"])
async def lighthouse_test():
    try:
        # Parse and validate the input
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "Request body must be JSON"}), 400

        # Validate using Pydantic
        target_url = URLModel(**json_data)
        response = await performance_metrics(target_url=target_url.url)
        return f" <h1> Lighthouse test results for {target_url.url}: {response} </h1>"
    except Exception as e:
        return f'<h1> {str(e)} </h1>', 500

@app.route("/load_tests/", methods=["POST"])
async def load_tests():
    try:
        # Parse and validate the input
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "Request body must be JSON"}), 400

        # Validate using Pydantic
        target_url = URLModel(**json_data)

        # Step 1: Scrape and validate links
        # import asyncio
        valid_links = (generate_valid_links(target_url.url))
        print(valid_links)
        if isinstance(valid_links, list):
            # Step 2: Run the load test
            await load_test_main(target_urls=valid_links)

        return f'<h1>{valid_links}!!!</h1>'
    except ValidationError as ve:
        return jsonify({"error": ve.errors()}), 422
    except Exception as e:
        return f'<h1> {str(e)} </h1>', 500

@app.route("/gernerate_valid_links/", methods=["POST"])
async def gernerate_valid_links():
    try:
        # Parse and validate the input
        json_data = request.get_json()
        if not json_data:
            return jsonify({"error": "Request body must be JSON"}), 400

        # Validate using Pydantic
        target_url = URLModel(**json_data)
        response = generate_valid_links(target_url=target_url.url)
        return {"message": f"Valid links for {target_url.url}: {response}"}
    except Exception as e:
        return f'<h1> {str(e)} </h1>', 500


from automation import create_stealth_driver
@app.route("/test_driver", methods=["GET"])
def test_driver():
    try:
        device = 'tablet'
        driver = create_stealth_driver(device)  # Call directly
        driver.get("https://www.google.com")
        screenshot_path = "test_screenshot.png"
        driver.save_screenshot(screenshot_path)
        driver.quit()
        return jsonify({"message": f"Driver initialized, screenshot saved at {screenshot_path}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# if __name__ == "__main__":
#     from gevent.pywsgi import WSGIServer

#     http_server = WSGIServer(("0.0.0.0", 5000), app)
#     http_server.serve_forever()
