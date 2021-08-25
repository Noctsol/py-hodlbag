import sys 
sys.path.append('.')

from library import environment


env = environment.Environment("./secret/environment.env")

env.load()

keyval_dict = {"key1":"valuer1", "key2":"value2", "key3":""}

for key in keyval_dict:
    try:
        env.add_var(key, keyval_dict[key])
        value = env.get(key)
    except Exception as e:
        print(f"Fail: {key}--{e}")
        continue

    print(f"Pass: {key}--{value}")
