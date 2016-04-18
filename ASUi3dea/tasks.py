from celery import Celery

app = Celery('tasks', backend='amqp',
                      broker='amqp://Prafulla:praf1249@10.143.219.75:5672/py_env')

@app.task
def add(mode):
    return mode

@app.task
def change_state(mode):
    return success

@app.task
def adjust_voltage(new_voltage):
    return success

@app.task
def adjust_power_quality(new_quality):
    return success

@app.task
def adjust_current(new_current):
    return success

@app.task
def adjust_wattage(new_wattage):
    return success

@app.task
def pull_data(inverter_pk):
    return data

@app.task
def set_max_frequency():
    return success

@app.task
def set_min_frequency():
    return success

@app.task
def set_max_voltage():
    return success

@app.task
def set_min_voltage():
    return success

@app.task
def sanity_test():
    return data
