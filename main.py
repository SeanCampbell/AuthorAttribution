import features
#import lib.cloudstorage as gcs
import os
import webapp2

#from google.appengine.api import app_identity
import tensorflow
import keras

'''
def read_gcs_file(file_path):
    bucket_name = os.environ.get(
        'BUCKET_NAME',
        app_identity.get_default_gcs_bucket_name())
    file_name = '/' + bucket_name + file_path
    gcs_file = gcs.open(file_name)
    contents = gcs_file.read()
    gcs_file.close()
    return contents
'''
# As far as I can tell, you can't read from GCS for an app running locally,
# so this lets us switch easily between the two.
# https://github.com/GoogleCloudPlatform/appengine-gcs-client/issues/54
def read_local_file(file_path):
    return open(file_path).read()

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
        #contents = read_gcs_file('/author_files/Adams/Defense1.txt')
        contents = read_local_file('author_files/Adams/Defense1.txt')
        self.response.write(contents)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/apply-feature', ApplyFeature),
    ('/show-doc', DocPage),
], debug=True)

def main():
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()
