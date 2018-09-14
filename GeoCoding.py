import sys
import http.client
import http.server
import json
import urllib.parse

class handler(http.server.BaseHTTPRequestHandler):
    def do_GET(req):
        q=req.path[1:]  #remove heading `/'
        q=urllib.parse.quote_plus(q)
        lat=None
        long=None
        return_value=None
        
        try:
            h=http.client.HTTPConnection("geocoder.api.here.com")
            h.request("GET","/6.2/geocode.json?app_id="+sys.argv[1]+"&app_code="+sys.argv[2]+"&searchtext="+q)
            r=h.getresponse().read()
            o=json.loads(r)
            l=o["Response"]["View"][0]["Result"][0]["Location"]["DisplayPosition"]

            lat=l["Latitude"]
            long=l["Longitude"]

        except:
            h=http.client.HTTPSConnection("maps.googleapis.com")
            h.request("GET","/maps/api/geocode/json?address="+q+"&key="+sys.argv[3])
            r=h.getresponse().read()
            o=json.loads(r)
            if o["status"]=="OK":
                results=o["results"]
                if len(results):
                    l=results[0]["geometry"]["location"]
                    lat=l["lat"]
                    long=l["lng"]

        if lat and long:
            return_value={'Latitude':lat,'Longitude':long}
        else:
            print("Cannot retreive location")
            
        req.send_response(http.HTTPStatus.OK)
        req.send_header('Content-type', 'application/json')
        req.end_headers()
        ser=json.dumps(return_value)
        req.wfile.write(ser.encode('utf-8'))
        


if len(sys.argv)<5 or sys.argv[1]== "-h":
    print("Usage: python GeoCoding.py <HERE app-id> <ERE app-code> <Google API-key> <Port>")
else:
    httpd =  http.server.HTTPServer(('',int(sys.argv[4])),handler)
    httpd.serve_forever()


