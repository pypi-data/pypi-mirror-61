=========
DeepCINAC
=========

DeepCINAC stands for Deep Calcium Imaging Neuronal Activity Classifier.

It's a deep-learning-based Python toolbox for inferring calcium imaging neuronal activity based on movie visualization.

The code is currently being cleaned and documented so the toolbox could be easily used and work for a wide variety of data.

Keep it mind that it is still a **beta** version. The version 1.0 will be published by the 16th of February 2020 with a major documentation update.

Please let us know if you encounter any issue, we will be glad to help you.

Contact us at julien.denis3{at}gmail.com

BioRxiv paper
------------- 

https://www.biorxiv.org/content/10.1101/803726v1


Installation
------------

See the `installation page <https://deepcinac.readthedocs.io/en/latest/install.html>`_ of our documentation.


Documentation
-------------

Documentation of DeepCINAC can be found `here <https://deepcinac.readthedocs.io/en/latest/index.html>`_.


Establishing ground truth and visualising predictions
-----------------------------------------------------

.. image:: images/exploratory_GUI.png
    :width: 400px
    :align: center
    :alt: DeepCINAC screenshot

A GUI (Graphical User Interface) offers the tools to carefully examine the activity of each cell
over the course of the recording.

Allows to:

* Play the calcium imaging movie between any given frames, zoomed on a cell, with the traces scrolling.

* Display the source and transient profiles of cells and correlation of any transient profile with the source profiles of overlapped cells, such as described in `Gauthier et al. <https://www.biorxiv.org/content/10.1101/473470v1.abstract>`_.

* Select / deselect active periods, allowing to establish a ground truth.

* Display the predictions of the classifier 

* Diplay neuronal activity inferred using other methods.

* Save ground truth segments in the cinac file format.

* Indicate the cell type of any cell

Check-out this video for a quick overview of the GUI: http://www.youtube.com/watch?v=Pz7xAUqszME


**Follow our** `tutorial <https://deepcinac.readthedocs.io/en/latest/tutorial_gui.html>`_ **to get to know how to use the GUI.**

To launch the GUI execute this command in a terminal :

.. code::

    python -m deepcinac


Inferring neuronal activity
---------------------------

The classifier takes as inputs the motion corrected calcium imaging movie and spatial footprints of the sources (cells).

The outputs are float values between 0 and 1 for each frame and each source,
representing the probability for a cell to be active at that given frame.

The classifier we provide was trained to consider a cell as active during the rise time of its transients.

**On google colab**

If you just want to infer neuronal activity of your calcium imaging data
and you don't possess a GPU or don't want to go through the process of configuring your environment to make use of it,
you can run this `notebook <https://gitlab.com/cossartlab/deepcinac/tree/master/demos/notebooks/demo_deepcinac_predictions.ipynb>`_
using `google colab <https://colab.research.google.com>`_.

Google provides free virtual machines for you to use: with about 12GB RAM and 50GB hard drive space, and TensorFlow is pre-installed.

You will need a google account. Upload the notebook on google colab, then just follow the instructions in the notebook to go through.

**On your local device**

You can follow the steps described in this `demo file <https://gitlab.com/cossartlab/deepcinac/tree/master/demos/general/demo_deepcinac_predictions.py>`_. 

More informations in our `documentation <https://deepcinac.readthedocs.io/>`_.


Training your classifier to infer neuronal activity
---------------------------------------------------

Using the anotated .cinac files created with the GUI, you can now train your classifier.

Below are the few lines of codes needed to train the classifier:

.. code::

    cinac_model = CinacModel(results_path="/media/deepcinac/results",
                             n_epochs=20, batch_size=8)
    cinac_model.add_input_data_from_dir(dir_name="/media/deepcinac/data/cinac_ground_truth/for_training")
    cinac_model.prepare_model()
    cinac_model.fit()


Input data are the cinac files, you can either load all files in a directory 
or load files one by one. 

More detailed informations coming soon in our documentation, in addition to a notebook.

Predicting cell type
--------------------

Coming soon...

Training your classifier to predict cell type
---------------------------------------------

Training a classifier to predict cell type follow the same process as for 
predicting cell activity. 

You will need .cinac files with cell type annotated.

Here are the few lines of code to train it:

.. code::

    cinac_model = CinacModel(results_path="/media/deepcinac/results", 
                            n_epochs=10, 
                             verbose=1, batch_size=4,
                             cell_type_classifier_mode=True,
                             window_len=400, max_n_transformations=1,
                             max_height=10, max_width=10, 
                             lstm_layers_size=[64], bin_lstm_size=64,
                             overlap_value=0)
    cinac_model.add_input_data_from_dir(dir_name="/media/deepcinac/data/cinac_cell_type_ground_truth/for_training")
    cinac_model.prepare_model()
    cinac_model.fit()


Evaluating the performance of your classifier
---------------------------------------------

Coming soon...


Generating simulated calcium imaging movies
-------------------------------------------

**On google colab**

If you just want to generate simulated calcium imaging movie you can run
`this notebook <https://gitlab.com/cossartlab/deepcinac/tree/master/demos/notebooks/deepcinac_simulated_movie_generator.ipynb>`_
using `google colab <https://colab.research.google.com>`_.

**On your local device**

You can follow the steps described in `this demo file <https://gitlab.com/cossartlab/deepcinac/tree/master/demos/general/demo_deepcinac_simulated_movie_generator.py>`_.

**Examples**
You can download examples of simulated movies `here <https://gitlab.com/cossartlab/deepcinac/tree/master/demos/data/simulated_movies>`_.


