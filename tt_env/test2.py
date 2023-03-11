txt = '..aapl!@#$$%^&*/'
mytable = str.maketrans('.', ' ')
mydict = {46:None}
print(txt.translate(mydict))