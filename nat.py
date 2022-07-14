# http://127.0.0.1:9050/api/get_lat
# mobile 18264823455

# http://127.0.0.1:9050/api/send_message
# mobile / message

# http://127.0.0.1:9050/api/get_location
# longitude / latitude

from flask import Flask, request
import json
import requests
import xmltodict
import os
import subprocess

app = Flask(__name__)

# 得到经纬度
def GetLocationLatFunction(mobile):
    return_dict = {'status': '0', 'mobile': 'none', 'localtime': '0', 'longitude': 'none', 'latitude': 'none'}

    postcontent = '<?xml version="1.0" encoding="GB2312"?>'
    postcontent += '<REQ>'
    postcontent += '<CLIENT>'
    postcontent += '<LCSCLIENTID>{}</LCSCLIENTID>'.format("")
    postcontent += '<PASSWORD>{}</PASSWORD>'.format("")
    postcontent += '</CLIENT>'
    postcontent += '<ORIGINATOR>'
    postcontent += '<ORID>{}</ORID>'.format(mobile)
    postcontent += '<ORID_TYPE></ORID_TYPE>'
    postcontent += '</ORIGINATOR>'
    postcontent += '<SERVICEID>{}</SERVICEID>'.format("")
    postcontent += '<LIR>'
    postcontent += '<ORIGUSER_ACCESSTYPE>3</ORIGUSER_ACCESSTYPE>'
    postcontent += '<FINDME_INDIC></FINDME_INDIC>'
    postcontent += '<MSIDS>'
    postcontent += '<MSID>{}</MSID>'.format(mobile)
    postcontent += '<MSID_TYPE></MSID_TYPE>'
    postcontent += '</MSIDS>'
    postcontent += '<POSREQTYPE></POSREQTYPE>'
    postcontent += '<GEO_INFO>'
    postcontent += '<COORD_SYS></COORD_SYS>'
    postcontent += '<DATUM></DATUM>'
    postcontent += '<LL_FORMAT></LL_FORMAT>'
    postcontent += '</GEO_INFO>'
    postcontent += '<PQOS>'
    postcontent += '<RESP_REQ></RESP_REQ>'
    postcontent += '<HOR_ACC></HOR_ACC>'
    postcontent += '<ALT_ACC></ALT_ACC>'
    postcontent += '</PQOS>'
    postcontent += '<PRIO>1</PRIO>'
    postcontent += '</LIR>'
    postcontent += '</REQ>'

    try:
        req = requests.get("http://127.0.0.1", data=postcontent.encode('utf-8'), headers={'Content-Type': 'text/xml'})
        xmlparse = xmltodict.parse(req.text)
        jsonstr = json.loads(json.dumps(xmlparse, indent=1))

        if jsonstr["ANS"]["LIA"]["RESULT"] == "0":
            LOCALTIME = str(jsonstr["ANS"]["LIA"]["POSINFOS"]["POSINFO"]["LOCALTIME"])
            LATITUDE = str(jsonstr["ANS"]["LIA"]["POSINFOS"]["POSINFO"]["LATITUDE"])
            LONGITUDE = str(jsonstr["ANS"]["LIA"]["POSINFOS"]["POSINFO"]["LONGITUDE"])

            return_dict['status'] = '1'
            return_dict['mobile'] = mobile
            return_dict['localtime'] = LOCALTIME
            return_dict['longitude'] = LONGITUDE
            return_dict['latitude'] = LATITUDE
            return return_dict

        else:
            return_dict['status'] = '0'
            return_dict['mobile'] = mobile
            return_dict['localtime'] = 'none'
            return_dict['longitude'] = 'none'
            return_dict['latitude'] = 'none'
            return return_dict

    except Exception:
        return_dict['status'] = '0'
        return_dict['mobile'] = mobile
        return_dict['localtime'] = 'none'
        return_dict['longitude'] = 'none'
        return_dict['latitude'] = 'none'
        return return_dict
    return_dict['status'] = '0'
    return_dict['mobile'] = mobile
    return_dict['localtime'] = 'none'
    return_dict['longitude'] = 'none'
    return_dict['latitude'] = 'none'
    return return_dict

# 得到经纬度所在城市
def get_location_latlong(longitude,latitude):
    dic = {"adcode": "None", "towncode": "None", "province": "None", "district":"None", "formatted_address": "None"}
    try:
        parameters = {'location': str(longitude) + "," + str(latitude), 'key': '**************************'}
        response = requests.get("http://restapi.amap.com/v3/geocode/regeo", parameters)
        ref_json =response.json()
        if ref_json["status"] == "1":
            dic["adcode"] = ref_json["regeocode"]["addressComponent"]["adcode"]
            dic["towncode"] = ref_json["regeocode"]["addressComponent"]["towncode"]
            dic["province"] = ref_json["regeocode"]["addressComponent"]["province"]
            dic["district"] = ref_json["regeocode"]["addressComponent"]["district"]
            dic["formatted_address"] = ref_json["regeocode"]["formatted_address"]
            return dic
        else:
            dic["adcode"] = "None"
            dic["towncode"] = "None"
            dic["province"] = "None"
            dic["district"] = "None"
            dic["formatted_address"] = "None"
            return dic
    except Exception:
        dic["adcode"] = "None"
        dic["towncode"] = "None"
        dic["province"] = "None"
        dic["district"] = "None"
        dic["formatted_address"] = "None"
        return dic
    dic["adcode"] = "None"
    dic["towncode"] = "None"
    dic["province"] = "None"
    dic["district"] = "None"
    dic["formatted_address"] = "None"
    return dic

@app.route('/api/get_lat', methods=['POST'])
def GetLat():
    if request.method == "POST":
        mobile = request.form.get("mobile")
        ref_json = GetLocationLatFunction(mobile)
        return ref_json
    return None

@app.route('/api/get_location',methods=['POST'])
def GetLocation():
    if request.method == "POST":
        longitude = request.form.get("longitude")
        latitude = request.form.get("latitude")
        ref_json = get_location_latlong(longitude,latitude)
        return ref_json
    return None

if __name__ == '__main__':
    app.run(host='127.0.0.1',port='9050',debug=False)
