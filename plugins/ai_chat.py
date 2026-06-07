def run():
    print("\n🤖 AI CHAT STARTED (type 'exit' to quit)\n")

    while True:
        msg = input("You: ")

        if msg.lower() == "exit":
            break

        print(f"AI: You said -> {msg}")
