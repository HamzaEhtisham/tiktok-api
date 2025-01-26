from flask import Flask, jsonify, request, render_template_string
import requests
import logging

app = Flask(__name__)

API_HOST = "tiktok.evelode.com"
API_KEY = "fafe24d5e3684657009032fd363072aa"

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def fetch_data_from_api(endpoint):
    url = f"https://{API_HOST}/api/v1/{endpoint}"
    headers = {
        "x-rapidapi-host": API_HOST,
        "x-rapidapi-key": API_KEY
    }
    logging.debug(f"Request URL: {url}")  # Log the request URL
    logging.debug(f"Request Headers: {headers}")  # Log the request headers
    response = requests.get(url, headers=headers)
    logging.debug(f"Response Status Code: {response.status_code}")  # Log the response status code
    logging.debug(f"Response Content: {response.content}")  # Log the response content
    response.raise_for_status()
    return response.json()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        endpoint = request.form.get('endpoint_option', 'valid_endpoint')  # Get the selected endpoint
        param = None  # No parameter
        filter_option = request.form.get('filter_option')
        try:
            data = fetch_data_from_api(endpoint)
            logging.debug(f"Fetched data: {data}")  # Log the fetched data
            api_data = data.get('data', data)  # Fallback to the entire response if 'data' key is missing

            # Apply filter if selected
            if filter_option:
                api_data = {k: v for k, v in api_data.items() if filter_option in k}

        except requests.exceptions.RequestException as e:
            logging.error(f"RequestException: {e}")  # Log the error
            return render_template_string('''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Error</title>
                    <style>
                        body { font-family: Arial, sans-serif; margin: 40px; background: #141414; color: #e5e5e5; }
                        h1 { color: #e50914; }
                        a { color: #e50914; text-decoration: none; }
                        a:hover { text-decoration: underline; }
                    </style>
                </head>
                <body>
                    <h1>An error occurred</h1>
                    <p>{{ e }}</p>
                    <a href="/">Back</a>
                </body>
                </html>
            ''', e=e)

        return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Fetched Data</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background: #141414; color: #e5e5e5; }
                    h1 { color: #e50914; }
                    h2 { color: #e50914; }
                    p { line-height: 1.6; }
                    a { color: #e50914; text-decoration: none; }
                    a:hover { text-decoration: underline; }
                    .data-container { border: 1px solid #333; padding: 20px; border-radius: 5px; background: #333; }
                </style>
            </head>
            <body>
                <h1>Fetched Data from TikTok API</h1>
                <div class="data-container">
                    <h2>{{ api_data.get('name', 'N/A') }}</h2>
                    <p><strong>ID:</strong> {{ api_data.get('id', 'N/A') }}</p>
                    <p><strong>View Count:</strong> {{ api_data.get('view_count', 'N/A') }}</p>
                    <p><strong>Video Count:</strong> {{ api_data.get('video_count', 'N/A') }}</p>
                    <p><strong>Hashtag:</strong> {{ api_data.get('hashtag', 'N/A') }}</p>
                    <p><strong>Followers:</strong> {{ api_data.get('followers', 'N/A') }}</p>
                    <p><strong>Likes:</strong> {{ api_data.get('likes', 'N/A') }}</p>
                    <p><strong>Growth:</strong> {{ api_data.get('growth', 'N/A') }}</p>
                    <p><strong>All Data:</strong> {{ api_data }}</p>
                </div>
                <a href="/">Back</a>
            </body>
            </html>
        ''', api_data=api_data)

    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #141414; color: #e5e5e5; }
                h1 { color: #e50914; }
                form { margin-top: 20px; }
                label { font-weight: bold; }
                select, button { margin-top: 10px; }
                select { background: #333; color: #e5e5e5; border: 1px solid #333; padding: 5px; }
                button { background-color: #e50914; color: white; border: none; padding: 10px 20px; cursor: pointer; }
                button:hover { background-color: #b20710; }
            </style>
        </head>
        <body>
            <h1>Welcome to the TikTok API Service!</h1>
            <form method="post">
                <label for="endpoint_option">Endpoint:</label>
                <select id="endpoint_option" name="endpoint_option">
                    <option value="valid_endpoint">Valid Endpoint</option>
                    <option value="daily_virals">Daily Virals</option>
                </select>
                <label for="filter_option">Filter:</label>
                <select id="filter_option" name="filter_option">
                    <option value="">None</option>
                    <option value="likes">Likes</option>
                    <option value="followers">Followers</option>
                    <option value="growth">Growth</option>
                </select>
                <button type="submit">Submit</button>
            </form>
        </body>
        </html>
    ''')

@app.route('/daily-virals', methods=['GET'])
def daily_virals():
    endpoint = "daily_virals"  # Replace with the actual endpoint for daily virals
    try:
        data = fetch_data_from_api(endpoint)
        logging.debug(f"Fetched daily virals data: {data}")  # Log the fetched data
        api_data = data.get('data', data)  # Fallback to the entire response if 'data' key is missing

    except requests.exceptions.RequestException as e:
        logging.error(f"RequestException: {e}")  # Log the error
        return render_template_string('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Error</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; background: #141414; color: #e5e5e5; }
                    h1 { color: #e50914; }
                    a { color: #e50914; text-decoration: none; }
                    a:hover { text-decoration: underline; }
                </style>
            </head>
            <body>
                <h1>An error occurred</h1>
                <p>{{ e }}</p>
                <a href="/">Back</a>
            </body>
            </html>
        ''', e=e)

    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Daily Virals</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #141414; color: #e5e5e5; }
                h1 { color: #e50914; }
                h2 { color: #e50914; }
                p { line-height: 1.6; }
                a { color: #e50914; text-decoration: none; }
                a:hover { text-decoration: underline; }
                .data-container { border: 1px solid #333; padding: 20px; border-radius: 5px; background: #333; }
            </style>
        </head>
        <body>
            <h1>Daily Virals from TikTok API</h1>
            <div class="data-container">
                <h2>{{ api_data.get('name', 'N/A') }}</h2>
                <p><strong>ID:</strong> {{ api_data.get('id', 'N/A') }}</p>
                <p><strong>View Count:</strong> {{ api_data.get('view_count', 'N/A') }}</p>
                <p><strong>Video Count:</strong> {{ api_data.get('video_count', 'N/A') }}</p>
                <p><strong>Hashtag:</strong> {{ api_data.get('hashtag', 'N/A') }}</p>
                <p><strong>Followers:</strong> {{ api_data.get('followers', 'N/A') }}</p>
                <p><strong>Likes:</strong> {{ api_data.get('likes', 'N/A') }}</p>
                <p><strong>Growth:</strong> {{ api_data.get('growth', 'N/A') }}</p>
                <p><strong>All Data:</strong> {{ api_data }}</p>
            </div>
            <a href="/">Back</a>
        </body>
        </html>
    ''', api_data=api_data)

if __name__ == '__main__':
    app.run(debug=True)