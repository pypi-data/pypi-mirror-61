===========================
Trainable Initial State RNN
===========================

.. image:: https://img.shields.io/pypi/pyversions/trainable-initial-state-rnn
    :target: https://pypi.org/project/trainable-initial-state-rnn
    :alt: Python Version

.. image:: https://img.shields.io/pypi/v/trainable-initial-state-rnn
    :target: https://pypi.org/project/trainable-initial-state-rnn
    :alt: PyPI Package Version

.. image:: https://img.shields.io/github/last-commit/artemmavrin/trainable-initial-state-rnn/master
    :target: https://github.com/artemmavrin/trainable-initial-state-rnn
    :alt: Last Commit

.. image:: https://github.com/artemmavrin/trainable-initial-state-rnn/workflows/Python%20package/badge.svg
    :target: https://github.com/artemmavrin/trainable-initial-state-rnn/actions?query=workflow%3A%22Python+package%22
    :alt: GitHub Actions Build Status

.. image:: https://codecov.io/gh/artemmavrin/trainable-initial-state-rnn/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/artemmavrin/trainable-initial-state-rnn
    :alt: Code Coverage

.. image:: https://readthedocs.org/projects/trainable-initial-state-rnn/badge/?version=latest
    :target: https://trainable-initial-state-rnn.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/github/license/artemmavrin/trainable-initial-state-rnn
    :target: https://github.com/artemmavrin/trainable-initial-state-rnn/blob/master/LICENSE
    :alt: License

Treat the initial state(s) of TensorFlow Keras recurrent neural network (RNN)
layers as a parameter or parameters to be learned during training, as recommended in, e.g., [1]_.

Ordinary RNNs use an all-zero initial state by default. Why not let the neural
network learn a smarter initial state?

The ``trainable-initial-state-rnn`` package provides a class
``TrainableInitialStateRNN`` that can wrap any ``tf.keras`` RNN (or
bidirectional RNN) and manage new initial state variables in addition to the
RNN's weights.

Typical usage looks as follows.

.. code-block:: python

    import tensorflow as tf
    from trainable_initial_state_rnn import TrainableInitialStateRNN

    base_rnn = tf.keras.layers.LSTM(256)
    rnn = TrainableInitialStateRNN(base_rnn)  # Treats initial state as a variable!

    model = tf.keras.Model(...)  # Use rnn like any other tf.keras layer in your model
    model.compile(...)
    history = model.fit(...)

Documentation is available at
`Read the Docs <https://trainable-initial-state-rnn.readthedocs.io/en/latest/>`__.

Installation
------------

1.  Requirements:

    * Python >= 3.7
    * TensorFlow >= 2.1

2.  The ``trainable_initial_state_rnn`` package can be installed using the
    `pip <https://pip.pypa.io/en/stable/>`__ utility directly from the package's
    `GitHub page <https://github.com/artemmavrin/trainable-initial-state-rnn>`__:

    .. code-block:: bash

        pip install git+https://github.com/artemmavrin/trainable-initial-state-rnn.git

    Alternatively, install a recent release from the
    `Python Package Index (PyPI) <https://pypi.org/project/trainable-initial-state-rnn>`__:

    .. code-block:: bash

        pip install trainable-initial-state-rnn

    **Note.** To install the project for development (e.g., to make changes to
    the source code), clone the project repository from GitHub and run
    :code:`make dev`:

    .. code-block:: bash

        git clone https://github.com/artemmavrin/trainable-initial-state-rnn.git
        cd trainable-initial-state-rnn
        # Optional but recommended: create and activate a new Python virtual environment
        make dev

    This will additionally install the requirements needed
    to run tests, check code coverage, and produce documentation.

References
----------

.. [1] Felix A. Gers, Nicol N. Schraudolph, Jürgen Schmidhuber. Learning Precise
    Timing with LSTM Recurrent Networks. Journal of Machine Learning Research 3
    (2002) 115-143. (`Link <http://www.jmlr.org/papers/v3/gers02a.html>`__)
