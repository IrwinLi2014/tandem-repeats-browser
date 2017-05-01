import web
import shutil
import subprocess
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
        #web.debug(x['myfile'].value) # This is the file contents
        #web.debug(x['myfile'].file.read()) # Or use a file(-like) object

        raise web.seeother('/repeat')

class repeat:
    def GET(self):
        return """<html><head></head><body>
<form method="POST" enctype="multipart/form-data" action="">
<textarea name="rn" rows=1 cols=10 id="rn"></textarea>
<input type="file" id="myfile "name="myfile" />
<br/>
<input type="submit" />
</form>
</body></html>"""

    def POST(self):
        if gfastayes:
            x = web.input()
            rn = x.rn.encode('ascii','ignore')
            if rn == "":
                rn = '0'
            command = "python3 ./showrepeats.py -rn " + rn + " -m " + gm + " -w " + gw + " -a " + ga + " -b " + gb + " -i input.fna"
            subprocess.call(command, shell=True) 
        #web.debug(x['myfile'].value) # This is the file contents
        #web.debug(x['myfile'].file.read()) # Or use a file(-like) object

        raise web.seeother('/repeat')

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
