from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta
import jwt
from django.http import JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def index(request):
    return HttpResponse("Hello, cloud gaming world!")


@csrf_exempt
def generate_jwt_for_guacamole(request):
    # Example authentication check (update as needed for your auth logic)
    payload = {
        "GUAC_ID": "1",
        "guac.hostname": "34.175.63.31",
        "guac.protocol": "ssh",
        "guac.port": "8080",
        "exp": datetime.utcnow() + timedelta(seconds=3600),
    }

    jwtToken = jwt.encode(payload, "123456789", "HS512")
    print(jwtToken)
    resp = requests.post(
        "http://34.175.63.31:8080/guacamole/api/tokens", data={"token": jwtToken}
    )
    print(resp.status_code)
    # Check if the request was successful
    if resp.status_code == 200:
        # Parse the JSON response
        json_response = resp.json()

        # Access authToken from the parsed JSON, if it exists
        if "authToken" in json_response:
            return JsonResponse({"token": json_response["authToken"]})
        else:
            # Handle case where authToken is not in the response
            return JsonResponse(
                {"error": "authToken not found in the response"}, status=400
            )
    else:
        # Handle unsuccessful requests
        return JsonResponse(
            {"error": "Failed to retrieve authToken"}, status=resp.status_code
        )
