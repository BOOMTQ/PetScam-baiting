# from flask import Flask, request
#
# app = Flask(__name__)
#
#
# @app.route('/test')
# def test_page():
#     with open(r'D:\UoB\UG\大三\individual project\Petscam-baiting\test\test.html', 'r') as f:
#         return f.read()
#
#
# @app.route('/test', methods=['POST'])
# def contact_handler():
#     name = request.form.get('name')
#     email = request.form.get('email')
#     phoneNumber = request.form.get('PhoneNumber')
#     city = request.form.get('city')
#     state = request.form.get('state')
#     message = request.form.get('message')
#     # Here you would process the form data
#     print(f"Name: {name}, Email: {email}, PhoneNumber: {phoneNumber}, City: {city}, State: {state}, Message: {message}")
#     return 'Form submitted successfully', 200
#
#
# if __name__ == '__main__':
#     app.run(port=8080, debug=True)
