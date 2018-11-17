import features
from google.appengine.api import app_identity
import lib.cloudstorage as gcs
import os
import webapp2

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
        bucket_name = os.environ.get(
            'BUCKET_NAME',
            app_identity.get_default_gcs_bucket_name())
        doc = self.request.get('doc')
        file_name = '/' + bucket_name + '/author_files/Adams/Defense1.txt'
        gcs_file = gcs.open(file_name)
        contents = gcs_file.read()
        gcs_file.close()
        self.response.write(contents)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/apply-feature', ApplyFeature),
    ('/show-doc', DocPage),
], debug=True)
