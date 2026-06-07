from web.app import app as web_app
from network.tools import run as network_run
from ai.tools import run as ai_run
from github_tools.tools import run as github_run


def menu():

    while True:
        print("""
=====================
        NEXUS
=====================

1. Web Dashboard
2. Network Tools
3. AI Tools
4. GitHub Tools
5. Plugins
9. Support System
0. Exit
""")

        choice = input("Select: ")

        if choice == "1":
            web_app.run(host="0.0.0.0", port=5000)

        elif choice == "2":
            network_run()

        elif choice == "3":
            ai_run()

        elif choice == "4":
            github_run()

        elif choice == "5":
            from plugins.loader import load_plugins, list_plugins, run_plugin, delete_plugin

            load_plugins()

            while True:
                list_plugins()

                print("""
1. Run Plugin
2. Delete Plugin
0. Back
""")

                c = input("Select: ")

                if c == "0":
                    break

                elif c == "1":
                    p = input("Plugin number: ")
                    run_plugin(p)

                elif c == "2":
                    name = input("Plugin name: ")
                    delete_plugin(name)

                else:
                    print("Invalid option")

        elif choice == "9":
            from core.tickets import create_ticket, list_tickets

            while True:
                print("""
===== SUPPORT SYSTEM =====
1. Create Ticket
2. View Tickets
0. Back
""")

                c = input("Select: ")

                if c == "0":
                    break

                elif c == "1":
                    email = input("Your Email: ")
                    subject = input("Subject: ")
                    message = input("Message: ")

                    ticket_id = create_ticket(email, subject, message)

                    print("\n✔ Ticket Created Successfully")
                    print(f"🎫 Ticket ID: {ticket_id}")

                elif c == "2":
                    tickets = list_tickets()

                    if not tickets:
                        print("No tickets found")
                        continue

                    for t in tickets:
                        print("\n-------------------")
                        print(f"ID: {t['id']}")
                        print(f"Email: {t['email']}")
                        print(f"Subject: {t['subject']}")
                        print(f"Status: {t['status']}")

                else:
                    print("Invalid option")

        elif choice == "0":
            print("Goodbye 👋")
            break

        else:
            print("Invalid option")
