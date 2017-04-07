import smtplib
from email.message import EmailMessage
import mimetypes
import parser
import argparse
import sys


SESSION = ''
EMAIL = ''  # purely for generate function


def connect(email, password):
    global SESSION
    SESSION.ehlo()
    SESSION.starttls()
    try:
        SESSION.login(email, password)
    except smtplib.SMTPAuthenticationError as error:
        return("<b>AUTH ERROR:</b> Wrong email and/or password.")
    return(True)


def generate(mail):
    msg = EmailMessage()
    msg.set_content(mail['body'])
    msg['Subject'] = mail['subject']
    msg['From'] = EMAIL 
    msg['To'] = ", ".join(x for x in mail['to'])
    msg['CC'] = ", ".join(x for x in mail['cc'])

    files = mail['attachments']
    for filename in files:
        path = './attachments/{}'.format(filename)

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


def main(email, password, data, text, preview=True, i=None):
    global SESSION, EMAIL
    SESSION = smtplib.SMTP('smtp.office365.com', 587)
    EMAIL = email
    connected = connect(email, password)
    # connected = True
    if (connected is not True):
        return(connected)
        SESSION.quit()
    else:
        try:
            mails = parser.parse(data, text)
        except Exception as error:
            return(str(error))
        msgs = []
        logs = []
        if (i is None):
            for mail in mails:
                try:
                    msg = generate(mail)
                except FileNotFoundError as error:
                    SESSION.quit()
                    return(str(error))
                logs.append([msg.items(), str(msg.get_body())])
                msgs.append(msg)
            if (preview in [True, "True"]):  # handle string passed via CLI
                SESSION.quit()
                return(logs)
            else:
                send(msgs)
                SESSION.quit()
                return('messages sent')
        else:
            try:
                msg = generate(mails[i])
            except FileNotFoundError as error:
                SESSION.quit()
                return(str(error))
            if (preview in [True, "True"]):  # handle string passed via CLI
                SESSION.quit()
                return([msg.items(), str(msg.get_body())])
            else:
                send(msg)
                SESSION.quit()
                return('message sent')

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Send form emails. \n'
                                        'Supports attachments.')
    argparser.add_argument('email', help='Login email')
    argparser.add_argument('password', help='Login password')
    argparser.add_argument('data', help='Your data .csv file')
    argparser.add_argument('text', help='Your email body .txt file.')
    argparser.add_argument('-np', '--no-preview',
                           help='Send emails straight away (dangerous)',
                           action='store_true')
    argparser.add_argument('-i', '--idx',
                           help='Which data row to reference (zero-indexed)',
                           type=int)
    args = argparser.parse_args()
    print(main(args.email, args.password, args.data,
               args.text, not(args.no_preview), args.idx))
