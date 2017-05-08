# form-emailer 
Sends emails from a template and a data file.

## Introduction
I was tasked to send many similar emails. Each email had to be personalised
with the receipients' names and the attachments differed as well (each
recipient received their own Word document—see
[form-letterer](https://github.com/lieuzhenghong/form-letterer).)

This program automatically sends emails. Here's how it works:

![overview-1](img/overview1.png)
![overview-2](img/overview2.png)

## email.txt
**The first line of `email.txt` must be SUBJECT: XYZ**

Additionally, text in `email.txt` 

Here's a sample email:
```
SUBJECT: Happy birthday to you!
Dear `name`,

Thanks for being our loyal customer and for giving us `amount` dollars.

Sincerely,
iGlobe Partners
```

## data.csv
You can add as many columns and rows as you want to your `data.csv` file. The
only required column is the `to` column. All other columns don't have to be in
your `data.csv`.

Here's an example of a `data.csv` file:

| name  | amount | to | cc | bcc | attachments |
| ----- | ------------- | --- | --- | --- | --- |
| Jack | 500 | lzh@gmail.com, jack@email.com | pqrs@email2.com | | test.png, test1.pdf |
| CKY | 300 | cky@gmail.com | | pqrq@email3.com | test.png |

### to
**(REQUIRED)** Who the email will be sent to.
Separate multiple emails with commas: `guy1@email.com, guy2@email.com`
etc.

### cc
Self-explanatory. See `to`.

### bcc
Self-explanatory. See `to`.

### attachments
**All attachments must be in the attachments/ folder.**

Most file types **should** be accepted.

Separate multiple attachments with commas: `attach1.png, attach2.pdf`.

## Parameters

### path
**(REQUIRED)** The main folder your `data.csv`, `email.txt` and `attachments`
live in.

### email
**(REQUIRED)** Your email address. (Should be a Outlook Office 365 email.)

### password
**(REQUIRED)** Your password.

### data
Your `data.csv` file. Useful if your `data.csv` is not called `data.csv`. If
not specified, default is `data.csv`.

### email
Your `email.txt` file. If not specified, default is `email.txt`.

### index-start & index-end
None, either, or both of these parameters can be specified.

1. If neither are specified
2. If only `index-start` is specified
3. If only `index-end` is specified
4. If both are specified

#### If neither are specified
All emails will be selected.

#### If only `index-start` is specified
Only one email will be selected, which is the `index-start`. For example,
`--index-start 3` will select the third email.

#### If only `index-end` is specified
The first email to the `index-end`th email will be selected. (inclusive) 
For example, `--index-end 3` will select three emails, 1st, 2nd and 3rd.

#### If both are specified
Emails from `index-start` to `index-end` (inclusive) will be selected.
For example, `--index-start 2 --index-end 3` will select two emails: 2nd and 3rd.

### no-preview
Set `--no-preview` or `np` to actually send out the emails. By default, this is
not selected and the emails are not sent, only previewed.

### redirect
Not really important, but you can redirect messages to your email to preview
them before you send them—useful for checking formatting. Use `--redirect <your
email> --no-preview` to send emails to a target email address.

### bcc
Use `--bcc <your_email>` to BCC someone. You can also do this in `data.csv`.

## Limitations
Outlook limits the number of emails you can send at 30/minute. Hence if you try
to send too many, you'll get an error and not all emails will send. Work around
this by using `--index-start` and `--index-end` to send emails in batches.
