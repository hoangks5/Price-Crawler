from flask import (
    Flask,
    make_response,
    jsonify,
    request,
    send_file,
    send_from_directory,
    abort,
)
from flask_cors import CORS
import API

def response_body(status, data=None, status_code=200):
    status = int(status) 

    if status == 1:
        response_body_json = {
            "error": None,
            "data": data
        }
    else:
        message = None
        if status == 2:
            message = "token error"
            status_code = 401
        elif status == 3:
            message = "server error"
            status_code = 500
        elif status == 4:
            message = "data input error"
            status_code = 400

        response_body_json = {
            "error": {
                "error_code": status,
                "message": message
            },
            "data": None
        }

    res = make_response(jsonify(response_body_json), status_code)
    return res


def check_token(request):
    token = ""
    try:
        token = request.headers.get('Authorization')
    except:
        abort(response_body(2))
    if token != "ai_market":
        abort(response_body(2))


def check_data(request):
    try:
        json_data = request.json
        data = json_data['data']

        return data
    except Exception as error:
        print(str(error))
        abort(response_body(4))



app = Flask(__name__)
CORS(app)
@app.route("/",methods=['GET'])
def get_service():
    return 'price feed'
@app.route("/price/median",methods=['POST'])
def median():
    check_token(request)
    data = check_data(request)

    try:
        result = API.median(data)
        return response_body(status=1, data=result)
    except Exception as error:
        print(str(error))
        abort(response_body(status=3))

@app.route("/price/vwa",methods=['POST'])
def vwa():
    check_token(request)
    data = check_data(request)

    try:
        result = API.vwa(data)
        return response_body(status=1, data=result)
    except Exception as error:
        print(str(error))
        abort(response_body(status=3))

@app.route("/price",methods=['POST'])
def all():
    check_token(request)
    data = check_data(request)

    try:
        result = API.test(data)
        return response_body(status=1, data=result)
    except Exception as error:
        print(str(error))
        abort(response_body(status=3))
app.run(debug=True)


