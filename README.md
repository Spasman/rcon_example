# Boring Man v2.0.0 RCON documentation & example
Here's a stupid Python 3 example for communicating with the Boring Man v2.0.0 RCON port. Python 2 might work but I haven't tested it.

I recommend you to be pretty familiar with programming and how networking works before using this guide. The set-up guide below will get you started on connecting the example to your B-Man server, but you are on your own past that point.

Below is the JSON documentation for each RCON event and RCON requests. RCON request documentation is towards the bottom of this read me.

Each RCON event and request has a number after it, defining its enum value. You're also welcome to copy paste the enum structures from this example.

### Set-up Guide

To get RCON going on your server, open the bm_server.ini file in Notepad or w/e for your server(s) and find the [Rcon] section. It should look like this first run:

```
RconEnabled="0"
RconPort="42070"
RconPassword="admin"
```

Set "RconEnabled" to "1" to enable RCON on your server. RCON has a slight impact on server performance, so don't leave it on if you're not going to use it. You can then set a password with RconPassword, which is what your app will need to send to the server to log into it's RCON feature. You can actually leave RconPassword blank and it will accept any RCON connections without needing a login, but it's not recommended, obviously.

Lastly is the RconPort value, which you can optionally change and is recommended to do so if you plan on running multiple servers utilizing RCON. You will also need to portforward this port on TCP if you plan on using RCON remotely. If your RCON app is running alongside your B-Man server on the same device (Connecting using 127.0.0.1), then port forwarding is not required.

### RCON events and their JSON data

When something happens in your Boring Man server, any RCON clients connected to it will receive an RCON event if available, which is any of the values listed below:

```
GLOBAL:
These entries are present in every RCON event.
"Time": Unix timestamp the RCON event was sent.
"EventID": The enum ID of the RCON event.

server_startup (0):
Triggers when the server starts. Although I'm not sure if it's possible to receive..
No additional JSON data.

server_shutdown (1):
Triggers when the server is shutdown.
No additional JSON data.

lobby_connect (2):
Triggers when the server connects to the server list.
No additional JSON data.

lobby_disconnect (3):
Triggers when the server loses connection to the server list.
No additional JSON data.

player_connect (4):
Triggers when a new player connects to the server.
"IP": The IP address of the connecting player.
"Store": The platform the player is using (Steam, gamejolt, etc)
"PlayerID": The player ID of the connecting player.
"Profile": The profile ID of the connected player. (Steam profile, gamejolt, etc)
"IsAdmin": Returns whether the connecting player is an admin (1) or not (0).

player_spawn (5):
Triggers when a player or NPC respawns.
"PlayerID": Returns the ID of the player who spawned.
"X": Returns the X coordinate of where the player spawned.
"Y": Returns the Y coordinate of where the player spawned.
"Hat": Returns the hat ID of the player
"Name": Returns the player's name in a string
"Color": Returns the player's character color in GML color code.
"Team": Returns what player the team is on.
"Weap1": Returns the player's primary weapon.
"Weap2": Returns the player's holstered weapon.
"Equip": Returns the player's grenade or equipment third slot item.
"OffWeap": Returns the player's "offhand" weapon when dual-wielding. Returns as 0 if they aren't dual-wielding.
"OffWeap2": Returns the player's "offhand" holstered weapon when dual-wielding with compact weapons. Returns as 0 if they aren't dual-wielding.
"EnemyType": If the player is a survival or zombrains enemy, returns their enemy ID.
"EnemyRank": If the player is a survival enemy, returns their enemy rank ID. (Outline color difficulty)

player_death (6):	
Triggers when a player dies.
"VictimID": ID of the player who was killed.
"KillerID": ID of the player who killed the victim.
"AssisterID": ID of the assisting player if there was an assist.
"KillerWeapon": The ID of the weapon that the killer used.
"Headshot": Returns whether the victim was killed by a head shot (or other critical attacks)
"DeathType": Returns the death animation of the victim, if available.
"Teamkill": Returns whether the kill was a teamkill or not. Friendly Fire mutator required.
"VictimX": Returns the X coordinate of where the victim died, if available.
"VictimY": Returns the Y coordinate of where the victim died, if available.
"KillerX": Returns the X coordinate of where the killer was when the victim died, if available.
"KillerY": Returns the Y coordinate of where the killer was when the victim died, if available.
"AssistX": Returns the X coordinate of where the assisting player was when the victim died, if available.
"AssistY": Returns the Y coordinate of where the assisting player was when the victim died, if available.

player_disconnect (7):
Triggers when a player disconnects from the server.
"IP": The IP address of the disconnecting player.
"PlayerID": The player ID of the disconnected player.
"Profile": The profile ID of the disconnected player.
"Store": The platform the player is using (Steam, gamejolt, etc)
"IsAdmin": Returns whether the disconnecting player is an admin (1) or not (0).
"Kicked": Returns whether the player was kicked or banned (1) or disconnected on their own (0).
"KickReason": Returns the kick reason string if the disconnecting player was kicked or banned.

player_team_change (8):
Triggers when a player changes team.
"PlayerID": Player ID of the player changing teams.
"OldTeam": Player's old team.
"NewTeam": Team player is changing to.
"Autobalanced": Returns whether the player was autobalanced (1) or not (0).

player_level_up (9):
Triggers when a player levels up.
"PlayerID": ID of player who leveled up.
"Level": New level of the player who leveled up.
"NewWeapon": Returns a weapon ID if the player unlocked a new weapon.
"SkinWeapon": Returns the weapon ID of the weapon skin if the player unlocked a new skin.
"SkinType": Returns the skin ID of the weapon skin if the player unlocked a new skin.

player_get_powerup (10):
Triggers when a player gets a power up
"PlayerID": ID of player who got a power up.
"PowerUp": Power up ID of the type of power up the player got.
"X": X coordinate of the player when the power up was activated.
"Y": Y coordinate of the player when the power up was activated.

player_damage (11): (DISABLED FOR NOW)
Triggers when a player takes damage.
"AttackerID": Damage dealer's player ID.
"VictimID": Damage receiver's player ID.
"Headshot": Returns whether it's headshot damage (1) or not (0).
"Damage": Amount of damage dealt in the event.

player_loaded (12):
Triggers when a player is finished loading their map.
"PlayerID": ID of player who has finished loading.

tdm_round_start (13):
Triggers when a Team Deathmatch round starts.
"Alive1": Returns how many USC players are currently alive when the round starts.
"Alive2": Returns how many THE MAN players are currently alive when the round starts.
"Players1": Returns how many USC players are currently connected when the round starts.
"Players2": Returns how many THE MAN players are currently connected when the round starts.

tdm_round_end (14):
Triggers when a Team Deathmatch round ends.
"Players1": Returns how many USC players are currently connected when the round ended.
"Players2": Returns how many THE MAN players are currently connected when the round ended.
"Winner": Returns who won the round. 0 = draw, 1 = USC, 2 = THE MAN
"Score1": Returns the current score of USC
"Score2": Returns the current score of THE MAN
"RoundEndType": Returns a value depending on how the round ended. 0 = Round time ran out, 1 = At least one team was eliminated, 2 = flag was captured
"Flawless": Returns whether the winning team had all their players alive when the round ended. Does not return "1" if there is only 1 connected player on the team.

tdm_flag_unlocked (15):
Triggers when the Team Deathmatch flag unlocks for capture.
"Alive1": Returns how many USC players are currently alive when the flag unlocks.
"Alive2": Returns how many THE MAN players are currently alive when the flag unlocks.
"Players1": Returns how many USC players are currently connected when the flag unlocks.
"Players2": Returns how many THE MAN players are currently connected when the flag unlocks.
"FlagX": Returns the X coordinate of the flag, if available.
"FlagY": Returns the Y coordinate of the flag, if available.

tdm_switch_sides (16):
Triggers when the server switches team sides in Team Deathmatch.
"Score1": Returns the updated score of USC
"Score2": Returns the updated score of THE MAN

ctf_taken (17):
Triggers when a flag in CTF is stolen.
"CarrierID": Returns the player ID of the flag carrier
"FlagTeam": Returns the team ID of the flag that has been stolen.
"WasHome": Returns whether the flag was taken from home base (1) or not (0).
"FlagX": Returns the X coordinate of the flag.
"FlagY": Returns the Y coordinate of the flag.

ctf_dropped (18):
Triggers when a flag in CTF is dropped by a flag carrier.
"CarrierID": Returns the player ID of the flag carrier
"FlagTeam": Returns the team ID of the flag that has been stolen.
"Thrown": Returns whether or not the flag was thrown purposely by the carrier.
"FlagX": Returns the X coordinate of the flag.
"FlagY": Returns the Y coordinate of the flag.

ctf_returned (19):
Triggers when a flag is returned to home base.
"ReturnPlayerID": The player ID of the flag returner, if available.
"ReturnType": Returns a value that determines how the flag was returned. 0 = Voided out of map, 1 = Returned by player, 2 = fell in lava, 3 = Timed out
"FlagX": Returns the X coordinate of the flag before it went back to home base.
"FlagY": Returns the Y coordinate of the flag before it went back to home base.

ctf_scored (20):
Triggers when a team scores a point in CTF.
"CarrierID": Returns the player ID of the scoring flag carrier.
"ScoringTeam": Returns the team ID of the scoring team.
"Score1": Returns the score for USC
"Score2": Returns the score for The Man

ctf_generator_repaired (21):
Triggers when a generator is repaired.
"ID": ID of the generator
"Team": Returns the team ID of the generator that was repaired.
"RepairerID": Returns the player ID of the player who repaired the generator, if available.

ctf_generator_destroyed (22):
Triggers when a generator is destroyed.
"ID": ID of the generator
"Team": Returns the team ID of the generator that was destroyed.
"KillerID": Returns the player ID of the player who destroyed the generator, if available.

ctf_turret_repaired (23):
Triggers when a turret is repaired.
"ID": ID of the base turret
"Team": Returns the team ID of the turret that was repaired.
"RepairerID": Returns the player ID of the player who repaired the turret, if available.

ctf_turret_destroyed (24):
Triggers when a turret is destroyed.
"ID": ID of the base turret
"Team": Returns the team ID of the turret that was destroyed.
"KillerID": Returns the player ID of the player who destroyed the turret, if available.

ctf_resupply_repaired (25):
Triggers when a resupply station is repaired.
"ID": ID of the resupply station
"Team": Returns the team ID of the resupply that was repaired.
"RepairerID": Returns the player ID of the player who repaired the resupply, if available.

ctf_resupply_destroyed (26):
Triggers when a resupply station is destroyed.
"ID": ID of the resupply station
"Team": Returns the team ID of the resupply that was destroyed.
"KillerID": Returns the player ID of the player who destroyed the resupply, if available.

match_end (27):
Triggers when the current match ends.
"WinnerText": Returns the string displayed on the scoreboard that says the winner or otherwise.
"WinnerColor": Returns the GML color code of the WinnerText string.
"WinnerID": Returns the player ID of the winner, if it's a game mode like Deathmatch. Returns -1 if not available.
"WinnerTeam": Returns the team ID that won the match if its a team-based game mode. Returns -1 if not available.
"GameModeID": Returns the ID of the currently selected game mode.
"NextMapFile": The file path for the next map being loaded.
"NextMap": The name of the next map, if found. If not, defaults to file name.
"PlayerData<ID#>": Holds additional JSON data for each player, similar when using rcon_receive.request_player command.

match_overtime (28):
Triggers when the match enters over time.
No additional JSON data.

match_start (29):
Triggers when a new match starts, does not trigger until warm up phase ends (if there is one).
"MapName": The name of the currently loaded map.
"MapFile": The file path of the currently loaded map.
"GameModeID": Returns the ID of the currently selected game mode.
"WorkshopID": Returns the Steam Workshop ID of the map, if it has one.
"MD5": Returns the MD5 hash string of the manifest bmap.txt file for the current map. It's used for checking file consistency.

survival_new_wave (30):
Triggers at the start of a new wave in Survival mode.
"WaveNumber": The current wave the Survival match is on.
"Enemies": Returns the amount of enemies needed to be defeated this wave.
"Chests": Returns the amount of chests that have spawned.
"ChestPrice": Returns the money cost of opening a chest for this wave.
"CaptureProgress": Returns the capture progress of the flag before the wave ended.
"ChestCrash": Returns whether chest prices have crashed and are cheaper.

survival_flag_unlocked (31):
Triggers when the control point flag unlocks for enemies to capture.
"WaveNumber": The current wave the Survival match is on.

survival_buy_chest (32):
Triggers when a player opens a chest.
"PlayerID": Player ID of the player who opened the chest.
"ChestID": ID of the chest that was opened.
"ChestCost": Returns the cost to open the chest, only on Survival mode.
"PlayerMoney": Returns what the buying player's money amount is after buying the chest, only on Survival mode.

log_message (33):
Triggers when a message is logged into the server console.
"Message": Returns the log message itself.
"Color": Returns the text color of the log message.

request_data (34):
Triggered when an RCON client makes a request. See below for more documentation on this RCON event.
"CaseID": The original request enum that was sent.
"RequestID": The unique ID sent in the original request that can be used for identifiying.

command_entered (35):
Triggered when a command is entered into the console.
"Command": The full string of the command that was entered.
"Source": The source of the command. 0 = In-game console window, 1 = RCON
"ReturnText": Returns the console message generated from the command.

rcon_logged_in (36):
Triggers when an RCON client successfully logs in.
"RconIP": IP address of the connected RCON client.
"RconPort": Port of the connected RCON client.
"RconSocket": TCP Socket ID of the connected RCON client.
"GameModeID": The current game mode of the server that was connected to.
"MapName": The name of the current map running on the server that was connected to.

match_paused (37):
Triggered when the server is paused.
No additional JSON data.

match_unpaused (38):
Triggered when the server is unpaused.
No additional JSON data.

warmup_start (39):
Triggered when the warm up phase has begun.
"WarmupTime": Returns how many seconds the warm up phase will last.

rcon_disconnect (40):
Triggers when an RCON client disconencts.
"RconIP": IP address of the connected RCON client.
"RconPort": Port of the connected RCON client.
"RconSocket": TCP Socket ID of the connected RCON client.

rcon_ping (41):
Triggers every 5 seconds for each connected RCON client.
No additional JSON data.

chat_message (42):
Triggers when a player sends a chat message in the Server tab.
"PlayerID": Gives the ID of the player who sent the message.
"Name": Name of the user who sent the message.
"Profile": Returns the profile ID of the sending user.
"Store": The platform the player is using (Steam, gamejolt, etc)
"Message": Returns the chat message itself.

survival_get_vice (43):
Triggers when a player collects a vice in Survival mode.
"PlayerID": The player ID of the collecting player
"ViceID": The ID of the type of vice collected
"X": The X position of where the vice was.
"Y": The Y position of where the vice was.

survival_use_vice (44):
Triggers when a player uses a consumable vice. (Rubbing Alcohol, Smokes, etc)
"PlayerID": The player ID of who used the vice.
"ViceID": The ID of the vice being consumed

survival_player_revive (45):
Triggers when a player is revived outside of a new wave starting.
"RevivingPlayerID": The player ID of the reviving player.
"SaviorPlayerID": The player ID of the player who revived the dead player. Will be the same as RevivingPlayerID if they revived themselves.
"Antacids": Will be set to "1" if the savior player used the antacids vice.
"Cost": The amount of money it cost to revive the dead player, unless they used the antacids vice then it is set to "1"

player_taunt (46):
Triggers when a player uses a emote, such as /drink or /smoke
"PlayerID": The ID of the player who emoted.
"TauntID": The ID of the emote used.

survival_complete_mission (47):
Triggered when a player completes a mission from the bar in Survival.
"PlayerID": The ID of the player.
"Reward": Returns how much money the player was rewarded.
"Type": Returns the ID of what mission was completed.

survival_take_mission (48):
Triggered when a player accepts a mission from the bar in Survival.
"PlayerID": The ID of the player.
"Reward": Returns how much money the player will be rewarded.
"Type": Returns the ID of what mission was accepted.

survival_fail_mission (49):
Triggered when a player fails or abandons a mission from the bar in Survival.
"PlayerID": The ID of the player.
"Reward": Returns how much money the player would have been rewarded.
"Type": Returns the ID of what mission was failed.
```

### PlayerData JSON

Some RCON events return sets of JSONs that contain data for specific players.
The root JSON key for these sets is named "PlayerData" following the specific player's ID (Ex. PlayerData26)

Look below on further documentation for using the request_data RCON event and the RCON requests associated with PlayerData.

```
"PlayerData#": {
  "ID": The ID of the player in the server. Also the number listed after root PlayerData key
  "Name": The name of the player.
  "Color": The character color of the player
  "Team": The ID of the team the player is on. (USC = 1, The Man = 2, Spectator = 3, Deathmatch = 0, Unknown/Not connected = -1)
  "Kills": How many kills the player currently has.
  "Deaths": How many deaths the player currently has.
  "Assists": How many assists the player currently has.
  "Score": The players current score.
  "Profile": The profile ID of the player.
  "Store": What platform the player is on. (Steam, Gamejolt, etc)
  "Alive": Returns "1" if the player is currently alive, "0" for dead
  "Bot": Returns "1" if this player is a bot. "0" for human.
  "Hat": The ID of the current hat the player is wearing.
  "Money": The current amount of money the player has in Survival or Zombrains.
  "RespawnCost": The player's respawn cost needed to revive in Survival.
  "Premium": Returns "1" if the player owns Boring Man Premium, "0" if they are F2P.
}
```

### Sending requests and processing request_data

You can send RCON requests to the server to return data such as the specific player data above. There is other information you can request as well.

To make a request, load a 16-bit signed integer and then a string after it into a packet. The integer should have one of the enums listed below to tell the B-Man server what kind of request your making.

With the string, each RCON request is different, check the list of enums below for each requirement and the expected response.

```
login (0):
Send this request when you want your app to login into the B-Man server. For the string, use the RCON password that is set in your bm_server.ini file. 
You will need to do this first before anything else. You will get a rcon_logged_in RCON event if you successfully log in. 
If you're having trouble logging in, the B-Man console window should output login error messages if the connection was made successfully.

ping (1):
Send this request periodically to keep your RCON connection alive. You should use this to respond to the rcon_ping RCON event that is sent every 5 seconds to any RCON clients from the B-Man server. 
There is no requirement as to what to put in the string, but you should put something like "1" because Game Maker sometimes can't process empty strings.

command (2):
Send this request to manually input a B-Man console command into the server. The string should contain the entire command you want to enter. (Ex. sending the string " kick "Spasman" "Cheating" " to kick the player Spasman from the server for the reason 'Cheating'). 
You should get a command_entered RCON event containing the resulting game console log message from entering the command, whether the command was successful or comes back with an error.

confirm (6):
When your B-Man server has RCON clients, it will throttle sending RCON requests every 10 ticks for each individual client. You can skip this throttle by sending back a confirm enum back to the B-Man server when your app receives an RCON event.
This is entirely OPTIONAL, and only recommended to be used if you plan to have your B-Man server connected to multiple RCON clients or if you want your app to receive RCON events slightly faster.
There is no requirement as to what to put in the string, but you should put something like "1" because Game Maker sometimes can't process empty strings.
```

The below RCON requests are special, as they need two parameters in the string to be processed succesfully. The first parameter is the "Request ID", which is something unique you can set. A random number, an incremental value or even a word, but it will always need to be a string in quotes since it will be entered into the B-Man console. The second parameter is unique to each enum request and is documented below.

When you get a successful response from making any of the requests below, it will be a "request_data" RCON event. In the JSON for the request_data event, it will contain the key "CaseID" to identify what kind of rcon request it was replying to, and "RequestID" which is something you can have your app set if you need to uniquely identify RCON request responses.

The CaseID value should be used to identify the request enum listed below for further processing, while optionally using the RequestID value to tie the response to any code you have awaiting for a reply.

For example, receiving a CaseID of "3" signals that it's a request_player request, and should have a PlayerData key stored in the JSON that contains the player info.

```
request_player (3):
Send this request to get a 'PlayerData#' JSON for the specified player (Check above for documentation on PlayerData).
The first parameter in the string should be your request ID and the second parameter should contain the name of the player OR their player ID.
You should get a request_data RCON event that contains the PlayerData# JSON you need. You won't get anything if the player wasn't found.

request_bounce (4):
You can't actually send this to the B-Man server as it won't do anything, it's just a response enum when the "rcon" command is entered into the B-Man server's console window.
The "rcon" console command lets you send any string you want to *ALL* connected and logged in rcon clients. The response itself will contain a JSON key called "String" which is the string data sent out by the "rcon" command.
I wouldn't worry about this enum unless you know what you're doing.

request_match (5):
You can send this request enum to get some current match data, such as time left and the team scores.
The first parameter in the string should be your request ID and there is no requirement for the second paramter, but you should put something like "1" because a second parameter is always required because I'm a bad programmer.
Along with "CaseID" and "RequestID", you should get additional JSON keys that return data for the current match, they are listed below.

"ServerName": The name of the server.
"GamemodeName": The name of the game mode the server is currently running.
"GamemodeID": The ID of the game mode the server is currently running.
"Map": The name of the map the server is currently running.
"Players": Returns how many players are currently connected.
"MaxPlayers": Returns the maximum amount of players allowed on the server.
"TimeLeft": Returns how many 'ticks' are left in the time.
"MaxTime": Returns the starting maximum amount of time the server is using, in 'ticks'.
"TimeStr": Returns a timestamp string of how much time is left, to make it easier on you.
"Overtime": Returns "1" if the match is currently in overtime, "0" if not.
"Version": Returns a string that contains the current version of the game the server is running.
"MaxScore": Returns the maximum score needed to win the match, if available.
"Team1Score": Returns the current score of USC, if available.
"Team2Score": Returns the current score of The Man, if available.

request_scoreboard (7):
Send this enum to get a response similar to request_match, but it also contains PlayerData nested JSONs *for every connected player in the game*.
If your server is heavily populated, this will make a HUGE JSON, so use this RCON request sparingly. Each nested PlayerData JSON will have the player's ID number after PlayerData, like mentioned above, along with some current match data that is listed below.
See above for documentation on PlayerData JSONs.

"ServerName": The name of the server.
"GamemodeName": The name of the game mode the server is currently running.
"GamemodeID": The ID of the game mode the server is currently running.
"Map": The name of the map the server is currently running.
"TimeStr": Returns a timestamp string of how much time is left, to make it easier on you.
"Team1Score": Returns the current score of USC, if available.
"Team2Score": Returns the current score of The Man, if available.

```
