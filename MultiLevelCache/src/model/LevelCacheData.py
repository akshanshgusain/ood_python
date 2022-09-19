class LevelCacheData:
    def __init__(self, read_time: int, write_time: int):
        self.read_time: int = read_time
        self.write_time: int = write_time
