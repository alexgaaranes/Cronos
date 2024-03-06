# Commands module
import datetime, check, wikipedia


def wiki(content):
  return wikipedia.summary(content, sentences=3)


def addReminder(content, db, id, channel):
  time = content.split(" ")[1]  # get raw time
  hour = int(time.split(":")[0])
  min = int(time.split(":")[1])

  now = datetime.datetime.now()

  remind_hour = int(now.hour) + hour
  remind_min = int(now.minute) + min

  remind_hour = check.formatHour(remind_hour)
  remind_min = check.formatMin(remind_min)

  db["reminders"] = {
      str(id): {
          "hour": remind_hour,
          "min": remind_min,
          "channel": channel,
          "addedHr": hour,
          "addedMin": min
      }
  }

  #print(db)

  return db, hour, min


def delReminder(db, id):
  del db["reminders"][id]
  return db


def checkReminder(db):
  now = datetime.datetime.now()
  current_hour = int(now.hour)
  current_minute = int(now.minute)

  for user_id in db["reminders"]:
    remind_hour = db["reminders"][user_id]["hour"]
    remind_minute = db["reminders"][user_id]["min"]
    if remind_hour == current_hour and remind_minute == current_minute:

      channel = db["reminders"][user_id]["channel"]

      return user_id, channel, db["reminders"][user_id]["addedHr"], db[
          "reminders"][user_id]["addedMin"], True
  return None, None, None, None, False
