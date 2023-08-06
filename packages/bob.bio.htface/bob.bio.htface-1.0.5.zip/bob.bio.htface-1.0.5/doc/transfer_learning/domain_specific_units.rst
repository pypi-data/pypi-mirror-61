.. vim: set fileencoding=utf-8 :
.. Tiago de Freitas Pereira <tiago.pereira@idiap.ch>


Domain Specific Units
---------------------

Many researchers pointed out that DCNNs progressively compute more powerful feature detectors as depth increases REF{Mallat2016}.
The authors from REF{Yosinski2014} and REF{Hongyang2015} demonstrated that feature detectors that are closer to the input signal (called low level features) are base features that resemble Gabor features, color blobs, edge detectors, etc.
On the other hand, features that are closer to the end of the neural network (called high level features) are considered to be more task specific and carry more discriminative power.

In :ref:`first insights section <first-insights>` we observed that the feature detectors from :math:`\mathcal{D}^s` (VIS) have some discriminative power over all three target domains we have tested; with VIS-NIR being the "easiest" ones and the VIS-Thermal being the most challenging ones.
With such experimental observations, we can draw the following hypothesis:

.. note::
   Given :math:`X_s=\{x_1, x_2, ..., x_n\}` and :math:`X_t=\{x_1, x_2, ..., x_n\}` being a set of samples from :math:`\mathcal{D}^s` and :math:`\mathcal{D}^t`, respectively, with their correspondent shared set of labels :math:`Y=\{y_1, y_2, ..., y_n\}` and :math:`\Theta` being all set of DCNN feature detectors from :math:`\mathcal{D}^s` (already learnt), there are two  consecutive subsets: one that is domain \textbf{dependent}, :math:`\theta_t`, and one that is domain \textbf{independent}, :math:`\theta_s`, where :math:`P(Y|X_s, \Theta) = P(Y|X_t, [\theta_s, \theta_t])`. Such :math:`\theta_t`, that can be learnt via back-propagation, is so called **Domain Specific Units**.


A possible assumption one can make is that :math:`\theta_t` is part of the set of low level features, directly connected to the input signal.
In this paper we test this assumption.
Figure bellow presents a general schematic of our proposed approach.
It is possible to observe that each image domain has its own specific set of feature detectors (low level features) and they share the same face space (high level features) that was previously learnt using VIS.

.. image:: ../img/DSU_general_schematic.png


Our approach consists in learning :math:`\theta_t`, for each target domain, jointly with the DCNN from the source domain.
In order to jointly learn :math:`\theta_t` with :math:`D_s` we propose two different architectural arrangements described in the next subsections.



Siamese DSU
***********

In the architecture described below, :math:`\theta_t` is learnt using Siamese Neural Networks REF{Chopra2005}.
During the forward pass, Figure (a), a pair of face images, one for each domain (either sharing the same identity or not), is passed through the DCNN.
The image from the source domain is passed through the main network (the one at the top in Figure (a)) and the image from the target domain is passed first to its domain specific set of feature detectors and then amended to the main network.
During the backward pass, Figure (b), errors are backpropagated only for :math:`\theta^t`.
With such structure only a small subset of feature detectors are learnt, reducing the capacity of the joint model.
The loss :math:`\mathcal{L}` is defined as:

:math:`\mathcal{L}(\Theta) = 0.5\Bigg[ (1-Y)D(x_s, x_t) + Y \max(0, m - D(x_s, x_t))\Bigg]`,
where :math:`m` is the contrastive margin, :math:`Y` is the label (1 when :math:`x_s` and :math:`x_t` belong to the same subject and 0 otherwise) and :math:`D` is defined as:

:math:`D(x_s, x_t) = || \phi(x_s) -  \phi(x_t)||_{2}^{2}`,
where :math:`\phi` are the embeddings from the jointly trained DCNN.


.. image:: ../img/DSU_siamese-0.png
.. image:: ../img/DSU_siamese-1.png

Results
-------

.. warning::

  Decribe the results from the paper


Understanding the Domain Specific Units
---------------------------------------

In this section we break down the covariate distribution of data points sensed in different image modalities layer by layer using tSNEs.

With these plots we expect to observe how data from different image modalities and different identities are organized along the DCNN transformations.

For each image domain we present: 
  - The covariate distribution using the base network as a reference (without any adaptation) in the **left** column.
  - The covariate distribution using the **best** DSU adapted network (for each database) in the **right** column.

For this analysis we make all the plots using the Inception Resnet v2 as a basis.


Pola Thermal
************

For this analysis, the columns on the right are generated using the :math:`\theta_{t[1-4]}` DSU.


Pixel level distribution
........................

Below we present the tSNE covariate distribution using the pixels as input.
Blue dots represent **VIS** samples and red dots represent **Thermal** samples.
It's possible to observe that images from different image modalities do cluster, which is an expected behaviour.

.. image:: ../plots/transfer-learning/understanding/THERMAL_pixel.png
   :width: 70%


Conv2d_1a_3x3 (:math:`\theta_{t[1-1]}` DSU adapted)
...................................................

Below we present the tSNE covariate distribution using the output of the first layer as input (:math:`\theta_{1-1}`).
We can observe that in the very first layer the identities are clustered for both, adapted and non adapted, DCNNs.
Moreover, the image modalities form two "big" clusters.


.. image:: ../plots/transfer-learning/understanding/THERMAL_NOadapt_1-4_1_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/THERMAL_adapt_1-4_1_flat.png
   :width: 45%


Conv2d_3b_1x1 (:math:`\theta_{t[1-2]}` DSU adapted)
...................................................

Below we present the tSNE covariate distribution using the output of the first layer as input (:math:`\theta_{1-2}`).
We can observe that in the very first layer the identities are clustered for both, adapted and non adapted, DCNNs.
Moreover, the image modalities form two "big" clusters.

.. image:: ../plots/transfer-learning/understanding/THERMAL_NOadapt_1-4_2_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/THERMAL_adapt_1-4_2_flat.png
   :width: 45%


Conv2d_4a_3x3 (:math:`\theta_{t[1-4]}` DSU adapted)
...................................................

Below we present the tSNE covariate distribution using the output of the first layer as input (:math:`\theta_{1-4}`).
We can observe that in the very first layer the identities are clustered for both, adapted and non adapted, DCNNs.
This is the last adapted layer for this setup and the image modalities are still organized in two different clusters, which is a behaviour that, at first glance, is not expected.


.. image:: ../plots/transfer-learning/understanding/THERMAL_NOadapt_1-4_4_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/THERMAL_adapt_1-4_4_flat.png
   :width: 45%


Mixed_5b (:math:`\theta_{t[1-5]}`)
..................................

From now, the layers are not DSU adapted.
Below we can observe the same behaviour as before.
Modalities are clustered in two "big" clusters and inside of these clusters, the identities are clustered.


.. image:: ../plots/transfer-learning/understanding/THERMAL_NOadapt_1-4_5b_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/THERMAL_adapt_1-4_5b_flat.png
   :width: 45%


Mixed_6a (:math:`\theta_{t[1-6]}`)
..................................

Below we can observe the same behaviour as before.
Modalities are clustered in two "big" clusters and inside of these clusters, the identities are clustered.

.. image:: ../plots/transfer-learning/understanding/THERMAL_NOadapt_1-4_6a_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/THERMAL_adapt_1-4_6a_flat.png
   :width: 45%


Mixed_7a
........

Below we can observe the same behaviour as before.
Modalities are clustered in two "big" clusters and inside of these clusters, the identities are clustered.


.. image:: ../plots/transfer-learning/understanding/THERMAL_NOadapt_1-4_7a_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/THERMAL_adapt_1-4_7a_flat.png
   :width: 45%

Conv2d_7b_1x1
.............

In the **left** tSNE (non DSU), we can observe the same behaviour as before.
However, in the tSNE on the **right** we can observe that images from the same identities, but different image modalities start to cluster.

.. image:: ../plots/transfer-learning/understanding/THERMAL_NOadapt_1-4_7b_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/THERMAL_adapt_1-4_7b_flat.png
   :width: 45%


PreLogitsFlatten
................

In the **left** tSNE (non DSU), we can observe the same behaviour as before.
However, in the tSNE on the **right** we can observe that images from the same identities, but different image modalities start to cluster.
We can use this layer as the final embedding.

.. image:: ../plots/transfer-learning/understanding/THERMAL_NOadapt_1-4_prelog_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/THERMAL_adapt_1-4_prelog_flat.png
   :width: 45%

Final Embedding
...............

In the **left** tSNE (non DSU), we can observe the same behaviour as before.
However, in the tSNE on the **right** we can observe that images from the same identities, but different image modalities start to cluster.
We can use this layer as the final embedding.

.. image:: ../plots/transfer-learning/understanding/THERMAL_NOadapt_1-4_emb_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/THERMAL_adapt_1-4_emb_flat.png
   :width: 45%



CUFSF
*****

For this analysis, the columns on the right is generated using the :math:`\theta_{t[1-5]}` DSU.


Pixel level distribution
........................

Below we present the tSNE covariate distribution using the pixels as input.
Blue dots represent **VIS** samples and red dots represents **Thermal** samples.
It's possible to observe that images from different image modalities do cluster, which is an expected behaviour.

.. image:: ../plots/transfer-learning/understanding/CUFSF_pixel.png
   :width: 70%


Conv2d_1a_3x3 (:math:`\theta_{t[1-1]}` DSU adapted)
...................................................

Below we present the tSNE covariate distribution using the output of the first layer as input (:math:`\theta_{1-1}`).
We can observe that in the very first layer the identities are clustered (**of course they are clustered, we have only one sample per identity/modality**) for both, adapted and non adapted, DCNNs.
Moreover, the image modalities form two "big" clusters.


.. image:: ../plots/transfer-learning/understanding/CUFSF_NOadapt_1-5_1_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/CUFSF_adapt_1-5_1_flat.png
   :width: 45%


Conv2d_3b_1x1 (:math:`\theta_{t[1-2]}` DSU adapted)
...................................................

Below we present the tSNE covariate distribution using the output of the first layer as input (:math:`\theta_{1-2}`).
We can observe that in the very first layer the identities are clustered (**of course they are clustered, we have only one sample per identity/modality**) for both, adapted and non adapted, DCNNs.
Moreover, the image modalities form two "big" clusters.

.. image:: ../plots/transfer-learning/understanding/CUFSF_NOadapt_1-5_2_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/CUFSF_adapt_1-5_2_flat.png
   :width: 45%


Conv2d_4a_3x3 (:math:`\theta_{t[1-4]}` DSU adapted)
...................................................

Below we present the tSNE covariate distribution using the output of the first layer as input (:math:`\theta_{1-4}`).
We can observe that in the very first layer the identities are clustered (**of course they are clustered, we have only one sample per identity/modality**) for both, adapted and non adapted, DCNNs.


.. image:: ../plots/transfer-learning/understanding/CUFSF_NOadapt_1-5_4_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/CUFSF_adapt_1-5_4_flat.png
   :width: 45%


Mixed_5b (:math:`\theta_{t[1-5]}` DSU adapted)
..............................................

From now, the layers are not DSU adapted.
Below we can observe the same behaviour as before.
This is the last adapted layer for this setup and the image modalities are still organized in two different clusters, which is a behaviour that, at first glance, is not expected.



.. image:: ../plots/transfer-learning/understanding/CUFSF_NOadapt_1-5_5_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/CUFSF_adapt_1-5_5_flat.png
   :width: 45%


Mixed_6a (:math:`\theta_{t[1-6]}`)
..................................

Below we can observe the same behaviour as before.
Modalities are clustered in two "big" clusters and inside of these clusters, the identities are clustered.

.. image:: ../plots/transfer-learning/understanding/CUFSF_NOadapt_1-5_6a_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/CUFSF_adapt_1-5_6a_flat.png
   :width: 45%


Mixed_7a
........

Below we can observe the same behaviour as before.
Modalities are clustered in two "big" clusters and inside of these clusters, the identities are clustered.


.. image:: ../plots/transfer-learning/understanding/CUFSF_NOadapt_1-5_7a_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/CUFSF_adapt_1-5_7a_flat.png
   :width: 45%

Conv2d_7b_1x1
.............

In the **left** tSNE (non DSU), we can observe the same behaviour as before.
However, in the tSNE on the **right** we can observe that images from the same identities, but different image modalities start to cluster.

.. image:: ../plots/transfer-learning/understanding/CUFSF_NOadapt_1-5_7b_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/CUFSF_adapt_1-5_7b_flat.png
   :width: 45%


PreLogitsFlatten
................

In the **left** tSNE (non DSU), we can observe the same behaviour as before.
However, in the tSNE on the **right** we can observe that images from the same identities, but different image modalities start to cluster.
We can use this layer as the final embedding.

.. image:: ../plots/transfer-learning/understanding/CUFSF_NOadapt_1-5_prelog_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/CUFSF_adapt_1-5_prelog_flat.png
   :width: 45%

Final Embedding
...............

In the **left** tSNE (non DSU), we can observe the same behaviour as before.
However, in the tSNE on the **right** we can observe that images from the same identities, but different image modalities start to cluster.
We can use this layer as the final embedding.

.. image:: ../plots/transfer-learning/understanding/CUFSF_NOadapt_1-5_emb_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/CUFSF_adapt_1-5_emb_flat.png
   :width: 45%




CUHK-CUFS
*********

For this analysis, the columns on the right is generated using the :math:`\theta_{t[1-5]}` DSU.


Pixel level distribution
........................

Below we present the tSNE covariate distribution using the pixels as input.
Blue dots represent **VIS** samples and red dots represents **Sketch** samples.
It's possible to observe that images from different image modalities do cluster, which is an expected behaviour.

.. image:: ../plots/transfer-learning/understanding/CUFS_pixel.png
   :width: 70%


Conv2d_1a_3x3 (:math:`\theta_{t[1-1]}` DSU adapted)
...................................................

Below we present the tSNE covariate distribution using the output of the first layer as input (:math:`\theta_{1-1}`).
We can observe that from this layer, in **both cases** (left and right), images from different image modalities belongs to the same cluster.
It's not possible to use a linear classifier to classify both modalities.
Moreover, the identities from different image modalities seems to form small clusters for some cases.
For information, this database has only **ONE** pair of images sensed in both modalities.


.. image:: ../plots/transfer-learning/understanding/CUFS_NOadapt_1-5_1_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/CUFS_adapt_1-5_1_flat.png
   :width: 45%


Conv2d_3b_1x1 (:math:`\theta_{t[1-2]}` DSU adapted)
...................................................

The same observation made in the last sub-section can be made for this case.

.. image:: ../plots/transfer-learning/understanding/CUFS_NOadapt_1-5_2_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/CUFS_adapt_1-5_2_flat.png
   :width: 45%


Conv2d_4a_3x3 (:math:`\theta_{t[1-4]}` DSU adapted)
...................................................

The same observation made in the last sub-section can be made for this case.

.. image:: ../plots/transfer-learning/understanding/CUFS_NOadapt_1-5_4_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/CUFS_adapt_1-5_4_flat.png
   :width: 45%


Mixed_5b (:math:`\theta_{t[1-5]}` DSU adapted )
...............................................

The same observation made in the last sub-section can be made for this case.

.. image:: ../plots/transfer-learning/understanding/CUFS_NOadapt_1-5_5_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/CUFS_adapt_1-5_5_flat.png
   :width: 45%


Mixed_6a (:math:`\theta_{t[1-6]}`)
..................................

The same observation made in the last sub-section can be made for this case.

.. image:: ../plots/transfer-learning/understanding/CUFS_NOadapt_1-5_6a_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/CUFS_adapt_1-5_6a_flat.png
   :width: 45%


Mixed_7a
........

The same observation made in the last sub-section can be made for this case.

.. image:: ../plots/transfer-learning/understanding/CUFS_NOadapt_1-5_7a_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/CUFS_adapt_1-5_7a_flat.png
   :width: 45%

Conv2d_7b_1x1
.............

The same observation made in the last sub-section can be made for this case.
Overall, the same observation made in the last sub-section can be made for this case.
We can observe some modality specific regions in the **left** plot, which can't be observed in the plot on the **right**.
Hence, it seems that the DSU has some effectiveness for this particular case.


.. image:: ../plots/transfer-learning/understanding/CUFS_NOadapt_1-5_7b_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/CUFS_adapt_1-5_7b_flat.png
   :width: 45%


PreLogitsFlatten
................

The same observation made in the last sub-section can be made for this case.
Overall, the same observation made in the last sub-section can be made for this case.
We can observe some modality specific regions in the **left** plot, which can't be observed in the plot on the **right**.
Hence, it seems that the DSU has some effectiveness for this particular case.



.. image:: ../plots/transfer-learning/understanding/CUFS_NOadapt_1-5_prelog_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/CUFS_adapt_1-5_prelog_flat.png
   :width: 45%

Final Embedding
...............

Overall, the same observation made in the last sub-section can be made for this case.
We can observe some modality specific regions in the **left** plot, which can't be observed in the plot on the **right**.
Hence, it seems that the DSU has some effectiveness for this particular case.


.. image:: ../plots/transfer-learning/understanding/CUFS_NOadapt_1-5_emb_flat.png
   :width: 45%
.. image:: ../plots/transfer-learning/understanding/CUFS_adapt_1-5_emb_flat.png
   :width: 45%



Triplet DSU
***********

In the architecture described in Figure below, :math:`\theta_t` is learnt using Triplet Neural Networks REF{Schroff2015}.
During the forward pass, Figure (a), a triplet of face images are presented as inputs to the network.
In its figure, :math:`x_s^{a}` consist of face images sensed in the source domain, and :math:`x_t^{p}` and :math:`x_t^{n}` are images sensed in the target domain, where :math:`x_s^{a}` and :math:`x_t^{p}` are from the same identity and :math:`x_s^{a}` and :math:`x_t^{n}` are from different identities.
As before, face images from the source domain are passed through the main network (the one at the top in Figure (a)) in  and face images from the target domain are passed first to its domain specific set of feature detectors and then amended to the main network.
During the backward pass, Figure (b), errors are backpropagated only for :math:`\theta^t`, that is shared between the inputs :math:`x_t^{p}` and :math:`x_t^{n}`.
With such structure only a small subset of features are learnt, reducing the capacity of the model.
The loss :math:`\mathcal{L}` is defined as:


:math:`\mathcal{L}(\theta) = ||\phi(x_s^{a}) - \phi(x_t^{p})||_2^{2} - ||\phi(x_s^{a}) - \phi(x_t^{n})||_2^{2}  + \lambda`,
where :math:`\lambda` is the triplet margin and :math:`\phi` are the embeddings from the DCNN.

.. image:: ../img/DSU_triplet-0.png
.. image:: ../img/DSU_triplet-1.png



For our experiments, two DCNN are chosen for :math:`D_s`: the Inception Resnet v1 and Inception Resnet v2.
Such networks presented one of the highest recognition rates under different image domains.
Since our target domains are one channel only, we selected the gray scaled version of it.
Details of such architecture is presented in the Supplementary Material.

Our task is to find the set of low level feature detectors, :math:`\theta_t`, that maximizes the recognition rates for each image domain.
In order to find such set, we exhaustively try, layer by layer (increasing the DCNN depth), adapting both Siamese and Triplet Networks.
Five possible :math:`\theta_t` sets are analysed and they are called :math:`\theta_{t[1-1]}`, :math:`\theta_{t[1-2]}`, :math:`\theta_{t[1-4]}`, :math:`\theta_{t[1-5]}` and :math:`\theta_{t[1-6]}`.
A full description of which layers compose :math:`\theta_t` is presented in the Supplementary material of the paper.
The Inception Resnet v2 architecture batch normalize REF[Ioffe2015] the forward signal for every layer.
For convolutions, such batch normalization step is defined, for each layer :math:`i`, as the following:

:math:`h(x) = \beta_i + \frac{g{(W_i * x)}  +  \mu_i}{\sigma_i}`,
where :math:`\beta` is the batch normalization offset (role of the biases), :math:`W` are the convolutional kernels, :math:`g` is the non-linear function applied to the convolution (ReLU activation), :math:`\mu` is the accumulated mean of the batch and :math:`\sigma` is the accumulated standard deviation of the batch.

In the Equation, two variables are updated via backpropagation, the values of the kernel (:math:`W`) and the offset (:math:`\beta`).
With these two variables, two possible scenarios for :math:`\theta_{t[1-n]}` are defined.
In the first scenario, we consider that :math:`\theta_{t[1-n]}` is composed by the set of batch normalization offsets (:math:`\beta`) only and the convolutional kernels :math:`W` are shared between :math:`\mathcal{D}_s` and :math:`\mathcal{D}_t`.
We may hypothesize that, since the target object that we are trying to model has the same structure among domains (frontal faces with neutral expression most of the time), the feature detectors for :math:`\mathcal{D}_s` and :math:`\mathcal{D}_t`, encoded in :math:`W`, are the same and just offsets need to be domain specific.
In this work such models are represented as :math:`\theta_{t[1-n]}(\beta)`.
In the second scenario, both :math:`W` and :math:`\beta` are made domain specific (updated via back-propagation) and they are represented as :math:`\theta_{t[1-n]}(\beta + W)`.

