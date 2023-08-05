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


    from group_lasso import GroupLasso
    from sklearn.linear_model import Ridge
    from sklearn.metrics import r2_score
    from sklearn.pipeline import Pipeline
    from utils import (
        get_groups_from_group_sizes,
        generate_group_lasso_coefficients,
    )
    import numpy as np
    import matplotlib.pyplot as plt


    np.random.seed(0)









Set dataset parameters
----------------------


.. code-block:: default

    group_sizes = [np.random.randint(10, 20) for i in range(50)]
    active_groups = [np.random.randint(2) for _ in group_sizes]
    groups = get_groups_from_group_sizes(group_sizes)
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
                    group_reg=1.3,
                    subsampling_scheme=1,
                    supress_warning=True,
                ),
            ),
            ("regressor", Ridge(alpha=0.1)),
        ],
    )
    pipe.fit(X, y)





.. code-block:: pytb

    Traceback (most recent call last):
      File "/home/yngvem/anaconda3/lib/python3.7/site-packages/sphinx_gallery/gen_rst.py", line 440, in _memory_usage
        out = func()
      File "/home/yngvem/anaconda3/lib/python3.7/site-packages/sphinx_gallery/gen_rst.py", line 425, in __call__
        exec(self.code, self.globals)
      File "/home/yngvem/Programming/morro/group-lasso/examples/example_group_lasso_pipeline.py", line 90, in <module>
        supress_warning=True,
    TypeError: __init__() got an unexpected keyword argument 'supress_warning'




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
    true_R2 = r2_score(y_true, yhat)



Print performance metrics
-------------------------


.. code-block:: default

    print(f"Number variables: {len(sparsity_mask)}")
    print(f"Number of chosen variables: {sparsity_mask.sum()}")
    print(f"R^2: {R2}, best possible R^2 = {R2_best}")
    print(f"R^2 compared to noise-free data: {R2}")



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


.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  0.842 seconds)


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
