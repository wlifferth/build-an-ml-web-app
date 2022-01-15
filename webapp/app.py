from flask import Flask, render_template, request

import json

app = Flask(__name__)

app.secret_key = 'asdf'

AVERAGE_SQUARE_FOOTAGE = 1827
AVERAGE_PRICE_PER_SQUARE_FOOT = 195


@app.route('/', methods=['GET', 'POST'])
def home():
    print(request)
    if request.method == 'POST':
        try:
            livingArea = int(request.form['livingArea'])
        except:
            livingArea = AVERAGE_SQUARE_FOOTAGE # Default to the average square footage
        prediction = livingArea * AVERAGE_PRICE_PER_SQUARE_FOOT
    else:
        prediction = None
        
    states = json.load(open('states.json'))
    
    return render_template('index.html', states=states, prediction=prediction)

if __name__ == '__main__':
    app.run(port=1234)