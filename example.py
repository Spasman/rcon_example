import socket
import struct
import sys
import datetime
import json
import time
from enum import Enum

#developed in python 3 but it might work in 2???
#RCON events and requests will have documentation soon
#This is for Boring Man v2.0.0+ NOT Boring Man v1.2.7.7

#put your game server's IP address and **RCON** port (not the server port), then your server's rcon password
server_address = ('127.0.0.1', 42070)
server_password = "admin"

#Initialize enum. These are the same enums B-Man uses. this may be updated as the game is developed
#these enums identify game events, such as a flag being captured in CTF or a round ending in TDM
class rcon_event(Enum):
	server_startup = 0
	server_shutdown = 1
	lobby_connect = 2
	lobby_disconnect = 3
	player_connect = 4
	player_spawn = 5
	player_death = 6
	player_disconnect = 7
	player_team_change = 8
	player_level_up = 9
	player_get_powerup = 10
	player_damage = 11
	player_loaded = 12
	tdm_round_start = 13
	tdm_round_end = 14
	tdm_flag_unlocked = 15
	tdm_switch_sides = 16
	ctf_taken = 17
	ctf_dropped = 18
	ctf_returned = 19
	ctf_scored = 20
	ctf_generator_repaired = 21
	ctf_generator_destroyed = 22
	ctf_turret_repaired = 23
	ctf_turret_destroyed = 24
	ctf_resupply_repaired = 25
	ctf_resupply_destroyed = 26
	match_end = 27
	match_overtime = 28
	match_start = 29
	survival_new_wave = 30
	survival_flag_unlocked = 31
	survival_buy_chest = 32
	log_message = 33
	request_data = 34
	command_entered = 35
	rcon_logged_in = 36
	match_paused = 37
	match_unpaused = 38
	warmup_start = 39
	rcon_disconnect = 40
	rcon_ping = 41
	chat_message = 42

#use these enums when sending requests to your server so the server knows what to do with them
class rcon_receive(Enum):
	login = 0
	ping = 1
	command = 2
	request_player = 3
	request_bounce = 4
	request_match = 5
	confirm = 6
	request_scoreboard = 7

#initialize some globals for network data reading
#sock.recv() uses bytes so lets make them empty byte arrays
buffer = b''
get_data = b''
data = b''

#these two are the delimiters for B-Man packets
start_read = b'\xe2\x94\x90' #translates to ascii character "┐"
end_read = b'\xe2\x94\x94' #translates to ascii character "└"

connected = 0 #used for allowing the main loop during a connection
timeout = 0 #used for timing out a bad connection

#this function isn't used but its example code of parsing the 'PlayerData' JSON set
#It itorates through an entire JSON string looking for keys that start with the string 'PlayerData'
#If found, you can use the 'k' variable as an accessor for each key/value pair
#just look at the damn code, whatever, fuck
def scoreboard(jsonString):
	js = json.loads(jsonString)
	for (k, v) in js.items():
		if k.startswith("PlayerData"):
			name = js[k]['Name']
			kills = js[k]['Kills']
			deaths = js[k]['Deaths']
			assists = js[k]['Assists']
			print(str(name)+" - K: "+str(kills)+" D: "+str(deaths)+" A: "+str(assists))

#declaring a function for sending packets over socket to game maker networking
#the message contains a signed integer for the enum event ID, then a string with data to process on the server
def send_packet(packetData,packetEnum):
	global sock #get the global socket ID value
	packet_message = packetData+"\00" #add a null terminating character at the end of your string because game maker is stupid
	packet_size = len(bytes(packet_message, 'utf-8')) #get the byte size of your string
	s = struct.Struct('h'+str(packet_size)+'s') #create a data structure with an int and a string (with the string size)
	packet = s.pack(packetEnum,packet_message.encode('utf-8')) #pack and encode your message for game maker usage
	try:
		sock.send(packet) #send that bitch
	except:
		print("Server error!") #crash if you can't
		sys.exit()

#attempt a connection to the Boring Man server, or crash if you can't
try:
	#create a global TCP socket, Boring Man RCON uses a separate TCP socket unlike the rest of the games netcode
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#we turn TCP blocking on and off because its just easier that way
	sock.setblocking(1)
	sock.connect(server_address)
	sock.setblocking(0)
	#send a 'rcon_receive.login' packet with your RCON password as the string data
	send_packet(server_password,rcon_receive.login.value)
	connected = 1 #set connected to 1 to signal the while loop
except:
	#take the above code out of the 'try' block to see the specific crash
	print("Could not connect!")
	sys.exit()

if connected == 1: #use 'connected' to start the main loop if a connection is made
	while True:
		timeout += 1
		if timeout > 3600000:
			#increase timeout value and if it reaches more then 3600000, kill the app
			#timeout is reset when rcon receives an "rcon_event.rcon_ping.value" event from the game server
			print("Timed out from server!")
			sys.exit()
		data = b'' #reset main data byte array
		try:
			#attempt to load bytes from the network
			#buffer size read per cycle set to 64k because YEET
			#set it to something lower if youre having network performance problems
			get_data = sock.recv(64000)
		except:
			get_data = b'' #return empty byte array is fail
		if get_data != b'':#if the byte array is not empty, load them into the current data buffer
			buffer += get_data
		while True: #a second while loop is needed to loop through the buffer to make sure all data is processed
			if buffer.find(end_read) != -1 and buffer.find(start_read) != -1: #this if-else statement checks if the data buffer has the beginning delimiter and the end delimiter
				start_index = buffer.find(start_read) #find the beginning byte position of the Boring Man packet
				end_index = buffer.find(end_read)+3 #find the ending byte position of the Boring Man packet and offset it to make sure its included (1 character string = 3 bytes)
				data = buffer[start_index:end_index] #carve out the complete packet out of the data buffer and assign it to the 'data' variable for processing
				buffer = buffer[end_index:] #take the complete packet out of the buffer so only the unused data is left so it can be used next cycle
				if data != b'': #make sure the data variable isn't empty
					data_info = struct.unpack_from('<'+'3s'+'h',data,0) #read the beginning delimiter character, and then the JSON string size (in bytes)
					event_data = struct.unpack_from('<'+'3s'+'h'+'h'+str(data_info[1])+'s',data,0) #read the beginning delimiter character, and then the JSON string size, then the event ID integer, then the JSON string itself using the size value from the line above
					data = b'' #reset the data variable 
					event_id = event_data[2] #get the event ID number
					message_string = event_data[3].decode().strip() #get the JSON string and sanitize it
					message_string = message_string[:-1] #remove the ending delimiter character (└)
					#
					#uncomment the print line below to see the event IDs received and the JSON data that comes with them
					#print("EVENT ID: "+str(event_id)+" - JSON: "+str(message_string)) 
					#
					#!!BELOW IS WHERE YOU SHOULD START PROCESSING THE GAME'S JSON DATA!!
					#
					if event_id == rcon_event.rcon_ping.value: #if the event is a ping
						#event ID for pinging. Boring Man will send each RCON client a ping event every few seconds, reply to it to keep your connection alive
						#use the 'rcon_receive.ping' enum for pinging, this tells the server its just a ping packet and to do nothing with it
						print("Replying to ping")
						timeout = 0 #reset timeout if a ping is received
						send_packet("1",rcon_receive.ping.value) #i put a "1" string cuz sometimes game maker gets mad at empty strings
					#
					#this event ID is for logging in-game console messages in your python window
					if event_id == rcon_event.log_message.value:
						js = json.loads(message_string)
						print(js['Message']) #load the JSON key 'Message' to get the log message
					#
					#
					if event_id == rcon_event.server_shutdown.value:
						#end the app if it receives a "server_shutdown" event
						print("Server disconnected")
						sys.exit()
					#
					#this a little example of a in-game chat command. type '!time' in the in-game chat window while this example is connected and see what happens!
					if event_id == rcon_event.chat_message.value:
						js = json.loads(message_string) #message_string is the json string, so pass it through the json module
						timestamp = str(datetime.datetime.now().strftime("%H:%M:%S")) #generate a time stamp
						id = int(js['ID']) #get the player ID of the player who sent the message and make it an integer
						username = js['Name'] #get the username of the player who sent the message
						chat = js['Message'] #get the message text that was sent
						if id != -1: #ignore the message if it was sent by the server (ID will be -1)
							print("Received chat message from player "+str(id)) #notify
							if chat.startswith('!time'): #check if the message starts with the command '!time'
								send_packet('rawsay "Hello '+str(username)+'! The time is '+str(timestamp)+'."',rcon_receive.command.value) #reply back to the server with an in-game console command
			else:
				break; #break out of this while loop if the beginning or ending delimiter characters aren't found and go back to reading network data
