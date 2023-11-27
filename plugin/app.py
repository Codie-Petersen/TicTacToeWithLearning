from plugin.routes.info import info_blueprint as info
from quart_cors import cors
import asyncio
import signal
import quart

class App():
    """Define the app and all of its routes and components."""

    def __init__(self, name=__name__, host="0.0.0.0", port=5000, cors_on=False):
        """Initialize the app."""
        self.app = quart.Quart(name)
        if cors_on:
            self.app = cors(self.app, allow_origin="*")
        self.app.register_blueprint(info)
        self.host = host
        self.port = port

    def _handle_sigint(self, sig, frame):
        """Help shutdown the app."""
        print("Received SIGINT, shutting down...")
        asyncio.create_task(self.app.shutdown())

    def _add_signal_handlers(self, loop):
        """Add signal handlers to the event loop."""
        for signal_name in {"SIGINT", "SIGTERM", "SIGBREAK"}:
            if hasattr(signal, signal_name):
                try:
                    loop.add_signal_handler(getattr(signal, signal_name), self._handle_sigint)
                except NotImplementedError:
                    signal.signal(getattr(signal, signal_name), self._handle_sigint)
    
    def run(self):
        loop = asyncio.get_event_loop()
        self._add_signal_handlers(loop)
        self.app.run(debug=True, host=self.host, port=self.port)
