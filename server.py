import web
import shutil
import subprocess
import csv
import tandem
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
myseq = ""  #cut and paste sequence

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
        # tandem.tandem_repeats(x.maxtolerance.encode('ascii','ignore'), x.windowsize.encode('ascii','ignore'), alphabet=alph, infile=input.fna, lower_bond=bond)
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
        global myseq
        if x['fileselect']=="Upload file in FASTA format" and x.myfile.file:
            gfastayes = True
            destFile = open('./input.fna', 'wb')
            destFile.write(x.myfile.file.read())
            destFile.close()
        if x['fileselect']=="Cut and paste sequence":
            myseq = x.seq.encode('ascii','ignore')
            gfastayes = False
            command = "python3 ./tandem.py -m " + x.maxtolerance.encode('ascii','ignore') + " -w " + x.windowsize.encode('ascii','ignore') + " -a " + alph + " -s " + x.seq.encode('ascii','ignore') + " -b " + bond
        print('command', command)
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
            h1   {background-color:Grey; text-align:center; font-size:300%; color:white; font-family:verdana;}
            h2   {background-color:Grey; text-align:center; font-size:200%; color:white; font-family:verdana;}

            li a {
                display: block;
                color: DarkBlue;
                text-align: center;
                padding: 16px;
                text-decoration: none;
                font-family:verdana;
            }

            li a:hover {
                background-color: #FFFFCC;
            }
            pre {
                word-wrap: break-word;
                width: 100px;
                color:DarkBlue;
                font-size:120%;
                font-family:courier;
            }
            </style>
            </head>
            <body>
            <h1>Tandem Repeats Found</h1>
            <h2><a href='/'>Back</a></h2>
            <pre><b>search repeat (using index):</b></pre>
            <form method="POST" enctype="multipart/form-data" action=""><textarea name="rn" rows=1 cols=10 id="rn"></textarea><input type="submit" /></form>
            <pre><b>search result:</b></pre>
            
            """
    page_body = []
    page_tail = "</body></html>"
    def GET(self):
        self.page_body = []
        global repeatfound
        print("repeat: ", repeatfound)
        data = web.input(id=-1)
        if (data.id!=-1):
            command = "python3 ./showrepeats_2.py -rn " + data.id + " -m " + str(gm) + " -w " + str(gw) + " -a " + str(ga) + " -b " + str(gb) + " -i input.fna > repeat_found"
            subprocess.call(command, shell=True)
            with open("repeat_found", 'rb') as f:
                repeatfound = f.read()
        if (gfastayes==True) and (repeatfound):
            self.page_body.append("""<pre><b>""" + repeatfound +  """</b></pre>""")
        if (gfastayes==False):
            self.page_body.append("""<ul><li><a href='/repeat'>You selected cut and paste sequence.  Found tandem repeats are displayed below, each repeat followed by its indices:</a></li></ul>""")
        self.page_body.append("""<ul><li><a href='/repeat'><b>[ index , start point of repeat, end point of the 1st pattern , end point of repeat  ]</b> </a></li></ul>""")
        rs = []
        with open('out.csv', 'rb') as csvfile:
            repeats = csv.reader(csvfile, delimiter=',')
            n = 0
            for row in repeats:
                r = "<ul><li><a href='/repeat?id=" + str(n)+ "''>[ " + str(n) + " , " + row[0] + " , " +row[1] + " , " + row[2] + " ] </a></li></ul>"
                if gfastayes:
                    self.page_body.append(r)
                else:
                    rs.append(r)
                n+=1
        if gfastayes == False:
            command = "python3 ./showrepeats_2.py -m " + str(gm) + " -w " + str(gw) + " -a " + str(ga) + " -b " + str(gb) + " -s " + myseq
            subprocess.call(command, shell=True)
            x = 0
            with open('myrpts.csv', 'rb') as myrptscsv:
                repeats = csv.reader(myrptscsv)
                for row in repeats:
                    for i in range(len(row)):
                        self.page_body.append("""<ul><li><a href='/repeat'>""" + row[i] + """</a></li></ul>""")
                        self.page_body.append(rs[x])
                        x+=1
        return (self.page_head + " ".join(self.page_body) + self.page_tail)

    def POST(self):
        global repeatfound
        if gfastayes:
            x = web.input()
            rn = x.rn.encode('ascii','ignore')
            if rn == "":
                rn = '0'
            if gfastayes:
                command = "python3 ./showrepeats_2.py -rn " + rn + " -m " + str(gm) + " -w " + str(gw) + " -a " + str(ga) + " -b " + str(gb) + " -i input.fna > repeat_found"
            else:
                command = "python3 ./showrepeats_2.py -rn " + rn + " -m " + str(gm) + " -w " + str(gw) + " -a " + str(ga) + " -b " + str(gb) + " -s " + myseq
            subprocess.call(command, shell=True)
            with open("repeat_found", 'rb') as f:
                repeatfound = f.read()
            print(repeatfound)
        
        raise web.seeother('/repeat')

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
