import os
import textwrap
import requests

class Line:
    def __init__(self, datastore):
        self.datastore = datastore

    def notify(self, program):
        if self.datastore.is_updated(program):
            print(program)
            self.notify_to_line(program)
            self.datastore.update_notify_date(program)
        else:
            print('no update')

    def notify_to_line(self, program):
        token = os.environ.get('LINE_TOKEN')
        if token is None:
            print('no token')
            return

        url = "https://notify-api.line.me/api/notify"
        headers = {"Authorization": "Bearer {}".format(token)}
        message = self.format_message(program.title, program.date, program.name,
                                 program.description)
        payload = {"message": message}
        requests.post(url, headers=headers, data=payload)

    def format_message(self, title, date, name, description):
        template = textwrap.dedent("""番組名: {title}
            次回放送: {date}
            ゲスト: {name}
            番組説明: {description}
        """)
        return template.format(
            title=title, date=date, name=name, description=description)