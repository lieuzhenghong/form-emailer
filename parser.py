'''
TODO:
0. Check for the presence of data.csv, email.txt, and attachments.
1. Parse data.csv. Get To:, CC:
2. Parse email.txt. Get subject and replace the `stuff` and {{stuffs}} using
data.csv.
3. Return a list of dictionaries (one dictionary per email) to the
automated email sender

What that dictionary of strings looks like:
{
    to: ['investor@investor.com']
    cc: ['finance@investor.com', 'otherguy@investor.com']
    subject: ["Nerdwallet letter"]
    body: ["Hello Investor,\n, I am writing to inform you... \n"]
    attachments: ['letter_2.0_investor.docx', 'letter_3.0_investor.docx']
}
'''
import csv
import re

headers = []

def replace(row, text):
    final = text
    m = re.findall(r'`(.+?)`', final)
    for match in m:
        try:
            rep = str(row[headers.index(match)])
        except ValueError as error:
            raise Exception('<b>VALUE ERROR: ' + str(error) + '</b><p>This'
                   ' means that your text has `' + match +
                   '` which does not '
                   'exist in your csv file.'
                   'Check again.')
        n = '`'+match+'`'
        final = final.replace(n, rep)
    return(final)

def parse(csv_filename, email_filename):
    global headers
    out = []
    data = []
    first = ''
    body = ''
    with open(csv_filename) as csvfile:
        reader = csv.reader(csvfile)
        for idx, row in enumerate(reader):
            if idx == 0:
                headers = row
            else:
                data.append(row)
    t = open(email_filename, 'r')
    # The first line of email.txt should always start with "SUBJECT:<subject>“
    first = t.readline().strip()
    if (first.startswith('SUBJECT:') or first.startswith('subject:')):
        pass
    else:
        raise Exception("<b>EMAIL.TXT ERROR:</b>" + 
                        "You didn't start email.txt with 'SUBJECT:'." + 
                        "Don't forget the colon! (:)")
    body = t.read()
    t.close()

    for row in data:
        payload = {}
        payload['to'] = [x.strip() for x in
                        row[headers.index('email')].split(',')]
        payload['cc'] = [x.strip() for x in
                        row[headers.index('email_cc')].split(',')]
        payload['subject'] = first.replace('SUBJECT:', '').strip()
        payload['body'] = replace(row, body)
        payload['attachments'] = [x.strip() for x in
                                row[headers.index('attachment_name')].split(',')]
        out.append(payload) 
    return(out)

if __name__ == "__main__":
    import sys
    print(parse(sys.argv[1], sys.argv[2]))
