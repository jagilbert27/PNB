# from website import create_app

# app = create_app()

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask
application = Flask(__name__)
app = application
@application.route('/')
def hello_world():
        return 'howdy'