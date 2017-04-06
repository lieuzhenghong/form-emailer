import smtplib
from email.message import EmailMessage
import mimetypes
import parser
import sys

def send(email, password):
    smtp_obj = smtplib.SMTP('smtp.office365.com', 587)
    print(smtp_obj.ehlo())
    print(smtp_obj.starttls())
    try:
        print(smtp_obj.login(email, password))
    except smtplib.SMTPAuthenticationError as error:
        print("<b>AUTH ERROR:</b> Wrong email and/or password.")
        sys.exit(1)

    test_obj = parser.parse('data.csv', 'email.txt')[0]
    msg = EmailMessage()
    msg.set_content(test_obj['body'])
    msg['Subject'] = test_obj['subject']
    msg['From'] = 'research@iglobepartners.com'
    msg['To'] = ", ".join(x for x in test_obj['to'])
    msg['CC'] = ", ".join(x for x in test_obj['cc'])

    files = test_obj['attachments']
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
            print('{} attached successfully'.format(filename))
    smtp_obj.send_message(msg)
    print('messages sent')
    smtp_obj.quit()

if __name__ == "__main__":
    send(sys.argv[1], sys.argv[2])
