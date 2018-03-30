import sys
import os
import getpass

import xlrd, xlwt

from netmiko import ConnectHandler
from login import logincisco
from findcrash import findcrash


USERNAME = logincisco()
print('Your username: ', USERNAME)
PASSWORD = getpass.getpass()
Command = 'show flash:'
Loopcrash = []
Errorlist = []

rb=xlrd.open_workbook("C:\\..."
                      "...\\loopbacks.xlsx")

sheet = rb.sheet_by_index(0)
vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]



for IP in vals:

  try:
        DEVICE_PARAMS = {'device_type': 'cisco_ios',
                         'ip': IP[1],
                         'username': USERNAME,
                         'password': PASSWORD}

        with ConnectHandler(**DEVICE_PARAMS) as ssh:

            print('Connecting to device {}...'.format(IP[1]))

            ssh.enable()
            flash = ssh.send_command(Command)

  except Exception:
      print('Error')
      Errorlist.append(IP)
      

  match = findcrash(flash)

  if match == None:
     print('Not Found')
  else:
     print('File CRASHINFO found!')
     Loopcrash.append(IP[1])    


print(Errorlist)
print(Loopcrash)     
