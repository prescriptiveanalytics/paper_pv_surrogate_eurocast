"""
This script finds good locations for PV modules in the data. 
It filters any points not within the specified country and ensures that no two points are too close to each other:
- That areas around points are within the specified country
- That areas around points do not overlap with each other
- Draws a map of the area using the points
"""

from math import radians
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
from geopy.distance import geodesic

from pv_surrogate_eurocast.constants import GeoData, Paths, SystemData


def filter_non_overlapping_points_within_country(
    natural_earth_data, country_name: str, points: gpd.GeoDataFrame, radius_km: float
):
    # Load country boundaries and project to a suitable UTM zone
    world = gpd.read_file(natural_earth_data)
    country = world[world["NAME"] == country_name]
    country = country.to_crs(epsg=32632)  # Example for Germany, adjust UTM zone as needed

    # Ensure the points GeoDataFrame is in the same CRS as the country
    old_crs = points.crs
    points = points.to_crs(epsg=32632)

    # Initialize list to keep track of valid points
    valid_points = []

    for _, point in points.iterrows():
        buffer = point.geometry.buffer(radius_km * 1000)  # Create a buffer (circle) around the point
        # Check if the buffer is fully within the country
        if not country.geometry.contains(buffer).any():
            continue  # Skip points where the buffer is not fully contained

        # Check for overlap with previously accepted buffers
        overlap = False
        for valid_point in valid_points:
            if buffer.intersects(valid_point.geometry.buffer(radius_km * 1000)):
                overlap = True
                break

        if not overlap:
            valid_points.append(point)

    # Convert valid points list to GeoDataFrame
    filtered_points_gdf = gpd.GeoDataFrame(valid_points, crs=points.crs)

    # Optionally, transform back to geographic coordinates
    filtered_points_gdf = filtered_points_gdf.to_crs(old_crs)

    return filtered_points_gdf


def generate_circular_points(point, distance_km: int) -> gpd.GeoDataFrame:
    """
    Generate 5 points distributed equally around a center point at a given distance.

    Args:
        center (Tuple[float, float]): Tuple of (latitude, longitude) for the center point.
        distance_km (float): Distance in kilometers from the center point.

    Returns:
        gpd.GeoDataFrame: A GeoDataFrame containing the generated points including bearings
    """
    lat, lon = point.geometry.y, point.geometry.x

    properties = point.to_dict()
    # delete unused property
    del properties["geometry"]

    bearings = [0, 72, 144, 216, 288]  # Bearings in degrees

    new_points = []
    for bearing in bearings:
        # Calculate the new point given the center, distance, and bearing
        radians(bearing)
        destination = geodesic(kilometers=distance_km).destination((lat, lon), bearing)
        new_points.append(
            {
                "lat": destination.latitude,
                "lon": destination.longitude,
                "bearing": bearing,
                "distance": distance_km,
                **properties,
            }
        )

    return new_points


def plot_points_on_map(
    natural_earth_data: str,
    country_name: str,
    points: gpd.GeoDataFrame,
    outward_points: gpd.GeoDataFrame,
    target_path: Path,
):
    # plotting
    _, ax = plt.subplots(figsize=(10, 10))
    ax.set_axis_off()

    world = gpd.read_file(natural_earth_data).to_crs(epsg=4326)
    country = world[world["NAME"] == country_name]
    points = points.set_crs(country.crs).to_crs(epsg=4326)
    outward_points = outward_points.set_crs(country.crs).to_crs(epsg=4326)

    country.to_crs(epsg=4326).plot(ax=ax, color="white", edgecolor="black")
    points.plot(ax=ax, color="red", marker="x", markersize=20, label="Starting Points")
    outward_points.plot(ax=ax, color="blue", marker="o", markersize=10, label="Outward Points")

    for x, y, label in zip(points.geometry.x, points.geometry.y, points.sample_id):
        ax.annotate(label, xy=(x, y), xytext=(3, 15), textcoords="offset points")

    plt.legend(frameon=False, loc="upper right")
    plt.savefig(target_path)


def calculate_points_outwards(
    starting_points: gpd.GeoDataFrame,
    max_radius_km: int,
    target_path: Path,
    initial_step_km: int = 5,
    step_size_km: int = 5,
) -> gpd.GeoDataFrame:
    new_points = []
    for _, point in starting_points.iterrows():
        for distance in range(initial_step_km, max_radius_km, step_size_km):
            new_points.extend(
                generate_circular_points(point, distance),
            )

    outward_points = gpd.GeoDataFrame.from_records(new_points)
    outward_points = gpd.GeoDataFrame(
        geometry=gpd.points_from_xy(outward_points["lon"], outward_points["lat"]), data=outward_points
    ).drop(columns=["lat", "lon"])
    outward_points.to_parquet(target_path)


def main():
    natural_earth_data = GeoData.natural_earth_data
    country_name = "Germany"
    radius_km = 65  # 65 radius results in about 10 points

    # Assuming you have a GeoDataFrame of pre-selected points
    points = gpd.read_parquet(SystemData.german_enriched_test_distribution)
    points.set_crs(epsg=4326, inplace=True)

    starting_points = filter_non_overlapping_points_within_country(natural_earth_data, country_name, points, radius_km)
    starting_points.to_parquet(SystemData.german_starting_points)

    # calculate_points_outwards(
    #     starting_points, radius_km * 2, SystemData.german_outward_points
    # )

    starting_points = gpd.read_parquet(SystemData.german_starting_points)
    outward_points = gpd.read_parquet(SystemData.german_outward_points)
    plot_points_on_map(
        natural_earth_data, country_name, starting_points, outward_points, Paths.figure_dir / "starting_points.pdf"
    )


if __name__ == "__main__":
    main()
