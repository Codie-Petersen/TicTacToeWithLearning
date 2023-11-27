from quart import Blueprint, request
from plugin.__init__ import CORS_ON, CONFIG_ROUTE, IS_LOCAL, PORT
from quart_cors import cors
import quart


info_blueprint = Blueprint("info", __name__)
if CORS_ON:
    info_blueprint = cors(info_blueprint, allow_origin="*")


@info_blueprint.route("/info/health", methods=["GET"])
async def health():
    """A simple health check function for the plugin."""
    return "OK"


@info_blueprint.route("/.well-known/ai-plugin.json", methods=["GET"])
async def manifest():
    """A function for stores and applications to get the manifest of the plugin."""
    host = request.headers["Host"]
    filename = f"{CONFIG_ROUTE}/ai-plugin.json"
    hostname = f"https://{host}"

    if IS_LOCAL:
        hostname = f"http://localhost:{PORT}"
    
    yaml_route = f"{hostname}/info/openapi.yaml"
    logo_route = f"{hostname}/info/logo.png"
    with open(filename) as file:
        text = file.read()
        text = text.replace("OPENAPI_YAML_ROUTE", yaml_route)
        text = text.replace("LOGO_ROUTE", logo_route)
        return quart.Response(text, mimetype="application/json")


@info_blueprint.route("/info/logo.png", methods=["GET"])
async def logo():
    """A function to return the logo of the plugin for any store."""
    return await quart.send_file(f"{CONFIG_ROUTE}/logo.png")


@info_blueprint.route("/info/openapi.yaml", methods=["GET"])
async def openapi():
    """OpenAPI documentation for the plugin consumers."""
    host = request.headers["Host"]
    filename = f"{CONFIG_ROUTE}/openapi.yaml"
    hostname = f"https://{host}"

    if IS_LOCAL:
        hostname = f"http://localhost:{PORT}"
    
    with open(filename) as file:
        text = file.read()
        text = text.replace("PLUGIN_HOSTNAME", hostname)
        return quart.Response(text, mimetype="text/yaml")


@info_blueprint.route("/info/help", methods=["GET"])
async def help():
    """
    A function to return the help page for the plugin. You should only add information about
    the functionality that users can use.
    """
    return await quart.send_file(f"{CONFIG_ROUTE}//help.json")