from functools import wraps


def update_time_stamp_label(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.ids.time_stamp_info.text = (
            f"{self.time_stamp_index}/{len(self._time_stamp)-1}"
        )
        return result

    return wrapper
