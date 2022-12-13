from flask import Flask, Response, request
from datetime import datetime
import json
import rest_utils
from user_playlist_resource import UserPlaylistResource
from flask_cors import CORS, cross_origin

__VERSION__ = '1.3'   # For testing

# Create the Flask application object.
app = Flask(__name__,
            static_url_path='/',
            static_folder='static/class-ui/',
            template_folder='web/templates')

CORS(app)

@app.route("/api/health", methods=["GET", "OPTIONS"])
@cross_origin()
def get_health():
    if request.method == 'OPTIONS':
        return handle_options()
    t = str(datetime.now())
    msg = {
        "name": "PlaylistAccess Microservice",
        "health": "Good",
        "at time": t,
        "version": __VERSION__
    }

    # DFF TODO Explain status codes, content type, ... ...
    result = Response(json.dumps(msg), status=200, content_type="application/json")

    return result

@app.route("/api/playlistaccess/<playlistId>/access/<userId>", methods=["GET", "OPTIONS"])
@cross_origin()
def hasAccessToPlaylist(userId, playlistId):
    if request.method == 'OPTIONS':
        return handle_options()
    request_inputs = rest_utils.RESTContext(request)

    res = UserPlaylistResource.doesUserPlaylistExist(userId, playlistId)
    rsp = Response(json.dumps(res), status=200, content_type="application/json")

    return rsp

@app.route("/api/playlistaccess/<playlistId>/add/<newUserId>", methods=["POST", "OPTIONS"])
@cross_origin()
def addUserToPlaylist(playlistId, newUserId):
    if request.method == 'OPTIONS':
        return handle_options()
    request_inputs = rest_utils.RESTContext(request)

    res = UserPlaylistResource.addUserToPlaylist(newUserId, playlistId)
    rsp = Response(json.dumps(res), status=200, content_type="application/json")

    return rsp


@app.route("/api/playlistaccess/<playlistId>/remove/<userIdToRemove>", methods=["DELETE", "OPTIONS"])
@cross_origin()
def removeUserFromPlaylist(playlistId, userIdToRemove):
    if request.method == 'OPTIONS':
        return handle_options()

    res = UserPlaylistResource.removeUserFromPlaylist(userIdToRemove, playlistId)
    rsp = Response(json.dumps(res), status=200, content_type="application/json")

    return rsp

# @app.route("/api/playlistaccess/<playlistId>/create/<userId>", methods=["POST", "OPTIONS"])
# @cross_origin()
# def createPlaylistForUser(playlistId, userId):
#     if request.method == 'OPTIONS':
#         return handle_options()
#     request_inputs = rest_utils.RESTContext(request)
#
#     res = UserPlaylistResource.createPlaylistForUser(userId, playlistId)
#     rsp = Response(json.dumps(res), status=200, content_type="application/json")
#     return rsp


@app.route("/api/playlistaccess/info", methods=["GET", "OPTIONS"])
@cross_origin()
def dbgUserPlaylist():
    if request.method == 'OPTIONS':
        return handle_options()
    request_inputs = rest_utils.RESTContext(request)

    res = UserPlaylistResource.info()
    rsp = Response(res, status=200, content_type="application/json")
    return rsp


@app.route("/api/playlistaccess/info/<userId>", methods=["GET", "OPTIONS"])
@cross_origin()
def dbgUserPlaylistForUser(userId):
    if request.method == 'OPTIONS':
        return handle_options()
    request_inputs = rest_utils.RESTContext(request)

    res = UserPlaylistResource.info(userId)
    rsp = Response(res, status=200, content_type="application/json")
    return rsp


def handle_options():
    rsp = Response("Options", status=200, content_type="application/json")
    return rsp

if __name__ == '__main__':
    # @TODO: remove the test db at some point
    # import os
    # import pymysql
    # import os
    # usr = os.environ.get("DBUSER")
    # pw = os.environ.get("DBPW")
    # h = os.environ.get("DBHOST")
    # print(usr, h)
    # conn = pymysql.connect(
    #     user=usr,
    #     password=pw,
    #     host=h,
    #     cursorclass=pymysql.cursors.DictCursor,
    #     autocommit=True
    # )
    # cursor = conn.cursor()
    # with open("test_db.sql", "r") as f:
    #     lines = f.read().split(";")[:-1]
    # for i, req in enumerate(lines):
    #     req += ";"
    #     print(req)
    #     cursor.execute(req)
    # conn.commit()

    app.run(host="0.0.0.0", port=5011)
