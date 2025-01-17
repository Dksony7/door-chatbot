import g4f
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    response = g4f.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": user_input}]
    )
    return jsonify({'response': response.choices[0].message['content']})

if __name__ == '__main__':
    app.run(debug=True)
