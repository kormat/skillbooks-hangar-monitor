import evelink
from google.appengine.api import memcache

from keys import keyid, vcode
from config import stationname, containername


eve = evelink.eve.EVE()
vn = evelink.corp.Corp(evelink.api.API(api_key = (keyid, vcode)))

def get_container_id():
    stationid = memcache.get("stationid")
    if(stationid is None):
        stationid = get_station_id()
        memcache.add("stationid", stationid)

    assets = vn.assets().result[stationid]["contents"][0]["contents"]
    # containers are in station -> content -> office -> contents
    ids = []
    for asset in assets:
        # to check if an asset is a container which we can access,
        # we simply check if it has contents
        if "contents" in asset:
            ids.append(asset["id"])


    # and then we go through the Locations to find the right one
    locs = vn.locations(ids).result
    for id, loc in locs.iteritems():
        if loc['name'] == containername:
            return id

def get_station_id():
    stations = eve.conquerable_stations().result
    for idstation, station in stations.iteritems():
        if station["name"] == stationname:
            return idstation+6000000
