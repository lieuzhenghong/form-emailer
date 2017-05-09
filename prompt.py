import getpass
import sendr

smtp_url = input('SMTP server URL (defaults to outlook.office.com): ')
smtp_port = input('SMTP server port (defaults to 587): ')
email = input('Email address: ')
password = getpass.getpass('Password: ')
path = input('Location of folder: ')
idx_start = input('Start index (if any?): ')
idx_end = input('End index (if any?): ')
no_preview = input('Send without previewing? (y/n): ')


if no_preview == 'y' or no_preview == 'Yes' or no_preview == 'Y' or no_preview == 'yes':
    no_preview = True
else:
    no_preview = False

if smtp_url.strip(' ') == '':
    smtp_url = 'outlook.office.com'

if smtp_port.strip(' ') == '':
    smtp_port = 587

if idx_start.strip(' ') == '':
    idx_start = None
else:
    idx_start = int(idx_start.strip(' '))

if idx_end.strip(' ') == '':
    idx_end = None
else:
    idx_end = int(idx_end.strip(' '))

try:
    sendr.main(path,
               email,
               password,
               smtp_url,
               int(smtp_port),
               'data.csv',
               'email.txt',
               not(no_preview), 
               None,
               idx_start,
               idx_end
               )
except:
    import sys
    print(sys.exc_info()[0])
    import traceback
    print(traceback.format_exc())
finally:
    print("Press Enter to exit.")
    input()
