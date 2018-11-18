import features
#import lib.cloudstorage as gcs
import keras
import numpy as np
import os
import tensorflow as tf
import webapp2

from tensorflow.keras import layers
#from google.appengine.api import app_identity

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
        self.response.write('Hello world again!')

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

class ClassifyPage(webapp2.RequestHandler):
    def get(self):
        data = np.random.random((1000, 32))
        labels = np.random.random((1000, 10))

        inputs = tf.keras.Input(shape=(32,))
        x = layers.Dense(64, activation='relu')(inputs)
        x = layers.Dense(64, activation='relu')(x)
        predictions = layers.Dense(10, activation='softmax')(x)

        model = tf.keras.Model(inputs=inputs, outputs=predictions)
        model.compile(optimizer=tf.train.RMSPropOptimizer(0.001),
                        loss='categorical_crossentropy',
                        metrics=['accuracy'])
        model.fit(data, labels, batch_size=32, epochs=5)
        loss, acc = model.evaluate(data, labels)

        self.response.write('loss = %.2f, acc = %.2f' % (loss, acc))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/apply-feature', ApplyFeature),
    ('/show-doc', DocPage),
    ('/classify', ClassifyPage),
], debug=True)

def main():
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8080')

if __name__ == '__main__':
    main()
