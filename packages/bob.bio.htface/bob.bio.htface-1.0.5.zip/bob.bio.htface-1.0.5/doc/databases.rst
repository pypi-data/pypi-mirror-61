.. vim: set fileencoding=utf-8 :
.. Tiago de Freitas Pereira <tiago.pereira@idiap.ch>


=============================
 Heterogeneous Face Databases
=============================


CUHK Face Sketch Database (CUFS)
--------------------------------
.. _db-CUHK-CUFS:


CUHK Face Sketch database (`CUFS <http://mmlab.ie.cuhk.edu.hk/archive/facesketch.html>`_) is composed by viewed sketches.
It includes 188 faces from the Chinese University of Hong Kong (CUHK) student database, 123 faces from the `AR database <http://www2.ece.ohio-state.edu/~aleix/ARdatabase.html>`_ and 295 faces from the `XM2VTS database <http://www.ee.surrey.ac.uk/CVSSP/xm2vtsdb/>`_.

There are 606 face images in total. 
For each face image, there is a sketch drawn by an artist based on a photo taken in a frontal pose, under normal lighting condition and with a neutral expression.

There is no evaluation protocol established for this database.
Each work that uses this database implements a different way to report the results.
In [Wang2009]_ the 606 identities were split in three sets (153 identities for training, 153 for development, 300 for evaluation).
The rank-1 identification rate in the evaluation set is used as performance measure.
Unfortunately the file names for each set were not distributed.

In [Klare2013]_ the authors created a protocol based on a 5-fold cross validation splitting the 606 identities in two sets with 404 identities for training and 202 for testing.
The average rank-1 identification rate is used as performance measure.
In [Bhatt2012]_, the authors evaluated the error rates using only the pairs (VIS -- Sketch) corresponding to the CUHK Student Database and AR Face Database and in [Bhatt2010]_ the authors used only the pairs corresponding to the CUHK Student Database.
In [Yi2015]_ the authors created a protocol based on a 10-fold cross validation splitting the 606 identities in two sets with 306 identities for training and 300 for testing.
Also the average rank-1 identification error rate in the test is used to report the results.
Finally in [Roy2016]_, since the method does not requires a background model, the whole 606 identities were used for evaluation and also to tune the hype-parameters; which is not a good practice in machine learning.
Just by reading what is written in the paper (no source code available), we can claim that the evaluation is biased.

For comparison reasons, we will follow the same strategy as in [Klare2013]_ and do a 5 fold cross-validation splitting the 606 identities in two sets with 404 identities for training and 202 for testing and use the average rank-1 identification rate, in the evaluation set as a metric.
For reproducibility purposes, this evaluation protocol is published in a python package `format <https://pypi.python.org/pypi/bob.db.cuhk_cufs>`_.
In this way future researchers will be able to reproduce exactly the same tests with the same identities in each fold (which is not possible today).


CASIA NIR-VIS 2.0 face database
-------------------------------

CASIA NIR-VIS 2.0 database [Li2013]_ offers pairs of mugshot images and their correspondent NIR photos. 
The images of this database were collected in four recording sessions: 2007 spring, 2009 summer, 2009 fall and 2010 summer, in which the first session is identical to the CASIA HFB database [Li2009]_. 
It consists of 725 subjects in total. 
There are [1-22] VIS and [5-50] NIR face images per subject.
The eyes positions are also distributed with the images.

This database has a well defined protocol and it is publicly available for `download <http://www.cbsr.ia.ac.cn/english/NIR-VIS-2.0-Database.html>`_.
We also organized this protocol in the same way as for CUFS database and it is also freely available for download `(bob.db.cbsr_nir_vis_2) <https://pypi.python.org/pypi/bob.db.cbsr_nir_vis_2>`_.
The average rank-1 identification rate in the evaluation set (called view 2) is used as an evaluation metric.



CUHK Face Sketch FERET Database (CUFSF)
---------------------------------------
.. _db-CUHK-CUFSF:

The CUHK Face Sketch FERET Database (CUFSF) is composed by viewed sketches.
It includes 1,194 face images from the `FERET database <http://www.itl.nist.gov/iad/humanid/feret/>`_ and theirs respectively sketch draw by an artist.

There is not an evaluation protocol established for this database.
Each work that uses this database implements a different way to report the results.
In [Zhang2011]_ the authors split the 1,194 identities in two sets with 500 identities for training and 694 for testing.
Unfortunately the file names for each set was not distributed.
The Verification Rate (**VR**) considering a False Acceptance Rate ($FAR$) of 0.1\% is used as a performance measure.
In [Lei2012]_ the authors split the 1,194 identities in two sets with 700 identities for training and 494 for testing.
The rank-1 identification rate is used as performance measures.
We also organized this protocol in the same way as for CUFS database and it is also freely available for download `(bob.db.cuhk_cufsf) <https://pypi.python.org/pypi/bob.db.cuhk_cufsf>`_.



Long Distance Heterogeneous Face Database
-----------------------------------------

Long Distance Heterogeneous Face Database (LDHF-DB) contains pairs of VIS and NIR face images at distances of 60m, 100m, and 150m outdoors and at a 1m distance indoors of 100 subjects (70 males and 30 females).
For each subject one image was captured at each distance in daytime and nighttime. 
All the images of individual subjects are frontal faces without glasses, and collected in a single sitting.

The short distance visible light images (1m) were collected under a fluorescent light by using a DSLR camera with Canon F1.8 lens, and NIR images were collected using the modified DSLR camera and NIR illuminator of 24 IR LEDs without visible light.
Long distance (over 60m) VIS images were collected during the daytime using a telephoto lens coupled with a DSLR camera, and NIR images were collected using the DSLR camera with NIR light provided by RayMax300 illuminator.

For evaluation purposes, the authors of the database [Kang2014]_ defined a 10-fold cross validation with 90 subjects for training and 10 subjects for testing.
ROC (Receiver Operating Characteristic) and CMC (Cumulative Match Characteristic) were used for comparison.
For reproducibility purposes, the evaluation protocols of this database is freelly available in a python package `(bob.db.ldhf) <https://pypi.python.org/pypi/bob.db.ldhf>`_.


Pola Thermal
------------
.. _db-polathermal:

Collected by the U.S. Army Research Laboratory (ARL), the Polarimetric Thermal Face Database (first of this kind), contains polarimetric LWIR (longwave infrared) imagery and simultaneously acquired visible spectrum imagery from a set of 60 distinct subjects.

For the data collection, each subject was asked to sit in a chair and remove his or her glasses. 
A floor lamp with a compact fluorescent light bulb rated at 1550 lumens was placed 2m in front of the chair to illuminate the scene for 
the visible cameras and a uniform background was placed approximately 0.1m behind the chair.
Data was collected at three distances: Range 1 (2.5m), Range 2 (5m), and Range 3 (7.5m).
At each range, a baseline condition is first acquired where the subject is asked to maintain a neutral expression looking at the polarimetric thermal imager.
A second condition, which is referred as the "expressions" condition, was collected where the subject is asked to count out loud numerically from one upwards.
Counting orally results in a continuous range of motions of the mouth, and to some extent, the eyes, which can be recorded to produce variations in the facial imagery.
For each acquisition, 500 frames are recorded with the polarimeter (duration of 8.33 s at 60 fps), while 300 frames are recorded with each visible spectrum camera (duration of 10s at 30 fps).
For reproducibility purposes, the evaluation protocols of this database is freelly available in a python package `(bob.db.pola_thermal) <https://pypi.python.org/pypi/bob.db.pola_thermal>`_.


Near-Infrared and Visible-Light (NIVL) Dataset
----------------------------------------------
.. _db-nivl:


Collected by University of Notre Dame, the NIVL contains VIS and NIR face images from the same subjects.
The capturing process was carried out over the course of two semesters (fall 2011 and spring 2012).
The VIS images were collected using a Nikon D90 camera.
The Nikon D90 uses a :math:`23.6 \times 15.8` mm CMOS sensor and the resulting images have a :math:`4288 \times 2848` resolution.
The images were acquired using automatic exposure and automatic focus settings.
All images were acquired under normal indoor lighting at about a 5-foot standoff with frontal pose and a neutral facial expression.

The NIR images were acquired using a Honeywell CFAIRS system.
CFAIRS uses a modified Canon EOS 50D camera with a :math:`22.3 \times 14.9` CMOS sensor.
The resulting images have a resolution of :math:`4770 \times 3177`.
All images were acquired under normal indoor lighting with frontal pose and neutral facial expression.
NIR images were acquired at both a 5ft and 7ft standoff.

The dataset contains a total of 574 subjects.
There are a total of 2,341 VIS images and 22,264 NIR images from the 574 subjects.
A total of 402 subjects had both VIS and NIR images acquired during at least one session during both the fall and spring semesters.
Both VIS and NIR images were acquired in the same session, although not simultaneously.
For reproducibility purposes, the evaluation protocols of this database is freelly available in a python package `(bob.db.nivl) <https://pypi.python.org/pypi/bob.db.nivl>`_.


Cross Eye
---------
.. _db-cross-eye:

Collected by University of Reading, the Cross-Spectrum Iris/Periocular contains VIS and NIR periocular images from the same subjects form the left and right eyes.
The databseset contains data from only 20 subjects and has the following image distribution:

 - 8 VIS captures from the left eye
 - 8 NIR captures from the left eye
 - 8 VIS captures from the right eye
 - 8 NIR captures from the right eye

Such dataset was used in the context of the "2nd Cross-Spectrum Iris/Periocular Recognition Competition" and for that only the training set is released.
The test is in the possession of the owners in order to independently run evaluations.
Since we don't have access to the test set, we created our own evaluation protocols with the data available and such protocols are freelly available in a python package `(bob.db.pericrosseye) <https://pypi.python.org/pypi/bob.db.pericrosseyel>`_


The UoM-SGFS Database
---------------------

The UoM-SGFS database contains software generated sketches of 300 subjects in the Color-FERET database, created using the `EFIT-V <http://www.visionmetric.com/products/about-efit-v/>`_ software which is commonly used by law enforcement agencies.
The EFIT-V operator was trained by a qualified forensic scientist from the Malta Police Force so as to ensure that practices adopted in real-life were also used in the creation of the UoM-SGFS database.

This database contains two viewed sketches for each of the 300 subjects considered, and is thus partitioned into two sets, where each contains the sketch of one subject.
Set A contains those sketches created using EFIT-V where the number of steps performed in the program was minimised so as to lower the risk of producing composites that are overly similar to the original photo.
The average time taken to create sketches varied between approximately 30 to 45 minutes.
The sketches in Set A were then edited using the Corel PaintShop Pro X7 Image editing software to fine-tune details which cannot be easily modified with EFIT-V, yielding Set B. 
Consequently, sketches in Set B are generally closer in appearance to the original face-photos.
On average, editing spanned approximately 15 to 30 minutes only, to retain inaccuracies as found in real-life forensic sketches.
The Corel software was also used for sketches in Set A, but only to modify the hair component.
The EFIT-V software also allows the depiction of shoulders in the sketch, which can indicate the type of clothes that the perpetrator was wearing and the physique (e.g. fat, muscular, etc.).
While the type of clothing is important, more emphasis was given to correctly representing the physique of the subject since it provides more salient information.
In addition, any accessories such as jewellery and hats are generally slightly different to those shown in the original photograph and sometimes omitted in the UoM-SGFS sketches to mimic memory loss effect of eyewitnesses.


E-PRIP Database
---------------

The E-PRIP database contains 123 pairs of composite sketches and photographs taken from on from the AR Face dataset.
The composite sketches are split in four sets, which one created by a different subject.
One set is created by an American artist using `FACES <http://www.iqbiometrix.com/products_faces_40.html>`_ software, two sets of databases are created by Asian artist using both FACES and `Identi-Kit <http://identikit.net/>`_ tools, and one set is created by an Indian
artist using FACES software.


