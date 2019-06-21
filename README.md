# rcon_example
Here's a stupid Python 3 example for communicating with the Boring Man v2.0.0 RCON port.

Below is the JSON documentation for each RCON event.
Documentation for request events will come later

```
GLOBAL:
These entries are present in every RCON event.
"Time": Unix timestamp the RCON event was sent.
"EventID": The enum ID of the RCON event.

server_startup:
Triggers when the server start.
No additional JSON data.

server_shutdown:
Triggers when the server start.
No additional JSON data.

chat_message:
Triggers when a player sends a chat message in the Server tab.
"Name": Name of the user who sent the message.
"Profile": Returns the profile ID of the sending user. (Steam, Gamejolt, etc)
"Message": Returns the chat message itself.

log_message:
Triggers when a message is logged into the server console.
"Message": Returns the log message itself.
"Color": Returns the text color of the log message.

rcon_logged_in:
Triggers when an RCON client successfully logs in.
"RconIP": IP address of the connected RCON client.
"RconPort": Port of the connected RCON client.
"RconSocket": TCP Socket ID of the connected RCON client.

rcon_disconnect:
Triggers when an RCON client disconencts.
"RconIP": IP address of the connected RCON client.
"RconPort": Port of the connected RCON client.
"RconSocket": TCP Socket ID of the connected RCON client.

rcon_ping:
Triggers every 5 seconds for each connected RCON client.
No additional JSON data.

lobby_connect:
Triggers when the server connects to the server list.
No additional JSON data.

lobby_disconnect:
Triggers when the server loses connection to the server list.
No additional JSON data.

player_team_change:
Triggers when a player changes team.
"PlayerID": Player ID of the player changing teams.
"OldTeam": Player's old team.
"NewTeam": Team player is changing to.
"Autobalanced": Returns whether the player was autobalanced (1) or not (0).

player_damage: (DISABLED FOR NOW)
Triggers when a player takes damage.
"AttackerID": Damage dealer's player ID.
"VictimID": Damage receiver's player ID.
"Headshot": Returns whether it's headshot damage (1) or not (0).
"Damage": Amount of damage dealt in the event.

player_loaded:
Triggers when a player is finished loading their map.
"PlayerID": ID of player who has finished loading.

player_level_up:
Triggers when a player levels up.
"PlayerID": ID of player who leveled up.
"Level": New level of the player who leveled up.
"NewWeapon": Returns a weapon ID if the player unlocked a new weapon.
"SkinWeapon": Returns the weapon ID of the weapon skin if the player unlocked a new skin.
"SkinType": Returns the skin ID of the weapon skin if the player unlocked a new skin.

player_get_powerup:
Triggers when a player gets a power up
"PlayerID": ID of player who got a power up.
"PowerUp": Power up ID of the type of power up the player got.
"X": X coordinate of the player when the power up was activated.
"Y": Y coordinate of the player when the power up was activated.

player_taunt:
Triggers when a player uses a emote, such as /drink or /smoke
"PlayerID": The ID of the player who emoted.
"TauntID": The ID of the emote used.

player_spawn:
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

player_death:	
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

tdm_round_start:
Triggers when a Team Deathmatch round starts.
"Alive1": Returns how many USC players are currently alive when the round starts.
"Alive2": Returns how many THE MAN players are currently alive when the round starts.
"Players1": Returns how many USC players are currently connected when the round starts.
"Players2": Returns how many THE MAN players are currently connected when the round starts.

tdm_flag_unlocked:
Triggers when the Team Deathmatch flag unlocks for capture.
"Alive1": Returns how many USC players are currently alive when the flag unlocks.
"Alive2": Returns how many THE MAN players are currently alive when the flag unlocks.
"Players1": Returns how many USC players are currently connected when the flag unlocks.
"Players2": Returns how many THE MAN players are currently connected when the flag unlocks.
"FlagX": Returns the X coordinate of the flag, if available.
"FlagY": Returns the Y coordinate of the flag, if available.

tdm_round_end:
Triggers when a Team Deathmatch round ends.
"Players1": Returns how many USC players are currently connected when the round ended.
"Players2": Returns how many THE MAN players are currently connected when the round ended.
"Winner": Returns who won the round. 0 = draw, 1 = USC, 2 = THE MAN
"Score1": Returns the current score of USC
"Score2": Returns the current score of THE MAN
"RoundEndType": Returns a value depending on how the round ended. 0 = Round time ran out, 1 = At least one team was eliminated, 2 = flag was captured
"Flawless": Returns whether the winning team had all their players alive when the round ended. Does not return "1" if there is only 1 connected player on the team.

player_connect:
Triggers when a new player connects to the server.
"IP": The IP address of the connecting player.
"Port": The port of the connecting player.
"PlayerID": The player ID of the connecting player.
"Profile": The profile ID of the connected player. (Steam profile, gamejolt, etc)
"IsAdmin": Returns whether the connecting player is an admin (1) or not (0).

player_disconnect:
Triggers when a player disconnects from the server.
"IP": The IP address of the disconnecting player.
"Port": The port of the disconnecting player.
"PlayerID": The player ID of the disconnected player.
"Profile": The profile ID of the disconnected player. (Steam profile, gamejolt, etc)
"IsAdmin": Returns whether the disconnecting player is an admin (1) or not (0).
"Kicked": Returns whether the player was kicked or banned (1) or disconnected on their own (0).
"KickReason": Returns the kick reason string if the disconnecting player was kicked or banned.

tdm_switch_sides:
Triggers when the server switches team sides in Team Deathmatch.
"Score1": Returns the updated score of USC
"Score2": Returns the updated score of THE MAN

ctf_taken:
Triggers when a flag in CTF is stolen.
"CarrierID": Returns the player ID of the flag carrier
"FlagTeam": Returns the team ID of the flag that has been stolen.
"WasHome": Returns whether the flag was taken from home base (1) or not (0).
"FlagX": Returns the X coordinate of the flag.
"FlagY": Returns the Y coordinate of the flag.

ctf_dropped:
Triggers when a flag in CTF is dropped by a flag carrier.
"CarrierID": Returns the player ID of the flag carrier
"FlagTeam": Returns the team ID of the flag that has been stolen.
"Thrown": Returns whether or not the flag was thrown purposely by the carrier.
"FlagX": Returns the X coordinate of the flag.
"FlagY": Returns the Y coordinate of the flag.

ctf_returned:
Triggers when a flag is returned to home base.
"ReturnPlayerID": The player ID of the flag returner, if available.
"ReturnType": Returns a value that determines how the flag was returned. 0 = Voided out of map, 1 = Returned by player, 2 = fell in lava, 3 = Timed out
"FlagX": Returns the X coordinate of the flag before it went back to home base.
"FlagY": Returns the Y coordinate of the flag before it went back to home base.

ctf_scored:
Triggers when a team scores a point in CTF.
"CarrierID": Returns the player ID of the scoring flag carrier.
"ScoringTeam": Returns the team ID of the scoring team.
"Score1": Returns the score for USC
"Score2": Returns the score for The Man

ctf_generator_destroyed:
Triggers when a generator is destroyed.
"ID": ID of the generator
"Team": Returns the team ID of the generator that was destroyed.
"KillerID": Returns the player ID of the player who destroyed the generator, if available.

ctf_resupply_destroyed:
Triggers when a resupply station is destroyed.
"ID": ID of the resupply station
"Team": Returns the team ID of the resupply that was destroyed.
"KillerID": Returns the player ID of the player who destroyed the resupply, if available.

ctf_turret_destroyed:
Triggers when a turret is destroyed.
"ID": ID of the base turret
"Team": Returns the team ID of the turret that was destroyed.
"KillerID": Returns the player ID of the player who destroyed the turret, if available.

ctf_generator_repaired:
Triggers when a generator is repaired.
"ID": ID of the generator
"Team": Returns the team ID of the generator that was repaired.
"RepairerID": Returns the player ID of the player who repaired the generator, if available.

ctf_resupply_repaired:
Triggers when a resupply station is repaired.
"ID": ID of the resupply station
"Team": Returns the team ID of the resupply that was repaired.
"RepairerID": Returns the player ID of the player who repaired the resupply, if available.

ctf_turret_repaired:
Triggers when a turret is repaired.
"ID": ID of the base turret
"Team": Returns the team ID of the turret that was repaired.
"RepairerID": Returns the player ID of the player who repaired the turret, if available.

match_start:
Triggers when a new match starts, does not trigger until warm up phase ends (if there is one).
"MapName": The name of the currently loaded map.
"MapFile": The file path of the currently loaded map.
"GameModeID": Returns the ID of the currently selected game mode.
"WorkshopID": Returns the Steam Workshop ID of the map, if it has one.

match_end:
Triggers when the current match ends.
"WinnerText": Returns the string displayed on the scoreboard that says the winner or otherwise.
"WinnerColor": Returns the GML color code of the WinnerText string.
"WinnerID": Returns the player ID of the winner, if it's a game mode like Deathmatch. Returns -1 if not available.
"WinnerTeam": Returns the team ID that won the match if its a team-based game mode. Returns -1 if not available.
"NextMapFile": The file path for the next map being loaded.
"NextMap": The name of the next map, if found. If not, defaults to file name.
"PlayerData<ID#>": Holds additional JSON data for each player, similar when using rcon_receive.request_player command.

match_overtime:
Triggers when the match enters over time.
No additional JSON data.

survival_new_wave:
Triggers at the start of a new wave in Survival mode.
"WaveNumber": The current wave the Survival match is on.
"Enemies": Returns the amount of enemies needed to be defeated this wave.
"Chests": Returns the amount of chests that have spawned.
"ChestPrice": Returns the money cost of opening a chest for this wave.
"CaptureProgress": Returns the capture progress of the flag before the wave ended.
"ChestCrash": Returns whether chest prices have crashed and are cheaper.

survival_flag_unlocked:
Triggers when the control point flag unlocks for enemies to capture.
"WaveNumber": The current wave the Survival match is on.

survival_buy_chest:
Triggers when a player opens a chest.
"PlayerID": Player ID of the player who opened the chest.
"ChestID": ID of the chest that was opened.
"ChestCost": Returns the cost to open the chest, only on Survival mode.
"PlayerMoney": Returns what the buying player's money amount is after buying the chest, only on Survival mode.

survival_get_vice:
Triggers when a player collects a vice in Survival mode.
"PlayerID": The player ID of the collecting player
"ViceID": The ID of the type of vice collected
"X": The X position of where the vice was.
"Y": The Y position of where the vice was.

survival_use_vice:
Triggers when a player uses a consumable vice. (Rubbing Alcohol, Smokes, etc)
"PlayerID": The player ID of who used the vice.
"ViceID": The ID of the vice being consumed

survival_player_revive:
Triggers when a player is revived outside of a new wave starting.
"RevivingPlayerID": The player ID of the reviving player.
"SaviorPlayerID": The player ID of the player who revived the dead player. Will be the same as RevivingPlayerID if they revived themselves.
"Antacids": Will be set to "1" if the savior player used the antacids vice.
"Cost": The amount of money it cost to revive the dead player, unless they used the antacids vice then it is set to "1"

command_entered:
Triggered when a command is entered into the console.
"Command": The full string of the command that was entered.
"Source": The source of the command. 0 = In-game console window, 1 = RCON
"ReturnText": Returns the console message generated from the command.

match_paused:
Triggered when the server is paused.
No additional JSON data.

match_unpaused:
Triggered when the server is unpaused.
No additional JSON data.

warmup_start:
Triggered when the warm up phase has begun.
"WarmupTime": Returns how many seconds the warm up phase will last.
```
