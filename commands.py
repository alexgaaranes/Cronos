# Commands module
import datetime, check, wikipedia


# WIKI
def wiki(content):
  return wikipedia.summary(content, sentences=3)


# ADD REMINDER
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


# DELETE REMINDER
def delReminder(db, id):
  del db["reminders"][id]
  return db


# CHECK REMINDER
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


# Add schedule
def addSched(db, user_id, day, time, offset, desc, channel):
  time = time.split(":")
  hour = int(time[0])  # For different time zone
  min = int(time[1])
  hour = check.formatHour(hour)
  min = check.formatMin(min)

  db["schedule"] = {
      user_id: {
          "day": day,
          "time": {
              "hour": hour,
              "min": min
          },
          "desc": desc,
          "channel": channel,
          "offset": offset
      }
  }


# Check schedule
def checkSched(db):
  now = datetime.datetime.now()
  current_hour = int(now.hour)
  current_minute = int(now.minute)
  current_day = now.strftime("%a")[0:3]

  for user_id in db["schedule"]:
    day = db["schedule"][user_id]["day"]
    time = db["schedule"][user_id]["time"]
    offset = db["schedule"][user_id]["offset"]

    if day == current_day:
      if time["hour"] == (current_hour +
                          offset) and time["min"] == current_minute:
        desc = db["schedule"][user_id]["desc"]
        channel = db["schedule"][user_id]["channel"]
        return (day, time, desc, user_id, channel, True)

  return None, None, None, None, None, False
