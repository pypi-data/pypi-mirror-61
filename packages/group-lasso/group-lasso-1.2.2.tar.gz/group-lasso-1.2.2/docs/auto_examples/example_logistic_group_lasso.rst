.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_auto_examples_example_logistic_group_lasso.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_example_logistic_group_lasso.py:


A sample script that runs group lasso for logistic regression.



.. rst-class:: sphx-glr-horizontal


    *

      .. image:: /auto_examples/images/sphx_glr_example_logistic_group_lasso_001.png
            :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/images/sphx_glr_example_logistic_group_lasso_002.png
            :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/images/sphx_glr_example_logistic_group_lasso_003.png
            :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/images/sphx_glr_example_logistic_group_lasso_004.png
            :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/images/sphx_glr_example_logistic_group_lasso_005.png
            :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/images/sphx_glr_example_logistic_group_lasso_006.png
            :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/images/sphx_glr_example_logistic_group_lasso_007.png
            :class: sphx-glr-multi-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Generating data
    Generating coefficients
    Generating logits
    Generating targets
    Starting fit
    /home/yngvem/Programming/morro/group-lasso/src/group_lasso/_group_lasso.py:673: UserWarning: You have passed 2 targets to a single class classifier. This will simply train 2 different models meaning that multiple classes can be predicted as true at once.
      ).format(n=n)
    /home/yngvem/Programming/morro/group-lasso/src/group_lasso/_group_lasso.py:383: UserWarning: 
    The behaviour has changed since v1.1.1, before then, a bug in the optimisation
    algorithm made it so the regularisation parameter was scaled by the largest 
    eigenvalue of the covariance matrix.

    To use the old behaviour, initialise the class with the keyword argument 
    `old_regularisation=True`.

    To supress this warning, initialise the class with the keyword argument
    `supress_warning=True`

      warnings.warn(_OLD_REG_WARNING)
    Starting FISTA: 
            Initial loss: 1.5469933045630193
    Completed iteration 0:
            Loss: 1.2104737299414416
            Weight difference: 0.9443762628127634
            Weight norm: 0.8324221455638038
            Grad: 0.24870737019386993
    Completed iteration 1:
            Loss: 1.1293096614225477
            Weight difference: 0.45272828530236536
            Weight norm: 1.0956665292124017
            Grad: 0.16626800884384027
    Completed iteration 2:
            Loss: 1.0960272856147482
            Weight difference: 0.31879555610615284
            Weight norm: 1.3813446462334156
            Grad: 0.11984356968643563
    Completed iteration 3:
            Loss: 1.0818659171365028
            Weight difference: 0.22620115995914178
            Weight norm: 1.6012161702273917
            Grad: 0.09361360654126186
    Completed iteration 4:
            Loss: 1.0760839913023614
            Weight difference: 0.14821651374693584
            Weight norm: 1.748250012557008
            Grad: 0.07962102914468852
    Completed iteration 5:
            Loss: 1.0758889722113512
            Weight difference: 0.010296775767152794
            Weight norm: 1.7530816354842258
            Grad: 0.07905265192843676
    Completed iteration 6:
            Loss: 1.075758635974486
            Weight difference: 0.006378188245077589
            Weight norm: 1.7567628508281379
            Grad: 0.07866522633791057
    Completed iteration 7:
            Loss: 1.0756324461123972
            Weight difference: 0.00567308374359215
            Weight norm: 1.7606264529914977
            Grad: 0.07828605385712081
    Completed iteration 8:
            Loss: 1.0755259555244765
            Weight difference: 0.00431603966821332
            Weight norm: 1.7640802456995124
            Grad: 0.0779641637723975
    Completed iteration 9:
            Loss: 1.075446494235434
            Weight difference: 0.002953322547411224
            Weight norm: 1.7667648571034589
            Grad: 0.07772419672708429
    Completed iteration 10:
            Loss: 1.0754366056804587
            Weight difference: 0.00046924595097268257
            Weight norm: 1.7671306382067469
            Grad: 0.07769571709538842
    Completed iteration 11:
            Loss: 1.0754290609883368
            Weight difference: 0.000325769962621024
            Weight norm: 1.7674068038844315
            Grad: 0.07767377716810711
    Completed iteration 12:
            Loss: 1.0754211196332495
            Weight difference: 0.00032202670342592997
            Weight norm: 1.7676950955077648
            Grad: 0.0776505170734689
    Completed iteration 13:
            Loss: 1.0754139871652284
            Weight difference: 0.00027479989497381814
            Weight norm: 1.7679518041331712
            Grad: 0.07762948084579076
    Completed iteration 14:
            Loss: 1.07540840919371
            Weight difference: 0.00020736998798394818
            Weight norm: 1.7681508211913002
            Grad: 0.077612922377394
    Completed iteration 15:
            Loss: 1.0754076245665203
            Weight difference: 2.95868665242795e-05
            Weight norm: 1.7681778365889238
            Grad: 0.07761054337275429
    Completed iteration 16:
            Loss: 1.0754070339770558
            Weight difference: 2.191694410739497e-05
            Weight norm: 1.7681982973282901
            Grad: 0.0776087584551642
    Completed iteration 17:
            Loss: 1.0754064188770847
            Weight difference: 2.2642972351499354e-05
            Weight norm: 1.7682197090068033
            Grad: 0.0776069040682837
    Completed iteration 18:
            Loss: 1.0754058724024138
            Weight difference: 2.002972972791038e-05
            Weight norm: 1.7682388234228816
            Grad: 0.07760526070688431
    Completed iteration 19:
            Loss: 1.0754054496556755
            Weight difference: 1.5487540441188068e-05
            Weight norm: 1.7682536807937863
            Grad: 0.07760399260636042
    Completed iteration 20:
            Loss: 1.0754053927044391
            Weight difference: 2.1487224429666147e-06
            Weight norm: 1.7682557189712749
            Grad: 0.07760382345452645
    Completed iteration 21:
            Loss: 1.0754053495067593
            Weight difference: 1.620097912054739e-06
            Weight norm: 1.7682572610754945
            Grad: 0.07760369495953716
    Completed iteration 22:
            Loss: 1.075405304250348
            Weight difference: 1.6913901458021526e-06
            Weight norm: 1.7682588736720248
            Grad: 0.0776035601891484
    Completed iteration 23:
            Loss: 1.075405263803996
            Weight difference: 1.50780869101816e-06
            Weight norm: 1.7682603122761402
            Grad: 0.07760343960996673
    Completed iteration 24:
            Loss: 1.0754052323307624
            Weight difference: 1.1716209440522112e-06
            Weight norm: 1.7682614298324943
            Grad: 0.07760334568293635
    Completed iteration 25:
            Loss: 1.0754052279948918
            Weight difference: 1.6173091843438317e-07
            Weight norm: 1.7682615828707173
            Grad: 0.07760333269402486
    Completed iteration 26:
            Loss: 1.0754052247162498
            Weight difference: 1.2239468890247182e-07
            Weight norm: 1.768261698740912
            Grad: 0.07760332287897734
    Completed iteration 27:
            Loss: 1.0754052212892153
            Weight difference: 1.280547028935984e-07
            Weight norm: 1.7682618199760636
            Grad: 0.07760331262512404
    Completed iteration 28:
            Loss: 1.0754052182332137
            Weight difference: 1.143365928949507e-07
            Weight norm: 1.7682619281964715
            Grad: 0.07760330348631818
    Completed iteration 29:
            Loss: 1.075405215860119
            Weight difference: 8.893678074030635e-08
            Weight norm: 1.7682620123222073
            Grad: 0.07760329639352523
    Completed iteration 30:
            Loss: 1.075405215535582
            Weight difference: 1.2272000138931868e-08
            Weight norm: 1.7682620238754343
            Grad: 0.07760329542556182
    X shape: (100000, 470)
    Transformed X shape: (100000, 299)
    True intercept: 2
    Estimated intercept: [0.48654341 0.50288003]
    Accuracy: 0.789405
    /home/yngvem/Programming/morro/group-lasso/examples/example_logistic_group_lasso.py:106: UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.
      plt.show()






|


.. code-block:: default


    from group_lasso import LogisticGroupLasso
    from utils import (
        get_groups_from_group_sizes,
        generate_group_lasso_coefficients,
    )
    import group_lasso._singular_values
    import group_lasso._group_lasso
    import numpy as np


    group_lasso._singular_values._DEBUG = True
    group_lasso._group_lasso._DEBUG = True
    LogisticGroupLasso.LOG_LOSSES = True


    if __name__ == "__main__":
        import matplotlib.pyplot as plt

        np.random.seed(0)

        group_sizes = [np.random.randint(5, 15) for i in range(50)]
        groups = get_groups_from_group_sizes(group_sizes)
        num_coeffs = sum(group_sizes)
        num_datapoints = 100000
        noise_level = 1
        coeff_noise_level = 0.05

        print("Generating data")
        X = np.random.randn(num_datapoints, num_coeffs)
        intercept = 2

        print("Generating coefficients")
        w1 = generate_group_lasso_coefficients(group_sizes)
        w2 = generate_group_lasso_coefficients(group_sizes)
        w = np.hstack((w1, w2))
        w += np.random.randn(*w.shape) * coeff_noise_level

        print("Generating logits")
        y = X @ w
        y += np.random.randn(*y.shape) * noise_level * y
        y += intercept

        print("Generating targets")
        p = 1 / (1 + np.exp(-y))
        z = np.random.binomial(1, p)

        print("Starting fit")
        gl = LogisticGroupLasso(
            groups=groups,
            n_iter=100,
            tol=1e-8,
            group_reg=1e-3,
            l1_reg=1e-3,
            subsampling_scheme=1,
            fit_intercept=True,
        )
        gl.fit(X, z)

        for i in range(w.shape[1]):
            plt.figure()
            plt.plot(w[:, i], ".", label="True weights")
            plt.plot(gl.coef_[:, i], ".", label="Estimated weights")
            plt.legend()

        for i in range(w.shape[1]):
            plt.figure()
            plt.plot(
                w[:, i] / np.linalg.norm(w[:, i]),
                ".",
                label="Normalised true weights",
            )
            plt.plot(
                gl.coef_[:, i] / np.linalg.norm(gl.coef_[:, i]),
                ".",
                label="Normalised estimated weights",
            )
            plt.legend()

        plt.figure()
        plt.plot(gl.losses_)
        plt.title("Loss curve")
        plt.xlabel("Iteration")
        plt.ylabel("Loss")

        plt.figure()
        plt.plot(np.arange(1, len(gl.losses_)), gl.losses_[1:])
        plt.title("Loss curve, ommitting first iteration")
        plt.xlabel("Iteration")
        plt.ylabel("Loss")

        plt.figure()
        plt.plot([w.min(), w.max()], [gl.coef_.min(), gl.coef_.max()], "gray")
        plt.scatter(w, gl.coef_, s=10)
        plt.ylabel("Learned coefficients")
        plt.xlabel("True coefficients")

        print("X shape: {shape}".format(shape=X.shape))
        print("Transformed X shape: {shape}".format(shape=gl.transform(X).shape))
        print("True intercept: {intercept}".format(intercept=intercept))
        print("Estimated intercept: {intercept}".format(intercept=gl.intercept_))
        print("Accuracy: {accuracy}".format(accuracy=np.mean(z == gl.predict(X))))
        plt.show()


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  12.039 seconds)


.. _sphx_glr_download_auto_examples_example_logistic_group_lasso.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: example_logistic_group_lasso.py <example_logistic_group_lasso.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: example_logistic_group_lasso.ipynb <example_logistic_group_lasso.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
