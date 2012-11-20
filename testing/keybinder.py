import threading

class Keybinder(threading.Thread):
    def __init__(self, callback, keycode):
        super(Keybinder, self).__init__()
        self.keycode = keycode
        self.callback = callback
        self.quit = False

    def run(self):
        disp = Display()
        root = disp.screen().root
        root.change_attributes(event_mask = X.KeyPressMask)
        root.grab_key(self.keycode, X.AnyModifier, 1,X.GrabModeAsync, X.GrabModeAsync)
        while 1:
            event = root.display.next_event()
            if event.type == X.KeyPress:
                self.callback()