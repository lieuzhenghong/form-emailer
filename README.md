# form-emailer 

## How to use
You need a `data.csv` with header row.
Each row corresponds to one document to be created.

The following columns are required:
* email (who to send the email to)
* email_cc
* attachment_name (supports multiple attachments, separated by commas)

'''usage: sendr.py [-h] [-np] [-re [REDIRECT]] [-i [IDX [IDX ...]]]
                path email password [data] [text]

Send form emails. Supports attachments.

positional arguments:
  path                  The main folder
  email                 Login email
  password              Login password
  data                  Your data .csv file
  text                  Your email body .txt file.

optional arguments:
  -h, --help            show this help message and exit
  -np, --no-preview     Send emails straight away (dangerous)
  -re [REDIRECT], --redirect [REDIRECT]
                        Redirect to the email
  -i [IDX [IDX ...]], --idx [IDX [IDX ...]]
                        Which data row to reference (zero-indexed). Can take a
                        range'''
