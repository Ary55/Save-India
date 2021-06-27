from flask import Flask, render_template
app = Flask(__name__)
app.secret_key = '6yTWFOE7j05WpVr8ic'


@app.route('/')
def home_page():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
