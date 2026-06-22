class TaskNotFoundException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class NotificationNotFoundException(Exception):
    pass


class DeviceTokenNotFoundException(Exception):
    pass


class InvalidTaskActionException(Exception):
    pass


class InvalidNotificationActionException(Exception):
    pass


class FCMNotificationException(Exception):
    pass