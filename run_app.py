from plugin.__init__ import CORS_ON, PORT
from plugin.app import App

if __name__ == "__main__":
    app = App(name="Template Plugin", cors_on=CORS_ON, port=PORT)
    app.run()