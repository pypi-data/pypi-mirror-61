.. note::
    :class: sphx-glr-download-link-note

    Click :ref:`here <sphx_glr_download_auto_examples_example_group_lasso_pipeline.py>` to download the full example code
.. rst-class:: sphx-glr-example-title

.. _sphx_glr_auto_examples_example_group_lasso_pipeline.py:


GroupLasso as a transformer
============================

A sample script to demonstrate how the group lasso estimators can be used
for variable selection in a scikit-learn pipeline.

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





.. image:: /auto_examples/images/sphx_glr_example_group_lasso_pipeline_001.png
    :class: sphx-glr-single-img





Generate pipeline and train it
------------------------------


.. code-block:: default

    pipe = Pipeline(
        memory=None,
        steps=[
            (
                "variable_selection",
                GroupLasso(
                    groups=groups,
                    group_reg=20,
                    l1_reg=0,
                    scale_reg="inverse_group_size",
                    subsampling_scheme=1,
                    supress_warning=True,
                ),
            ),
            ("regressor", Ridge(alpha=0.1)),
        ],
    )
    pipe.fit(X, y)






.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /home/yngvem/Programming/morro/group-lasso/src/group_lasso/_fista.py:55: RuntimeWarning: The FISTA iterations did not converge to a sufficient minimum.
    You used subsampling then this is expected, otherwise,try to increase the number of iterations or decreasing the tolerance.
      RuntimeWarning,

    Pipeline(memory=None,
             steps=[('variable_selection',
                     GroupLasso(fit_intercept=True, frobenius_lipschitz=None,
                                group_reg=20,
                                groups=array([[ 0],
           [ 0],
           [ 0],
           [ 0],
           [ 0],
           [ 0],
           [ 0],
           [ 0],
           [ 0],
           [ 0],
           [ 0],
           [ 0],
           [ 0],
           [ 0],
           [ 0],
           [ 1],
           [ 1],
           [ 1],
           [ 1],
           [ 1],
           [ 1],
           [ 1],
           [ 1],
           [ 1],
           [ 1],
           [ 2],
           [ 2],
           [ 2],
           [ 2],
           [ 2],
           [ 2],
           [ 2],
           [ 2],
           [ 2],
           [ 2],
           [ 2],
           [ 2],
           [ 2],
           [ 3],
           [ 3],
           [ 3],
           [ 3],
           [ 3],
           [ 3],
           [ 3],
           [ 3],
           [ 3],
           [ 3],
           [ 3],
           [ 3],
           [ 3],
           [ 4],
           [ 4],
           [ 4],
           [ 4...
           [49],
           [49],
           [49],
           [49],
           [49],
           [49],
           [49]]),
                                l1_reg=0, n_iter=100, old_regularisation=False,
                                random_state=None, scale_reg='inverse_group_size',
                                subsampling_scheme=1, supress_warning=True,
                                tol=1e-05, warm_start=False)),
                    ('regressor',
                     Ridge(alpha=0.1, copy_X=True, fit_intercept=True,
                           max_iter=None, normalize=False, random_state=None,
                           solver='auto', tol=0.001))],
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

    Number variables: 720
    Number of chosen variables: 285
    R^2: 0.32350423515906845, best possible R^2 = 0.46262785225190173




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

      .. image:: /auto_examples/images/sphx_glr_example_group_lasso_pipeline_002.png
            :class: sphx-glr-multi-img

    *

      .. image:: /auto_examples/images/sphx_glr_example_group_lasso_pipeline_003.png
            :class: sphx-glr-multi-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    /home/yngvem/Programming/morro/group-lasso/examples/example_group_lasso_pipeline.py:133: UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.
      plt.show()





.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  2.025 seconds)


.. _sphx_glr_download_auto_examples_example_group_lasso_pipeline.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download

     :download:`Download Python source code: example_group_lasso_pipeline.py <example_group_lasso_pipeline.py>`



  .. container:: sphx-glr-download

     :download:`Download Jupyter notebook: example_group_lasso_pipeline.ipynb <example_group_lasso_pipeline.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
