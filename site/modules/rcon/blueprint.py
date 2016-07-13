from flask import Blueprint, jsonify, request, current_app
import os

rcon = Blueprint("rcon", __name__, url_prefix="/rcon")

@rcon.route("/github/<key>/", methods=["POST"])
def github_webhook(key):
    if request.headers["X-GitHub-Event"] != "push":
        return jsonify(ok=True, error=None, note="webhook not a push so doing nothing")

    if not current_app.config["ALLOW_RCON"]:
        return jsonify(ok=False, error="rcon disabled", note=None)

    if key != os.getenv("RCON_KEY", False):
        return jsonify(ok=False, error="rcon key incorrect", note=None)

    data = request.get_json()
    if "testing" in data["ref"]:
        os.system("bash -c '/home/tft/run.sh & disown'")
        return jsonify(ok=True, error=None, note="pulled")

    return jsonify(ok=True, error=None, note="not testing")
