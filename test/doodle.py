
# x = ["A", "b", "c"]

# length = len(x)
# counter = 0
# while counter < length:

#     print(counter)

#     counter+=1

# test_cases = [
#     [["y","B"],1, "test"],
#     ["https://cheese.com", "https://allurinfoismine.com"],
#     [[["y",["nested", "stuff"]]], 1, "test"],
#     [[1,2], ["my", "dog"], ["is","supercute"]]
# ]

# import datetime
# def convert(lst):
#     postgres_insert_strings = []

#     for i in lst:
#         new_value = i

#         if isinstance(i, list):
#             new_value = convert(i)
#         elif isinstance(i, str):
#             new_value = f"\"{i}\""
#         elif isinstance(i, datetime.datetime):
#             new_value = i.strftime("timestamp '%Y-%m-%d %H:%M:%S'")
#         elif isinstance(i, int):
#             new_value = str(i)
#         elif isinstance(i, float):
#             new_value = str(i)

#         postgres_insert_strings.append(new_value)

#     joined = ",".join(postgres_insert_strings)
#     pg_string = f"{{{joined}}}"

#     return pg_string

# for i in test_cases:
#     print(convert(i))

import datetime

def months(d1, d2):
    return d1.month - d2.month + 12*(d1.year - d2.year)


cos = datetime.datetime(1966, 4, 30)

ts = datetime.datetime(2021, 11, 5)

delta = ts - cos

print(months(ts, cos))