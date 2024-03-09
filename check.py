# Check module

# Check if the id exists in the database
from typing import ParamSpecArgs


def id_exists(id, db):
  if id in db["user_ids"]:
    return True
  else:
    return False


# String Format Time
def formatTime(time):
  if time < 10:
    return "0" + str(time)
  else:
    return str(time)


# Format hour
def formatHour(hr):
  while hr >= 24:
    hr -= 24
  return hr


# Format minute
def formatMin(min):
  while min >= 60:
    min -= 60
  return min


# Check if valid day of the week
def checkDay(day):
  list_day = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
  if day in list_day:
    return True
  return False


# Check if valid time format
def checkTime(time):
  if 0 <= int(time.split(":")[0]) <= 23 and 0 <= int(time.split(":")[1]) <= 59:
    return True
  return False


# Sort dictionary of time
def sortTime(timeHash):
  list_time = []
  sorted_keys = []
  for key_time in timeHash:
    key_time = key_time.split(":")
    intTime = int(key_time[0] + key_time[1])
    key_time = key_time[0] + ":" + key_time[1]

    if list_time == []:
      list_time.append([key_time, intTime])
    else:
      for i in range(len(list_time)):
        if intTime < list_time[i][1]:
          list_time.insert(i, [key_time, intTime])
          break
        elif i == len(list_time) - 1:
          list_time.append([key_time, intTime])
          break

  # get keys only
  for element in list_time:
    sorted_keys.append(element[0])

  return sorted_keys
