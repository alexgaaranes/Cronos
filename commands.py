# Commands module
import datetime, check, wikipedia


# WIKI
def wiki(content):
  return wikipedia.summary(content, sentences=3)


# ADD REMINDER
def addReminder(content, db, id, channel):
  # print(content)
  time = content.split(" ")[1]  # get raw time
  hour = int(time.split(":")[0])
  min = int(time.split(":")[1])

  # print(str(hour) + ":" + str(min))
  now = datetime.datetime.now()

  remind_hour = int(now.hour) + hour
  remind_min = int(now.minute) + min

  # print(str(remind_hour) + ":" + str(remind_min))

  remind_hour = check.formatHour(remind_hour)
  remind_min = check.formatMin(remind_min)

  # print(str(remind_hour) + ":" + str(remind_min))

  db["reminders"][str(id)] = {
      "channel": str(channel),
      "hour": remind_hour,
      "min": remind_min,
      "addedHr": hour,
      "addedMin": min
  }

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
  split_time = time.split(":")
  hour = int(split_time[0])  # For different time zone
  min = int(split_time[1])
  hour = check.formatHour(hour)
  min = check.formatMin(min)

  offset = int(offset)

  if str(user_id) not in db["schedule"][day]:  # NEW USER
    db["schedule"][day][user_id] = {
        time: {
            "hour": hour,
            "min": min,
            "offset": offset,
            "desc": desc,
            "channel": str(channel)
        }
    }
  else:  # EXISTING USER
    db["schedule"][day][str(user_id)][time] = {
        "hour": hour,
        "min": min,
        "offset": offset,
        "desc": desc,
        "channel": str(channel)
    }

  return db


# Check schedule
def checkSched(db, day, reminded):
  now = datetime.datetime.now()
  current_hour = int(now.hour)
  current_minute = int(now.minute)

  for user_id in db["schedule"][day]:
    if user_id not in reminded:
      for string_time in db["schedule"][day][user_id]:
        time = db["schedule"][day][user_id][string_time]
        offset = time["offset"]

        if time["hour"] == (current_hour +
                            offset) and time["min"] == current_minute:
          desc = time["desc"]
          channel = time["channel"]
          return (time, desc, user_id, channel, True)

  return None, None, None, None, None, False


# View Schedule
def viewSched(db_sched, user_id):
  view_str = "=====================================\n|\n"

  for day in db_sched:
    view_str += "| " + day + " -\n"

    for id in db_sched[day]:
      if str(user_id) == str(id):
        user_sched = db_sched[day][id]  # A dictionary
        sorted_time = check.sortTime(user_sched)
        for time in sorted_time:
          view_str += "|\t" + time + " - " + user_sched[time]["desc"] + "\n"

    view_str += "|------------------------------------\n"

  view_str += "|\n=====================================\n"
  return view_str


# Delete schedule
def delSched(db, user_id, day, time):
  if str(user_id) in db["schedule"][day]:
    del db["schedule"][day][str(user_id)][time]

  return db


# clear schedule
def clearSched(db, user_id):
  for day in db["schedule"]:
    if str(user_id) in db["schedule"][day]:
      del db["schedule"][day][str(user_id)]

  return db
