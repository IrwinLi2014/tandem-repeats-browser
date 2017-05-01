import web
import shutil
import subprocess
import numpy
render = web.template.render('webpage/')

urls = (
    '/', 'index',
    '/repeat', 'repeat'
)

gfastayes = True
gm = 0
gw = 0
ga = 0
gb = 0

class index:
    def GET(self):
        return render.index()

    def POST(self):
        x = web.input(myfile={})
        alph = x.alpha.encode('ascii','ignore')
        bond = x.bond.encode('ascii','ignore')
        if alph == "":
            alph = 'ATCG'
        if bond == "":
            bond = '0'
        command = "python3 ./tandem.py -m " + x.maxtolerance.encode('ascii','ignore') + " -w " + x.windowsize.encode('ascii','ignore') + " -a " + alph + " -i input.fna -b " + bond
        global gm
        gm = x.maxtolerance.encode('ascii','ignore')
        global gw
        gw = x.windowsize.encode('ascii','ignore')
        global ga
        ga = alph
        global gb
        gb = bond
        global gfastayes
        if x['fileselect']=="Upload file in FASTA format" and x.myfile.file:
            destFile = open('./input.fna', 'wb')
            destFile.write(x.myfile.file.read())
            destFile.close()
        if x['fileselect']=="Cut and paste sequence":
            gfastayes = False
            command = "python3 ./tandem.py -m " + x.maxtolerance.encode('ascii','ignore') + " -w " + x.windowsize.encode('ascii','ignore') + " -a " + alph + " -s " + x.seq.encode('ascii','ignore') + " -b " + bond
        print('command', command)
        subprocess.call(command, shell=True)
        raise web.seeother('/repeat')

class repeat:
    page=["""<html>
            <head>
            <style>
            ul {
                list-style-type: none;
                margin: 0;
                padding: 0;
                overflow: hidden;
                background-color: #333333;
            }

            li a {
                display: block;
                color: white;
                text-align: center;
                padding: 16px;
                text-decoration: none;
            }

            li a:hover {
                background-color: #111111;
            }
            </style>
            </head>
            <body>"""]
    def GET(self):
        page.append( """
<form method="POST" enctype="multipart/form-data" action="">
<textarea name="rn" rows=1 cols=10 id="rn"></textarea>
<input type="submit" />
</form>
</body></html>""")
        return (" ".join(page))

    def POST(self):
        if gfastayes:
            x = web.input()
            rn = x.rn.encode('ascii','ignore')
            if rn == "":
                rn = '0'
            command = "python3 ./showrepeats.py -rn " + rn + " -m " + gm + " -w " + gw + " -a " + ga + " -b " + gb + " -i input.fna > repeat_found"
            subprocess.call(command, shell=True)
            with open("repeat_found", 'rb') as f:
                repeat = f.read()
            print(repeat)

        raise web.seeother('/repeat')

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
