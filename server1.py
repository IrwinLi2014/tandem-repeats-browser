import web
import shutil
import subprocess
import csv
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
repeatfound=None

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
        # print('command', command)
        subprocess.call(command, shell=True)
        raise web.seeother('/repeat')

class repeat:
    page_head="""<html>
            <head>
            <style>
            ul {
                list-style-type: none;
                margin: 0;
                padding: 0;
                overflow: hidden;
                background-color: #E0E0E0;
            }

            li a {
                display: block;
                color: DarkBlue;
                text-align: center;
                padding: 16px;
                text-decoration: none;
            }

            li a:hover {
                background-color: #FFFFCC;
            }
            pre {
                color:DarkBlue;
                font-size:120%;
                font-family:courier;
            }
            </style>
            </head>
            <body>
            <pre><b>search repeat (using index):</b></pre>
            <form method="POST" enctype="multipart/form-data" action=""><textarea name="rn" rows=1 cols=10 id="rn"></textarea><input type="submit" /></form>
            <pre><b>search result:</b></pre>
            
            """
    page_body = []
    page_tail = "</body></html>"
    def GET(self):
        self.page_body = []
        global repeatfound
        # print("repeat: ", repeatfound)
        if (repeatfound):
            self.page_body.append("""<pre><b>""" + repeatfound +  """</b></pre>""")
        self.page_body.append("""<ul><li><a href='"+str(n)+"'>[ index , start point of repeat, end point of the 1st pattern , end point of repeat " ] </a></li></ul>""")
        with open('out.csv', 'rb') as csvfile:
            repeats = csv.reader(csvfile, delimiter=',')
            n = 0
            for row in repeats:
                r = "<ul><li><a href=n>[  #" + str(n) + " , " + row[0] + " , " +row[1] + " , " + row[2] + " ] </a></li></ul>"
                self.page_body.append(r)
                n+=1
        return (self.page_head + " ".join(self.page_body) + self.page_tail)

    def POST(self):
        global repeatfound
        if gfastayes:
            x = web.input()
            rn = x.rn.encode('ascii','ignore')
            if rn == "":
                rn = '0'
            command = "python3 ./showrepeats.py -rn " + rn + " -m " + str(gm) + " -w " + str(gw) + " -a " + str(ga) + " -b " + str(gb) + " -i input.fna > repeat_found"
            subprocess.call(command, shell=True)
            with open("repeat_found", 'rb') as f:
                repeatfound = f.read()
            # print(repeatfound)
        
        raise web.seeother('/repeat')

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
