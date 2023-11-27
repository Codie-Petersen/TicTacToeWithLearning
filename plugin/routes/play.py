from quart import Blueprint, request
from plugin.__init__ import CORS_ON, CONFIG_ROUTE, IS_LOCAL, PORT
from quart_cors import cors
import quart


play_blueprint = Blueprint("play", __name__)
if CORS_ON:
    play_blueprint = cors(play_blueprint, allow_origin="*")


@play_blueprint.route("/play/new", methods=["POST"])
async def play():
    """A function to play the game."""
    return "OK"


@play_blueprint.route("/play/move", methods=["POST"])
async def move():
    """A function to make a move."""
    return "OK"