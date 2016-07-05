from flask import Blueprint, jsonify, request, current_app
import json
import os

rcon = Blueprint("rcon", __name__, url_prefix="/rcon")

@rcon.route("/github/<key>/", methods=["POST"])
def github_webhook(key):
    if not current_app.config["ALLOW_RCON"]:
        return jsonify(ok=False, error="rcon disabled", note=None)

    if key != os.getenv("RCON_KEY", False):
        return jsonify(ok=False, error="rcon key incorrect", note=Nonw)

    data = json.loads(request.data)
    if "testing" in data["ref"]:
        os.system("bash -c '/home/tft/run.sh & disown'")
        return jsonify(ok=True, error=None, note="pulled")

    return jsonify(ok=True, error=None, note="not testing")
