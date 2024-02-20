import re
from urllib.parse import urlparse

def detect_waf(api_url):
    parsed_uri = urlparse(api_url)
    switches_on = False
  
    try:
        resp = requests.get(api_url)
        
        # Check for common WAF headers
        if 'X-WAF' in resp.headers:
            return 'Unknown WAF (with X-WAF header)'
        elif 'CloudFront' in resp.headers['Server']:
            return 'Amazon CloudFront'
        elif 'AkamaiGHost' in resp.headers['Server']:
            return 'Akamai'
        elif 'Fastly' in resp.headers['Server']:
            return 'Fastly'
        
        # Check for modified response body
        if re.search(r'<script.*?>([\s\S]*?)<\/script>', resp.text):
            switches_on = True
        
        # Check for unusual HTTP status codes or headers
        if resp.status_code == 403 and 'Forbidden' not in resp.headers['Server']:
            return 'Unknown WAF (with 403 Forbidden response)'
        elif resp.status_code == 502 and 'Bad Gateway' not in resp.headers['Server']:
            return 'Unknown WAF (with 502 Bad Gateway response)'
        
        # Check for unusual HTTP request headers
        if 'X-Forwarded-For' in resp.headers or \
           'X-Forwarded-Proto' in resp.headers or \
           'X-Forwarded-Host' in resp.headers:
            return 'Unknown WAF (with X-Forwarded headers)'
        
        # Check for unusual HTTP request body
        if re.search(r'<\s*script.*?>([\s\S]*?)<\/script>', resp.text):
            switches_on = True
        
        # Check for modified response headers
        if 'X-Content-Type-Options' in resp.headers or \
           'X-Frame-Options' in resp.headers or \
           'X-XSS-Protection' in resp.headers:
            switches_on = True
        
        # Check for unusual HTTP response headers
        if 'Server' not in resp.headers and 'Vary' not in resp.headers:
            return 'Unknown WAF (with missing Server/Vary headers)'
        
        # If no clear indications found, return "Not Detected"
        if not switches_on:
            return 'Not Detected'
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return 'Not Detected'
    
# Usage example:
api_url = "https://api.example.com/endpoint"
print(detect_waf(api_url))