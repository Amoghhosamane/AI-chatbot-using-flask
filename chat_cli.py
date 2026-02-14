from chatbot_engine import ChatbotEngine

def start_chat():
    engine = ChatbotEngine()
    print("Initializing Chatbot Engine...")
    engine.load_all()
    
    print("\n" + "="*50)
    print("   AI Chatbot (Terminal Mode) - Type 'quit' to exit")
    print("="*50)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Bot: Goodbye! Have a great day.")
            break
            
        if not user_input.strip():
            continue
            
        response = engine.get_response(user_input)
        print(f"Bot: {response}")

if __name__ == "__main__":
    start_chat()
