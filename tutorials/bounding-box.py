"""bounding-box: see the accompanying Markdown guide."""
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parent)
from example_output import display, save_plots

if __name__ == "__main__":
    # Step 4
    # Convert the OpenEO Bounding Box to WKT
    bbox = {
        'east': 16.6379,  # max long
        'south': 59.5735, # min lat
        'west': 16.4677,  # min long
        'north': 59.6588, # max lat
    }
    wkt = f"POLYGON(({bbox['west']} {bbox['south']}, {bbox['west']} {bbox['north']}, {bbox['east']} {bbox['north']}, {bbox['east']} {bbox['south']}, {bbox['west']} {bbox['south']}))"

    display(
    print(wkt)
    )

    # Step 7
    import matplotlib.pyplot as plt
    from shapely.geometry import box
    import geopandas as gpd

    # Define the bounding box (using the earlier example for Västerås)
    bbox = {
        'east': 16.6379,  # max long
        'south': 59.5735, # min lat
        'west': 16.4677,  # min long
        'north': 59.6588, # max lat
    }

    # Create a Shapely box object from the bounding box coordinates
    bounding_box = box(bbox['west'], bbox['south'], bbox['east'], bbox['north'])

    # Create a GeoDataFrame to plot the box
    gdf = gpd.GeoDataFrame({"geometry": [bounding_box]}, crs="EPSG:4326")

    # Plotting
    fig, ax = plt.subplots(figsize=(8, 8))
    gdf.boundary.plot(ax=ax, linewidth=2, color="blue")
    ax.set_title("Bounding Box Visualization")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    plt.grid(True)
    display(
    plt.show()
    )

    # Step 9
    from pyproj import CRS, Transformer

    # 1. Define the bounding box in EPSG:3006
    bbox_3006 = {
        'west': 582000,  # Example coordinates for Västerås
        'south': 6600000,
        'east': 587000,
        'north': 6605000,
    }

    # 2. Create a transformer object for converting EPSG:3006 to EPSG:4326
    transformer = Transformer.from_crs(CRS.from_epsg(3006), CRS.from_epsg(4326), always_xy=True)

    # 3. Transform the coordinates
    west, south = transformer.transform(bbox_3006['west'], bbox_3006['south'])
    east, north = transformer.transform(bbox_3006['east'], bbox_3006['north'])

    # 4. Define the bounding box in WGS84
    bbox_wgs84 = {
        'west': west,
        'south': south,
        'east': east,
        'north': north,
    }

    display(
    print("Bounding Box in WGS84:", bbox_wgs84)
    )

    # Step 11
    from shapely import wkt
    from shapely.geometry import mapping
    from shapely.ops import transform
    from pyproj import CRS, Transformer

    # 1. Define a WKT polygon in EPSG:3006 (Västerås area)
    wkt_polygon_3006 = "POLYGON((582000 6600000, 582000 6605000, 587000 6605000, 587000 6600000, 582000 6600000))"

    # 2. Convert the WKT string to a Shapely geometry
    polygon_3006 = wkt.loads(wkt_polygon_3006)

    print("WKT Polygon in EPSG:3006:", wkt_polygon_3006)

    # 3. Create a transformer object for converting EPSG:3006 to EPSG:4326
    transformer = Transformer.from_crs(CRS.from_epsg(3006), CRS.from_epsg(4326), always_xy=True)

    # 4. Transform the polygon coordinates
    polygon_wgs84 = transform(transformer.transform, polygon_3006)

    # 5. Convert to GeoJSON format
    geojson_wgs84 = mapping(polygon_wgs84)

    print("GeoJSON Polygon in WGS84:", geojson_wgs84)

    # 6. Extract the bounding box from the GeoJSON
    minx, miny, maxx, maxy = polygon_wgs84.bounds

    bbox_wgs84 = {
        'west': minx,
        'south': miny,
        'east': maxx,
        'north': maxy,
    }

    display(
    print("Bounding Box in WGS84:", bbox_wgs84)
    )
    save_plots()
