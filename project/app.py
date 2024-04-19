from flask import Flask, jsonify, render_template
from script import get_all_motor

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_all_motor', methods=['GET'])
def get_all_motor_route():
    all_motors = get_all_motor()
    return jsonify(all_motors)

if __name__ == '__main__':
    app.run(debug=False)
