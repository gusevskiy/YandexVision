from datetime import datetime, timedelta, time

res = '2024-04-07T03:55:09.855960545Z'

date_time = datetime.strptime(res[:26]+'Z', '%Y-%m-%dT%H:%M:%S.%fZ')

if date_time - datetime.today() < timedelta(hours=7):
    print("Время вышло")

print(timedelta(hours=7))