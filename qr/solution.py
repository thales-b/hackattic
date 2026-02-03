import requests
import imutils
import cv2


def main():
    print("CV2 version:", cv2. __version__)
    response = requests.get('https://hackattic.com/challenges/reading_qr/problem?access_token=9099aaae9c650db1')

    image_url = response.json()['image_url']
    print("Image URL:",image_url)
    image = imutils.url_to_image(image_url)
    detector = cv2.QRCodeDetector()
    code, _, _ = detector.detectAndDecode(image)
    print("Code:", code)

    result = {'code':code}
    response = requests.post('https://hackattic.com/challenges/reading_qr/solve?access_token=9099aaae9c650db1', json=result)
    print("Response:", response.content)

main()
