class CharacterCriticalError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'CharacterCriticalError, {0} '.format(self.message)
        else:
            return 'CharacterCriticalError has been raised'


class JobError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return 'JobRetryError, {0} '.format(self.message)
        else:
            return 'JobRetryError has been raised'


class LoginError(Exception):
    pass


class RetryError(Exception):
    pass
