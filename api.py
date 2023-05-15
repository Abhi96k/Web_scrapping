import requests


# def get_vehicle_details(registration_number):
#     url = f"https://api.vahan.info/vahan4api/vahan/{registration_number}"
#     headers = {"Accept": "application/json"}
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         return None


# print(get_vehicle_details('MH42AN2667'))

# import requests

# url = "https://car-data.p.rapidapi.com/cars"

# querystring = {"limit": "10", "page": "0"}

# headers = {
#     "X-RapidAPI-Key": "2002e4b67bmshbc5291ee503b5bap1cab56jsnd20bd87f064e",
#     "X-RapidAPI-Host": "car-data.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params=querystring)

# print(response.json())


# url = f"https://api.vahan.info/vahan4api/vahan/MH14JT9993"
# headers = {"Accept": "application/json"}
# response = requests.get(url, headers=headers)
# print(response)

# import requests

# # Replace the placeholder API key with your own key
# API_KEY = 'your_api_key_here'
# # Replace the placeholder vahan number with the actual vahan number of the vehicle you want to retrieve details for
# VAHAN_NUMBER = 'vahan_number_here'

# # Define the API endpoint URL
# API_ENDPOINT = f'https://api.vaahan.com/v2/vehicle-details?apikey={API_KEY}&vahan={VAHAN_NUMBER}'

# # Send a GET request to the API endpoint and retrieve the response
# response = requests.get(API_ENDPOINT)

# # Check if the request was successful (status code 200)
# if response.status_code == 200:
#     # Parse the response as JSON data
#     vehicle_details = response.json()

#     # Extract the relevant details from the JSON data
#     owner_name = vehicle_details['owner']['name']
#     registration_date = vehicle_details['registration']['registrationDate']
#     make = vehicle_details['vehicle']['make']
#     model = vehicle_details['vehicle']['model']
#     fuel_type = vehicle_details['vehicle']['fuelType']

#     # Print the extracted details
#     print(f'Owner name: {owner_name}')
#     print(f'Registration date: {registration_date}')
#     print(f'Make: {make}')
#     print(f'Model: {model}')
#     print(f'Fuel type: {fuel_type}')
# else:
#     # Print an error message if the request was unsuccessful
#     print(f'Request failed with status code {response.status_code}')
# response = requests.get(
#     'https://apisetu.gov.in/certificate/v3/transport/chaln')
# print(response)

import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmList


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(1)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
