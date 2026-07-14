import random
import pandas as pd


def generate_live_data():

    hours = list(range(24))

    users = []

    buffering = []

    bitrate = []

    cpu = []

    memory = []

    errors = []

    for h in hours:

        users.append(random.randint(2500,9000))

        buffering.append(round(random.uniform(0.4,3.5),2))

        bitrate.append(round(random.uniform(3.2,8.5),2))

        cpu.append(random.randint(25,95))

        memory.append(random.randint(35,92))

        errors.append(random.randint(0,35))

    return pd.DataFrame({

        "hour":hours,

        "live_users":users,

        "buffering":buffering,

        "bitrate":bitrate,

        "cpu":cpu,

        "memory":memory,

        "errors":errors

    })