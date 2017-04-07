from flask import Flask, request 
from flask_cors import CORS, cross_origin
import email_send

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
    print(params)
    email = params.get('email')
    pw = params.get('pw')
    data = params.get('data')+'.csv'
    body = params.get('body')+'.txt'
    preview = True if params.get('preview') == 'true' else False 
    return(str(email_send.main(email, pw , data, body, 0, preview=preview)[0]))

if __name__ == "__main__":
    app.run()
