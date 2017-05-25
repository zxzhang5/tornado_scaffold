# encoding: utf-8

import json
import sys
import os.path
from shutil import copy2

from helper import *
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options
from tornado_json.application import Application

# 设置系统字符编码
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path = ['modules'] + sys.path


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
        template_path = base_path("templates", tpl)
        # 模版文件存在则渲染，否则渲染404页面模版
        if os.path.isfile(template_path):
            self.render(tpl, path=file_path)
        else:
            self.set_status(404)
            if file_path[0:4] == '/api':
                self.write('{"status": "fail", "data": "The requested URL '
                           + file_path + ' was not found on this server."}')
            else:
                self.render("errors/404.html", path=file_path)


def main():
    env_file = base_path(".env")
    if not os.path.isfile(env_file):
        env_example = base_path(".env.example")
        copy2(env_example, env_file)
    env = read_env()
    port = env.getint('APP', 'APP_PORT')
    address = env.get('APP', 'APP_ADDRESS')
    debug = env.getboolean('APP', 'APP_DEBUG')

    # 定义默认端口
    define("port", default=port, help="run on the given port", type=int)

    # 根据配置动态加载API模块
    api_modules = env.items("MODULE")
    routes = []
    for module, on in api_modules:
        if on == '1':
            routes += get_module_api_routes(module)
    print(routes)
    template_path = base_path("templates")
    static_path = base_path("static")
    # 服务参数设置
    app = Application(routes=routes, settings={
        'debug': debug,                              # 调试模式，产品环境设为False
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