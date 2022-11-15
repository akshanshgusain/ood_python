# class Server:
#     def __init__(self, name):
#
#         self.app = FastAPI(name)
#
#         @self.app.route('/')
#         def __index():
#             return self.index()
#
#         @self.app.route('/hello')
#         def __hello():
#             return self.hello()
#
#         @self.app.route('/user_agent')
#         def __user_agent():
#             return self.user_agent()
#
#         @self.app.route('/factorial/<n>', methods=['GET'])
#         def __factorial(n):
#             return self.factorial(n)
#
#     def index(self):
#         return 'Index Page'
#
#     def hello(self):
#         return 'Hello, World'
#
#     def user_agent(self):
#         return request.headers.get('User-Agent')
#
#     def factorial(self, n):
#         n = int(n)
#         fact = 1
#         for num in range(2, n + 1):
#             fact = fact * num
#         return str(fact)
#
#     def run(self, host, port):
#         self.app.run(host=host, port=port)
#
#
# def main():
#     server = Server(__name__)
#     server.run(host='0.0.0.0', port=5000)
#
#
# if __name__ == '__main__':
#     main()