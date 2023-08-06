import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.linear_model import LogisticRegression
import keras

# TODO add docstrings
# TODO implement keywords properly


def tokenizer_filter(text, remove_punctuation=True, remove_stopwords=True, lemmatize=True,
                     lemmatize_pronouns=False):
    """
    :param text: (series) Text to process
    :param remove_punctuation: (bool) Strip all punctuation
    :param remove_stopwords: (bool) Remove all stopwords TODO enable custom stopword lists
    :param lemmatize: (bool) Lemmatize all words
    :param lemmatize_pronouns: (bool) lemmatize pronouns to -PRON-
    :return: (list) tokenized and processed text
    """

    import en_core_web_sm

    """
    Define filter
    """
    nlp = en_core_web_sm.load()
    docs = list(text)
    filtered_tokens = []
    if remove_stopwords and remove_punctuation:
        def token_filter(token):
            return not (token.is_punct | token.is_space | token.is_stop)
    elif remove_punctuation:
        def token_filter(token):
            return not (token.is_punct | token.is_space)
    elif remove_stopwords:
        def token_filter(token):
            return not (token.is_stop | token.is_space)
    else:
        def token_filter(token):
            return not token.is_space

    """
    Do filtering
    """

    if lemmatize and lemmatize_pronouns:
        for doc in nlp.pipe(docs, n_threads=-1, batch_size=10000):
            tokens = [token.lemma_.lower() for token in doc if token_filter(token)]
            filtered_tokens.append(tokens)
        return filtered_tokens
    elif lemmatize:
        for doc in nlp.pipe(docs):
            # pronouns lemmatize to -PRON- which is undesirable when using pre-trained embeddings
            tokens = [token.lemma_.lower() if token.lemma_ != '-PRON-'
                      else token.lower_ for token in doc if token_filter(token)]
            filtered_tokens.append(tokens)
        return filtered_tokens
    else:
        # lemmatizing pronouns to -PRON- is desirable when not using pre-trained embeddings
        for doc in nlp.pipe(docs):
            tokens = [token.lower_ for token in doc if token_filter(token)]
            filtered_tokens.append(tokens)
        return filtered_tokens


class SentimentAnalyzer:
    def __init__(self, bow_param=None, lstm_param=None, glove_param=None, glove_index=None):
        """
        Constructor for SentimentAnalyzer module
        :param BoW: (bool)
        """
        self.BoW_classifier = None
        self.LSTM_GloVE_classifier = None
        self.LSTM_classifier = None

        self.bow_param = bow_param
        self.lstm_param = lstm_param
        self.glove_param = glove_param
        self.glove_index = glove_index

    def fit(self, X, y):
        """
        Fits the enabled models onto X. Note that this rebuilds the models, as it is not currently possible to update
        the tokenizers
        :param X: (array) Feature matrix
        :param y: (vector) Targets
        :return:
        """

        if self.glove_param is not None:
            self.LSTM_GloVE_classifier = self.GloVE_Model(glove_index=self.glove_index, **self.glove_param)
            self.LSTM_GloVE_classifier.fit(X, y)

        if self.bow_param is not None:
            self.BoW_classifier = self.BoW_Model(**self.bow_param)
            self.BoW_classifier.fit(X, y)

        if self.lstm_param is not None:
            self.LSTM_classifier = self.LSTM_Model(**self.lstm_param)
            self.LSTM_classifier.fit(X, y)

    def refine(self, X, y):
        """
        Refits the trained models onto additional data. Not that this does NOT retrain the tokenizers, so it will not
        retrain the vocabulary
        :param X: (array) Feature matrix
        :param y: (vector) Targets
        """

        if self.glove_param is not None:
            self.LSTM_GloVE_classifier = self.GloVE_Model(glove_index=self.glove_index, **self.glove_param)
            self.LSTM_GloVE_classifier.refine(X, y)

        if self.bow_param is not None:
            self.BoW_classifier = self.BoW_Model(**self.bow_param)
            self.BoW_classifier.refine(X, y)

        if self.lstm_param is not None:
            self.LSTM_classifier = self.LSTM_Model(**self.lstm_param)
            self.LSTM_classifier.refine(X, y)

    def predict(self, X):
        """
        Predicts the sentiment of some
        :param X:
        :return:
        """
        prediction = []
        if self.bow_param is not None:
            prediction.append(self.BoW_classifier.predict(X).reshape(-1))
        if self.glove_param is not None:
            prediction.append(self.LSTM_GloVE_classifier.predict(X).reshape(-1))
        if self.lstm_param is not None:
            prediction.append(self.LSTM_classifier.predict(X).reshape(-1))

        return np.round(np.mean(prediction, axis=0))

    class BoW_Model:

        def __init__(self, vocab_size=100000, max_iter=10000, **kwargs):
            """
            Constructor for BoW_Model
            :param vocab_size: (int) Maximum vocabulary size. Default 1E6
            :param max_iter: (int) Maximum number of fit iterations
            """
            # TODO test effect of vocab_size

            self.vectorizer = None
            self.classifier = None
            self.vocab_size = vocab_size
            self.max_iter = max_iter

        def fit(self, train_data, y):
            """
            Fit the model (from scratch)
            :param train_data: (List-like) List of strings to train on
            :param y: (vector) Targets
            """

            filtered_data = tokenizer_filter(train_data, remove_punctuation=True, remove_stopwords=True, lemmatize=True)

            self.vectorizer = TfidfVectorizer(analyzer=str.split, max_features=self.vocab_size)
            cleaned_data = [' '.join(tweet) for tweet in filtered_data]
            X = self.vectorizer.fit_transform(cleaned_data)
            self.classifier = LogisticRegression(random_state=0, max_iter=self.max_iter).fit(X, y)
            self.classifier.fit(X, y)

        def refine(self, train_data, y):
            """
            Train the models further
            :param train_data: (List-like) List of strings to train on
            :param y: (vector) Targets
            """

            filtered_data = tokenizer_filter(train_data, remove_punctuation=True, remove_stopwords=True, lemmatize=True)

            cleaned_data = [' '.join(tweet) for tweet in filtered_data]
            X = self.vectorizer.transform(cleaned_data)
            self.classifier = LogisticRegression(random_state=0, max_iter=self.max_iter).fit(X, y)
            self.classifier.fit(X, y)

        def predict(self, data):
            """
            Makes predictions
            :param data: (List-like) List of strings to predict sentiment
            :return: (vector) Un-binarized Predictions 
            """
            if self.classifier is None:
                raise ValueError('Model has not been trained!')
            filtered_data = tokenizer_filter(data, remove_punctuation=True, remove_stopwords=True, lemmatize=True)
            cleaned_data = [' '.join(tweet) for tweet in filtered_data]
            X = self.vectorizer.transform(cleaned_data)
            return self.classifier.predict(X)

    class GloVE_Model:

        def __init__(self, glove_index, max_length=25, vocab_size=1000000, max_iter=100, batch_size=10000, neurons=100,
                     dropout=0.2, rec_dropout=0.2, activ='hard_sigmoid', optimizer='adam', **kwargs):
            """
            Constructor for LSTM classifier using pre-trained embeddings
            :param glove_index: (dict) Embedding dictionary
            :param max_length: (int) Maximum text length, ie, number of temporal nodes. Default 25
            :param vocab_size: (int) Maximum vocabulary size. Default 1E7
            :param max_iter: (int) Number of training epochs. Default 100
            :param neurons: (int) Depth (NOT LENGTH) of LSTM network. Default 100
            :param dropout: (float) Dropout
            :param activ: (String) Activation function (for visible layer). Default 'hard_sigmoid'
            :param optimizer: (String) Optimizer. Default 'adam'
            """
            # TODO infer embed_vec_len from glove_index

            self.max_length = max_length
            self.glove_index = glove_index
            self.max_iter = max_iter
            self.vocab_size = vocab_size
            self.neurons = neurons
            self.dropout = dropout
            self.rec_dropout = rec_dropout
            self.activ = activ
            self.optimizer = optimizer
            self.batch_size = batch_size
            self.embed_vec_len = 200

            self.vectorizer = None
            self.classifier = None
            self.word_index = None
            self.embedding_matrix = None

        def fit(self, train_data, y, **kwargs):
            """
            :param train_data:
            :param y:
            :param max_iter:
            :param vocab_size:
            :return:
            """

            """
            # Preprocess and tokenize text
            """

            filtered_data = tokenizer_filter(train_data, remove_punctuation=False, remove_stopwords=False,
                                             lemmatize=True)
            cleaned_data = [' '.join(tweet) for tweet in filtered_data]
            self.tokenizer = Tokenizer(num_words=self.vocab_size)

            self.tokenizer.fit_on_texts(cleaned_data)
            train_sequences = self.tokenizer.texts_to_sequences(cleaned_data)

            self.word_index = self.tokenizer.word_index
            print('Found %s unique tokens.' % len(self.word_index))

            X = pad_sequences(train_sequences, maxlen=self.max_length, padding='pre')

            self.embedding_matrix = np.zeros((len(self.word_index) + 1, self.embed_vec_len))
            for word, i in self.word_index.items():
                embedding_vector = self.glove_index.get(word)
                if embedding_vector is not None:
                    # words not found in embedding index will be all-zeros.
                    self.embedding_matrix[i] = embedding_vector

            neurons = self.neurons  # Depth (NOT LENGTH) of LSTM network
            dropout = self.dropout  # Dropout - around 0.25 is probably best
            rec_dropout = self.rec_dropout
            activ = self.activ
            costfunction = 'binary_crossentropy'

            """
            Create LSTM model
            """

            print("Creating LSTM model")
            init = keras.initializers.glorot_uniform(seed=1)
            optimizer = self.optimizer

            # TODO input_dim is kludged, MUST FIX - should be able to trim embedding matrix in embed_glove.py

            self.classifier = keras.models.Sequential()

            self.classifier.add(keras.layers.embeddings.Embedding(input_dim=len(self.word_index) + 1,
                                                                  output_dim=self.embed_vec_len,
                                                                  input_length=self.max_length,
                                                                  mask_zero=True, trainable=False,
                                                                  embeddings_initializer=keras.initializers.Constant(
                                                                      self.embedding_matrix)))
            self.classifier.add(keras.layers.SpatialDropout1D(dropout))
            self.classifier.add(keras.layers.LSTM(units=neurons, input_shape=(self.max_length, self.embed_vec_len),
                                                  kernel_initializer=init, dropout=dropout,
                                                  recurrent_dropout=rec_dropout))
            self.classifier.add(keras.layers.Dense(units=1, kernel_initializer=init, activation=activ))
            self.classifier.compile(loss=costfunction, optimizer=optimizer, metrics=['acc'])
            print(self.classifier.summary())
            self.classifier.fit(X, y, batch_size=self.batch_size, epochs=self.max_iter, verbose=1)

            def refine(self, train_data, y, **kwargs):
                """
                Train model further
                :param train_data:
                :param y:
                :param max_iter:
                :param vocab_size:
                :return:
                """

                """
                # Preprocess and tokenize text
                """

                filtered_data = tokenizer_filter(train_data, remove_punctuation=False, remove_stopwords=False,
                                                 lemmatize=True)
                cleaned_data = [' '.join(tweet) for tweet in filtered_data]
                train_sequences = self.tokenizer.texts_to_sequences(cleaned_data)

                X = pad_sequences(train_sequences, maxlen=self.max_length, padding='pre')

                self.classifier.fit(X, y, batch_size=self.batch_size, epochs=self.max_iter, verbose=1)

        def predict(self, data):
            from keras.preprocessing.sequence import pad_sequences
            if self.tokenizer is None:
                raise ValueError('Model has not been trained!')
            filtered_data = tokenizer_filter(data, remove_punctuation=True, remove_stopwords=True, lemmatize=True)
            cleaned_data = [' '.join(tweet) for tweet in filtered_data]
            X = pad_sequences(self.tokenizer.texts_to_sequences(cleaned_data), maxlen=self.max_length)
            return self.classifier.predict(X)

    class LSTM_Model:

        def __init__(self, max_length=25, vocab_size=1000000, max_iter=25, neurons=50,
                     dropout=0.25, rec_dropout=0.25, activ='hard_sigmoid', optimizer='adam', batch_size=10000, **kwargs):
            """
            Constructor for LSTM classifier using pre-trained embeddings
            :param max_length: (int) Maximum text length, ie, number of temporal nodes. Default 25
            :param vocab_size: (int) Maximum vocabulary size. Default 1E7
            :param max_iter: (int) Number of training epochs. Default 100
            :param neurons: (int) Depth (NOT LENGTH) of LSTM network. Default 100
            :param dropout: (float) Dropout
            :param activ: (String) Activation function (for visible layer). Default 'hard_sigmoid'
            :param optimizer: (String) Optimizer. Default 'adam'
            """
            # TODO infer embed_vec_len from glove_index

            self.max_length = max_length
            self.max_iter = max_iter
            self.batch_size = batch_size
            self.vocab_size = vocab_size
            self.neurons = neurons
            self.dropout = dropout
            self.rec_dropout = rec_dropout
            self.activ = activ
            self.optimizer = optimizer

            self.embed_vec_len = 200

            self.vectorizer = None
            self.classifier = None
            self.word_index = None
            self.embedding_matrix = None

        def fit(self, train_data, y, **kwargs):
            """
            :param train_data:
            :param y:
            :param max_iter:
            :param vocab_size:
            :return:
            """

            """
            # Preprocess and tokenize text
            """

            filtered_data = tokenizer_filter(train_data, remove_punctuation=False, remove_stopwords=False,
                                             lemmatize=True)
            cleaned_data = [' '.join(tweet) for tweet in filtered_data]
            self.tokenizer = Tokenizer(num_words=self.vocab_size)

            self.tokenizer.fit_on_texts(cleaned_data)
            train_sequences = self.tokenizer.texts_to_sequences(cleaned_data)

            self.word_index = self.tokenizer.word_index
            print('Found %s unique tokens.' % len(self.word_index))

            X = pad_sequences(train_sequences, maxlen=self.max_length, padding='pre')

            neurons = self.neurons  # Depth (NOT LENGTH) of LSTM network
            dropout = self.dropout  # Dropout - around 0.25 is probably best
            rec_dropout = self.rec_dropout
            activ = self.activ
            costfunction = 'binary_crossentropy'

            """
            Create LSTM model
            """

            print("Creating LSTM model")
            init = keras.initializers.glorot_uniform(seed=1)
            optimizer = self.optimizer

            # TODO input_dim is kludged, MUST FIX - should be able to trim embedding matrix in embed_glove.py

            self.classifier = keras.models.Sequential()

            self.classifier.add(keras.layers.embeddings.Embedding(input_dim=len(self.word_index) + 1,
                                                                  output_dim=self.embed_vec_len,
                                                                  input_length=self.max_length,
                                                                  mask_zero=True,
                                                                  embeddings_initializer=keras.initializers.glorot_normal(seed=None)))
            self.classifier.add(keras.layers.SpatialDropout1D(dropout))
            self.classifier.add(keras.layers.LSTM(units=neurons, input_shape=(self.max_length, self.embed_vec_len),
                                                  kernel_initializer=init, dropout=dropout,
                                                  recurrent_dropout=rec_dropout))
            self.classifier.add(keras.layers.Dense(units=1, kernel_initializer=init, activation=activ))
            self.classifier.compile(loss=costfunction, optimizer=optimizer, metrics=['acc'])
            print(self.classifier.summary())
            self.classifier.fit(X, y, batch_size=self.batch_size, epochs=self.max_iter, verbose=1)

        def refine(self, train_data, y, **kwargs):
            """
            Train model further
            :param train_data:
            :param y:
            :param max_iter:
            :param vocab_size:
            :return:
            """

            """
            # Preprocess and tokenize text
            """

            filtered_data = tokenizer_filter(train_data, remove_punctuation=False, remove_stopwords=False,
                                             lemmatize=True)
            cleaned_data = [' '.join(tweet) for tweet in filtered_data]
            train_sequences = self.tokenizer.texts_to_sequences(cleaned_data)

            X = pad_sequences(train_sequences, maxlen=self.max_length, padding='pre')

            self.classifier.fit(X, y, batch_size=self.batch_size, epochs=self.max_iter, verbose=1)

        def predict(self, data):
            from keras.preprocessing.sequence import pad_sequences
            if self.tokenizer is None:
                raise ValueError('Model has not been trained!')
            filtered_data = tokenizer_filter(data, remove_punctuation=True, remove_stopwords=True, lemmatize=True)
            cleaned_data = [' '.join(tweet) for tweet in filtered_data]
            X = pad_sequences(self.tokenizer.texts_to_sequences(cleaned_data), maxlen=self.max_length)
            return self.classifier.predict(X)
