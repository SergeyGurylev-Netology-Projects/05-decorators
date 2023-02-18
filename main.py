import datetime
import os


def logger(old_function):
    def add_log(**log_data):
        with open('main.log', 'a') as f:
            f.write(f"function name: {log_data['func_name']}\n")
            f.write(f"time start: {log_data['time_start']}\n")
            f.write(f"time end: {log_data['time_end']}\n")
            f.write(f"runtime: {log_data['time_end'] - log_data['time_start']}\n")
            f.write(f"params: {log_data['params']}\n")
            f.write(f"result: {log_data['result']}\n\n")

    def new_function(*args, **kwargs):
        time_start = datetime.datetime.now()

        result = old_function(*args, **kwargs)

        add_log(
            func_name = old_function.__name__,
            time_start = time_start,
            time_end = datetime.datetime.now(),
            params = f'{args} {kwargs}',
            result = result
        )

        return result
    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()