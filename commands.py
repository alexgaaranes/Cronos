# Commands module
import datetime, check


def addReminder(content, db, id, channel):
  time = content.split(" ")[1]  # get raw time
  remind_hour = int(time.split(":")[0])
  remind_min = int(time.split(":")[1])

  db["reminders"] = {
      str(id): {
          "hour": remind_hour,
          "min": remind_min,
          "channel": channel
      }
  }

  return db, remind_hour, remind_min


def delReminder(db, id):
  del db["reminders"][id]
  return db


def checkReminder(db):
  now = datetime.datetime.now()
  current_hour = int(now.hour) + 8  # in PH only
  current_minute = int(now.minute)

  print(str(current_hour) + ":" + str(current_minute))

  for user_id in db["reminders"]:
    if db["reminders"][user_id]["hour"] == current_hour and db["reminders"][
        user_id]["min"] == current_minute:
      
      channel = db["reminders"][user_id]["channel"]

      current_hour = check.formatTime(current_hour)
      current_minute = check.formatTime(current_minute)

      return user_id, channel, current_hour, current_minute, True
  return None, None, None, None, False
