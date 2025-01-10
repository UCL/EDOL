import math
from dataclasses import dataclass


def magic_transform_coorinates_to_grid(
    coordinate_value: float,
    intercept: int,
    slope: int,
    minimum_value: int,
) -> int:
    diff_from_min_lat = coordinate_value - minimum_value
    return math.ceil(intercept + slope * diff_from_min_lat)


class EdolGridCell:
    """
    The grid_cell variable is in the format xx_yy where xx indicates latitude and yy indicates longitude such that 00_00 refers
    to latitude 61 and longitude -8 and an increasew of 1 in xx represents a -0.25 change in latitude and an increase of 1 in yy
    indicates a +0.25 increase in longitude
    [Details](https://doc.ukdataservice.ac.uk/doc/8666/mrdoc/pdf/8666_serl_climate_documentation_edition07.pdf)
    """

    def __init__(self, xx: int, yy: int):
        self.xx = xx
        self.yy = yy

    def __str__(self):
        return f"{self.xx:02d}_{self.yy:02d}"

    def __repr__(self):
        return f"{self.xx:02d}_{self.yy:02d}"

    def __eq__(self, other):
        return self.xx == other.xx and self.yy == other.yy

    @staticmethod
    def from_str(grid_cell: str) -> "EdolGridCell":
        xx, yy = grid_cell.split("_")
        xx = int(xx)
        yy = int(yy)

        if xx < 0 or xx > 180:
            raise ValueError("Latitude should be between 0 and 180")

        if yy < 0 or yy > 360:
            raise ValueError("Longitude should be between 0 and 360")

        return EdolGridCell(xx, yy)

    @staticmethod
    def from_coordinates(lat: float, lon: float) -> "EdolGridCell":
        # [cdinu] - I have no idea what these values are
        # I just copied them from @cceamik (Daniel)'s original code,
        # which is itself a copy of Ed's original code
        xx = magic_transform_coorinates_to_grid(lat, 44, -4, 50)
        yy = magic_transform_coorinates_to_grid(lon, 0, 4, -8)
        return EdolGridCell(xx, yy)
