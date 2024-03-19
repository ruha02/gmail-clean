import os.path
from pprint import pprint
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tqdm import tqdm

SCOPES = ["https://www.googleapis.com/auth/gmail.modify", "https://mail.google.com/"]


def get_users():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("gmail", "v1", credentials=creds)
        return service.users()
    except HttpError as error:
        print(f"An error occurred: {error}")


def get_messages(u, from_address):
    m = u.messages().list(userId="me", q=f"from:{from_address}").execute()
    return m.get("messages", None)


def read_message(u, messageId, only_snippet=True):
    m = u.messages().get(userId="me", id=messageId).execute()
    if only_snippet:
        return m["snippet"]
    else:
        return m


def delete_message(u, messageId):
    return u.messages().delete(userId="me", id=messageId).execute()


def find_and_delete(u, from_address):
    ms = get_messages(u, from_address)
    if ms is None:
        # print(f"No messages from {from_address}")
        return
    bar = tqdm(ms, leave=False)

    for m in bar:
        bar.set_description(f"Message {m['id']}")
        delete_message(u, m["id"])


def main():
    u = get_users()
    with open("spamlist.txt", 'r') as f:
        spam_list = f.read().splitlines()
    bar = tqdm(spam_list)
    for spam in bar:
        bar.set_description(f"From {spam}")
        find_and_delete(u, spam)


if __name__ == "__main__":
    main()
