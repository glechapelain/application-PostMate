import sys
import http.client
import json
import urllib.parse

if len(sys.argv)<4 or sys.argv[1]== "-h":
    print("Usage: python GeoCoding.py <HERE app-id> <ERE app-code> <Google API-key> <Address>")
else:
    q=' '.join(sys.argv[4:])
    q=urllib.parse.quote_plus(q)
    lat=None
    long=None
    
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
        print("Latitude:\t" + str(lat ))
        print("Longitude:\t"+ str(long))
    else:
        print("Cannot retreive location")

        
