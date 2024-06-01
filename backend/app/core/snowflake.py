import time

from app.config import settings


class SnowFlake:
    __instance = None

    def __new__(cls, worker_id=None, data_center_id=None):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initiated = False
        return cls.__instance

    def __init__(self, worker_id, data_center_id):
        if self.__initiated:
            return
        self.twepoch = 1705485898883
        self.worker_id_bits = 5
        self.data_center_id_bits = 5
        self.max_worker_id = -1 ^ (-1 << self.worker_id_bits)
        self.max_data_center_id = -1 ^ (-1 << self.data_center_id_bits)
        self.sequence_bits = 12
        self.worker_id_shift = self.sequence_bits
        self.data_center_id_shift = self.sequence_bits + self.worker_id_bits
        self.timestamp_left_shift = (
            self.sequence_bits + self.worker_id_bits + self.data_center_id_bits
        )
        self.sequence_mask = -1 ^ (-1 << self.sequence_bits)
        self.worker_id = worker_id
        self.data_center_id = data_center_id
        self.sequence = 0
        self.last_timestamp = -1
        self.__initiated = True

    def _gen_timestamp(self):
        return int(time.time() * 1000)

    def _til_next_millis(self, last_timestamp):
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp

    def get_id(self):
        timestamp = self._gen_timestamp()
        if timestamp < self.last_timestamp:
            raise Exception(
                "Clock moved backwards. Refusing"
                f"to generate id for {self.last_timestamp} milliseconds"
            )
        if self.last_timestamp == timestamp:
            self.sequence = (self.sequence + 1) & self.sequence_mask
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0
        self.last_timestamp = timestamp
        return (
            ((timestamp - self.twepoch) << self.timestamp_left_shift)
            | (self.data_center_id << self.data_center_id_shift)
            | (self.worker_id << self.worker_id_shift)
            | self.sequence
        )


snowflake = SnowFlake(
    settings.SNOWFLAKE_WORKER_ID,
    settings.SNOWFLAKE_DATA_CENTER_ID
)
