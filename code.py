import web
import shutil
render = web.template.render('webpage/')

urls = (
    '/', 'index',
    '/upload', 'Upload'
)

class index:
    def GET(self):
        return render.index()

    def POST(self):
        x = web.input(input_file={})
	if x.input_file.file:
            destFile = open('./input', 'wb')
            destFile.write(x.input_file.file.read())
            destFile.close()
        web.debug(x['input_file'].filename) # This is the filename
        web.debug(x['input_file'].value) # This is the file contents
        web.debug(x['input_file'].file.read()) # Or use a file(-like) object
        raise web.seeother('/upload')


class Upload:
    def GET(self):
        return """<html><head></head><body>
<form method="POST" enctype="multipart/form-data" action="">
<input type="file" id="myfile "name="myfile" />
<br/>
<input type="submit" />
</form>
</body></html>"""


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
