import requests
import json

# Base URL
BASE_URL = "http://localhost:8000"

def test_api():
    print("🚀 Testing Somali Subtitle Generator API")
    
    # 1. Register a user
    print("\n1. Registering user...")
    register_data = {
        "username": "testuser3",
        "email": "test3@example.com", 
        "password": "testpassword"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ User registered successfully")
            user_data = response.json()
            print(f"User ID: {user_data['id']}")
        else:
            print(f"❌ Registration failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # 2. Login to get token
    print("\n2. Logging in...")
    login_data = {
        "username": "test3@example.com",
        "password": "testpassword"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data["access_token"]
            print("✅ Login successful")
            print(f"Token: {access_token[:50]}...")
        else:
            print(f"❌ Login failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # 3. Upload a file
    print("\n3. Uploading audio file...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        with open("backend/test_audio/test.wav", "rb") as f:
            files = {"file": ("test.wav", f, "audio/wav")}
            response = requests.post(f"{BASE_URL}/media/upload", headers=headers, files=files)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                upload_data = response.json()
                media_id = upload_data["id"]
                print("✅ File uploaded successfully")
                print(f"Media ID: {media_id}")
            else:
                print(f"❌ Upload failed: {response.text}")
                return
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return
    
    # 4. Transcribe the file
    print("\n4. Starting transcription...")
    try:
        response = requests.post(f"{BASE_URL}/transcribe/{media_id}", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            transcribe_data = response.json()
            print("✅ Transcription completed!")
            print(f"Processing time: {transcribe_data['data']['processing_time']:.2f}s")
            print(f"Transcript ID: {transcribe_data['data']['transcript_id']}")
        else:
            print(f"❌ Transcription failed: {response.text}")
            return
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return
    
    # 5. Get transcription results
    print("\n5. Getting transcription results...")
    try:
        response = requests.get(f"{BASE_URL}/transcribe/{media_id}", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            transcript_data = response.json()
            print("✅ Transcription retrieved!")
            print(f"Content: {transcript_data['data']['content'][:100]}...")
            print(f"Language: {transcript_data['data']['language_code']}")
            print(f"Confidence: {transcript_data['data']['confidence_score']:.2f}")
        else:
            print(f"❌ Retrieval failed: {response.text}")
    except Exception as e:
        print(f"❌ Retrieval error: {e}")
    
    print("\n🎉 API Test Complete!")

if __name__ == "__main__":
    test_api()
