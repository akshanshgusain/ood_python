class BadRequestException(BaseException):
    pass


class LockerAlreadyExistsException(BaseException):
    pass


class NoSlotAvailableException(BaseException):
    pass


class SlotAlreadyOccupiedException(BaseException):
    pass
