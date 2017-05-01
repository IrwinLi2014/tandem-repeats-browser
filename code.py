import web
import shutil
import subprocess
render = web.template.render('webpage/')

urls = (
    '/', 'index',
    '/upload', 'Upload'
)

class index:
    def GET(self):
        return render.index()


#class Upload:
#    def GET(self):
#        return """<html><head></head><body>
#<form method="POST" enctype="multipart/form-data" action="">
#<input type="file" id="myfile "name="myfile" />
#<br/>
#<input type="submit" />
#</form>
#</body></html>

    def POST(self):
        x = web.input(myfile={}, alpha='ATCG', cutpasteyes='')
        command = "python3 ./tandem.py -m " + x.maxtolerance.encode('ascii','ignore') + " -w " + x.windowsize.encode('ascii','ignore') + " -a " + x.alpha.encode('ascii','ignore') + " -i input.fna"
	    print(command)
        if x.fileyes and x.myfile.file:
            destFile = open('./input.fna', 'wb')
            destFile.write(x.myfile.file.read())
            destFile.close()
        if x.cutpasteyes!='':
            command = "python3 ./tandem.py -m " + x.maxtolerance.encode('ascii','ignore') + " -w " + x.windowsize.encode('ascii','ignore') + " -a " + x.alpha.encode('ascii','ignore') + " -s " + x.seq.encode('ascii','ignore')
        subprocess.call(command, shell=True)
        #web.debug(x['myfile'].value) # This is the file contents
        #web.debug(x['myfile'].file.read()) # Or use a file(-like) object

	raise web.seeother('/')

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
