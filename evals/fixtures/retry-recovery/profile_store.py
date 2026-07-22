class StorageFailure(RuntimeError):
    pass


class ProfileStore:
    def __init__(self, profile, fail_on_attempts=()):
        self._profile = dict(profile)
        self._fail_on_attempts = set(fail_on_attempts)
        self.attempts = 0

    def snapshot(self):
        return dict(self._profile)

    def replace_many(self, changes):
        self.attempts += 1
        for index, (field, value) in enumerate(changes.items()):
            self._profile[field] = value
            if self.attempts in self._fail_on_attempts and index == 0:
                raise StorageFailure("storage failed after a partial write")


def update_profile(store, changes, attempts=2):
    last_error = None
    for _ in range(attempts):
        try:
            store.replace_many(changes)
            return
        except StorageFailure as error:
            last_error = error
    raise last_error
