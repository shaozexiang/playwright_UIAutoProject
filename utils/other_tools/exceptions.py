# python3
# -- coding: utf-8 --
"""
@Author : shao
@File : exceptions.py
"""
class MyBaseFailure(Exception):
    pass


class JsonpathExtractionFailed(MyBaseFailure):
    pass


class NotFoundError(MyBaseFailure):
    pass


class FileNotFound(FileNotFoundError, NotFoundError):
    pass


class SqlNotFound(NotFoundError):
    pass


class AssertTypeError(MyBaseFailure):
    pass


class DataAcquisitionFailed(MyBaseFailure):
    pass


class ValueTypeError(MyBaseFailure):
    pass


class SendMessageError(MyBaseFailure):
    pass


class ValueNotFoundError(MyBaseFailure):
    pass


class LocatorNotFoundError(MyBaseFailure):
    pass


class LocatorNotVisibleError(MyBaseFailure):
    pass


class RequestSendError(MyBaseFailure):
    pass
