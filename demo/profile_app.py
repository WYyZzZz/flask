import cProfile
from functools import wraps

import flask
from flask import Flask
from line_profiler import LineProfiler


def line_profiler_func_line_time(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        func_return = f(*args, **kwargs)
        profile = LineProfiler()
        profile.enable()  # 开始分析
        profile_wrap = profile(f)
        profile_wrap(*args, **kwargs)
        profile.disable()  # 停止分析
        profile.print_stats()  # 打印出性能分析结果
        return func_return

    return decorator


def profile_some_functions():
    """
    该函数用于动态地给Flask源码中的特定函数添加@profile装饰器。
    这里以Flask.app的dispatch_request方法为例。
    """
    original_dispatch_request = flask.app.Flask.full_dispatch_request

    @line_profiler_func_line_time
    def profiled_dispatch_request(*args, **kwargs):
        return original_dispatch_request(*args, **kwargs)

    flask.app.Flask.full_dispatch_request = profiled_dispatch_request

    # 也可以添加其他函数的profile装饰器
    original_make_response = flask.app.Flask.make_response

    @line_profiler_func_line_time
    def profiled_make_response(*args, **kwargs):
        return original_make_response(*args, **kwargs)

    flask.app.Flask.make_response = profiled_make_response


if __name__ == "__main__":
    # 在Flask应用对象创建之前，调用profile_some_functions
    from src.flask.app import Flask as my_flask
    from my_blueprint import my_blueprint

    profile_some_functions()

    flask.app.Flask = my_flask

    app = Flask(__name__)

    # 在应用对象上注册蓝图对象
    app.register_blueprint(my_blueprint, url_prefix='/bp')

    print(app.get_send_file_max_age())


    @app.route('/')
    def home():
        return 'Hello, World!'


    @app.route('/')
    def hello_world():
        return 'Hello, World!'


    cProfile.run('app.run(debug=True)', 'my_profile')
