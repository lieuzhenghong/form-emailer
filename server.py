from flask import Flask, request 
from flask_cors import CORS, cross_origin
import generator

app = Flask(__name__)
CORS(app)

@app.route("/run")
def run():
    params = request.args
    d = params.get('data')
    p = params.get('letter')
    return(generator.generate_letters(d, p))

if __name__ == "__main__":
    app.run()
