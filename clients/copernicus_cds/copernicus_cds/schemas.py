from typing import List, Literal, get_args

"""
Type for a default variable to request from the CDS API.
"""
Default_CDS_Request_Variable = Literal[
    "mean_total_precipitation_rate",
    "precipitation_type",
    "surface_pressure",
    "surface_solar_radiation_downwards",
    "total_cloud_cover",
    "10m_wind_gust_since_previous_post_processing",
    "2m_dewpoint_temperature",
    "2m_temperature",
    "clear_sky_direct_solar_radiation_at_surface",
    "instantaneous_10m_wind_gust",
    "large_scale_snowfall_rate_water_equivalent",
    "maximum_2m_temperature_since_previous_post_processing",
    "snow_depth",
    "snowfall",
    "soil_temperature_level_1",
    "total_precipitation",
    "total_sky_direct_solar_radiation_at_surface",
    "large_scale_rain_rate",
    "large_scale_precipitation",
    "mean_sea_level_pressure",
    "minimum_2m_temperature_since_previous_post_processing",
    "skin_temperature",
    "10m_u_component_of_wind",
    "10m_v_component_of_wind",
]

"""
Type for a list of default variables to request from the CDS API.
"""
Default_CDS_Request_Variable_List = List[Default_CDS_Request_Variable]

"""
The list of default variables to request from the CDS API.
"""
Default_CDS_Request_Variables = list(get_args(Default_CDS_Request_Variable))
