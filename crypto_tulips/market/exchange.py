
import websocket # pylint: disable=import-error
try:
    import threading
except ImportError:
    import _thread as thread

class Exchange(threading.Thread):
    WEBSOCKET_URL = None
    REST_URL = None
    SUBSCRIBE_TRADES = None
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.websocket_url = self.WEBSOCKET_URL
        self.rest_url = self.REST_URL
        self.subscribe_trades = self.SUBSCRIBE_TRADES
        
        websocket.enableTrace(False)
        
    def run(self):
        self.ws = websocket.WebSocketApp(self.WEBSOCKET_URL,
                                on_message = self.on_message,
                                on_error = self.on_error,
                                on_close = self.on_close)
        self.ws.on_open = self.on_open
        self.ws.run_forever()
        self.ws.keep_running = True

    def on_trade(self, data):
        return self.trade_pricestamp_adaptor(data)

    def trade_pricestamp_adaptor(self, data):
        raise NotImplementedError

    def on_message(self, ws, message):
        raise NotImplementedError

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        ws.send(self.SUBSCRIBE_TRADES)
    def stop(self):
        self.ws.close()

