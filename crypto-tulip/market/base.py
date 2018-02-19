
import websocket # pylint: disable=import-error
try:
    import thread
except ImportError:
    import _thread as thread

class Exchange():
    WEBSOCKET_URL = None
    REST_URL = None
    SUBSCRIBE_TRADES = None
    def __init__(self, *args, **kwargs):
        self.websocket_url = self.WEBSOCKET_URL
        self.rest_url = self.REST_URL
        self.subscribe_trades = self.SUBSCRIBE_TRADES
        # if websocket 
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(self.WEBSOCKET_URL,
                                on_message = self.on_message,
                                on_error = self.on_error,
                                on_close = self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()

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
        def run(*args):
            ws.send(self.SUBSCRIBE_TRADES)
        thread.start_new_thread(run, ())
        