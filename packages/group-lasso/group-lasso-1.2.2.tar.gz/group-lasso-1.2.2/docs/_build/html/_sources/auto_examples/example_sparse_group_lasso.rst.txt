.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_auto_examples_example_sparse_group_lasso.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_example_sparse_group_lasso.py:


A sample script for group lasso regression



.. rst-class:: sphx-glr-horizontal


    *

      .. image:: /auto_examples/images/sphx_glr_example_sparse_group_lasso_001.png
            :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/images/sphx_glr_example_sparse_group_lasso_002.png
            :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/images/sphx_glr_example_sparse_group_lasso_003.png
            :class: sphx-glr-multi-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Generating data
    /home/yngvem/anaconda3/lib/python3.7/site-packages/sklearn/preprocessing/_encoders.py:415: FutureWarning: The handling of integer data will change in version 0.22. Currently, the categories are determined based on the range [0, max(values)], while in the future they will be determined based on the unique values.
    If you want the future behaviour and silence this warning, you can specify "categories='auto'".
    In case you used a LabelEncoder before this OneHotEncoder to convert the categories to integers, then you can now use the OneHotEncoder directly.
      warnings.warn(msg, FutureWarning)
    Generating coefficients
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
    X shape: (10000, 160)
    Transformed X shape: (10000, 120)
    True intercept: 2
    Estimated intercept: [1.49455008]
    /home/yngvem/Programming/morro/group-lasso/examples/example_sparse_group_lasso.py:92: UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.
      plt.show()






|


.. code-block:: default


    from group_lasso import GroupLasso
    from group_lasso.utils import extract_ohe_groups
    from utils import (
        get_groups_from_group_sizes,
        generate_group_lasso_coefficients,
    )
    import numpy as np
    from scipy import sparse
    from sklearn.preprocessing import OneHotEncoder
    import matplotlib.pyplot as plt


    GroupLasso.LOG_LOSSES = True


    if __name__ == "__main__":
        np.random.seed(1)

        num_categories = 20
        min_options = 2
        max_options = 10
        num_datapoints = 10000
        noise_level = 1
        coeff_noise_level = 0.2

        print("Generating data")
        X_cat = np.empty((num_datapoints, num_categories))
        for i in range(num_categories):
            X_cat[:,  i] = np.random.randint(min_options, max_options, num_datapoints)

        ohe = OneHotEncoder()
        X = ohe.fit_transform(X_cat)
        groups = extract_ohe_groups(ohe)
        group_sizes = [np.sum(groups == g) for g in np.unique(groups)]
        group_weights = [np.random.randint(0, 2) for _ in np.unique(groups)]

        intercept = 2

        print("Generating coefficients")
        w = np.concatenate(
            [weight*np.random.standard_normal(group_size) for weight, group_size in zip(group_weights, group_sizes)]
        ).reshape(-1, 1)
        w *= np.random.random((len(w), 1)) > 0.4
        w += np.random.randn(*w.shape) * coeff_noise_level

        print("Generating targets")
        y = X @ w
        y += np.random.randn(*y.shape) * noise_level * y
        y += intercept

        gl = GroupLasso(
            groups=groups,
            n_iter=1000,
            tol=1e-3,
            l1_reg=0,
            group_reg=0.02,
            frobenius_lipschitz=False,
            subsampling_scheme=None,
            fit_intercept=True,
        )
        print("Starting fit")
        gl.fit(X, y)

        for i in range(w.shape[1]):
            plt.figure()
            plt.subplot(211)
            plt.plot(w[:, i], ".", label="True weights")
            plt.plot(gl.coef_[:, i], ".", label="Estimated weights")

            plt.subplot(212)
            plt.plot(w[gl.sparsity_mask, i], ".", label="True weights")
            plt.plot(gl.coef_[gl.sparsity_mask, i], ".", label="Estimated weights")
            plt.legend()

        plt.figure()
        plt.plot([w.min(), w.max()], [gl.coef_.min(), gl.coef_.max()], "gray")
        plt.scatter(w, gl.coef_, s=10)
        plt.ylabel("Learned coefficients")
        plt.xlabel("True coefficients")

        plt.figure()
        plt.plot(gl.losses_)

        print("X shape: {X.shape}".format(X=X))
        print("Transformed X shape: {shape}".format(shape=gl.transform(X).shape))
        print("True intercept: {intercept}".format(intercept=intercept))
        print("Estimated intercept: {intercept}".format(intercept=gl.intercept_))
        plt.show()


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  0.862 seconds)


.. _sphx_glr_download_auto_examples_example_sparse_group_lasso.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: example_sparse_group_lasso.py <example_sparse_group_lasso.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: example_sparse_group_lasso.ipynb <example_sparse_group_lasso.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
