# https://discord.com/oauth2/authorize?client_id=1214107803283624006&permissions=133120&scope=bot
import discord, requests, json, os, datetime, check, commands, asyncio
from discord.channel import _threaded_guild_channel_factory
from discord import user
from replit import db

# CLEARING FOR TESTING ONLY
# clear database
# for i in db:
#   del db[i]

# add user_ids
# db["user_ids"] = []
# db["reminders"] = {}
# db["schedule"] = {
#     "Mon": {},
#     "Tue": {},
#     "Wed": {},
#     "Thu": {},
#     "Fri": {},
#     "Sat": {},
#     "Sun": {}
# }
# db = {"user_ids": [], "reminders": {}, "schedule": {}}

# REMINDED USER_IDS
reminded = {}


class MyClient(discord.Client):

  # RUNNING ON_START
  async def on_ready(self):
    print("Logged on as {0}".format(self.user))
    client.loop.create_task(client.check_reminder_time())
    client.loop.create_task(client.check_sched())

  # GET CHANNEL ID
  async def get_channel_id(self, guild, channel_name):
    for channel in guild.channels:
      if isinstance(channel,
                    discord.TextChannel) and channel.name == channel_name:
        return channel.id

    return None

  # CHECK REMINDER
  async def check_reminder_time(self):
    await self.wait_until_ready()
    while True:
      matched = False
      if db["reminders"] != {}:  # IF NOT EMPTY
        user_id, channel, hour, minute, matched = commands.checkReminder(db)

      if matched:
        # Get Channel
        guild = discord.utils.get(client.guilds, name=self.guilds[0].name)
        channel = await self.get_channel_id(guild, channel)
        channel = client.get_channel(channel)

        await channel.send(
            f"<@{int(user_id)}>, {hour} hour/s and {minute} minute/s has passed!"
        )
        commands.delReminder(db, user_id)

      await asyncio.sleep(10)

  # CHECK SCHEDULE
  async def check_sched(self):
    await self.wait_until_ready()

    global reminded
    temp_min = None
    while True:
      now = datetime.datetime.now()
      current_min = int(now.minute)  # Get current minute
      current_day = now.strftime("%a")[0:3]
      matched = False

      if db["schedule"] != {}:  # IF NOT EMPTY
        tup = commands.checkSched(db, current_day, reminded)
        time = tup[0]
        desc = tup[1]
        user_id = tup[2]
        channel = tup[3]
        matched = tup[4]

      if matched:
        if (user_id not in reminded):
          # Add to reminded users in the current min
          reminded[str(user_id)] = current_min
          temp_min = current_min

          # Get Channel
          guild = discord.utils.get(client.guilds, name=self.guilds[0].name)
          channel = await self.get_channel_id(guild, channel)
          channel = client.get_channel(channel)
          # Format time
          time = check.formatTime(time["hour"]) + ":" + check.formatTime(
              time["min"])
          await channel.send(f"<@{int(user_id)}>, {desc} at {time}")

      if temp_min != current_min:
        reminded = {}

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
            f"{author.mention} registered. Check commands using ``$help``")
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
          "```Command List```\n**$setup** - ``setup your account``\n\n**$remind <hours:minutes>** - ``set reminder hours:min from current time``\n\n**$addsched <day> <time> <time_zone_offset> <desc>** - ``Add a schedule on a 24-hour format time in a day of a week. Use the same command to edit an already existing schedule at the same time``\n\n**$viewsched** - ``Views the user's schedule``\n\n**$delsched <day> <time>** - ``delete a schedule on a time of a day``\n\n**$wiki <topic>** - ``show summary of the topic``\n\n**$ping** - ``show bot's latency``\n\n**$help** - ``show commands``"
      )

    # SEARCH WIKI
    if content.startswith("$wiki"):
      if check.id_exists(id, db):
        try:
          topic = content[6:]
          await channel.send(f"Searching wiki about {topic}...")
          result = commands.wiki(topic)

          await channel.send(f"```Topic: {topic} - \n{result}```")
        except:
          await channel.send("Invalid topic / Unable to find anything")
      else:
        await channel.send("You need to setup your account first.")

    # PING
    if content.startswith("$ping"):
      await channel.send(f"Tick! Tock! {round(self.latency * 1000)}ms")

    # ADD SCHEDULE
    if content.startswith("$addsched"):  # $addsched <day> <time> <desc>
      if check.id_exists(id, db):
        try:
          contents = content.split(" ")
          day = contents[1]
          time = contents[2]
          offset = int(contents[3])
          desc = " ".join(contents[4:])

          if check.checkTime(time) and check.checkDay(day):
            db = commands.addSched(db, id, day, time, offset, desc, channel)
            await channel.send(
                f"{author.mention} added a schedule.\n{day} - {time} - {desc}")
          else:
            await channel.send(
                "Invalid time format. Use ``$addsched <day> <time> <offset> <desc>``"
            )

        except:
          await channel.send(
              "Invalid time format. Use ``$addsched <day> <time> <offset> <desc>``"
          )

      else:
        await channel.send("You need to setup your account first.")

    # VIEW SCHEDULE
    if content.startswith("$viewsched"):
      if check.id_exists(id, db):
        try:
          await channel.send("Viewing your schedule...")
          view_str = commands.viewSched(db["schedule"], id)

          await channel.send(f"{author.mention}'s Schedule\n" + "```" +
                             view_str + "```")
        except:
          await channel.send(
              "An error occured while trying to view your schedule")
      else:
        await channel.send("You need to setup your account first.")

    # DELETE SCHEDULE
    if content.startswith("$delsched"):  #$delsched <day> <time>
      if check.id_exists(id, db):
        try:
          day = content.split(" ")[1]
          time = content.split(" ")[2]

          confirm_msg = await channel.send(
              "Are you sure you want to delete this schedule?")
          await confirm_msg.add_reaction("✅")
          await confirm_msg.add_reaction("❌")

          def check_reaction(reaction, user):
            return user == author and str(reaction.emoji) in [
                "✅", "❌"
            ] and reaction.message.id == confirm_msg.id

          reaction, user = await client.wait_for("reaction_add",
                                                 timeout=60.0,
                                                 check=check_reaction)

          if str(reaction.emoji) == "✅":
            try:
              db = commands.delSched(db, id, day, time)
              await channel.send(f"{author.mention} deleted a schedule.")
            except:
              await channel.send(
                  "An error occured while trying to delete your schedule")
          else:
            await channel.send("Deletion Cancelled")

        except asyncio.TimeoutError:
          await channel.send("No reaction received. Deletion cancelled.")
        # except:
        #   await channel.send(
        #       "Invalid time format. Use ``$delsched <day> <time>``")
      else:
        await channel.send("You need to setup your account first.")


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

client.run(os.getenv('TOKEN'))  # token
