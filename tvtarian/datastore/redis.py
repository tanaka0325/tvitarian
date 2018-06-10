import datetime
import os
import redis


class Redis:
    def __init__(self):
        self.conn = redis.from_url(os.environ.get("REDIS_URL"))

    def is_updated(self, program):
        notified_date_bytes = self.conn.get(program.id)
        if notified_date_bytes is None:
            return True

        l = notified_date_bytes.decode('utf-8').split('-')
        notified_date = datetime.date(int(l[0]), int(l[1]), int(l[2]))

        return notified_date < program.date

    def update_notify_date(self, program):
        self.conn.set(program.id, program.date)
