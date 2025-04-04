from osgeo import gdal
from qgis.core import QgsVectorLayer, QgsPointXY, QgsProject

path = "C:/Users/user/Desktop/Alena/uni/prog_2semester/gis-programming-class/no_crs/5.tif"
raster_data = gdal.Open(path)

arrays = []
raster_count = raster_data.RasterCount

for i in range(1, raster_count + 1):
    band = raster_data.GetRasterBand(i)
    band_array = band.ReadAsArray().astype('float32')
    arrays.append(band_array)

#создание копии исходного изображения
driver = gdal.GetDriverByName('GTiff')
output_path = "C:/Users/user/Desktop/Alena/uni/prog_2semester/raster_copy.tif"
out_raster = driver.Create(output_path, raster_data.RasterXSize, raster_data.RasterYSize, raster_count, gdal.GDT_Float32)

for i in range(raster_count):
    out_band = out_raster.GetRasterBand(i + 1)
    out_band.WriteArray(arrays[i])
    
footprint_name = 'footprint_5'
footprint_layer = QgsVectorLayer('C:/Users/user/Desktop/Alena/uni/prog_2semester/gis-programming-class/footprints/footprint_5.geojson', footprint_name, 'ogr')

#нулевой объект
feature = footprint_layer.getFeature(0)
geometry = feature.geometry().asPolygon()[0]

coords = []
for point in geometry:
    coords.append((point.x(), point.y()))

crs = footprint_layer.crs()
out_raster.SetProjection(crs.toWkt())

gcp_list = []
pixel, line = 0,0
for i in range(4):
    x, y = coords[i]
    z = 0
    if i == 0: 
        pixel = 0 
        line = 0
    elif i == 1: 
        pixel = raster_data.RasterXSize - 1 
        line = 0
    elif i == 2: 
        pixel = raster_data.RasterXSize - 1
        line = raster_data.RasterYSize - 1
    elif i == 3: 
        pixel = 0
        line = raster_data.RasterYSize - 1
    else: continue
    gcp = gdal.GCP(x, y, z, pixel, line)
    gcp_list.append(gcp)
    
out_raster.SetGCPs(gcp_list, out_raster.GetProjection())
out_raster.FlushCache()
        
