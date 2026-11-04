"""030_GEOM_030-Polygons-Areas: see the accompanying Markdown guide."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
from example_output import display, save_plots

if __name__ == "__main__":
    # Step 2
    import geopandas as gpd
    import matplotlib.pyplot as plt
    from shapely.geometry import shape

    # Example geometry
    geom = {'type': 'Polygon', 'coordinates': [[[17.665270930775755, 59.995379244747966],
                                                [17.67062992671201, 59.99726841066224],
                                                [17.6706665367172, 59.99731246487363],
                                                [17.66865618054931, 59.998562597273036],
                                                [17.667887659980714, 59.998350223136455],
                                                [17.667531275365462, 59.99793238650041],
                                                [17.66668280978647, 59.99774021838905],
                                                [17.667259639988757, 59.99742845749122],
                                                [17.666987595091204, 59.99715474568522],
                                                [17.666593975117546, 59.99712641147649],
                                                [17.664064888468328, 59.998133391566974],
                                                [17.6637266530725, 59.99590200378276],
                                                [17.66490257827024, 59.995624959444285],
                                                [17.665270930775755, 59.995379244747966]]]}

    # Convert to a GeoDataFrame
    gdf = gpd.GeoDataFrame({'geometry': [shape(geom)]}, crs="EPSG:4326")

    # Plot
    gdf.plot()
    display(
    plt.show()
    )

    # Step 4
    from shapely.geometry import shape
    from pyproj import Transformer
    from shapely.ops import transform

    # Example geometry as a Shapely object
    polygon = shape(geom)

    # 1. Define a transformer to convert from EPSG:4326 to EPSG:3006 (UTM zone 33N)
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3006", always_xy=True)

    # 2. Reproject the geometry to UTM for accurate area calculation
    polygon_projected = transform(transformer.transform, polygon)

    # 3. Calculate the area in square meters
    area_meters = polygon_projected.area
    display(
    print(f"Area in square meters: {area_meters}")
    )

    # Step 7
    # 1. Convert to a GeoDataFrame
    gdf = gpd.GeoDataFrame({'geometry': [shape(geom)]}, crs="EPSG:4326")

    # 2. Reproject to UTM for accurate area calculation
    gdf_projected = gdf.to_crs(epsg=3006)  # Example UTM zone

    # 3. Calculate the area
    gdf_projected['area'] = gdf_projected.area
    display(
    print(gdf_projected['area'])
    )

    # Step 10
    import openeo 
    from config import user,passwd,eo_service_url

    # Connect to OpenEO
    conn = openeo.connect(eo_service_url)

    conn.authenticate_basic(username=user, password=passwd)

    # 1. Load the data
    datacube = conn.load_collection(
        collection_id = "s2_msi_l2a",
        bands=["scl"], # We may add more bands here give that they have the same resolution
        spatial_extent=geom,
        temporal_extent=["2023-06-12", "2023-06-13"]
    )
    # 2. Mask out valid pixels
    masked_datacube = datacube.mask(datacube.band("scl") != 4) # 4 represents 'vegetation'
    masked_datacube =  masked_datacube == 4 
    # 3. Calculate area using pixel count
    pixel_area = 20 * 20  # For 10m x 10m resolution
    # FIXME: disabled until OpenEO server bug has been fixed.
    #valid_pixel_count = masked_datacube.aggregate_spatial(geom, "sum").execute()
    #total_area = valid_pixel_count['data'][0][0][0] * pixel_area
    #total_area
    save_plots()
