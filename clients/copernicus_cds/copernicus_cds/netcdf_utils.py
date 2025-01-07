import logging
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import IO

import pandas as pd
import xarray as xr
from copernicus_cds.geo_to_grid import EdolGridCell

REQUIRED_COLUMNS = {"latitude", "longitude", "valid_time"}

logger = logging.getLogger(__name__)


@dataclass
class ProcessingConfig:
    """Configuration for NetCDF processing."""

    output_columns: list[str] | None = None
    netcdf_field_mapping: dict[str, str] | None = None
    grid_cells_of_interest: list[str] | None = None
    debug: bool = False


class NetCDFProcessor:
    """Handles processing of NetCDF files to CSV format."""

    def __init__(self, config: ProcessingConfig = ProcessingConfig()):
        self.dataframe = None
        self.config = config

    def validate_dataset(self, ds: xr.Dataset) -> None:
        """Validate required columns in dataset."""
        missing_cols = REQUIRED_COLUMNS - set(ds.variables)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")

    def process_dataset(self, ds: xr.Dataset) -> pd.DataFrame:
        """Process xarray Dataset into pandas DataFrame."""
        # Rename columns according to mapping
        if self.config.netcdf_field_mapping:
            ds = ds.rename(
                {
                    key: self.config.netcdf_field_mapping[key]
                    for key in self.config.netcdf_field_mapping
                    if key in ds.variables
                }
            )

        # Add grid cell information
        ds["grid_cell"] = xr.apply_ufunc(
            lambda lat, lon: str(EdolGridCell.from_coordinates(lat, lon)),
            ds["latitude"],
            ds["longitude"],
            vectorize=True,
        )

        # Add analysis date and preserve original datetime
        ds["date_time"] = ds["valid_time"]
        ds["analysis_date"] = xr.apply_ufunc(
            lambda valid_time: pd.to_datetime(valid_time).date(),
            ds["valid_time"],
            vectorize=True,
        )
        df = ds.to_dataframe().reset_index()

        # filter grid cells of interest
        # i tried to do it with the ds xarray, but it crashed the process
        if self.config.grid_cells_of_interest:
            logger.debug(
                f"Filtering {len(self.config.grid_cells_of_interest)} grid cells of interest"
            )
            df = df[df["grid_cell"].isin(self.config.grid_cells_of_interest)]

        # drop columns that are not in the default output columns
        if self.config.output_columns:
            available_columns = ["valid_time"]
            available_columns.extend(
                [col for col in self.config.output_columns if col in df.columns]
            )
            df = df[available_columns]

        return df

    def netcdf_to_df(self, netcdf_fd: IO[bytes]) -> pd.DataFrame:
        """Convert NetCDF file to DataFrame."""
        with xr.open_dataset(netcdf_fd) as ds:
            self.validate_dataset(ds)
            return self.process_dataset(ds)

    def process_zip_file(self, input_path: Path, output_path: Path) -> None:
        """Process compressed NetCDF files and save to a single CSV."""
        try:
            with zipfile.ZipFile(input_path, "r") as zip_ref:
                file_list = zip_ref.namelist()
                logger.debug(f"Files in archive: {file_list}")

                netcdf_files = [f for f in file_list if f.endswith(".nc")]
                if not netcdf_files:
                    raise ValueError("No NetCDF files found in archive")

                # Process each NC file
                for file_name in netcdf_files:
                    logger.debug(f"Processing {file_name}...")
                    with zip_ref.open(file_name) as nc_file:
                        df = self.netcdf_to_df(nc_file)
                        logger.debug(
                            f"Processed {file_name}, columns: {list(df.columns)}"
                        )
                        if self.dataframe is None:
                            self.dataframe = df
                        else:
                            logger.debug(f"Merging {file_name} with existing data...")

                            # merge with suffix to avoid column name conflicts
                            self.dataframe = pd.merge(
                                self.dataframe,
                                df,
                                on=[
                                    "valid_time",
                                    "grid_cell",
                                    "analysis_date",
                                    "date_time",
                                ],
                                how="outer",
                                suffixes=("", file_name),
                            )

                # Combine all dataframes
                if self.dataframe is None:
                    raise ValueError("No data processed from NC files")

                if self.config.output_columns:
                    self.dataframe = self.dataframe[self.config.output_columns]

                self.dataframe.to_csv(output_path, index=False)
                logger.debug(f"Saved combined data to {output_path}")

        except zipfile.BadZipFile:
            raise ValueError(f"Invalid or corrupted zip file: {input_path}")
        except Exception as e:
            logger.debug(f"Error processing zip file: {e}", exc_info=True)
            raise e
