from flask import (
    Flask,
    abort,
    request
)
import json

# Create the application instance
app = Flask(__name__)

@app.route('/search', methods=['GET'])
def query_search():
    qy = request.args.get("query")
    print('Request: {} '.format(qy))
    return json.dumps(qy)

# @app.route('/search', methods=['POST'])
# def query_search():
#     if not request.json:
#         abort(400)
#     print(request.json)
#     return json.dumps(request.json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)