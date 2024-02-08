from flask import Flask, jsonify, request
from flask_cors import CORS
from joblib import load

presence_classifier = load('api/presence_classifier.joblib')
presence_vect = load('api/presence_vectorizer.joblib')
category_classifier = load('api/category_classifier.joblib')
category_vect = load('api/category_vectorizer.joblib')

app = Flask(__name__)
CORS(app)
@app.route('/main', methods=['POST'])
def main():
    if request.method == 'POST':
        output = []
        data = request.get_json().get('tokens')

        for token in data:
            result = presence_classifier.predict(presence_vect.transform([token]))
            if result == 'Dark':
                cat = category_classifier.predict(category_vect.transform([token]))
                output.append(cat[0])
            else:
                output.append(result[0])

        dark = [data[i] for i in range(len(output)) if output[i] == 'Dark']
        for d in dark:
            print(d)
        print()
        print(len(dark))

        message = '{ \'result\': ' + str(output) + ' }'
        print(message)

        json = jsonify(message)

        return json

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
