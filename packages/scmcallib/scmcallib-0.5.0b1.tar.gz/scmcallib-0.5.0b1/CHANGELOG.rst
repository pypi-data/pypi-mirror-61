Changelog
---------

master
======

- (`!67 <https://gitlab.com/magicc/scmcallib/merge_requests/67>`_) Extend ``KeyedParameterSet`` to handle more than 1 dimension
- (`!66 <https://gitlab.com/magicc/scmcallib/merge_requests/66>`_) Use result of maximising bayesopt Gaussian Processes as the optimal set of parameters
- (`!65 <https://gitlab.com/magicc/scmcallib/merge_requests/65>`_) Pass target data via the tuningcore "JSON" structure
- (`!64 <https://gitlab.com/magicc/scmcallib/merge_requests/64>`_) Fix of the fix for always casting to floats
- (`!63 <https://gitlab.com/magicc/scmcallib/merge_requests/63>`_) Replace ``update_deps`` makefile target with ``conda-environment``
- (`!61 <https://gitlab.com/magicc/scmcallib/merge_requests/61>`_) Log the steps performed by the optimiser

v0.4.2
======

- (`!62 <https://gitlab.com/magicc/scmcallib/merge_requests/62>`_) Fix always casting floats to int's for scenset values

v0.4.1
======

- (`!60 <https://gitlab.com/magicc/scmcallib/merge_requests/60>`_) Use scmdata>=0.2.0

v0.4.0
======

- (`!59 <https://gitlab.com/magicc/scmcallib/merge_requests/59>`_) Add ``diff`` transform
- (`!58 <https://gitlab.com/magicc/scmcallib/merge_requests/58>`_) Add support for latin hypercube sampling
- (`!57 <https://gitlab.com/magicc/scmcallib/merge_requests/57>`_) Use new CMIP6 SCENSET format and deprecate the older .mat format
- (`!56 <https://gitlab.com/magicc/scmcallib/merge_requests/56>`_) Add ``data_dir`` argument to the ``create_point_model`` function

v0.3.0
======

- (`!53 <https://gitlab.com/magicc/scmcallib/merge_requests/53>`_) Migrate to using `scmdata` and remove `openscm` dependency
- (`!52 <https://gitlab.com/magicc/scmcallib/merge_requests/52>`_) Add `transforms` which are run after model runs to allow arbitary changes to be made to the model output
- (`!51 <https://gitlab.com/magicc/scmcallib/merge_requests/51>`_) Failed metric calculations now return a large negative value instead of a nan
- (`!50 <https://gitlab.com/magicc/scmcallib/merge_requests/50>`_) Fix summary plots
- (`!49 <https://gitlab.com/magicc/scmcallib/merge_requests/49>`_) Breaking change for how SCM objects are handled. SCM's should now
  be used as a context manager so to have better control as to when they are cleaned up.

v0.2.1
======

- (`!48 <https://gitlab.com/magicc/scmcallib/merge_requests/48>`_) Update to use pymagicc 2.0.0b4 and a tagged version of openscm
- (`!47 <https://gitlab.com/magicc/scmcallib/merge_requests/47>`_) Fix tuningstruc writing filename handling
- (`!46 <https://gitlab.com/magicc/scmcallib/merge_requests/46>`_) Add SummaryPlot and live plotting
- (`!45 <https://gitlab.com/magicc/scmcallib/merge_requests/45>`_) Fix tuningstruc writing for single items and add ``mat4py`` submodule (details on their MIT license are `here <https://opensource.org/licenses/MIT>`_ and `here <http://www.gnu.org/licenses/license-list.en.html>`_ with `short summary here <https://tldrlegal.com/license/mit-license>`_)
- (`!44 <https://gitlab.com/magicc/scmcallib/merge_requests/44>`_) Drop and warn on any nan values in the target timeseries
- (`!39 <https://gitlab.com/magicc/scmcallib/merge_requests/39>`_) Add `only` argument to ``MAGICC7_SCM.run``
- (`!38 <https://gitlab.com/magicc/scmcallib/merge_requests/38>`_) Add the ability to weight timeseries for PointEstimateFinder and move to sklearn metrics
- (`!35 <https://gitlab.com/magicc/scmcallib/merge_requests/35>`_) Add `iter_over` argument to `set_target`
- (`!34 <https://gitlab.com/magicc/scmcallib/merge_requests/34>`_) Add `convert_tuningstruc_to_scmdf` and `convert_scmdf_to_tuningstruc`
- (`!33 <https://gitlab.com/magicc/scmcallib/merge_requests/33>`_) Added callable parameters which are evaluated at runtime and renamed parameter types to config and tune
- (`!27 <https://gitlab.com/magicc/scmcallib/merge_requests/27>`_) Moved to using IamDataFrame's internally for dealing with scm data. Added the
  ability to handle multiple target time series
- (`!22 <https://gitlab.com/magicc/scmcallib/merge_requests/22>`_) Moved to using adapters for the optimiser backend. Added bayesian opts backend
- (`!19 <https://gitlab.com/magicc/scmcallib/merge_requests/19>`_) Add scm_kwargs parameter for specifying a custom root_dir for MAGICC_SCM


v0.1.0
======

- (`!8 <https://gitlab.com/magicc/scmcallib/merge_requests/8>`_) Added versioneer support
- (`!9 <https://gitlab.com/magicc/scmcallib/merge_requests/9>`_) Add ParameterSet class for holding prior variables before emulation or calibration
- (`!12 <https://gitlab.com/magicc/scmcallib/merge_requests/12>`_) Added AR5IR SCM for testing
- (`!11 <https://gitlab.com/magicc/scmcallib/merge_requests/11>`_) Refactored API to no longer require everything to be within a with block
- (`!16 <https://gitlab.com/magicc/scmcallib/merge_requests/16>`_) Differentiate between fixed and free parameters in ParameterSets
- (`!17 <https://gitlab.com/magicc/scmcallib/merge_requests/17>`_) Improve the handling of the conda environments, while also supporting pip

