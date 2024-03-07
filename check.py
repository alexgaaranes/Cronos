# Check module


# Check if the id exists in the database
def id_exists(id, db):
  if id in db["user_ids"]:
    return True
  else:
    return False


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
