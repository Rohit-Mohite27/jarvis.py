from flask import Flask, render_template, request, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='.', template_folder='.')

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/speak', methods=['POST'])
def speak():
    data = request.json
    text = data.get('text', '')
    # Here you can call your JARVIS speak/text-to-speech function
    print("JARVIS should say:", text)
    # Optionally, call your speak(text) function here
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(debug=True)
<!-- Add inside your <body> in main.html -->
<div style="margin-top:2em;">
  <input id="text-input" type="text" placeholder="Type for JARVIS..." style="padding:8px; width:220px;">
  <button onclick="sendToJarvis()">Send</button>
</div>
<script>
function sendToJarvis() {
  const text = document.getElementById('text-input').value;
  fetch('/speak', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({text})
  }).then(res => res.json()).then(data => {
    alert("Sent to JARVIS: " + text);
  });
}
</script>
python server.py