__author__ = 'sweemeng'
import gmail
import datetime
from dateutil.relativedelta import *
import yaml
import logging


class GmailAutomator(object):
    def __init__(self, email, password):
        self.client = gmail.login(email, password)

    def actions(self, mailbox, actions, **filter_):
        if actions is not list:
            actions = [actions]
        if set(actions).issubset(set(["unread", "delete", "spam", "star", "archive"])):
            raise Exception("Action Not supported")
        mails = self.client.mailbox(mailbox).mail(**filter_)
        for mail in mails:
            for action in actions:
                getattr(mail, action)()

    def cleanup(self):
        self.client.logout()


if __name__ == "__main__":
    logging.basicConfig(filename="gmail_automator.log", level=logging.DEBUG)
    config = yaml.load(open("config.yaml"))
    logging.debug("setting up automator")
    automator = GmailAutomator(config["username"], config["password"])
    logging.debug("Cleaning up amanz email")
    last_friday = datetime.date.today() + relativedelta(weekday=FR(-1))
    automator.actions("amanz", "read", before=last_friday, unread=True)
    logging.debug("Cleaning up book sale")
    last_month = datetime.date.today() + relativedelta(months=-1)
    automator.actions("Book Sale", "read", before=last_month, unread=True)
    logging.debug("cleaning up myself")
    automator.cleanup()
    logging.debug("completed")

