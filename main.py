# This implementation of the Telegram Bot was done to view the data from my APC 1500 UPS.
# it is connected thorugh USB to my RaspberryPi Model 3. A service is attached to it and I can send or receive any notification from it.
# I'll implementate a function to call a number when the power is off. 

# Requirements:
# install apcupsd 
# Install PyTelegramBotAPI, do not install TELEBOT.


# This is my first attempt to perform a Telegram bot in Python 3.5 to make something useful.
# Juan Blanc, 2/15/2021



#DATA
#raw is something like 
#[b'APC', b':', b'001,036,0859', b'DATE', b':', b'2021-02-16', b'01:06:21', b'+0000', b'HOSTNAME', b':', b'raspberrypi', b'VERSION', b':', b'3.14.14', b'(31', b'May', b'2016)', b'debian', b'UPSNAME', b':', b'myups', b'CABLE', b':', b'USB', b'Cable', b'DRIVER', b':', b'USB', b'UPS', b'Driver', b'UPSMODE', b':', b'Stand', b'Alone', b'STARTTIME:', b'2021-02-15', b'23:29:52', b'+0000', b'MODEL', b':', b'Back-UPS', b'RS', b'1500G', b'STATUS', b':', b'ONLINE', b'LINEV', b':', b'219.0', b'Volts', b'LOADPCT', b':', b'6.0', b'Percent', b'BCHARGE', b':', b'100.0', b'Percent', b'TIMELEFT', b':', b'87.1', b'Minutes', b'MBATTCHG', b':', b'5', b'Percent', b'MINTIMEL', b':', b'3', b'Minutes', b'MAXTIME', b':', b'0', b'Seconds', b'SENSE', b':', b'Medium', b'LOTRANS', b':', b'176.0', b'Volts', b'HITRANS', b':', b'294.0', b'Volts', b'ALARMDEL', b':', b'30', b'Seconds', b'BATTV', b':', b'27.4', b'Volts', b'LASTXFER', b':', b'Low', b'line', b'voltage', b'NUMXFERS', b':', b'0', b'TONBATT', b':', b'0', b'Seconds', b'CUMONBATT:', b'0', b'Seconds', b'XOFFBATT', b':', b'N/A', b'SELFTEST', b':', b'NO', b'STATFLAG', b':', b'0x05000008', b'SERIALNO', b':', b'oneSerial', b'BATTDATE', b':', b'2018-11-10', b'NOMINV', b':', b'230', b'Volts', b'NOMBATTV', b':', b'24.0', b'Volts', b'NOMPOWER', b':', b'865', b'Watts', b'FIRMWARE', b':', b'878.L5', b'.I', b'USB', b'FW:L5', b'END', b'APC', b':', b'2021-02-16', b'01:06:23', b'+0000']

# raw_2 is something like this, (the basic output of a service call )
#● apcupsd.service - UPS power management daemon
#   Loaded: loaded (/lib/systemd/system/apcupsd.service; enabled; vendor preset: enabled)
#   Active: active (running) since Mon 2021-02-15 23:29:52 GMT; 1h 23min ago
#     Docs: man:apcupsd(8)
#  Process: 532 ExecStartPre=/lib/apcupsd/prestart (code=exited, status=0/SUCCESS)
#  Process: 542 ExecStart=/sbin/apcupsd (code=exited, status=0/SUCCESS)
# Main PID: 548 (apcupsd)
#    Tasks: 3 (limit: 2062)
#   CGroup: /system.slice/apcupsd.service
#           └─548 /sbin/apcupsd

#Feb 15 23:29:51 raspberrypi systemd[1]: Starting UPS power management daemon...
#Feb 15 23:29:52 raspberrypi systemd[1]: apcupsd.service: Can't open PID file /run/apcupsd.pid (yet?) after start: No such file or directory
#Feb 15 23:29:52 raspberrypi apcupsd[548]: apcupsd 3.14.14 (31 May 2016) debian startup succeeded
#Feb 15 23:29:52 raspberrypi apcupsd[548]: NIS server startup succeeded
#Feb 15 23:29:52 raspberrypi systemd[1]: Started UPS power management daemon.

import telebot
import subprocess
from subprocess import Popen, PIPE
tb =telebot.TeleBot('AAAAAAA:BBBBBBBBBBBBBBBBBBBBBBBBB') # Please set your own token

print ("Program started")
@tb.message_handler(commands=['start'])
def send_welcome(message):
	tb.reply_to(message, "Welcome to The UPS Bot, please use the commands to get information.\nSuscribe notification is WIP")

@tb.message_handler(commands=['read'])
def reply_read(message): 
    chat_id=message.from_user
    print ("Read request from ID:" + str(chat_id.id))
    tb.send_message(str(chat_id.id), "Reading UPS Status...")
    sprun = subprocess.run(['apcaccess', 'status'], stdout=subprocess.PIPE)
    chat_id=message.from_user
    raw = sprun.stdout.decode("utf-8")
    first_line = (sprun.stdout).split()
    #as first_line was an output of stdout, we must decode it in order to see it as character and not bytes.
    data =  ("Time " + first_line[6].decode("utf-8") + " GMT 00:00 Date " + first_line[5].decode("utf-8") + "\n")  
    # the first string was generated, we'll append the rest 
    data += ("Line Voltage:" + first_line[48].decode("utf-8") + " [V]" + "\n")
    data += ("Battery Voltage: " + first_line[91].decode("utf-8") + " [V]" + "\n")
    data += ("Load: " + first_line[52].decode("utf-8") + "%" + "\n")
    data += ("Battery Load:" + first_line[56].decode("utf-8")  + "%" + "\n")
    data += ("Remaining Time: " + first_line[60].decode("utf-8") + " Min" + "\n") 
    tb.send_message(str(chat_id.id),data)

@tb.message_handler(commands=['service'])
def reply_serv(message):
    chat_id=message.from_user
    print ("Service request from ID:" + str(chat_id.id))
    sprun = subprocess.run(['service', 'apcupsd', 'status'], stdout=subprocess.PIPE)
    raw_2= sprun.stdout.decode("utf-8")
    first_line = raw_2.split()
    sec_line = first_line[14].split(':')
    data = ("Service Status: " + sec_line[0])
    tb.send_message(str(chat_id.id),data)

@tb.message_handler(func=lambda message: True)
def dummy_response(message):  
    chat_id = message.from_user
    tb.send_message(str(chat_id.id), "This Bot is configured to use with commands, please do not use text")
    print ("message was request from ID:" + str(chat_id.id))
    
tb.polling() #the keep-alive
