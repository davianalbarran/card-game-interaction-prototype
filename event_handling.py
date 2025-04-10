class Event:
    def __init__(self, event_type, data = None):
        self.type = event_type
        self.data = data

class EventDispatcher:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    def post(self, event):
        if event.type in self.subscribers:
            for callback in self.subscribers[event.type]:
                callback(event)
