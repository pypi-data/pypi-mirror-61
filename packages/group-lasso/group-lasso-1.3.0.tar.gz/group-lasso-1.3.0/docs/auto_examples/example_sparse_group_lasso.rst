.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_auto_examples_example_sparse_group_lasso.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_example_sparse_group_lasso.py:


GroupLasso for linear regression with dummy variables
=====================================================

A sample script for group lasso with dummy variables

Setup
-----


.. code-block:: default


    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import sparse
    from sklearn.linear_model import Ridge
    from sklearn.metrics import r2_score
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder

    from group_lasso import GroupLasso
    from group_lasso.utils import extract_ohe_groups

    np.random.seed(42)
    GroupLasso.LOG_LOSSES = True









Set dataset parameters
----------------------


.. code-block:: default

    num_categories = 30
    min_options = 2
    max_options = 10
    num_datapoints = 10000
    noise_std = 1









Generate data matrix
--------------------


.. code-block:: default

    X_cat = np.empty((num_datapoints, num_categories))
    for i in range(num_categories):
        X_cat[:, i] = np.random.randint(min_options, max_options, num_datapoints)

    ohe = OneHotEncoder()
    X = ohe.fit_transform(X_cat)
    groups = extract_ohe_groups(ohe)
    group_sizes = [np.sum(groups == g) for g in np.unique(groups)]
    active_groups = [np.random.randint(0, 2) for _ in np.unique(groups)]






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /home/yngvem/anaconda3/lib/python3.7/site-packages/sklearn/preprocessing/_encoders.py:415: FutureWarning: The handling of integer data will change in version 0.22. Currently, the categories are determined based on the range [0, max(values)], while in the future they will be determined based on the unique values.
    If you want the future behaviour and silence this warning, you can specify "categories='auto'".
    In case you used a LabelEncoder before this OneHotEncoder to convert the categories to integers, then you can now use the OneHotEncoder directly.
      warnings.warn(msg, FutureWarning)




Generate coefficients
---------------------


.. code-block:: default

    w = np.concatenate(
        [
            np.random.standard_normal(group_size) * is_active
            for group_size, is_active in zip(group_sizes, active_groups)
        ]
    )
    w = w.reshape(-1, 1)
    true_coefficient_mask = w != 0
    intercept = 2









Generate regression targets
---------------------------


.. code-block:: default

    y_true = X @ w + intercept
    y = y_true + np.random.randn(*y_true.shape) * noise_std









View noisy data and compute maximum R^2
---------------------------------------


.. code-block:: default

    plt.figure()
    plt.plot(y, y_true, ".")
    plt.xlabel("Noisy targets")
    plt.ylabel("Noise-free targets")
    # Use noisy y as true because that is what we would have access
    # to in a real-life setting.
    R2_best = r2_score(y, y_true)





.. image:: /auto_examples/images/sphx_glr_example_sparse_group_lasso_001.png
    :class: sphx-glr-single-img





Generate pipeline and train it
------------------------------


.. code-block:: default

    pipe = pipe = Pipeline(
        memory=None,
        steps=[
            (
                "variable_selection",
                GroupLasso(
                    groups=groups,
                    group_reg=0.1,
                    l1_reg=0,
                    scale_reg=None,
                    supress_warning=True,
                    n_iter=100000,
                    frobenius_lipschitz=False,
                ),
            ),
            ("regressor", Ridge(alpha=1)),
        ],
    )
    pipe.fit(X, y)






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none


    Pipeline(memory=None,
             steps=[('variable_selection',
                     GroupLasso(fit_intercept=True, frobenius_lipschitz=None,
                                group_reg=0.1,
                                groups=array([ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,  1.,  1.,  1.,  1.,
            1.,  1.,  1.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  2.,  3.,  3.,
            3.,  3.,  3.,  3.,  3.,  3.,  4.,  4.,  4.,  4.,  4.,  4.,  4.,
            4.,  5.,  5.,  5.,  5.,  5.,  5.,  5.,  5.,  6.,  6.,  6.,  6.,
            6.,  6.,  6.,  6.,  7.,  7.,  7.,  7.,  7.,  7.,  7.,  7.,  8.,
            8.,  8.,  8.,  8.,  8.,  8.,  8.,  9...
           27., 27., 27., 28., 28., 28., 28., 28., 28., 28., 28., 29., 29.,
           29., 29., 29., 29., 29., 29.]),
                                l1_reg=0, n_iter=100000, old_regularisation=False,
                                random_state=None, scale_reg=None,
                                subsampling_scheme=None, supress_warning=True,
                                tol=1e-05, warm_start=False)),
                    ('regressor',
                     Ridge(alpha=1, copy_X=True, fit_intercept=True, max_iter=None,
                           normalize=False, random_state=None, solver='auto',
                           tol=0.001))],
             verbose=False)



Extract results and compute performance metrics
-----------------------------------------------


.. code-block:: default


    # Extract from pipeline
    yhat = pipe.predict(X)
    sparsity_mask = pipe["variable_selection"].sparsity_mask
    coef = pipe["regressor"].coef_.T

    # Construct full coefficient vector
    w_hat = np.zeros_like(w)
    w_hat[sparsity_mask] = coef

    R2 = r2_score(y, yhat)

    # Print performance metrics
    print(f"Number variables: {len(sparsity_mask)}")
    print(f"Number of chosen variables: {sparsity_mask.sum()}")
    print(f"R^2: {R2}, best possible R^2 = {R2_best}")






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Number variables: 240
    Number of chosen variables: 144
    R^2: 0.9278324913862297, best possible R^2 = 0.9394648554757948




Visualise regression coefficients
---------------------------------


.. code-block:: default

    for i in range(w.shape[1]):
        plt.figure()
        plt.plot(w[:, i], ".", label="True weights")
        plt.plot(w_hat[:, i], ".", label="Estimated weights")

    plt.figure()
    plt.plot([w.min(), w.max()], [coef.min(), coef.max()], "gray")
    plt.scatter(w, w_hat, s=10)
    plt.ylabel("Learned coefficients")
    plt.xlabel("True coefficients")
    plt.show()



.. rst-class:: sphx-glr-horizontal


    *

      .. image:: /auto_examples/images/sphx_glr_example_sparse_group_lasso_002.png
            :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/images/sphx_glr_example_sparse_group_lasso_003.png
            :class: sphx-glr-multi-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /home/yngvem/Programming/morro/group-lasso/examples/example_sparse_group_lasso.py:142: UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.
      plt.show()





.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  2.269 seconds)


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
