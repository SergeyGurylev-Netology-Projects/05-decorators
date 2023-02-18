import datetime
from time import sleep


def logger(max_tries, timeout, path):
    def add_log(**log_data):
        log_data['time_end'] = datetime.datetime.now()
        with open(path, 'a') as f:
            f.write(f"function name: {log_data['func_name']}\n")
            f.write(f"time start: {log_data['time_start']}\n")
            f.write(f"time end: {log_data['time_end']}\n")
            f.write(f"runtime: {log_data['time_end'] - log_data['time_start']}\n")
            f.write(f"tries: {log_data['n_tries']}\n")
            f.write(f"params: {log_data['params']}\n")
            if log_data.get('result'):
                f.write(f"result: {log_data['result']}\n\n")
            if log_data.get('except'):
                f.write(f"except: {log_data['except']}\n\n")

    def __logger(old_function):
        n_tries = 0

        def new_function(*args, **kwargs):
            log_data = {'func_name': old_function.__name__, 'params': f'{args} {kwargs}'}

            error = None
            for i in range(max_tries):
                nonlocal n_tries
                n_tries += 1
                log_data['time_start'] = datetime.datetime.now()
                log_data['n_tries'] = n_tries
                try:
                    result = old_function(*args, **kwargs)
                    log_data['result'] = result
                    add_log(**log_data)
                    return result
                except Exception as er:
                    error = er
                    log_data['except'] = error
                    add_log(**log_data)
                    sleep(timeout)

            raise error

        return new_function
    return __logger
