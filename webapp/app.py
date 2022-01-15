from flask import Flask, render_template, request, flash
from predict import predict

import json

app = Flask(__name__)

app.secret_key = 'asdf'

AVERAGE_SQUARE_FOOTAGE = 1827
AVERAGE_PRICE_PER_SQUARE_FOOT = 195


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        form_dict = request.form
        try:
            prediction = predict(request.form)
        except Exception as e:
            print(e)
            flash('We weren\'t able to make a prediction. Maybe check your input and try again?')
            prediction = None
    else:
        form_dict = {}
        prediction = None
        
    states = json.load(open('states.json'))
    print(form_dict)
    return render_template('index.html', states=states, prediction=prediction, form_dict=form_dict)

if __name__ == '__main__':
    app.run(port=1234, debug=True)