import getpass
import sendr

smtp_url = input('SMTP server URL (defaults to outlook.office.com): ')
smtp_port = input('SMTP server port (defaults to 587): ')
email = input('Email address: ')
password = getpass.getpass('Password: ')
path = input('Location of folder: ')
no_preview = input('Send without previewing? (y/n): ')
idx_start = 


if no_preview == 'y' or no_preview == 'Yes' or no_preview == 'Y':
    no_preview = True
else:
    no_preview = False


'''
sendr.main(path, email, password, smtp_url,
      int(smtp_port),
      not(no_preview), 
      args.redirect,
      int(idx_start),
      int(idx_end),
      args.bcc)
'''
