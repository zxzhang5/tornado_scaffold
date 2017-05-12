# encoding: utf-8

import os.path
import json
import tornado.ioloop
import tornado.options
import tornado.httpserver

from tornado_json.routes import get_routes
from tornado_json.application import Application
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


class PageHandler(tornado.web.RequestHandler):
    def get(self):
        file_path = self.request.path;
        if file_path == "/":
            tpl = "index.html";
        elif file_path[-5:] == ".html":
            tpl = file_path.lstrip('/')
        else:
            tpl = file_path.lstrip('/') + ".html"
        template_path = os.path.join(os.path.dirname(__file__), "templates", tpl)
        if os.path.isfile(template_path):
            self.render(tpl, path=file_path)
        else:
            self.set_status(404)
            self.render("errors/404.html", path=file_path)

def main():
    import helloworld
    routes = get_routes(helloworld)
    print("Routes\n======\n\n" + json.dumps(
        [(url, repr(rh)) for url, rh in routes],
        indent=2)
    )
    template_path = os.path.join(os.path.dirname(__file__), "templates")
    static_path = os.path.join(os.path.dirname(__file__), "static")
    app = Application(routes=routes, settings={
        'debug': True,
        'compiled_template_cache': False,
        'template_path': template_path,
        'static_path': static_path,
        'default_handler_class': PageHandler
    })
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
