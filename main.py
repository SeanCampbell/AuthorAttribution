import webapp2
import features
import cloudstorage as gcs

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('New hello world again!')

class ApplyFeature(webapp2.RequestHandler):
    def get(self):
        text = self.request.get('text')
        n = int(self.request.get('n'))
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(features.character_ngrams(text, n))
        self.response.write(read(''))

class DocPage(webapp2.RequestHandler):
    def get(self):
        doc = self.request.get('doc')
        file_name = 'author_files/Adams/Defense1.txt'
        gcs_file = gcs.open(file_name)
        contents = gcs_file.read()
        gcs_file.close()
        self.response.write(contents)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/apply-feature', ApplyFeature),
    ('/show-doc', DocPage),
], debug=True)
