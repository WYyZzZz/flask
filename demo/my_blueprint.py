from flask import Blueprint

# 创建一个蓝图对象，第一个参数是蓝图的名字，第二个参数是蓝图的模块或包
my_blueprint = Blueprint('my_blueprint', __name__)

@my_blueprint.route('/hello')
def hello():
    return 'Hello from Blueprint!'
