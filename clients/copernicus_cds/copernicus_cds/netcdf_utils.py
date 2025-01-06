import logging
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import IO

import pandas as pd
import xarray as xr
from copernicus_cds.edol_config import config as edol_config
from copernicus_cds.geo_to_grid import EdolGridCell

REQUIRED_COLUMNS = {"latitude", "longitude", "valid_time"}


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
        self.logger = logging.getLogger("NetCDFProcessor")
        if self.config.debug:
            self.log("Debug mode enabled")

    def log(self, message: str) -> None:
        if self.logger:
            self.logger.info(message)

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
                self.log(f"Files in archive: {file_list}")

                netcdf_files = [f for f in file_list if f.endswith(".nc")]
                if not netcdf_files:
                    raise ValueError("No NetCDF files found in archive")

                # Process each NC file
                for file_name in netcdf_files:
                    self.log(f"Processing {file_name}...")
                    with zip_ref.open(file_name) as nc_file:
                        df = self.netcdf_to_df(nc_file)
                        if self.dataframe is None:
                            self.dataframe = df
                        else:
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
                self.log(f"Saved combined data to {output_path}")

        except zipfile.BadZipFile:
            raise ValueError(f"Invalid or corrupted zip file: {input_path}")
        except Exception as e:
            self.log(f"Error processing zip file: {e}")
            raise e


def main():
    """Main execution function."""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)

    if len(sys.argv) != 3:
        logger.error("Usage: script.py input_file output_file")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        sys.exit(1)

    try:
        edol_processor_config = ProcessingConfig(
            output_columns=edol_config["output_columns"],
            netcdf_field_mapping=edol_config["netcdf_field_mapping"],
            grid_cells_of_interest=edol_config["grid_cells_of_interest"],
            debug=True,
        )
        processor = NetCDFProcessor(edol_processor_config)

        processor.process_zip_file(input_path, output_path)
        logger.info("Processing completed successfully")
    except Exception as e:
        logger.error(f"Error during processing: {e}")
        raise e
        sys.exit(1)


if __name__ == "__main__":
    main()
