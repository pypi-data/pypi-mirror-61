.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_auto_examples_example_multinomial_group_lasso.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_example_multinomial_group_lasso.py:


A sample script for multinomial group lasso.



.. rst-class:: sphx-glr-horizontal


    *

      .. image:: /auto_examples/images/sphx_glr_example_multinomial_group_lasso_001.png
            :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/images/sphx_glr_example_multinomial_group_lasso_002.png
            :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/images/sphx_glr_example_multinomial_group_lasso_003.png
            :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/images/sphx_glr_example_multinomial_group_lasso_004.png
            :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/images/sphx_glr_example_multinomial_group_lasso_005.png
            :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/images/sphx_glr_example_multinomial_group_lasso_006.png
            :class: sphx-glr-multi-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Generating data
    Generating coefficients
    Generating logits
    Generating targets
    Starting fit
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
            Initial loss: 1.7936224528455498
    Completed iteration 0:
            Loss: 1.4092334973568785
            Weight difference: 0.5681574892999739
            Weight norm: 0.8851784605016452
            Grad: 0.6089689546833283
    Completed iteration 1:
            Loss: 1.1835608419866392
            Weight difference: 0.432176955695365
            Weight norm: 1.023912899301717
            Grad: 0.5040511585281371
    Completed iteration 2:
            Loss: 1.0050575040485148
            Weight difference: 0.4563195070635173
            Weight norm: 1.318889163212281
            Grad: 0.4020463537559594
    Completed iteration 3:
            Loss: 0.8860513508054781
            Weight difference: 0.424863205775863
            Weight norm: 1.6688198084964736
            Grad: 0.32617128117179534
    Completed iteration 4:
            Loss: 0.811298568876369
            Weight difference: 0.37019895520851254
            Weight norm: 2.009602682338297
            Grad: 0.2753409139240611
    Completed iteration 5:
            Loss: 0.7627631113649875
            Weight difference: 0.3222460844983854
            Weight norm: 2.3156793743969737
            Grad: 0.2408731588984712
    Completed iteration 6:
            Loss: 0.7307388665311213
            Weight difference: 0.27893699465983923
            Weight norm: 2.5809798138047877
            Grad: 0.21796317340230428
    Completed iteration 7:
            Loss: 0.7092287973356712
            Weight difference: 0.2396353070869662
            Weight norm: 2.8063063796633245
            Grad: 0.20248573829222702
    Completed iteration 8:
            Loss: 0.6945498325271625
            Weight difference: 0.20479550391055748
            Weight norm: 2.994692805526359
            Grad: 0.19169683047058014
    Completed iteration 9:
            Loss: 0.684485363555204
            Weight difference: 0.17453373800896016
            Weight norm: 3.149868721647772
            Grad: 0.18413080249918515
    /home/yngvem/Programming/morro/group-lasso/src/group_lasso/_fista.py:54: RuntimeWarning: The FISTA iterations did not converge to a sufficient minimum.
    You used subsampling then this is expected, otherwise,try to increase the number of iterations or decreasing the tolerance.
      RuntimeWarning,
    X shape: (10000, 470)
    Transformed X shape: (10000, 288)
    True intercept: [-0.63245553 -0.31622777  0.          0.31622777  0.63245553]
    Estimated intercept: [-0.48617977 -0.4053203  -0.06709269  0.21911066  0.7394821 ]
    Accuracy: 0.7301
    /home/yngvem/Programming/morro/group-lasso/examples/example_multinomial_group_lasso.py:103: UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.
      plt.show()






|


.. code-block:: default


    from group_lasso import MultinomialGroupLasso
    from utils import (
        get_groups_from_group_sizes,
        generate_group_lasso_coefficients,
    )
    import group_lasso._singular_values
    import group_lasso._group_lasso
    import numpy as np


    group_lasso._singular_values._DEBUG = True
    group_lasso._group_lasso._DEBUG = True


    if __name__ == "__main__":
        import matplotlib.pyplot as plt

        np.random.seed(0)

        group_sizes = [np.random.randint(5, 15) for i in range(50)]
        groups = get_groups_from_group_sizes(group_sizes)
        num_coeffs = sum(group_sizes)
        num_datapoints = 10000
        num_classes = 5
        noise_level = 1
        coeff_noise_level = 0.05

        print("Generating data")
        X = np.random.randn(num_datapoints, num_coeffs)
        intercept = np.arange(num_classes) * 10

        print("Generating coefficients")
        w = np.random.randn(num_coeffs, num_classes)
        for group in np.unique(groups):
            w[groups == group, :] *= np.random.random() > 0.3
        w += np.random.randn(*w.shape) * coeff_noise_level

        print("Generating logits")
        y = X @ w
        y += (
            np.random.randn(*y.shape)
            * noise_level
            / np.linalg.norm(y, axis=1, keepdims=True)
        )
        y += intercept

        print("Generating targets")
        p = np.exp(y) / (np.exp(y).sum(1, keepdims=True))
        z = [np.random.choice(np.arange(num_classes), p=pi) for pi in p]
        z = np.array(z)

        print("Starting fit")
        gl = MultinomialGroupLasso(
            groups=groups,
            n_iter=10,
            tol=1e-8,
            group_reg=5e-3,
            l1_reg=1e-4,
            fit_intercept=True,
        )
        gl.fit(X, z)

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
            plt.title("Normalised coefficients")
            plt.legend()

        plt.figure()
        plt.plot([w.min(), w.max()], [gl.coef_.min(), gl.coef_.max()], "gray")
        plt.scatter(w, gl.coef_, s=10)
        plt.ylabel("Learned coefficients")
        plt.xlabel("True coefficients")

        print("X shape: {shape}".format(shape=X.shape))
        print("Transformed X shape: {shape}".format(shape=gl.transform(X).shape))
        print(
            "True intercept: {intercept}".format(
                intercept=(intercept - intercept.mean())
                / np.linalg.norm(intercept - intercept.mean())
            )
        )
        print(
            "Estimated intercept: {intercept}".format(
                intercept=(gl.intercept_ - gl.intercept_.mean())
                / np.linalg.norm(gl.intercept_ - gl.intercept_.mean())
            )
        )
        print("Accuracy: {accuracy}".format(accuracy=np.mean(z == gl.predict(X))))
        plt.show()


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  2.083 seconds)


.. _sphx_glr_download_auto_examples_example_multinomial_group_lasso.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: example_multinomial_group_lasso.py <example_multinomial_group_lasso.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: example_multinomial_group_lasso.ipynb <example_multinomial_group_lasso.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
