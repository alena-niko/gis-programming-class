from qgis.core import (
    QgsVectorLayer, 
    QgsFeature, 
    QgsGeometry, 
    QgsProject, 
    QgsField,
    QgsFields,
    QgsDataProvider,
    QgsSpatialIndex
)
from PyQt5.QtCore import QVariant

stations_layer = QgsVectorLayer('C:/Users/user/Desktop/Alena/uni/prog_2semester/gis-programming-class/stations.geojson', 'stations', 'ogr')
buffer_layer = QgsVectorLayer('Polygon?crs=EPSG:3857', 'Buffer Layer', 'memory')
buffer_provider = buffer_layer.dataProvider()

data_provider.addAttributes(stations_layer.fields())
buffered_layer.updateFields()

fields = stations_layer.fields()
buffer_provider.addAttributes(fields)
buffer_layer.updateFields()

for station_feat in stations_layer.getFeatures():
    attrs = station_feat.attributes()
    attr_dict = {field.name(): attrs[idx] for idx, field in enumerate(fields)}
    
    depth_value = attr_dict.get('depth', 1)
    try:
        depth = float(depth_value)
    except:
        depth = 0
    radius = (depth + 1) * 25
    
    geom = station_feat.geometry()
    buffer_geom = geom.buffer(radius, 8)
    
    new_feat = QgsFeature()
    new_feat.setGeometry(buffer_geom)
    new_feat.setAttributes(attrs)
    
    buffer_provider.addFeatures([new_feat])
buffer_layer.updateExtents()
QgsProject.instance().addMapLayer(buffer_layer)

districts_layer = QgsVectorLayer('C:/Users/user/Desktop/Alena/uni/prog_2semester/gis-programming-class/districts.geojson', 'Districts', 'ogr')
districts_index = QgsSpatialIndex(districts_layer.getFeatures())
found_ids = set()
for district_feat in districts_layer.getFeatures():
    district_geom = district_feat.geometry()
    
    ids = districts_index.intersects(district_geom.boundingBox())
    request = QgsFeatureRequest().setFilterFids(ids)

for feat in districts_layer.getFeatures(request):
        if feat.geometry().intersects(district_geom):
            found_ids.add(feat.id())
districts_layer.selectByIds(list(found_ids))
print(len(found_ids))