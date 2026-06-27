import logging
import sqlite3
import threading
import uuid
import queue

LOGGER = logging.getLogger("SqliteWorker")
SILENT_TOKEN_SUFFIX = '-silent'


class SqliteWorker:
    """Sqlite thread-safe object."""

    def __init__(self, file_name, max_queue_size=100, execute_init=(), max_count=50):
        self._file_name = file_name
        self._sql_queue = queue.Queue(maxsize=max_queue_size)
        self._results = {}
        self._tokens = set()
        self._select_events = {}
        self._lock = threading.Lock()
        self._close_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        self.execute_init = execute_init
        self.max_count = max_count

    def _run(self):
        try:
            self._process_queries()
        except Exception as err:
            LOGGER.critical(
                "Unhandled exception in query processor: %s", err, exc_info=True)
            raise

    def _process_queries(self):
        with sqlite3.connect(self._file_name, check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
            cursor = conn.cursor()
            for action in self.execute_init:
                cursor.execute(action)
            conn.commit()

            count = 0
            while not self._close_event.is_set() or not self._sql_queue.empty():
                try:
                    token, query, values = self._sql_queue.get(timeout=1)
                except queue.Empty:
                    continue
                if query:
                    count += 1
                    self._execute_query(cursor, token, query, values)

                if count >= self.max_count or self._sql_queue.empty():
                    count = 0
                    conn.commit()

    def _execute_query(self, cursor, token: str, query, values):
        try:
            cursor.execute(query, values)
            if not token.endswith(SILENT_TOKEN_SUFFIX):
                with self._lock:
                    self._results[token] = cursor.fetchall()
        except sqlite3.Error as err:
            LOGGER.error("Query error: %s: %s: %s", query, values, err)
            self._handle_query_error(token, err)
        self._notify_query_done(token)

    def _is_select_query(self, query):
        return query.lower().lstrip().startswith("select")

    def _notify_query_begin(self, token):
        self._select_events.setdefault(token, threading.Event())

    def _notify_query_done(self, token):
        self._select_events[token].set()

    def _handle_query_error(self, token, err):
        with self._lock:
            self._results[token] = err

    def close(self):
        self._close_event.set()
        self._sql_queue.put((None, None, None), timeout=5)
        self._thread.join()

    def execute(self, query, values=None, always_return_token=False):
        if self._close_event.is_set():
            raise RuntimeError("Worker is closed")

        should_return_token = (
            always_return_token or
            self._is_select_query(query)
        )

        token = uuid.uuid4().hex
        if should_return_token is None:
            token += SILENT_TOKEN_SUFFIX

        self._sql_queue.put((token, query, values or []), timeout=5)
        self._notify_query_begin(token)

        if should_return_token:
            return token
        return None

    def execute_and_fetch(self, query, values=None, always_synchronous=True):
        return self.fetch_results(self.execute(query, values, always_return_token=always_synchronous))

    def fetch_results(self, token):
        if token is None:
            return
        with self._lock:
            event = self._select_events.get(token)
        if event is None:
            return
        event.wait()
        with self._lock:
            return self._results.pop(token, None)

    @property
    def queue_size(self):
        return self._sql_queue.qsize()
