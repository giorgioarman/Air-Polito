import cherrypy
import json
import pandas as pd


# Creation of the class 'ResourceCatalog'
class ResourceCatalog(object): 
    exposed = True
    # Definzione funzione GET
    def GET(self, *uri, **param):
        with open("RcData.json", "r") as t: 
            tmpData = t.read()
            RcDataJson = json.loads(tmpData) #Reading and storage of datas from file 'RcData.json'

        if len(uri) == 0:
            return "you have not entered the command"
        else:
            RequestCommand = str(uri[0]).lower() #Managing of the request from other devices 
            if RequestCommand in RcDataJson:
                if RequestCommand=="devices":
                    res = RcDataJson[RequestCommand]
                    df = pd.DataFrame(res)
                    if len(uri) > 1:
                        deviceid = str(uri[1]).lower()
                        if deviceid.isdigit():
                            dfData = df.loc[df['device_id'] == int(deviceid)]
                            if len(dfData)> 0:
                                dictData = dfData.to_dict('records')
                                listData = dictData[0]
                                reqData = json.dumps(listData)
                                return reqData
                            else:
                                return "there is no data"
                        else:
                            return "device Id is not correct"
                    else:
                        return "you must enter the deviceid"
                else:
                    res = RcDataJson[RequestCommand]
                    reqData = json.dumps(res)
                    return reqData
            else:
                return "the command that entered not exist"


if '__main__' == __name__:

    with open("RcConfig.json", "r") as f:
        tmpConf = f.read()
        ResourceCatalogConfig = json.loads(tmpConf)

    RcIp = ResourceCatalogConfig["ResourseCatalogInfo"]["ip"]
    RcPort = ResourceCatalogConfig["ResourseCatalogInfo"]["port"]

    confCherry = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
        }
    }

    cherrypy.tree.mount(ResourceCatalog(), '/', confCherry)
    cherrypy.config.update({
        "server.socket_host": str(RcIp),
        "server.socket_port": int(RcPort),
    })
    cherrypy.engine.start()
    cherrypy.engine.block()

