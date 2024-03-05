# https://discord.com/oauth2/authorize?client_id=1214107803283624006&permissions=133120&scope=bot
import discord, requests, json, os, datetime, check, commands, asyncio
from discord import user
from replit import db

# CLEARING FOR TESTING ONLY
# clear database
for i in db:
  del db[i]

# add user_ids
db = {"user_ids": [], "reminders": {}}


class MyClient(discord.Client):

  # RUNNING ON_START
  async def on_ready(self):
    print("Logged on as {0}".format(self.user))
    self.loop.create_task(self.check_reminder_time())  # (CHECK REMINDERS)

  
  # CHECK REMINDER
  async def check_reminder_time(self):
    while True:
      matched = False
      if db["reminders"] != {}:  # IF NOT EMPTY
        user_id, channel, hour, minute, matched = commands.checkReminder(db)

      if matched:
        await channel.send(
            f"<@{int(user_id)}>, {hour} hour/s and {minute} minute/s has passed!"
        )
        commands.delReminder(db, user_id)

      await asyncio.sleep(10)

  
  # DETECT MESSAGES
  async def on_message(self, message):
    global db

    if message.author == self.user:  # Don't detect itself
      return

    
    # VARIABLES
    id = message.author.id
    content = message.content
    channel = message.channel
    author = message.author

    
    # SETUP
    if content.startswith("$setup"):
      if not check.id_exists(id, db):
        db["user_ids"].append(id)  # add user to db
        await channel.send(
            f"{author.mention} account was created. Check commands using ``$help``"
        )
      else:
        await channel.send(f"{author.mention} account already exists.")

    
    # SET REMINDER
    if content.startswith("$remind"):
      if check.id_exists(id, db):  # if the  id exists
        try:
          db, hour, min = commands.addReminder(content, db, id,
                                               channel)  # update db

          await channel.send(
              f"Reminder set {hour} hour/s and {min} minute/s from now"
          )  # confirmation
        except:  # NOT SURE WHAT ERROR YET
          await channel.send("Invalid time format. Use ``$remind HH:MM``.")
      else:
        await channel.send("You need to setup your account first.")

    
    # HELP
    if content.startswith("$help"):
      await channel.send(
          "Command List\n``$setup`` - setup your account\n``$remind HH:MM`` - set reminder hours:min from current time\n``$help`` - show commands"
      )


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

client.run(os.getenv('TOKEN'))  # token
