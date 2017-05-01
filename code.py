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
        x = web.input(myfile={}, alpha='ATCG')
        command = "python3 ./tandem.py -m %s -w %s -a %s -i input.fna", (x.maxtolerance, x.windowsize, x.alpha)
        if x.fileyes and x.myfile.file:
            destFile = open('./input.fna', 'wb')
            destFile.write(x.myfile.file.read())
            destFile.close()
        if x.cutpasteyes:
            command = "python3 ./tandem.py -m %s -w %s -a %s -s %s", (x.maxtolerance, x.windowsize, x.alpha, x.seq)
        subprocess.call(command, shell=True)
        #web.debug(x['myfile'].filename) # This is the filename
        #web.debug(x['myfile'].value) # This is the file contents
        #web.debug(x['myfile'].file.read()) # Or use a file(-like) object

	raise web.seeother('/')

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
