from datetime import datetime
from enum import Enum
from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel


class TadoClientConfig(BaseModel):
    name: str = "tado"
    api_base_url: str
    refresh_token_url: str
    client_id: str
    client_secret: str
    authorize_url: str
    authorize_params: dict[str, str] = {
        "response_type": "code",
        "scope": "identity:read home.webhooks home.details:read home.operation:read",
    }
    access_token_url: str
    access_token_params: str | None = None

    def __hash__(self) -> int:
        return hash(str(self.model_dump()))


TadoEventType = Literal["inside-temperature", "humidity"]

TadoWebHookEventType = Literal[
    "insideTemperature", "humidity", "setting", "overlayType", "tadoMode"
]


class TadoToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"]
    expires_at: int

    def __hash__(self) -> int:
        return hash(self.access_token)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TadoToken):
            return False
        return self.access_token == other.access_token


class WebHook(BaseModel):
    id: int
    url: str
    events: List[TadoWebHookEventType]


class TemperatureUnit(str, Enum):
    CELSIUS = "CELSIUS"
    FAHRENHEIT = "FAHRENHEIT"


class IncidentDetection(BaseModel):
    supported: bool
    enabled: bool


class ConnectionState(BaseModel):
    value: bool
    timestamp: datetime


class Characteristics(BaseModel):
    capabilities: List[str]


class MountingState(BaseModel):
    value: str
    timestamp: datetime


class Device(BaseModel):
    deviceType: str
    serialNo: str
    shortSerialNo: str
    currentFwVersion: str
    connectionState: ConnectionState
    characteristics: Characteristics
    batteryState: str
    duties: List[str]
    mountingState: Optional[MountingState] = None
    mountingStateWithError: Optional[str] = None
    orientation: Optional[str] = None
    childLockEnabled: Optional[bool] = None


class DazzleMode(BaseModel):
    supported: bool
    enabled: bool


class OpenWindowDetection(BaseModel):
    supported: bool
    enabled: bool
    timeoutInSeconds: int


class HumidityType(str, Enum):
    PERCENTAGE = "PERCENTAGE"


class Humidity(BaseModel):
    type: HumidityType
    percentage: float
    timestamp: datetime


class TemperatureType(str, Enum):
    TEMPERATURE = "TEMPERATURE"


class TemperaturePrecision(BaseModel):
    celsius: float
    fahrenheit: float


class InsideTemperature(BaseModel):
    celsius: float
    fahrenheit: float
    timestamp: datetime
    type: TemperatureType
    precision: TemperaturePrecision | None = None


class SensorDataPoint(BaseModel):
    insideTemperature: InsideTemperature | None = None
    humidity: Humidity | None = None


class ZoneState(BaseModel):
    tadoMode: Literal["HOME", "AWAY"]
    preparation: dict[str, str] | None = None
    geolocationOverride: bool | None = None
    overlay: Any | None = None
    setting: Any | None = None
    openWindow: Any | None = None
    link: Any | None = None
    sensorDataPoints: SensorDataPoint | None = None


class BaseZone(BaseModel):
    id: int
    name: str
    type: Literal["HEATING", "HOT_WATER", "AIR_CONDITIONING"]


class Zone(BaseZone):
    dateCreated: datetime
    deviceTypes: List[str]
    devices: List[Device]
    reportAvailable: bool
    showScheduleSetup: bool
    supportsDazzle: bool
    dazzleEnabled: bool
    dazzleMode: DazzleMode
    openWindowDetection: OpenWindowDetection
    state: ZoneState | None = None


class BaseHome(BaseModel):
    id: int
    name: str
    dateTimeZone: str | None = None
    partner: str | None = None
    zones: List[Zone] | None = None
    webhooks: List[WebHook] | None = None


class Home(BaseHome):
    dateCreated: datetime
    temperatureUnit: TemperatureUnit
    simpleSmartScheduleEnabled: bool
    awayRadiusInMeters: Union[int, float]
    installationCompleted: bool
    incidentDetection: IncidentDetection
    generation: str
    zonesCount: int
    language: str
    skills: List[str]
    christmasModeEnabled: bool
    showAutoAssistReminders: bool
    consentGrantSkippable: bool
    enabledFeatures: List[str]
    isAirComfortEligible: bool
    isBalanceAcEligible: bool
    isEnergyIqEligible: bool
    isHeatSourceInstalled: bool
    isHeatPumpInstalled: bool
    isBalanceHpEligible: bool
    supportsFlowTemperatureOptimization: bool


class InsideTemperatureEvent(BaseModel):
    timestamp: datetime
    home: Home
    zone: Zone
    insideTemperature: InsideTemperature


class HumidityEvent(BaseModel):
    timestamp: datetime
    home: Home
    zone: Zone
    humidity: Humidity


TadoEvent = InsideTemperatureEvent | HumidityEvent


class User(BaseModel):
    name: str
    email: str
    username: str
    homes: List[BaseHome | Home]
    locale: str
