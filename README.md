# form-emailer 

## Setup
You need a `data.csv` with header row.
Each row corresponds to one document to be created.

The following columns are required:
* email (who to send the email to)
* email_cc
* attachment_name (supports multiple attachments, separated by commas)

Here's what your data.csv could look like: ![data.csv](img/data.csv.png)

Feel free to add additional fields but this is the minimum.

You also need a `email.txt` which should look like this: ![email.txt](img/email.txt.png) 

The first line of `email.txt` **must** be `SUBJECT: your subject here`. Don't split the subject up into two lines, it has to be one line long. And don't forget the space after `SUBJECT:` either!



