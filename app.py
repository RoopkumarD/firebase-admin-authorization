import firebase_admin
from firebase_admin import auth, credentials

cred = credentials.Certificate(
    "./rasor-reference-firebase-adminsdk-otdli-f25650d806.json"
)
firebase_admin.initialize_app(cred)

# User UID for which you want to set a custom claim
user_uid = "lMhW25EvXaVyUOiAHieGY58R7iX2"

# Define the custom claims to set
custom_claims = {"isAdmin": True}

# Set the custom claims
try:
    auth.set_custom_user_claims(user_uid, custom_claims)
    print("Custom claims set successfully")
except Exception as e:
    print(f"Error setting custom claims: {e}")
