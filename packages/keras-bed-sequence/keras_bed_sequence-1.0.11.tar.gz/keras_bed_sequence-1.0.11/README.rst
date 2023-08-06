keras_bed_sequence
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy|
|code_climate_maintainability| |pip| |downloads|

Lazily one-hot encoding bed sequences using Keras Sequence.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install keras_bed_sequence

Tests Coverage
----------------------------------------------
Since some software handling coverages sometimes get
slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|

Usage examples
------------------------
The following examples are tested within the package test suite.

Classification task example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Let's start by building an extremely simple classification task model:

.. code:: python

    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Flatten
    from keras_mixed_sequence import MixedSequence

    model = Sequential([
        Flatten(),
        Dense(1)
    ])
    model.compile(
        optimizer="nadam",
        loss="MSE"
    )

We then proceed to load the training data into Keras Sequences,
using, in particular, a MixedSequence object:

.. code:: python

    import numpy as np
    from keras_mixed_sequence import MixedSequence
    from keras_bed_sequence import BedSequence

    batch_size = 32
    bed_sequence = BedSequence(
        "hg19",
        "path/to/bed/files.bed",
        batch_size
    )
    y = the_output_values
    mixed_sequence = MixedSequence(
        x=bed_sequence,
        y=y,
        batch_size=batch_size
    )

Finally, we can proceed to use the obtained MixedSequence
to train our model:

.. code:: python

    model.fit_generator(
        mixed_sequence,
        steps_per_epoch=mixed_sequence.steps_per_epoch,
        epochs=2,
        verbose=0,
        shuffle=True
    )

Auto-encoding task example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Let's start by building an extremely simple auto-encoding task model:

.. code:: python

    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, Reshape, Conv2DTranspose

    model = Sequential([
        Reshape((200, 4, 1)),
        Conv2D(16, kernel_size=3, activation="relu"),
        Conv2DTranspose(1, kernel_size=3, activation="relu"),
        Reshape((-1, 200, 4))
    ])
    model.compile(
        optimizer="nadam",
        loss="MSE"
    )

We then proceed to load the training data into Keras Sequences,
using, in particular, a MixedSequence object:

.. code:: python

    import numpy as np
    from keras_mixed_sequence import MixedSequence
    from keras_bed_sequence import BedSequence

    batch_size = 32
    bed_sequence = BedSequence(
        "hg19",
        "path/to/bed/files.bed",
        batch_size
    )
    mixed_sequence = MixedSequence(
        x=bed_sequence,
        y=bed_sequence,
        batch_size=batch_size
    )

Finally, we can proceed to use the obtained MixedSequence
to train our model:

.. code:: python

    model.fit_generator(
        mixed_sequence,
        steps_per_epoch=mixed_sequence.steps_per_epoch,
        epochs=2,
        verbose=0,
        shuffle=True
    )

Multi-task example (classification + auto-encoding)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Let's start by building an extremely simple multi-tasks model:

.. code:: python

    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Dense, Conv2D, Reshape, Flatten, Conv2DTranspose, Input

    inputs = Input(shape=(200, 4))

    flattened = Flatten()(inputs)

    output1 = Dense(
        units=1,
        activation="relu",
        name="output1"
    )(flattened)

    hidden = Reshape((200, 4, 1))(inputs)
    hidden = Conv2D(16, kernel_size=3, activation="relu")(hidden)
    hidden = Conv2DTranspose(1, kernel_size=3, activation="relu")(hidden)
    output2 = Reshape((200, 4), name="output2")(hidden)

    model = Model(
        inputs=inputs,
        outputs=[output1, output2],
        name="my_model"
    )

    model.compile(
        optimizer="nadam",
        loss="MSE"
    )

We then proceed to load the training data into Keras Sequences,
using, in particular, a MixedSequence object:

.. code:: python

    import numpy as np
    from keras_mixed_sequence import MixedSequence
    from keras_bed_sequence import BedSequence

    batch_size = 32
    bed_sequence = BedSequence(
        "hg19",
        "{cwd}/test.bed".format(
            cwd=os.path.dirname(os.path.abspath(__file__))
        ),
        batch_size
    )
    y = np.random.randint(
        2,
        size=(bed_sequence.samples_number, 1)
    )
    mixed_sequence = MixedSequence(
        bed_sequence,
        {
            "output1": y,
            "output2": bed_sequence
        },
        batch_size
    )

Finally, we can proceed to use the obtained MixedSequence
to train our model:

.. code:: python

    model.fit_generator(
        mixed_sequence,
        steps_per_epoch=mixed_sequence.steps_per_epoch,
        epochs=2,
        verbose=0,
        shuffle=True
    )


.. |travis| image:: https://travis-ci.org/LucaCappelletti94/keras_bed_sequence.png
   :target: https://travis-ci.org/LucaCappelletti94/keras_bed_sequence
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_keras_bed_sequence&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_keras_bed_sequence
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_keras_bed_sequence&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_keras_bed_sequence
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_keras_bed_sequence&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_keras_bed_sequence
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/keras_bed_sequence/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/keras_bed_sequence?branch=master
    :alt: Coveralls Coverage

.. |pip| image:: https://badge.fury.io/py/keras-bed-sequence.svg
    :target: https://badge.fury.io/py/keras-bed-sequence
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/keras-bed-sequence
    :target: https://pepy.tech/badge/keras-bed-sequence
    :alt: Pypi total project downloads

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/6bb591f3d405443a9549967eac35b723
    :target: https://www.codacy.com/manual/LucaCappelletti94/keras_bed_sequence?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LucaCappelletti94/keras_bed_sequence&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/d601fb2c7485f1ac3433/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/keras_bed_sequence/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/d601fb2c7485f1ac3433/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/keras_bed_sequence/test_coverage
    :alt: Code Climate
