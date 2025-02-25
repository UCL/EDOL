from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SensorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    temp: _ClassVar[SensorType]
    humidity: _ClassVar[SensorType]

class Period(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    day: _ClassVar[Period]
    week: _ClassVar[Period]
    month: _ClassVar[Period]

class Commodity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    elec: _ClassVar[Commodity]
    gas: _ClassVar[Commodity]

class DataSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    cad: _ClassVar[DataSource]
    dcc: _ClassVar[DataSource]
    amr: _ClassVar[DataSource]

class Units(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    Wh: _ClassVar[Units]
    l: _ClassVar[Units]

class SensorUnits(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    degc: _ClassVar[SensorUnits]
    percent: _ClassVar[SensorUnits]

class Ambient(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    none: _ClassVar[Ambient]
    red: _ClassVar[Ambient]
    amber: _ClassVar[Ambient]
    green: _ClassVar[Ambient]
temp: SensorType
humidity: SensorType
day: Period
week: Period
month: Period
elec: Commodity
gas: Commodity
cad: DataSource
dcc: DataSource
amr: DataSource
Wh: Units
l: Units
degc: SensorUnits
percent: SensorUnits
none: Ambient
red: Ambient
amber: Ambient
green: Ambient

class Metadata(_message.Message):
    __slots__ = ("events", "message_id", "sent")
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    SENT_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[Event]
    message_id: str
    sent: int
    def __init__(self, events: _Optional[_Iterable[_Union[Event, _Mapping]]] = ..., message_id: _Optional[str] = ..., sent: _Optional[int] = ...) -> None: ...

class Event(_message.Message):
    __slots__ = ("meter_event", "power_event", "cumulative_event", "sensor_event", "status_event", "price_event", "halfhour_event", "cumulative_history_event", "one_minute_event", "tariff_event", "meter_reading_delta_event")
    METER_EVENT_FIELD_NUMBER: _ClassVar[int]
    POWER_EVENT_FIELD_NUMBER: _ClassVar[int]
    CUMULATIVE_EVENT_FIELD_NUMBER: _ClassVar[int]
    SENSOR_EVENT_FIELD_NUMBER: _ClassVar[int]
    STATUS_EVENT_FIELD_NUMBER: _ClassVar[int]
    PRICE_EVENT_FIELD_NUMBER: _ClassVar[int]
    HALFHOUR_EVENT_FIELD_NUMBER: _ClassVar[int]
    CUMULATIVE_HISTORY_EVENT_FIELD_NUMBER: _ClassVar[int]
    ONE_MINUTE_EVENT_FIELD_NUMBER: _ClassVar[int]
    TARIFF_EVENT_FIELD_NUMBER: _ClassVar[int]
    METER_READING_DELTA_EVENT_FIELD_NUMBER: _ClassVar[int]
    meter_event: MeterEvent
    power_event: PowerEvent
    cumulative_event: CumulativeEvent
    sensor_event: SensorEvent
    status_event: StatusEvent
    price_event: PriceEvent
    halfhour_event: HalfHourEvent
    cumulative_history_event: CumulativeHistoryEvent
    one_minute_event: OneMinuteEvent
    tariff_event: TariffEvent
    meter_reading_delta_event: MeterReadingDeltaEvent
    def __init__(self, meter_event: _Optional[_Union[MeterEvent, _Mapping]] = ..., power_event: _Optional[_Union[PowerEvent, _Mapping]] = ..., cumulative_event: _Optional[_Union[CumulativeEvent, _Mapping]] = ..., sensor_event: _Optional[_Union[SensorEvent, _Mapping]] = ..., status_event: _Optional[_Union[StatusEvent, _Mapping]] = ..., price_event: _Optional[_Union[PriceEvent, _Mapping]] = ..., halfhour_event: _Optional[_Union[HalfHourEvent, _Mapping]] = ..., cumulative_history_event: _Optional[_Union[CumulativeHistoryEvent, _Mapping]] = ..., one_minute_event: _Optional[_Union[OneMinuteEvent, _Mapping]] = ..., tariff_event: _Optional[_Union[TariffEvent, _Mapping]] = ..., meter_reading_delta_event: _Optional[_Union[MeterReadingDeltaEvent, _Mapping]] = ...) -> None: ...

class MeterEvent(_message.Message):
    __slots__ = ("event_id", "received", "cad_id", "commodity", "reading_timestamp", "source", "units", "reading", "event_metadata")
    class EventMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_FIELD_NUMBER: _ClassVar[int]
    CAD_ID_FIELD_NUMBER: _ClassVar[int]
    COMMODITY_FIELD_NUMBER: _ClassVar[int]
    READING_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    READING_FIELD_NUMBER: _ClassVar[int]
    EVENT_METADATA_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    received: int
    cad_id: str
    commodity: Commodity
    reading_timestamp: int
    source: DataSource
    units: Units
    reading: int
    event_metadata: _containers.ScalarMap[str, str]
    def __init__(self, event_id: _Optional[str] = ..., received: _Optional[int] = ..., cad_id: _Optional[str] = ..., commodity: _Optional[_Union[Commodity, str]] = ..., reading_timestamp: _Optional[int] = ..., source: _Optional[_Union[DataSource, str]] = ..., units: _Optional[_Union[Units, str]] = ..., reading: _Optional[int] = ..., event_metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class PowerEvent(_message.Message):
    __slots__ = ("event_id", "received", "cad_id", "commodity", "reading_timestamp", "source", "reading", "ambient", "event_metadata")
    class EventMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_FIELD_NUMBER: _ClassVar[int]
    CAD_ID_FIELD_NUMBER: _ClassVar[int]
    COMMODITY_FIELD_NUMBER: _ClassVar[int]
    READING_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    READING_FIELD_NUMBER: _ClassVar[int]
    AMBIENT_FIELD_NUMBER: _ClassVar[int]
    EVENT_METADATA_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    received: int
    cad_id: str
    commodity: Commodity
    reading_timestamp: int
    source: DataSource
    reading: int
    ambient: Ambient
    event_metadata: _containers.ScalarMap[str, str]
    def __init__(self, event_id: _Optional[str] = ..., received: _Optional[int] = ..., cad_id: _Optional[str] = ..., commodity: _Optional[_Union[Commodity, str]] = ..., reading_timestamp: _Optional[int] = ..., source: _Optional[_Union[DataSource, str]] = ..., reading: _Optional[int] = ..., ambient: _Optional[_Union[Ambient, str]] = ..., event_metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class CumulativeEvent(_message.Message):
    __slots__ = ("event_id", "cloud_received_timestamp", "cad_id", "period_start_timestamp", "meter_update_timestamp", "period", "source", "commodity", "consumption", "consumption_units", "cost", "cost_exponent", "currency", "event_metadata")
    class EventMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RECEIVED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CAD_ID_FIELD_NUMBER: _ClassVar[int]
    PERIOD_START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    METER_UPDATE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    PERIOD_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    COMMODITY_FIELD_NUMBER: _ClassVar[int]
    CONSUMPTION_FIELD_NUMBER: _ClassVar[int]
    CONSUMPTION_UNITS_FIELD_NUMBER: _ClassVar[int]
    COST_FIELD_NUMBER: _ClassVar[int]
    COST_EXPONENT_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    EVENT_METADATA_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    cloud_received_timestamp: int
    cad_id: str
    period_start_timestamp: int
    meter_update_timestamp: int
    period: Period
    source: DataSource
    commodity: Commodity
    consumption: int
    consumption_units: Units
    cost: int
    cost_exponent: int
    currency: int
    event_metadata: _containers.ScalarMap[str, str]
    def __init__(self, event_id: _Optional[str] = ..., cloud_received_timestamp: _Optional[int] = ..., cad_id: _Optional[str] = ..., period_start_timestamp: _Optional[int] = ..., meter_update_timestamp: _Optional[int] = ..., period: _Optional[_Union[Period, str]] = ..., source: _Optional[_Union[DataSource, str]] = ..., commodity: _Optional[_Union[Commodity, str]] = ..., consumption: _Optional[int] = ..., consumption_units: _Optional[_Union[Units, str]] = ..., cost: _Optional[int] = ..., cost_exponent: _Optional[int] = ..., currency: _Optional[int] = ..., event_metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class CumulativeHistoryEvent(_message.Message):
    __slots__ = ("event_id", "cloud_received_timestamp", "cad_id", "period_start_timestamp", "period", "source", "commodity", "consumption", "consumption_units", "cost", "cost_exponent", "currency", "event_metadata")
    class EventMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RECEIVED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CAD_ID_FIELD_NUMBER: _ClassVar[int]
    PERIOD_START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    PERIOD_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    COMMODITY_FIELD_NUMBER: _ClassVar[int]
    CONSUMPTION_FIELD_NUMBER: _ClassVar[int]
    CONSUMPTION_UNITS_FIELD_NUMBER: _ClassVar[int]
    COST_FIELD_NUMBER: _ClassVar[int]
    COST_EXPONENT_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    EVENT_METADATA_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    cloud_received_timestamp: int
    cad_id: str
    period_start_timestamp: int
    period: Period
    source: DataSource
    commodity: Commodity
    consumption: int
    consumption_units: Units
    cost: int
    cost_exponent: int
    currency: int
    event_metadata: _containers.ScalarMap[str, str]
    def __init__(self, event_id: _Optional[str] = ..., cloud_received_timestamp: _Optional[int] = ..., cad_id: _Optional[str] = ..., period_start_timestamp: _Optional[int] = ..., period: _Optional[_Union[Period, str]] = ..., source: _Optional[_Union[DataSource, str]] = ..., commodity: _Optional[_Union[Commodity, str]] = ..., consumption: _Optional[int] = ..., consumption_units: _Optional[_Union[Units, str]] = ..., cost: _Optional[int] = ..., cost_exponent: _Optional[int] = ..., currency: _Optional[int] = ..., event_metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class SensorEvent(_message.Message):
    __slots__ = ("event_id", "cloud_received_timestamp", "cad_id", "meter_update_timestamp", "type", "reading", "source", "units", "event_metadata")
    class EventMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RECEIVED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CAD_ID_FIELD_NUMBER: _ClassVar[int]
    METER_UPDATE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    READING_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    EVENT_METADATA_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    cloud_received_timestamp: int
    cad_id: str
    meter_update_timestamp: int
    type: SensorType
    reading: int
    source: DataSource
    units: SensorUnits
    event_metadata: _containers.ScalarMap[str, str]
    def __init__(self, event_id: _Optional[str] = ..., cloud_received_timestamp: _Optional[int] = ..., cad_id: _Optional[str] = ..., meter_update_timestamp: _Optional[int] = ..., type: _Optional[_Union[SensorType, str]] = ..., reading: _Optional[int] = ..., source: _Optional[_Union[DataSource, str]] = ..., units: _Optional[_Union[SensorUnits, str]] = ..., event_metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class StatusEvent(_message.Message):
    __slots__ = ("event_id", "cloud_received_timestamp", "feature_flags", "device_timestamp", "last_boot_timestamp", "elec_import_site_id", "gas_import_site_id", "elec_connected", "gas_connected", "han_connected", "cloud_connected", "event_metadata")
    class EventMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RECEIVED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    FEATURE_FLAGS_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LAST_BOOT_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ELEC_IMPORT_SITE_ID_FIELD_NUMBER: _ClassVar[int]
    GAS_IMPORT_SITE_ID_FIELD_NUMBER: _ClassVar[int]
    ELEC_CONNECTED_FIELD_NUMBER: _ClassVar[int]
    GAS_CONNECTED_FIELD_NUMBER: _ClassVar[int]
    HAN_CONNECTED_FIELD_NUMBER: _ClassVar[int]
    CLOUD_CONNECTED_FIELD_NUMBER: _ClassVar[int]
    EVENT_METADATA_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    cloud_received_timestamp: int
    feature_flags: int
    device_timestamp: int
    last_boot_timestamp: int
    elec_import_site_id: str
    gas_import_site_id: str
    elec_connected: bool
    gas_connected: bool
    han_connected: bool
    cloud_connected: bool
    event_metadata: _containers.ScalarMap[str, str]
    def __init__(self, event_id: _Optional[str] = ..., cloud_received_timestamp: _Optional[int] = ..., feature_flags: _Optional[int] = ..., device_timestamp: _Optional[int] = ..., last_boot_timestamp: _Optional[int] = ..., elec_import_site_id: _Optional[str] = ..., gas_import_site_id: _Optional[str] = ..., elec_connected: bool = ..., gas_connected: bool = ..., han_connected: bool = ..., cloud_connected: bool = ..., event_metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class PriceEvent(_message.Message):
    __slots__ = ("event_id", "cloud_received_timestamp", "cad_id", "rate_start", "rate_valid_until", "commodity", "source", "rate", "rate_exponent", "standing_charge_applied", "standing_charge", "standing_charge_exponent", "currency", "event_metadata")
    class EventMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RECEIVED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CAD_ID_FIELD_NUMBER: _ClassVar[int]
    RATE_START_FIELD_NUMBER: _ClassVar[int]
    RATE_VALID_UNTIL_FIELD_NUMBER: _ClassVar[int]
    COMMODITY_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    RATE_FIELD_NUMBER: _ClassVar[int]
    RATE_EXPONENT_FIELD_NUMBER: _ClassVar[int]
    STANDING_CHARGE_APPLIED_FIELD_NUMBER: _ClassVar[int]
    STANDING_CHARGE_FIELD_NUMBER: _ClassVar[int]
    STANDING_CHARGE_EXPONENT_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    EVENT_METADATA_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    cloud_received_timestamp: int
    cad_id: str
    rate_start: int
    rate_valid_until: int
    commodity: Commodity
    source: DataSource
    rate: int
    rate_exponent: int
    standing_charge_applied: str
    standing_charge: int
    standing_charge_exponent: int
    currency: int
    event_metadata: _containers.ScalarMap[str, str]
    def __init__(self, event_id: _Optional[str] = ..., cloud_received_timestamp: _Optional[int] = ..., cad_id: _Optional[str] = ..., rate_start: _Optional[int] = ..., rate_valid_until: _Optional[int] = ..., commodity: _Optional[_Union[Commodity, str]] = ..., source: _Optional[_Union[DataSource, str]] = ..., rate: _Optional[int] = ..., rate_exponent: _Optional[int] = ..., standing_charge_applied: _Optional[str] = ..., standing_charge: _Optional[int] = ..., standing_charge_exponent: _Optional[int] = ..., currency: _Optional[int] = ..., event_metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class HalfHourEvent(_message.Message):
    __slots__ = ("event_id", "cloud_received_timestamp", "device_id", "period_start_timestamp", "commodity", "source", "consumption", "units", "cost", "cost_exponent", "currency", "event_metadata")
    class EventMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RECEIVED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    PERIOD_START_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    COMMODITY_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    CONSUMPTION_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    COST_FIELD_NUMBER: _ClassVar[int]
    COST_EXPONENT_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    EVENT_METADATA_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    cloud_received_timestamp: int
    device_id: str
    period_start_timestamp: int
    commodity: Commodity
    source: DataSource
    consumption: int
    units: Units
    cost: int
    cost_exponent: int
    currency: int
    event_metadata: _containers.ScalarMap[str, str]
    def __init__(self, event_id: _Optional[str] = ..., cloud_received_timestamp: _Optional[int] = ..., device_id: _Optional[str] = ..., period_start_timestamp: _Optional[int] = ..., commodity: _Optional[_Union[Commodity, str]] = ..., source: _Optional[_Union[DataSource, str]] = ..., consumption: _Optional[int] = ..., units: _Optional[_Union[Units, str]] = ..., cost: _Optional[int] = ..., cost_exponent: _Optional[int] = ..., currency: _Optional[int] = ..., event_metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class OneMinuteEvent(_message.Message):
    __slots__ = ("event_id", "cloud_received_timestamp", "device_id", "previous_reading_timestamp", "current_reading_timestamp", "commodity", "source", "consumption", "units", "cost", "cost_exponent", "currency", "event_metadata")
    class EventMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RECEIVED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_READING_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CURRENT_READING_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    COMMODITY_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    CONSUMPTION_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    COST_FIELD_NUMBER: _ClassVar[int]
    COST_EXPONENT_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    EVENT_METADATA_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    cloud_received_timestamp: int
    device_id: str
    previous_reading_timestamp: int
    current_reading_timestamp: int
    commodity: Commodity
    source: DataSource
    consumption: int
    units: Units
    cost: int
    cost_exponent: int
    currency: int
    event_metadata: _containers.ScalarMap[str, str]
    def __init__(self, event_id: _Optional[str] = ..., cloud_received_timestamp: _Optional[int] = ..., device_id: _Optional[str] = ..., previous_reading_timestamp: _Optional[int] = ..., current_reading_timestamp: _Optional[int] = ..., commodity: _Optional[_Union[Commodity, str]] = ..., source: _Optional[_Union[DataSource, str]] = ..., consumption: _Optional[int] = ..., units: _Optional[_Union[Units, str]] = ..., cost: _Optional[int] = ..., cost_exponent: _Optional[int] = ..., currency: _Optional[int] = ..., event_metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class MeterReadingDeltaEvent(_message.Message):
    __slots__ = ("event_id", "device_id", "previous_reading_timestamp", "current_reading_timestamp", "commodity", "source", "consumption", "units", "event_metadata")
    class EventMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_READING_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CURRENT_READING_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    COMMODITY_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    CONSUMPTION_FIELD_NUMBER: _ClassVar[int]
    UNITS_FIELD_NUMBER: _ClassVar[int]
    EVENT_METADATA_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    device_id: str
    previous_reading_timestamp: int
    current_reading_timestamp: int
    commodity: Commodity
    source: DataSource
    consumption: int
    units: Units
    event_metadata: _containers.ScalarMap[str, str]
    def __init__(self, event_id: _Optional[str] = ..., device_id: _Optional[str] = ..., previous_reading_timestamp: _Optional[int] = ..., current_reading_timestamp: _Optional[int] = ..., commodity: _Optional[_Union[Commodity, str]] = ..., source: _Optional[_Union[DataSource, str]] = ..., consumption: _Optional[int] = ..., units: _Optional[_Union[Units, str]] = ..., event_metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class TariffEvent(_message.Message):
    __slots__ = ("event_id", "cloud_received_timestamp", "device_id", "source", "tariff_name", "supplier_name", "commodity", "start", "end", "currency", "price_exponent", "time_zone", "standing_charge_applied", "standing_charge", "price_bands", "time_of_use_rates", "special_days", "block_rates", "event_metadata")
    class EventMetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    CLOUD_RECEIVED_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    TARIFF_NAME_FIELD_NUMBER: _ClassVar[int]
    SUPPLIER_NAME_FIELD_NUMBER: _ClassVar[int]
    COMMODITY_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    PRICE_EXPONENT_FIELD_NUMBER: _ClassVar[int]
    TIME_ZONE_FIELD_NUMBER: _ClassVar[int]
    STANDING_CHARGE_APPLIED_FIELD_NUMBER: _ClassVar[int]
    STANDING_CHARGE_FIELD_NUMBER: _ClassVar[int]
    PRICE_BANDS_FIELD_NUMBER: _ClassVar[int]
    TIME_OF_USE_RATES_FIELD_NUMBER: _ClassVar[int]
    SPECIAL_DAYS_FIELD_NUMBER: _ClassVar[int]
    BLOCK_RATES_FIELD_NUMBER: _ClassVar[int]
    EVENT_METADATA_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    cloud_received_timestamp: int
    device_id: str
    source: DataSource
    tariff_name: str
    supplier_name: str
    commodity: Commodity
    start: int
    end: int
    currency: int
    price_exponent: int
    time_zone: str
    standing_charge_applied: str
    standing_charge: int
    price_bands: _containers.RepeatedCompositeFieldContainer[PriceBand]
    time_of_use_rates: _containers.RepeatedCompositeFieldContainer[TimeOfUseRate]
    special_days: _containers.RepeatedCompositeFieldContainer[SpecialDay]
    block_rates: _containers.RepeatedCompositeFieldContainer[BlockRate]
    event_metadata: _containers.ScalarMap[str, str]
    def __init__(self, event_id: _Optional[str] = ..., cloud_received_timestamp: _Optional[int] = ..., device_id: _Optional[str] = ..., source: _Optional[_Union[DataSource, str]] = ..., tariff_name: _Optional[str] = ..., supplier_name: _Optional[str] = ..., commodity: _Optional[_Union[Commodity, str]] = ..., start: _Optional[int] = ..., end: _Optional[int] = ..., currency: _Optional[int] = ..., price_exponent: _Optional[int] = ..., time_zone: _Optional[str] = ..., standing_charge_applied: _Optional[str] = ..., standing_charge: _Optional[int] = ..., price_bands: _Optional[_Iterable[_Union[PriceBand, _Mapping]]] = ..., time_of_use_rates: _Optional[_Iterable[_Union[TimeOfUseRate, _Mapping]]] = ..., special_days: _Optional[_Iterable[_Union[SpecialDay, _Mapping]]] = ..., block_rates: _Optional[_Iterable[_Union[BlockRate, _Mapping]]] = ..., event_metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class PriceBand(_message.Message):
    __slots__ = ("id", "name", "price")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    price: int
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., price: _Optional[int] = ...) -> None: ...

class TimeOfUseRate(_message.Message):
    __slots__ = ("price_band_id", "days", "start_time", "start_date")
    PRICE_BAND_ID_FIELD_NUMBER: _ClassVar[int]
    DAYS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    price_band_id: str
    days: _containers.RepeatedScalarFieldContainer[int]
    start_time: str
    start_date: str
    def __init__(self, price_band_id: _Optional[str] = ..., days: _Optional[_Iterable[int]] = ..., start_time: _Optional[str] = ..., start_date: _Optional[str] = ...) -> None: ...

class BlockRate(_message.Message):
    __slots__ = ("price_band_id", "days", "threshold")
    PRICE_BAND_ID_FIELD_NUMBER: _ClassVar[int]
    DAYS_FIELD_NUMBER: _ClassVar[int]
    THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    price_band_id: str
    days: _containers.RepeatedScalarFieldContainer[int]
    threshold: int
    def __init__(self, price_band_id: _Optional[str] = ..., days: _Optional[_Iterable[int]] = ..., threshold: _Optional[int] = ...) -> None: ...

class SpecialDay(_message.Message):
    __slots__ = ("day_name", "date", "day_number")
    DAY_NAME_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    DAY_NUMBER_FIELD_NUMBER: _ClassVar[int]
    day_name: str
    date: str
    day_number: int
    def __init__(self, day_name: _Optional[str] = ..., date: _Optional[str] = ..., day_number: _Optional[int] = ...) -> None: ...
