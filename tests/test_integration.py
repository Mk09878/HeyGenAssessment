import unittest
import threading
import time
import asyncio
from server.app import app
from client.job_status import TimerClient
from werkzeug.serving import make_server

class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        app.logger.info('Starting server')
        self.server.serve_forever()

    def shutdown(self):
        app.logger.info('Shutting down server')
        self.server.shutdown()

class IntegrationTest(unittest.TestCase):
    def setUp(self):
        self.server = ServerThread(app)
        self.server.start()
        time.sleep(1)  # Allow some time for the server to start
        self.client = TimerClient()

    def tearDown(self):
        # Stop the Flask development server
        self.server.shutdown()
        self.server.join()

    def test_start_timer_endpoint(self):
        duration = 10  # Adjust the duration as needed
        response = self.client.start_timer(duration=duration)
        self.assertIsNotNone(response)  # Assuming the response contains useful information

        async def test_get_status():
            status_response = await self.client.get_timer_status()
            self.assertTrue(status_response)

        asyncio.run(test_get_status())

if __name__ == '__main__':
    unittest.main()
