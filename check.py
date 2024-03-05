# Check module


def id_exists(id, db):
  if id in db["user_ids"]:
    return True
  else:
    return False


def formatHour(hr):
  while hr >= 24:
    hr -= 24
  return hr


def formatMin(min):
  while min >= 60:
    min -= 60
  return min
