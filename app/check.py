import requests
import json

def send_image_url_to_api(image_url):
    url = "http://0.0.0.0:1234/api/"  # Thay đổi URL tới API của bạn
    
    payload = {"image_url": image_url}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Error:", err)
    
    return None

if __name__ == "__main__":
    image_url = "https://toi.sgp1.digitaloceanspaces.com/p/2024/03/65f65cf26a7db1d328081432_large.jpg"  # Đường dẫn URL của ảnh bạn muốn đọc
    response_data = send_image_url_to_api(image_url)
    
    if response_data is not None:
        # Lưu dữ liệu của ảnh xuống file
        print(response_data["Result"])
        
