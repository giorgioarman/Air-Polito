import cherrypy
import json
from DbClass import sqliteClass

db = sqliteClass('/home/pi/Desktop/Project/IndoorDb.db')

# Creation of the class 'ResourceCatalog'
class ResourceCatalog(object):
    exposed = True

    @cherrypy.tools.accept(media='application/json')

    # Definzione funzione GET
    def GET(self, *uri, **param):

        if len(uri) == 0:
            return "you have not entered the command"
        else:
            return "the command that entered not exist"

    def POST(self, *uri, **param):

        if len(uri) == 0:
            return "you have not entered the command"
        else:
            RequestCommand = str(uri[0]).lower() #Managing of the request from other devices
            if RequestCommand == 'getdata':
                rawData = cherrypy.request.body.read(int(cherrypy.request.headers['Content-Length']))
                recievedData = json.loads(rawData)
                sensorData = recievedData['data_sensor_json']
                sensorName = recievedData['data_sensor_name']
                sensorDate = recievedData['data_date']

                cResult = db.insert("sensors_data",
                                        "data_sensor_name,data_sensor_json,data_date",
                                        "'" + str(sensorName) + "','" + str(sensorData) + "','" + str(sensorDate) + "'")
                if cResult == 0:
                    return 'status=ok'
                else:
                    return 'status=error'
            else:
                return "the command that entered not exist"


def error_page_404(status, message, traceback, version):
    return "404 Error!"


if '__main__' == __name__:
    RcPort = 8090
    RcIp= "0.0.0.0"
    confCherry = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
        }
    }
    cherrypy.tree.mount(ResourceCatalog(), '/', confCherry)
    cherrypy.config.update({"server.socket_port": int(RcPort),
                            "server.socket_host": str(RcIp)})
    cherrypy.config.update({'error_page.404': error_page_404})
    cherrypy.engine.start()
    cherrypy.engine.block()

