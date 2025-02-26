import nltk
from nltk.chat.util import Chat, reflections

# Define chatbot patterns and responses
pairs = [
    [r"hi|hello|hey", ["Hello!", "Hey there!", "Hi! How can I assist you?"]],
    [r"how are you", ["I'm just a bot, but I'm doing great! How about you?" ]],
    [r"what is your name", ["I'm a chatbot created using NLTK. You can call me ChatBot!" ]],
    [r"(.*) your name", ["I am ChatBot, your virtual assistant."]],
    [r"quit|bye|exit", ["Goodbye! Have a great day!", "Bye! Take care."]],
    [r"(.*)", ["I'm not sure how to respond to that. Could you rephrase?"]]
]

# Create a chatbot instance
chatbot = Chat(pairs, reflections)

def start_chat():
    print("Hello! I'm your chatbot. Type 'quit' to exit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'bye', 'exit']:
            print("ChatBot: Goodbye! Have a great day!")
            break
        response = chatbot.respond(user_input)
        print(f"ChatBot: {response}")

if __name__ == "__main__":
    start_chat()
