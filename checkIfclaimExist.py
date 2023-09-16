import firebase_admin
from firebase_admin import auth

# Initialize the Firebase Admin SDK
cred = firebase_admin.credentials.Certificate(
    "./rasor-reference-firebase-adminsdk-otdli-f25650d806.json"
)
firebase_admin.initialize_app(cred)

# User UID for which you want to check the custom claim
user_uid = "oKCkFna2phanxoCqC5M6UFvG6AJ3"

# Get the user's Firebase Authentication token
try:
    user = auth.get_user(user_uid)
    custom_claims = user.custom_claims

    # Check if the custom claim exists and is set to true
    if custom_claims and custom_claims.get("writer"):
        print("User is an writer")
    else:
        print("User is not an admin or custom claim not set")
except Exception as e:
    print("Error:", e)
