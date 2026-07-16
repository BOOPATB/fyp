# server.py
import os
from livekit import api
from flask import Flask
from flask_cors import CORS
import dotenv
import json

dotenv.load_dotenv("env_example.env")
app = Flask(__name__)
CORS(app)

@app.route('/getToken')
def getToken():
  token = api.AccessToken(os.getenv('LIVEKIT_API_KEY'), os.getenv('LIVEKIT_API_SECRET')) \
    .with_identity("max") \
    .with_name("akash") \
    .with_grants(api.VideoGrants(
        room_join=True,
        room="my-name",
    ))

  return {"token": token.to_jwt()}
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)