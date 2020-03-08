# Dependencies
import sys, getopt
import distutils.util
from flask import Flask, request, jsonify, render_template
import traceback
import ktrain
from ktrain import text
import tensorflow as tf
# from tensorflow import Graph, Session
# preprocessing functions
from preprocess import clean
from preprocess import remove_signs
from preprocess import lemm
from preprocess import remove_stopwords

#####
# Keras and Ktrain need to be running in their own class in order to work
# otherwise we get an issue with sessions and graphs
# see https://stackoverflow.com/questions/51127344/tensor-is-not-an-element-of-this-graph-deploying-keras-model
class BertModel:
    def __init__(self):
        self.session = tf.compat.v1.Session()
        self.graph = tf.compat.v1.get_default_graph() 
        self.model = None 
        # for some reason in a flask app the graph/session needs to be used in the init else it hangs on other threads
        with self.graph.as_default():
            with self.session.as_default():
                print("BERT Model initialised")
                logging.info("BERT Model initialised")

    def loadmodel(self, path=None):
        with self.graph.as_default():
            with self.session.as_default():
                try:
                    if path is not None:
                        # load the model
                        self.model = ktrain.load_predictor(path)
                    logging.info("Bert predictor loaded: ")
                    return True
                except Exception as e:
                    print(e)
                    logging.exception(e)
                    return False

    def predict_proba(self, X):
        with self.graph.as_default():
            with self.session.as_default():
                return self.model.predict_proba(X)

# Your API definition
app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/predict_bert_sentence', methods=['POST'])
def predict_sentence():
    if len(dt_cls) >= 1:
        try:
            #json_ = request.json
            text = request.form
            if debug == True:
                print("received text:\n{}\n".format(text))
            for key, value in text.items():
                logging.info("key: %s\nvalue:\n%s\n", key, value)
            ###
            # predict the received text
            ###
            dt_preds, dt_probas = predict_text(value)
            dt_response = {}
            dt_response['predictions'] = dt_preds
            dt_response['probabilities'] = dt_probas
            ###
            # now return all the predictions
            ###
            return jsonify(dt_response)
        except:
            return jsonify({'trace': traceback.format_exc()})

    else:
        print('Train the model first')
        return ('No model here to use')

@app.route('/predict_bert', methods=['POST'])
def predict():
    if len(dt_cls) >= 1:
        try:
            #json_ = request.json
            text = request.form
            if debug == True:
                print("received text:\n{}\n".format(text))
            for key, value in text.items():
                logging.info("key: %s\nvalue:\n%s\n", key, value)
            ###
            # predict the received text
            ###
            dt_preds, dt_probas = predict_text(value)
            ###
            # now return the original text and all the predictions
            ###
            return render_template('index.html', input_text=value, pred=dt_preds, probability=dt_probas)

        except:
            return jsonify({'trace': traceback.format_exc()})
    else:
        print('Train the model first')
        return ('No model here to use')

@app.route('/about/')
def about():
    return render_template('about.html')

def predict_text(value):
    # preprocess the given string
    # clean strings
    prepro = clean(value)
    if debug == True:
        print("clean() done:\n{}\n\n ".format(prepro))
        logging.debug("clean() done:\n%s\n\n ", prepro)
    # remove punctuation
    prepro = remove_signs(prepro)
    if debug == True:
        print("remove_signs() done:\n{}\n\n ".format(prepro))
        logging.debug("remove_signs() done:\n%s\n\n ", prepro)
    # lemmatize the text
    #prepro = lemm(prepro)
    #if debug == True:
    #    print("lemm() done:\n{}\n\n".format(prepro))
    #    logging.debug("lemm() done:\n%s\n\n", prepro)
    # remove stop words
    #prepro = remove_stopwords(prepro)
    #if debug == True:
    #    print("remove_stopwords() done:\n{}\n\n".format(prepro))
    #    logging.debug("remove_stopwords() done:\n%s\n\n", prepro)
    # preprocessing finished

    ####
    # predict with all available scikit models
    dt_preds = {}
    dt_probas = {}
    for mod_name, model in dt_cls.items():
        if debug == True:
            #print("predicting with model name: {} and model: {}".format(mod_name, model))
            logging.debug("predicting with model: %s", mod_name)

        proba = model.predict_proba(prepro)

        if proba[0] >= 0.5:
            pred = 'not abusive'
        else:
            pred = 'abusive'

        dt_preds[mod_name] = pred
        # confidence of correctness for current model
        # probability = "{0:.2%}".format(proba.max())
        dt_probas[mod_name] = proba.tolist() #probability
        if debug == True:
            print("dt_probas: {}".format(dt_probas))

    return (dt_preds, dt_probas)

if __name__ == '__main__':
    import logging
    logging.basicConfig(filename='flask_detecthate_bert_api.log', level=logging.DEBUG)

    debug = True
    port = 12346

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hd:p:", ["debug=", "port="])
    except getopt.GetoptError:
        print('test.py -d <debugflag> -p <port>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h': # print help how to use this python script
            print('test.py -d <debugflag> -p <port>')
            sys.exit()
        elif opt in ("-d", "--debug"): # set debug flag if given
            debug = bool(distutils.util.strtobool(arg))
        elif opt in ("-p", "--port"): # set port if given
            port = arg


    print("Debug flag is: ", debug)
    print("Port is: ", port)
    logging.info("Debug flag is: %s", debug)
    logging.info("Port is: %s", port)
    # Load all models that are available
    # prepare dictionaries and initialize path to models
    dt_cls = {}
    # path = "./models/"
    path = "./bert/"
    model_name = 'dectet_hatespeech_79000_ep_1_20200105'
    file = path + model_name

    # todo: initialize the bert_class here, similar to lstm class in previous flask_app
    #####
    # initialize bert classifiers
    #####

    if debug == True:
        print("bert model file: {}, model: {}\n".format(file, model_name))
    bert_model = BertModel()
    bert_model.loadmodel(file)
    dt_cls['bert'] = bert_model
    if debug == True:
        print("predicting default sentence: {}".format(bert_model.predict_proba('hello my little Darling')))
        print("predicting 2nd sentence: {}".format(bert_model.predict_proba('hello you nasty bitch')))



    if debug == True:
        # all scikit classifiers
        print("dt_cls: {}".format(dt_cls.keys()))

    app.run(host='0.0.0.0', port=port, debug=debug)
