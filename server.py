from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import sendr 

app = Flask(__name__)
CORS(app)

@app.route("/run")
def run():
    params = request.args
    d = params.get('data')
    p = params.get('letter')
    return(generator.generate_letters(d, p))

@app.route("/send")
def send():
    params = request.args
    email = params.get('email')
    pw = params.get('pw')
    data = params.get('data')+'.csv'
    body = params.get('body')+'.txt'
    preview = True if params.get('preview') == 'true' else False 
    data = sendr.main(email, pw , data, body, preview=preview)
    
    payload = []
    if (type(data) == list):
        for msg in data:
            print(msg)
            output = {}
            output['subject'] = msg[0][1][1]
            output['from'] = msg[0][2][1]
            output['to'] = msg[0][3][1]
            output['cc'] = msg[0][4][1]
            output['body'] = msg[1]
            payload.append(output)
        return(jsonify(payload))
    else:
        return(data)

if __name__ == "__main__":
    app.run()
