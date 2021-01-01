import io
import falcon
from julia import HEROKU_APP_NAME


class MissJuliaRobot:
    def on_get(self, req, resp):
        if not req.params:
            resp.content_type = "text/html"
            resp.status = falcon.HTTP_200
            with io.open("index.html", "rb") as f:
                resp.body = f.read()
                return

        app = HEROKU_APP_NAME
        path = "/"

        if not app:
            resp.status = falcon.HTTP_501
            return


application = falcon.API()
application.add_route("/", MissJuliaRobot())
