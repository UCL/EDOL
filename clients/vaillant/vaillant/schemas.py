from datetime import datetime
from typing import List, Literal

from pydantic import BaseModel, RootModel


class TokenResponse(BaseModel):
    scope: List[Literal["DEVICE-READ", "DEVICE-WRITE", "DEVICE-NOTIFICATIONS-READ"]]
    client_id: str
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    expires_at: int | None = None


class TokenErrorResponse(BaseModel):
    error: str
    error_description: str

    def __str__(self):
        return f"{self.error}: {self.error_description}"


class VaillantApiException(Exception):
    def __init__(self, error_response: TokenErrorResponse):
        self.error_response = error_response
        super().__init__(str(error_response))


class ConsumptionDetail(BaseModel):
    electricity: int | None = None  # Wh
    gas: int | None = None  # Wh
    environmentalYield: int | None = None  # Wh
    generated: int | None = None  # Wh


class ConsumptionPeriod(BaseModel):
    from_: int
    to: int
    centralHeating: ConsumptionDetail | None = None
    domesticHotWater: ConsumptionDetail | None = None
    cooling: ConsumptionDetail | None = None
    solarYield: int | None = None  # Wh


class SystemComponentConsumption(BaseModel):
    systemComponentSerialNumber: str
    deviceType: str
    totalConsumption: int
    from_: int
    to: int
    consumptions: List[ConsumptionPeriod]


class ConsumptionErrorResponse(BaseModel):
    status: int | None = None
    reason: str | None = None
    incident: str | None = None
    request: str | None = None
    message: str | None = None


class Metadata(BaseModel):
    timestamp: int
    unit: str | None = None
    minimum: float | None = None
    maximum: float | None = None
    stepSize: float | None = None
    enum: List[str] | None = None


class ManualOverride(BaseModel):
    enabled: bool
    until: int | None = None
    roomTemperatureTarget: float | None = None


class DomesticHotWater(BaseModel):
    boost: ManualOverride | None = None
    temperatureTarget: float | None = None


class CentralHeating(BaseModel):
    powerOutput: int | None = None
    powerOutputMode: str | None = None
    enabled: bool | None = None
    roomTemperatureTarget: float | None = None
    useSchedule: bool | None = None
    dayProfile: dict | None = None
    nightProfile: dict | None = None
    manualOverride: ManualOverride | None = None
    awayOverride: ManualOverride | None = None
    holidayPeriod: dict | None = None


class SystemSettings(BaseModel):
    serialNumber: str
    type: str
    date: str | None = None
    time: str | None = None
    hoursTillService: int | None = None
    centralHeating: CentralHeating | None = None
    domesticHotWater: DomesticHotWater | None = None
    mode: str | None = None
    activeSchedule: str | None = None
    manualOverride: ManualOverride | None = None
    awayOverride: ManualOverride | None = None
    temperatureCorrections: dict | None = None
    _metadata: dict | None = None


class SystemSettingsResponse(RootModel):
    root: List[SystemSettings]


class Device(BaseModel):
    serialNumber: str
    type: str
    subType: str | None = None
    marketingName: str | None = None
    nomenclature: str | None = None
    articleNumber: str | None = None


class Location(BaseModel):
    busCouplerAddress: int
    ebusAddress: int


class UnidentifiedDevice(BaseModel):
    type: str
    subType: str
    location: Location


class Topology(BaseModel):
    devices: List[Device]
    unidentifiedDevices: List[UnidentifiedDevice]
    lastChangedAt: datetime
    lastDataReceivedAt: datetime
