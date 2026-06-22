# import firebase_admin

# from firebase_admin import credentials


# firebase_app = None


# def initialize_firebase():

#     global firebase_app

#     if firebase_app:
#         return firebase_app

#     cred = credentials.Certificate(
#         "firebase-service-account.json"
#     )

#     firebase_app = firebase_admin.initialize_app(
#         cred
#     )

#     return firebase_app




import os
import firebase_admin
from firebase_admin import credentials

firebase_app = None

def initialize_firebase():
    print("INITIALIZING FIREBASE")
    global firebase_app

    if firebase_app:
        return firebase_app

    # 1. Dynamically find the absolute path to your root folder
    # This goes up two directories from app/utils/firebase.py to FMC/
    current_dir = os.path.dirname(os.path.abspath(__file__))  # app/utils
    root_dir = os.path.dirname(os.path.dirname(current_dir))  # FMC
    
    cert_path = os.path.join(root_dir, "firebase-service-account.json")

    # 2. Initialize with the absolute path
    cred = credentials.Certificate(cert_path)

    firebase_app = firebase_admin.initialize_app(
        cred
    )

    return firebase_app