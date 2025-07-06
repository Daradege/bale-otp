class PbbOtpException(Exception):
    pass

class UnauthorizedException(PbbOtpException):
    pass

class BadRequest(PbbOtpException):
    pass

class InternalServerError(PbbOtpException):
    pass

class UserNotFound(PbbOtpException):
    pass

class PaymentRequired(PbbOtpException):
    pass

class PhoneFormatError(PbbOtpException):
    pass