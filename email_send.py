import smtplib
from email.message import EmailMessage
import mimetypes
import parser
import sys

SESSION = smtplib.SMTP('smtp.office365.com', 587)

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
    msg['From'] = 'research@iglobepartners.com'
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
            #print('{} attached successfully'.format(filename))
    return(msg)

def send(msg):
    global SESSION
    SESSION.send_message(msg)

def main(email, password, data, text, i=0, msg=None, preview=True):
    global SESSION
    # connected = connect(email,password)
    connected = True
    if (connected is not True): 
        return(connected)
    else:
        mails = parser.parse(data, text)
        for mail in mails[int(i):]:
            msg = generate(mail)
            if preview:
                print(msg)
                return([msg, i])
            else:
                #send(msg)
                pass
    SESSION.quit()

if __name__ == "__main__":
    print(main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))
