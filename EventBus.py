destroyBall = 'destroyBall'
draw = 'draw'

class EventBus:
    def __init__(self):
        self.listeners = {}

    def on(self, event, callback):
        if self.listeners.get(event):
            self.listeners[event].append(callback)
        else:
            self.listeners[event] = []
            self.listeners[event].append(callback)

    def off(self, event, callback):
        pass

    def emit(self, event, data):
        if self.listeners.get(event):
            callbacks = self.listeners[event]
            for callback in callbacks:
                callback(data)
