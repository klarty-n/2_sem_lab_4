class TaskValidationError(Exception):
    pass

class IdError(TaskValidationError):
    pass

class PriorityError(TaskValidationError):
    pass

class StatusError(TaskValidationError):
    pass

class PayloadError(TaskValidationError):
    pass

class StatusTransitionError(TaskValidationError):
    pass