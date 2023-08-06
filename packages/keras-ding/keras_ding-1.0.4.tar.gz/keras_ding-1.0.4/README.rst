keras_ding
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy| |code_climate_maintainability| |pip| |downloads|

Keras callback for playing a sound when training is complete. The callbacks additionally works also within jupyter notebook,
so that if you are working on a notebook on a remote machine it plays the audio within your browser and not in the server.

How do I install this package?
----------------------------------------------
You will need a couple packages that you might not already have installed:

.. code:: shell

    sudo apt install python3-dev
    sudo apt install libasound2-dev

Finally as usual, just download it using pip:

.. code:: shell

    pip install keras_ding

Tests Coverage
----------------------------------------------
Since some software handling coverages sometimes get slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|

Usage examples
-----------------------------------------------
So suppose you have your Keras model `my_keras_model` and you want to hear a sound when it is done training.
Here you go:

.. code:: python

    from keras_ding import Ding

    my_keras_model.fit(
        x, y,
        callbacks=[
            Ding()
        ]
    )

What abount a custom sound? Just pass it as an argument.

.. code:: python

    from keras_ding import Ding

    my_keras_model.fit(
        x, y,
        callbacks=[
            Ding(path="my_custom_sound.mp3")
        ]
    )


.. |travis| image:: https://travis-ci.org/LucaCappelletti94/keras_ding.png
   :target: https://travis-ci.org/LucaCappelletti94/keras_ding
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_keras_ding&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_keras_ding
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_keras_ding&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_keras_ding
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_keras_ding&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_keras_ding
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/keras_ding/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/keras_ding?branch=master
    :alt: Coveralls Coverage

.. |pip| image:: https://badge.fury.io/py/keras-ding.svg
    :target: https://badge.fury.io/py/keras-ding
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/keras-ding
    :target: https://pepy.tech/badge/keras-ding
    :alt: Pypi total project downloads 

.. |codacy|  image:: https://api.codacy.com/project/badge/Grade/0a2a0da8f69a4d2cb0f5065cadad8c87
    :target: https://www.codacy.com/manual/LucaCappelletti94/keras_ding?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LucaCappelletti94/keras_ding&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/34b3f4e943855bcc3a99/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/keras_ding/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/34b3f4e943855bcc3a99/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/keras_ding/test_coverage
    :alt: Code Climate Coverate