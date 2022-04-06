import sys


class Logger():
    stdout = sys.stdout
    messages = []

    def start(self):
        sys.stdout = self

    def stop(self):
        sys.stdout = self.stdout

    def write(self, text):
        self.messages.append(text)


log = Logger()

log.start()
print("sys", "123123")
log.stop()

print(log.messages)
