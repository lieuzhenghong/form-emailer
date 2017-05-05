jmport sendr
from appJar import gui
from tkinter.filedialog import askdirectory


'''
usage: sendr.py [-h] [-np] [-re [REDIRECT]] [-is [IDX_START]] [-ie [IDX_END]]
                path email password [data] [text]
(main(args.path, args.email, args.password, args.data,
      args.text, not(args.no_preview), args.redirect, args.idx))
'''
def add_file(btn):
    filename = askdirectory()
    app.setEntry('path', filename)

def press(btn):
    p = app.getEntry('path') 
    e = app.getEntry('email') 
    pw = app.getEntry('password')
    start = (None if (app.getEntry('start-idx')=='') else int(app.getEntry('start-idx')))
    end = (None if (app.getEntry('end-idx')=='') else int(app.getEntry('end-idx')))
    re = app.getEntry('Redirect email')
    np = app.getCheckBox('Don\'t preview: just send')
    print(e, pw, start, end, re, not(np))
    sendr.main(p, e, pw, 'data.csv', 'email.txt', not(np), re, start, end)
    
app = gui("Form emailer", "800x800")
app.setSticky("ew")
app.setStretch("column")
app.addEntry('path', 0, 0, 2)
app.setEntryDefault('path', 'path')
app.addButton('Choose path', add_file, 0, 2)
app.addAutoEntry("email", ['research@iglobepartners.com', 'kim@iglobepartners.com', 'weibin@iglobepartners.com'], 1, 0 )
#app.addEntry('email', 1, 0, 2)
app.addLabelSecretEntry("password", 1, 2)
app.addLabelEntry('start-idx', 2, 0);
app.addLabelEntry('end-idx', 2, 1);
app.setEntryDefault('start-idx', 'positive integer')
app.setEntryDefault('end-idx', 'positive integer')
app.addLabelEntry("Redirect email", 3,0, 2)
app.setEntryDefault('Redirect email', None)
app.addButton("Submit", press)
app.addCheckBox("Don't preview: just send" )
app.addLabel('preview', None)
app.go()
