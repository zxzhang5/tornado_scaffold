# encoding: utf-8

import ConfigParser
import json
import os.path
import sys
from shutil import copy2

import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options
from tornado_json.application import Application
from tornado_json.routes import get_routes

# 绝对路径
__DIR__ = os.path.abspath(os.path.dirname(__file__))
# 设置系统字符编码
reload(sys)
sys.setdefaultencoding('utf-8')


# 默认页面控制器
class PageHandler(tornado.web.RequestHandler):
    def get(self):
        file_path = self.request.path;
        # 根据路由生成默认模版名
        if file_path == "/":
            tpl = "index.html";
        elif file_path[-5:] == ".html":
            tpl = file_path.lstrip('/')
        else:
            tpl = file_path.lstrip('/') + ".html"
        # 模版文件路径
        template_path = os.path.join(__DIR__, "templates", tpl)
        # 模版文件存在则渲染，否则渲染404页面模版
        if os.path.isfile(template_path):
            self.render(tpl, path=file_path)
        else:
            self.set_status(404)
            self.render("errors/404.html", path=file_path)


# 加载API模块返回模块路由
def import_api_module(module):
    api_module_path = os.path.join(__DIR__, "api", module)
    if os.path.isdir(api_module_path):
        api_module = __import__("api." + module)
        routes = get_routes(api_module)
        return routes
    else:
        return []


def main():
    env_file = os.path.join(__DIR__, ".env")
    if not os.path.isfile(env_file):
        env_example = os.path.join(__DIR__, ".env.example")
        copy2(env_example, env_file)
    env = ConfigParser.ConfigParser()
    env.read(env_file)
    port = env.getint('APP', 'APP_PORT')
    address = env.get('APP', 'APP_ADDRESS')
    debug = env.getboolean('APP', 'APP_DEBUG')

    # 定义默认端口
    define("port", default=port, help="run on the given port", type=int)

    # 根据配置动态加载API模块
    api_modules = env.items("API_MODULE")
    routes = []
    for module, on in api_modules:
        if on == '1':
            routes += import_api_module(module)
            print("Routes\n======\n\n" + json.dumps(
                [(url, repr(rh)) for url, rh in routes],
                indent=2)
                  )

    template_path = os.path.join(__DIR__, "templates")
    static_path = os.path.join(__DIR__, "static")
    # 服务参数设置
    app = Application(routes=routes, settings={
        'debug': debug,                              # 调试模式，产品环境设为False
        'compiled_template_cache': not debug,        # 模版缓存，产品环境设为True
        'template_path': template_path,            # 模版文件存放路径
        'static_path': static_path,                # 静态文件存放路径
        'default_handler_class': PageHandler     # 默认页面控制器
    })
    # 解析命令行参数
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app)
    # 设置服务监听端口
    http_server.listen(options.port,address=address)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
