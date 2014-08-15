__author__ = 'sweemeng'
import gmail
import datetime
from dateutil.relativedelta import *
import yaml

# TODO: Create parameter
# TODO: Put into github
# TODO: See if we need a proper ui than writing a script, parameter maybe?
class GmailAutomator(object):
    def __init__(self, email, password):
        self.client = gmail.login(email, password)

    def actions(self, mailbox, actions, **filter_):
        if actions is not list:
            actions = [actions]
        if set(actions).issubset(set("unread", "delete", "spam", "star", "archive")):
            raise Exception("Action Not supported")
        mails = self.client.mailbox(mailbox).mail(**filter_)
        for mail in mails:
            for action in actions:
                getattr(mail, action)()


if __name__ == "__main__":
    config = yaml.load(open("../config.yaml"))
    automator = GmailAutomator(config["username"], config["password"])
    last_friday = datetime.date.today() + relativedelta(weekday=FR(-1))
    automator.actions("amanz", "read", before=last_friday)
    last_month = datetime.date.today() + relativedelta(month=-1)
    automator.actions("book-sale", "read", before=last_month)

