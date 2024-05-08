from flask import Flask, render_template


app = Flask(__name__, template_folder='news_portal/templates', static_folder='news_portal/static')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)