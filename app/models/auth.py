import json
from urllib.error import HTTPError
import requests

class Auth():

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/"
        self.headers = {"content-type": "application/json; charset=UTF-8"}

    def sign_in_with_email_and_password(self, email, password):
        request_ref = self.base_url + "verifyPassword?key={0}".format(self.api_key)

        data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
        request_object = requests.post(request_ref, headers=self.headers, data=data)
        raise_detailed_error(request_object)
        current_user = request_object.json()
        return current_user

    def create_user_with_email_and_password(self, email, password):
        request_ref = self.base_url + "signupNewUser?key={0}".format(self.api_key)
        data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
        request_object = requests.post(request_ref, headers=self.headers, data=data)
        raise_detailed_error(request_object)
        return request_object.json()
    
    def send_email_verification(self, id_token):
        request_ref = self.base_url + "getOobConfirmationCode?key={0}".format(self.api_key)
        data = json.dumps({"requestType": "VERIFY_EMAIL", "idToken": id_token})
        request_object = requests.post(request_ref, headers=self.headers, data=data)
        raise_detailed_error(request_object)
        return request_object.json()

    def send_password_reset_email(self, email):
        request_ref = self.base_url + "getOobConfirmationCode?key={0}".format(self.api_key)
        data = json.dumps({"requestType": "PASSWORD_RESET", "email": email})
        request_object = requests.post(request_ref, headers=self.headers, data=data)
        raise_detailed_error(request_object)
        return request_object.json()

def raise_detailed_error(request_object):
        try:
            request_object.raise_for_status()
        except HTTPError as e:
            raise HTTPError(e, request_object.text)