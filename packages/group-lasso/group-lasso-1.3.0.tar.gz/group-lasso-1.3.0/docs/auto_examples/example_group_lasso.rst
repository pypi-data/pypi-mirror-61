.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_auto_examples_example_group_lasso.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_example_group_lasso.py:


GroupLasso for linear regression
================================

A sample script for group lasso regression

Setup
-----


.. code-block:: default


    import matplotlib.pyplot as plt
    import numpy as np
    from sklearn.linear_model import Ridge
    from sklearn.metrics import r2_score
    from sklearn.pipeline import Pipeline

    from group_lasso import GroupLasso

    np.random.seed(0)
    GroupLasso.LOG_LOSSES = True









Set dataset parameters
----------------------


.. code-block:: default

    group_sizes = [np.random.randint(10, 20) for i in range(50)]
    active_groups = [np.random.randint(2) for _ in group_sizes]
    groups = np.concatenate(
        [size * [i] for i, size in enumerate(group_sizes)]
    ).reshape(-1, 1)
    num_coeffs = sum(group_sizes)
    num_datapoints = 10000
    noise_std = 20









Generate data matrix
--------------------


.. code-block:: default

    X = np.random.standard_normal((num_datapoints, num_coeffs))









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





.. image:: /auto_examples/images/sphx_glr_example_group_lasso_001.png
    :class: sphx-glr-single-img





Generate estimator and train it
-------------------------------


.. code-block:: default

    gl = GroupLasso(
        groups=groups,
        group_reg=5,
        l1_reg=0,
        frobenius_lipschitz=True,
        scale_reg="inverse_group_size",
        subsampling_scheme=1,
        supress_warning=True,
        n_iter=1000,
        tol=1e-3,
    )

    gl.fit(X, y)









Extract results and compute performance metrics
-----------------------------------------------


.. code-block:: default


    # Extract info from estimator
    yhat = gl.predict(X)
    sparsity_mask = gl.sparsity_mask
    w_hat = gl.coef_

    # Compute performance metrics
    R2 = r2_score(y, yhat)

    # Print results
    print(f"Number variables: {len(sparsity_mask)}")
    print(f"Number of chosen variables: {sparsity_mask.sum()}")
    print(f"R^2: {R2}, best possible R^2 = {R2_best}")






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Number variables: 720
    Number of chosen variables: 313
    R^2: 0.27127035561426716, best possible R^2 = 0.46262785225190173




Visualise regression coefficients
---------------------------------


.. code-block:: default

    for i in range(w.shape[1]):
        plt.figure()
        plt.plot(w[:, i], ".", label="True weights")
        plt.plot(gl.coef_[:, i], ".", label="Estimated weights")

    plt.figure()
    plt.plot([w.min(), w.max()], [gl.coef_.min(), gl.coef_.max()], "gray")
    plt.scatter(w, gl.coef_, s=10)
    plt.ylabel("Learned coefficients")
    plt.xlabel("True coefficients")

    plt.figure()
    plt.plot(gl.losses_)

    print("X shape: {X.shape}".format(X=X))
    print("True intercept: {intercept}".format(intercept=intercept))
    print("Estimated intercept: {intercept}".format(intercept=gl.intercept_))
    plt.show()



.. rst-class:: sphx-glr-horizontal


    *

      .. image:: /auto_examples/images/sphx_glr_example_group_lasso_002.png
            :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/images/sphx_glr_example_group_lasso_003.png
            :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/images/sphx_glr_example_group_lasso_004.png
            :class: sphx-glr-multi-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    X shape: (10000, 720)
    True intercept: 2
    Estimated intercept: [1.81098782]
    /home/yngvem/Programming/morro/group-lasso/examples/example_group_lasso.py:132: UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.
      plt.show()





.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  2.124 seconds)


.. _sphx_glr_download_auto_examples_example_group_lasso.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: example_group_lasso.py <example_group_lasso.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: example_group_lasso.ipynb <example_group_lasso.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
