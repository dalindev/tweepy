from flask import (
    Flask,
    abort,
    request
)
import json
import authenticate

# key for calling api, once we have database setup
# use proper login/auth
from app_config import LOGIN_TEMP_KEY
from model import search


# TODO - add login/auth


# Create the application instance
app = Flask(__name__)


@app.route('/search', methods=['GET'])
def query_search():

    # validate token...
    authenticate.validate()

    # request obj
    req = request.args

    search_query = req.get("query", "")
    counts = req.get("counts", 100)

    search.search_tweet(search_query, counts)
    print('Request: {} '.format(search_query))

    return json.dumps(search_query)

# @app.route('/search', methods=['POST'])
# def query_search():
#     if not request.json:
#         abort(400)
#     print(request.json)
#     return json.dumps(request.json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)