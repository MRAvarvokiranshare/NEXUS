from flask import Flask, request, jsonify, session, redirect
import json
from core.tickets import (
    create_ticket,
    get_ticket,
    list_tickets,
    close_ticket,
    add_reply
)

app = Flask(__name__)
app.secret_key = "nexus_secret_key"


# ---------------- AUTH CHECK ----------------
def auth():
    return "user" in session


# ---------------- API RESPONSE FORMAT ----------------
def ok(data=None, message="success"):
    return jsonify({
        "status": "success",
        "message": message,
        "data": data
    })


def error(msg="error"):
    return jsonify({
        "status": "error",
        "message": msg
    })


# ---------------- API: ALL TICKETS ----------------
@app.route("/api/tickets")
def api_tickets():
    return ok(list_tickets())


# ---------------- API: SINGLE TICKET ----------------
@app.route("/api/ticket/<ticket_id>")
def api_ticket(ticket_id):
    t = get_ticket(ticket_id)

    if not t:
        return error("Ticket not found"), 404

    return ok(t)


# ---------------- API: CLOSE ----------------
@app.route("/api/close/<ticket_id>")
def api_close(ticket_id):
    return ok({"closed": close_ticket(ticket_id)})


# ---------------- API: REPLY ----------------
@app.route("/api/reply/<ticket_id>")
def api_reply(ticket_id):
    msg = request.args.get("msg")

    if not msg:
        return error("message required")

    return ok({"replied": add_reply(ticket_id, msg)})


# ---------------- WEB DASHBOARD ----------------
@app.route("/")
def home():
    if not auth():
        return redirect("/login")

    data = list_tickets()

    open_count = len([t for t in data if t["status"] == "OPEN"])
    closed_count = len([t for t in data if t["status"] == "CLOSED"])

    return f"""
    <h1>NEXUS CONTROL PANEL</h1>
    <p>OPEN: {open_count}</p>
    <p>CLOSED: {closed_count}</p>
    <a href="/tickets">Tickets</a>
    """


# ---------------- TICKETS PAGE ----------------
@app.route("/tickets")
def tickets():
    if not auth():
        return redirect("/login")

    data = list_tickets()

    html = "<h1>TICKETS</h1>"

    for t in data:
        html += f"""
        <div style="border:1px solid #000;margin:10px;padding:10px;">
            <p>ID: {t['id']}</p>
            <p>Email: {t['email']}</p>
            <p>Status: {t['status']}</p>
            <a href="/close/{t['id']}">Close</a>
        </div>
        """

    return html


# ---------------- CLOSE WEB ----------------
@app.route("/close/<ticket_id>")
def close(ticket_id):
    if not auth():
        return redirect("/login")

    close_ticket(ticket_id)
    return redirect("/tickets")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")

        if u == "admin" and p == "1234":
            session["user"] = u
            return redirect("/")

        return "Wrong login"

    return """
    <form method="post">
        <input name="username">
        <input name="password">
        <button>Login</button>
    </form>
    """


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
