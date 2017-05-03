import smtplib
from email.message import EmailMessage
import mimetypes
import parser
import argparse
from argparse import RawDescriptionHelpFormatter
import sys


SESSION = ''
EMAIL = ''  # purely for generate function
BCC = '' # purely for generate function
PATH = ''


# Connects to the office365 SMTP server 
# 
def connect(email, password):
    global SESSION
    SESSION.ehlo()
    SESSION.starttls()
    try:
        SESSION.login(email, password)
    except smtplib.SMTPAuthenticationError as error:
        raise Exception("<b>AUTH ERROR:</b> Wrong email and/or password.")
    return(True)


# Generates a mail message and adds an attachment to it
# It takes in a mail object which is an object created by
# parser.py, parser.parse
def generate(mail):
    msg = EmailMessage()
    # Grab all the data from the mail object
    msg.set_content(mail['body'])
    msg['Subject'] = mail['subject']
    msg['From'] = EMAIL
    msg['To'] = ", ".join(x for x in mail['to'])
    msg['CC'] = ", ".join(x for x in mail['cc'])
    msg['BCC'] = BCC

    files = mail['attachments']
    for filename in files:
        path ='{}attachments/{}'.format(PATH, filename)

        # "Magic method" that is able to guess the attachment's filetype
        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        with open(path, 'rb') as fp:
            msg.add_attachment(fp.read(),
                               maintype=maintype,
                               subtype=subtype,
                               filename=filename)
    return(msg)


def send(msgs):
    if isinstance(msgs, list):
        for msg in msgs:
            SESSION.send_message(msg)
    else:
        SESSION.send_message(msgs)


# The main function responsible for doing everything
# Set
def main(path, email, password, data, text,
         preview=True, redirect=None, i=None, ie=None, bcc=None):
    global SESSION, EMAIL, PATH, BCC
    SESSION = smtplib.SMTP('smtp.office365.com', 587)
    EMAIL = email
    BCC = bcc
    PATH = (path if (path[-1] == '/' ) else (path + '/')) 
    #
    connected = connect(email, password)
    if (connected is not True):
        return(connected)
        raise Exception(str(connected))
        SESSION.quit()
    else:
        # Try parsing the mails, if it fails it means there was some problem
        # with the input data
        try:
            mails = parser.parse(PATH, data, text, redirect)
        except Exception as error:
            raise Exception(str(error))
        msgs = []
        logs = []
        # If no start index is specified, we send all the emails
        if (i is None):
            for mail in mails:
                try:
                    msg = generate(mail)
                except FileNotFoundError as error:
                    SESSION.quit()
                    raise Exception(str(error))
                logs.append([msg.items(), str(msg.get_body())])
                msgs.append(msg)
            # if preview flag is True (default), don't send, just print
            if (preview in [True, "True"]):  # handle "True" passed in via CLI
                SESSION.quit()
                print(logs)
            else:
                send(msgs)
                SESSION.quit()
        elif (ie is None): 
        # Here, i is not None, ie is None, so we send the i'th mail 
        # Changed it to be one-indexed
            try:
                msg = generate(mails[i-1])
            except FileNotFoundError as error:
                SESSION.quit()
                raise Exception(str(error))
            logs.append([msg.items(), str(msg.get_body())])
            msgs.append(msg)
            if (preview in [True, "True"]):  # handle string passed via CLI
                SESSION.quit()
                print(logs)
            else:
                send(msgs)
                SESSION.quit()
        # sends mail from i to ie, inclusively
        # so i = 1 i = 3 will get you the 1st to 3rd emails
        else:
            for mail in mails[(i-1):ie]:
                try:
                    msg = generate(mail)
                except FileNotFoundError as error:
                    SESSION.quit()
                    raise Exception(str(error))
                if (preview in [True, "True"]):  # handle string passed via CLj
                    print([msg.items(), str(msg.get_body())])
                else:
                    send(msg)
            SESSION.quit()

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='''
Send form emails. \n\
Supports attachments.\n\

This program requires a data.csv and a email.txt file, as well as a
folder entitled 'attachments' (even if no attachments are needed).
This program reads a data.csv file row
by row, where each row denotes an email to send out.
The data.csv should contain the following mandatory columns. All these
columns can take multiple comma-separated values (for example,
'attachment1.png, attach2.pdf').
The mandatory columns are:

| `email` (the To: field)
| `email_cc`
| `attachment_name`

The CSV may contain optional columns used for the purpose of doing
search-and-replace operations on the email text. 

Read README.md for more information.
''',
    formatter_class=RawDescriptionHelpFormatter
                                        )
    argparser.add_argument('path', help='The main folder. Make sure there\
                           exists a data.csv, email.txt and attachments/\
                           folder.')
    argparser.add_argument('email', help='Login email')
    argparser.add_argument('password', help='Login password')
    argparser.add_argument('data',
                           nargs='?',
                           help='Your data file (.csv)',
                           default='data.csv')
    argparser.add_argument('text',
                           nargs='?',
                           help='Your email body file (.txt)',
                           default='email.txt')
    argparser.add_argument('-np', '--no-preview',
                           help='Actually send the emails (dangerous!!!). By\
                           default (--no-preview=false), this will not send\
                           anything, just print out the emails to the\
                           terminal.',
                           action='store_true')
    argparser.add_argument('-re', '--redirect',
                           nargs='?',
                           help='--redirect takes an email address. All emails\
                           will be sent to the email address given. This is\
                           useful for testing.',
                           default=None
                           )
    argparser.add_argument('-is', '--idx-start',
                           nargs='?',
                           help='If --idx-end is not specified, gets only the\
                           --idx-start\'s entry from the data file. If\
                           --idx-end is specified, gets the --idx-start to\
                           --idx-end entries.',
                           default=None,
                           type=int)
    argparser.add_argument('-ie', '--idx-end',
                           nargs='?',
                           help='This should not be specified if --idx-start is\
                           not specified. See --idx-start.',
                           default=None,
                           type=int)
    argparser.add_argument('-bcc', '--bcc',
                           nargs='?',
                           help='Takes a comma-separated list of email\
                           addresses to BCC to', 
                           default=None,
                           )
    args = argparser.parse_args()
    print(args)
    (main(args.path, args.email, args.password, args.data,
          args.text, not(args.no_preview), args.redirect, args.idx_start, args.idx_end, args.bcc))
