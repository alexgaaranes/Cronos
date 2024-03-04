# Check module


def id_exists(id, db):
  if id in db["user_ids"]:
    return True
  else:
    return False


def formatTime(time):
  if time < 10:
    time = "0" + str(time)
  return time
