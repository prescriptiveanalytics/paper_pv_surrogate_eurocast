from pathlib import Path


class Paths:
    project_dir = Path(__file__).parents[0]

    data_dir = project_dir.parents[0] / "data"
    results = project_dir.parents[0] / "results"

    system_data_dir = data_dir / "system_data"
    mastr_system_dir = data_dir / "open-mastr"
    pvgis_data_dir = data_dir / "pvgis"
    pvgis_outward_data_dir = data_dir / "pvgis_outward"
    pvgis_fixed_location = data_dir / "pvgis_fixed_location"

    cache_dir = data_dir / "cache"

    figure_dir = data_dir / "figures"
    extrema_dir = figure_dir / "extrema"

    model_checkpoints = data_dir / "model_checkpoints"

    @staticmethod
    def ensure_directories_exists():
        Paths.cache_dir.mkdir(parents=True, exist_ok=True)
        Paths.data_dir.mkdir(parents=True, exist_ok=True)
        Paths.system_data_dir.mkdir(parents=True, exist_ok=True)
        Paths.results.mkdir(parents=True, exist_ok=True)
        Paths.data_dir.mkdir(parents=True, exist_ok=True)
        Paths.figure_dir.mkdir(parents=True, exist_ok=True)
        Paths.extrema_dir.mkdir(parents=True, exist_ok=True)
        Paths.pvgis_data_dir.mkdir(parents=True, exist_ok=True)
        Paths.pvgis_outward_data_dir.mkdir(parents=True, exist_ok=True)
        Paths.pvgis_fixed_location.mkdir(parents=True, exist_ok=True)


class GeoData:
    natural_earth_data_url = "https://naturalearth.s3.amazonaws.com/10m_cultural/ne_10m_admin_0_countries.zip"
    natural_earth_data = Paths.cache_dir / "ne_10m_admin_0_countries.zip"


class SystemData:
    austrian_systems = Paths.system_data_dir / "pvoutput_austrian_systems.parquet"
    meta_austrian_systems = Paths.system_data_dir / "pvoutput_austrian_systems_meta.parquet"

    german_systems = Paths.system_data_dir / "pvoutput_german_systems.parquet"
    meta_german_systems = Paths.system_data_dir / "pvoutput_german_systems_meta.parquet"

    italy_systems = Paths.system_data_dir / "pvoutput_italian_systems.parquet"
    meta_italy_systems = Paths.system_data_dir / "pvoutput_italian_systems_meta.parquet"

    mastr_system_data = Paths.mastr_system_dir / "mastr-solar-2023-08-08.parquet"
    mastr_system_data_filtered = Paths.mastr_system_dir / "mastr_filtered.parquet"
    filtered_mastr_system_data = Paths.mastr_system_dir / "samples_mastr-solar-2023-08-08.parquet"

    german_system_parameter_distribution = Paths.system_data_dir / "german_total_system_parameter_distribution.parquet"
    german_enriched_train_distribution = Paths.system_data_dir / "german_enriched_train_distribution.parquet"
    german_enriched_test_distribution = Paths.system_data_dir / "german_enriched_test_distribution.parquet"
    german_starting_points = Paths.system_data_dir / "german_starting_points.parquet"
    german_outward_points = Paths.system_data_dir / "german_outward_points.parquet"


class ModulesNearsGeoshpereReport:
    near_1_km = Paths.results / "modules_near_geoshpere_1km.png"
    near_5_km = Paths.results / "modules_near_geoshpere_5km.png"
    near_10_km = Paths.results / "modules_near_geoshpere_10km.png"
    near_20_km = Paths.results / "modules_near_geoshpere_20km.png"


class Figures:
    system_locations = Paths.figure_dir / "system_locations.png"
