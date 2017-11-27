# Crawler
Get data from https://map.ntu.edu.tw

# Methods

* Get the left menu on the website.

```
[POST]  https://map.ntu.edu.tw/ntu.htm?action=getDepatments
       
[Body] 
        locale:'tw'

[Response] JSON
```

* Get UID from college name.

```
[POST]  https://map.ntu.edu.tw/ntu.htm?action=getUid
       
[Body] 
        type:   <number defined in left menu>
        query:  <college name in left menu>
        locale:'tw'

[Response] JSON ({"data":[ list of UID ]})
```

* Get coordinates from UID.

```
[GET]  https://map.ntu.edu.tw/geoserver/wfs?[Params]
       
[Params] 
        service     = WFS
        version     = 1.0.0
        request     = GetFeature
        typename    = gips:ntu_building_bound
        CQL_FILTER  = uid='<UID of the building1>' or uid= ...

[Response] XML
```

* Get information from UID.

```
[POST]  https://map.ntu.edu.tw/ntu.htm
       
[Body] 
        type:   build
        uid:    uid
        id:     ext-gen1
        buildid:

[Response] JSON
```

