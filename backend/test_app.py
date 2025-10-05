import requests

def test_post():
    url = "http://127.0.0.1:8080/query"  # 🔹 Change this to your actual FastAPI route
    # payload = {
    #     "text": "What is the return policy for defective items?",
    # }
    payload = {
        "text": "What is the status of my order #12345?",
    }

    try:
        response = requests.post(url, json=payload)
        print(f"Status code: {response.status_code}")
        print("Response JSON:", response.json())
    except requests.exceptions.RequestException as e:
        print("Error:", e)

def test_get():
    url = "http://127.0.0.1:8080/"
    try:
        response = requests.get(url)
        print(f"Status code: {response.status_code}")
        print("Response JSON:", response.json())
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    

if __name__ == "__main__":
    test_post()
    # test_get()
