from dotenv import dotenv_values

config = dotenv_values(".env")
CORS_ON = config["CORS_ON"] == "True"
CONFIG_ROUTE = config["CONFIG_ROUTE"]
IS_LOCAL = config["IS_LOCAL"] == "True"
PORT = config["PORT"]