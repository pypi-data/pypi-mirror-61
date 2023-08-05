from queue import Queue, Empty
from threading import Thread

import time


class NonBlockingStreamReader:

    def __init__(self, stream, interval=1.0):
        self._stream = stream
        self._queue = Queue()
        self._to_break = False
        self._interval = interval

        self.MAX_LINE_TO_READ = 10

        self._thread = Thread(target=self.populate_queue, daemon=True)
        self._thread.start()  # start collecting lines from the stream

    def populate_queue(self):
        while not self._to_break:
            line = self._safely_read_line_from_stream()
            if line:
                self._queue.put(line)

            time.sleep(self._interval)

    def _safely_read_line_from_stream(self):
        try:
            return self._stream.readline().rstrip("\n\r")
        except:
            pass

    def _drain_stream(self):
        line = self._safely_read_line_from_stream()
        # Need tp limit the number of lines to drain, because if the health_check script will always print lines
        # we will never get out of this loop
        line_count = 0
        while line and line_count < self.MAX_LINE_TO_READ:
            self._queue.put(line)
            line = self._safely_read_line_from_stream()
            line_count += 1

    def stop(self):
        self._to_break = True
        self._thread.join(timeout=self._interval * 2)
        self._drain_stream()

    def read_line(self, timeout):
        try:
            return self._queue.get(block=True, timeout=timeout)
        except Empty:
            return None

    def read_lines(self):
        items = []
        try:
            while not self._queue.empty():
                items.append(self._queue.get(block=False))
        except Empty:
            pass
        return items


class UnexpectedEndOfStream(Exception):
    pass
