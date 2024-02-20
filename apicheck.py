import requests
from urllib.parse import urlparse

def detect_framework(api_url):
    parsed_uri = urlparse(api_url)
    try:
        resp = requests.get(api_url)
        if 'x-frame-options' in resp.headers or \
            'Content-Security-Policy' in resp.headers or \
            'X-Content-Type-Options' in resp.headers or \
            'Server' not in resp.headers:
               return 'Not Detected'
        else:
            server_header = resp.headers['Server']
            if 'Django/1.10.' in server_header:
                return 'Django'
            elif 'Express' in server_header:
                return 'Express'
            elif 'Ruby' in server_header:
                return 'Rails'
            elif 'Spring Boot' in server_header:
                return 'Spring Boot'
            elif 'Phoenix' in server_header:
                return 'Phoenix'
            elif 'FastAPI' in server_header:
                return 'Fast API'
            elif 'ASP.NET Core' in server_header:
                return 'ASP .NET Core'
            elif 'Flask' in server_header:
                return 'Flask'
            elif 'Swagger' in resp.text or 'openapi' in resp.text:
                return 'Swagger/OpenAPI'
            else:
                return 'Unknown Framework'
    except Exception as e:
        print(f"An error occurred: {e}")
        return 'Not Detected'

# Usage example:
api_url = "https://yourtestapi/endpoint"
print(detect_framework(api_url))