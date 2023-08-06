import io
import os
import sys
import datetime
import threading
import time
from queue import Empty as QueueEmptyException


from logbook import queues as logbook_queues, NOTSET
from logbook.handlers import (
    StreamHandler,
    MonitoringFileHandler,
    StderrHandler,
    RotatingFileHandler as LogBookRotatingFileHandler,
    TimedRotatingFileHandler,
    TestHandler,
    MailHandler,
    GMailHandler,
    SyslogHandler,
    NTEventLogHandler,
    FingersCrossedHandler,
    GroupHandler,
    rename,
    xrange,
    errno,

)

__all__ = [
    'StreamHandler', 'RotatingFileHandler',
    'MonitoringFileHandler', 'StderrHandler',
    'TimedRotatingFileHandler', 'TestHandler', 'MailHandler', 'GMailHandler',
    'SyslogHandler', 'NTEventLogHandler', 'FingersCrossedHandler', 'GroupHandler',
    'ThreadedWrapperHandler', 'TWHThreadRotatingFileHandler'
]


class TWHThreadController(logbook_queues.TWHThreadController):
    _running_instance = None

    def __init__(self, wrapper_handler, daemon=False, timeout=0.1):
        super(TWHThreadController, self).__init__(wrapper_handler)
        self._daemon = daemon
        self.timeout = timeout
        self.waiting_to_end = False

    def start(self):
        """Starts the task thread."""
        self.running = True
        self._thread = logbook_queues.Thread(target=self._target)
        self._thread.setDaemon(self._daemon)
        self._thread.start()

    def _target(self):
        while self.running:
            try:
                record = self.wrapper_handler.queue.get(timeout=self.timeout)
            except QueueEmptyException:
                if self.waiting_to_end:
                    self.running = False
                if self._check_main():
                    self.running = False
            else:
                if record is self._sentinel:
                    self.running = False
                self.wrapper_handler.handler.handle(record)

    def _check_main(self):
        from IQManager.manager.manage_info import get_current_instance
        current_running_instance = get_current_instance()
        if current_running_instance is not None:
            self._check_main = self._check_main_instance
            self._running_instance = current_running_instance
            return self._check_main()
        else:
            self._check_main = self._check_main_base
            return self._check_main()

    @staticmethod
    def _check_main_base():
        return not threading.main_thread().is_alive()

    def _check_main_instance(self):
        return self._running_instance.status == 'END'

    def shutdown(self):
        self.waiting_to_end = True

    def join(self):
        self.shutdown()
        self._thread.join()


class ThreadedWrapperHandler(logbook_queues.ThreadedWrapperHandler):
    def __init__(self, handler, maxsize=0):
        logbook_queues.WrapperHandler.__init__(self, handler)
        self.queue = logbook_queues.ThreadQueue(maxsize)
        self.controller = TWHThreadController(self)
        self.controller.start()

    def emit(self, record):
        # noinspection PyBroadException
        try:
            from IQEngine.core.engine import engine
            dt = engine.Engine.instance().trading_dt
            if dt is None:
                dt = datetime.datetime.now()
        except Exception:
            dt = datetime.datetime.now()
        record.time = dt
        record.msg = str(record.msg)
        super(ThreadedWrapperHandler, self).emit(record)

    def shutdown(self):
        self.controller.shutdown()

    def join(self):
        self.controller.join()


class RotatingFileHandler(LogBookRotatingFileHandler):

    def perform_rollover(self):
        self.stream.close()
        for x in xrange(self.backup_count - 1, 0, -1):
            src = '%s.%d' % (self._filename, x)
            if os.path.exists(src):
                break
        else:
            rename(self._filename, self._filename + '.1')
            self._open('w')
            return
        for i in xrange(x, 0, -1):
            src = '%s.%d' % (self._filename, i)
            dst = '%s.%d' % (self._filename, i + 1)
            try:
                rename(src, dst)
            except OSError:
                e = sys.exc_info()[1]
                if e.errno != errno.ENOENT:
                    raise
        rename(self._filename, self._filename + '.1')
        self._open('w')


class TWHThreadRotatingFileHandler(RotatingFileHandler):
    _running_instance = None

    def __init__(
            self, filename, mode='a', encoding='utf-8', level=NOTSET,
            format_string=None, delay=False, max_size=1024 * 1024,
            backup_count=5, filter=None, bubble=False,
            daemon=False, timeout=0.1
    ):
        super(TWHThreadRotatingFileHandler, self).__init__(
            filename, mode, encoding, level, format_string, delay,
            max_size, backup_count, filter, bubble
        )
        self._daemon = daemon
        self.timeout = timeout
        self.waiting_to_end = False
        self.running = False
        self._thread = None
        self._stream_buffer = io.StringIO()
        self.start()

    def start(self):
        """Starts the task thread."""
        self.running = True
        self._thread = logbook_queues.Thread(target=self._target)
        self._thread.setDaemon(self._daemon)
        self._thread.start()

    def _check_main(self):
        from IQManager.manager import get_current_instance
        current_instance = get_current_instance()
        if current_instance is not None:
            self._check_main = self._check_main_instance
            self._running_instance = current_instance
            return self._check_main()
        else:
            self._check_main = self._check_main_base
            return self._check_main()

    @staticmethod
    def _check_main_base():
        return not threading.main_thread().is_alive()

    def _check_main_instance(self):
        return self._running_instance.status == 'END'

    def _target(self):
        while self.running:
            if self._stream_buffer.tell():
                stream = self._stream_buffer
                self._stream_buffer = io.StringIO()
            else:
                if self.waiting_to_end or self._check_main():
                    self.running = False
                time.sleep(self.timeout)
                continue
            try:
                stream.seek(0)
                text = stream.read()
            except (IOError, EOFError, ValueError):
                if self.waiting_to_end or self._check_main():
                    self.running = False
                time.sleep(self.timeout)
                continue
            msg = self.encode(text[:-1])
            if self.should_rollover(msg, len(msg)):
                self.perform_rollover()
            self.write(msg)
            self.flush()
        
    def emit(self, record):
        self._exchange_engine_dt(record)
        msg = self.format(record)
        self._stream_buffer.write(msg)
        self._stream_buffer.write('\n')
        
    def _exchange_engine_dt(self, record):
        from IQManager.manager.manage_info import get_current_instance
        current_running_instance = get_current_instance()
        if current_running_instance is not None:
            self._running_instance = current_running_instance
            self._exchange_engine_dt = self._exchange_engine_dt_instance
        else:
            self._exchange_engine_dt = self._exchange_engine_dt_base
        return self._exchange_engine_dt(record)

    def _exchange_engine_dt_instance(self, record):
        record.time = self._running_instance.datetime
        return record

    @staticmethod
    def _exchange_engine_dt_base(record):
        return record

    def shutdown(self):
        self.waiting_to_end = True

    def join(self):
        self.shutdown()
        self._thread.join()
