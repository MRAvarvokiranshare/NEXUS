import json
import os
import time
import random
from core.logger import log
from core.emailer import send_email

DB_PATH = "data/tickets.json"


def load_db():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r") as f:
        return json.load(f)


def save_db(data):
    with open(DB_PATH, "w") as f:
        json.dump(data, f, indent=4)


def create_ticket(email, subject, message):
    data = load_db()

    ticket = {
        "id": str(int(time.time())) + str(random.randint(100, 999)),
        "email": email,
        "subject": subject,
        "message": message,
        "status": "OPEN",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "replies": []
    }

    data.append(ticket)
    save_db(data)

    log("CREATE_TICKET", ticket["id"])

    return ticket["id"]


def get_ticket(ticket_id):
    data = load_db()

    for t in data:
        if t["id"] == ticket_id:
            return t

    return None


def list_tickets():
    return load_db()


def close_ticket(ticket_id):
    data = load_db()

    for t in data:
        if t["id"] == ticket_id:
            t["status"] = "CLOSED"
            save_db(data)

            log("CLOSE_TICKET", ticket_id)

            return True

    return False


def add_reply(ticket_id, message):
    data = load_db()

    for t in data:
        if t["id"] == ticket_id:

            if "replies" not in t:
                t["replies"] = []

            t["replies"].append({
                "message": message,
                "time": time.strftime("%Y-%m-%d %H:%M:%S")
            })

            save_db(data)

            log("REPLY_TICKET", ticket_id)

            # 📧 EMAIL SEND
            send_email(
                t["email"],
                f"Reply to ticket {ticket_id}",
                message
            )

            return True

    return False
