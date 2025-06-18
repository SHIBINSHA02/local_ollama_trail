from flask import Flask, render_template, request, jsonify
import ollama

app = Flask(__name__)

# Store conversation history
conversation_history = []

@app.route('/')
def index():
    return render_template('index.html', conversation=conversation_history)

@app.route('/chat', methods=['POST'])
def chat():
    # Get user input from the form
    user_input = request.form['user_input']

    # Add user input to conversation history
    conversation_history.append({"role": "user", "content": user_input})

    # Prepare the prompt with conversation history
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        *conversation_history
    ]

    try:
        # Call the Ollama model
        response = ollama.chat(
            model="llama3",  # Replace with your model, e.g., gemma:2b
            messages=messages
        )

        # Extract the assistant's response
        assistant_response = response['message']['content']

        # Add assistant response to conversation history
        conversation_history.append({"role": "assistant", "content": assistant_response})

        # Return the updated conversation
        return jsonify({"conversation": conversation_history})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)