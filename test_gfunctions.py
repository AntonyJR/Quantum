from flask import Flask


def main():
    app = Flask(__name__)
    with app.test_request_context():


if __name__ == '__main__':
    main()
