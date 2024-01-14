import requests

def upload_image_to_imgbb(image_data, api_key="9bb994443a8420673355072d7696e605"):
    url = "https://api.imgbb.com/1/upload"
    
    params = {
        "expiration": "600",
        "key": api_key  # Pass your client API key here
    }

    files = {
        "image": image_data
    }

    response = requests.post(url, params=params, files=files)
    json_response = response.json()

    if json_response:
        return json_response['data']['url']
    else:
        return f"Error: {json_response['error']['message']}"
