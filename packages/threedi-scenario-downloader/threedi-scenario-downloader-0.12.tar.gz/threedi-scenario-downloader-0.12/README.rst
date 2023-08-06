threedi-scenario-downloader
==========================================

The threedi-scenario-downloader package includes functions in order to
automate most used download actions on the 3Di results.

Example methods are:

- Download raw results.
- Download logging.
- Download maximum waterdepth (non-temporal raster).
- Download waterdepth (temporal raster, supply timestamp for snapshot).
- Find all scenarios model slug or scenario name.

Examples
========================================
Start importing the package::
  
  $ from threedi_scenario_downloader import downloader as dl

Set headers for authentication to the Lizard API::
  
  $ dl.set_headers("your_username","your_password")

Find scenarios based on a model slug (unique model identifier) or scenario name. Returns last 10 matching results unless told otherwise::

  $ scenarios = dl.find_scenarios_by_model_slug("enter your model_uuid",limit=10)
  
or::

  $ scenarios = dl.find_scenarios_by_name("my_first_scenario",limit=100)

Do you want to download the raw 3Di-results (.nc and .h5 files) of a specific scenario? Use the following methods::

  $ dl.download_raw_results("scenario_uuid")
  $ dl.download_grid_administration("scenario_uuid")


or::

  $ dl.download_raw_results("scenario_uuid",pathname="save_under_different_name.nc")
  $ dl.download_grid_administration("scenario_uuid",pathname="save_under_different_name.h5")

Downloading (temporal) rasters of specific scenarios can be done using the following methods::

  $ dl.download_maximum_waterdepth_raster("scenario_uuid","EPSG:28992",10) 
  #download the full extent of the maximum waterdepth of the given scenario_uuid with a 10 meter resolution in the RD New/Amersfoort projection (EPSG:28992)
  
  $ dl.download_waterdepth_raster("scenario_uuid","EPSG:28992",10,"2019-01-01T02:00") 
  #download the full extend of the waterdepth at the supplied timestamp given scenario_uuid, on 10 meter resolution in the RD New/Amersfoort projection (EPSG:28992)

The raster download methods creates a task for the API. Depending on the size and resolution it takes some time for the raster to be prepared. These methods will keep on checking if the raster is ready to be downloaded.
When a raster is ready to be downloaded a message in the Lizard portal is created as well. If you want to delete these messages (due to bulk downloading for example), use the following method::

  $dl.clear_inbox()

Installation
------------

We can be installed with::

  $ pip install threedi-scenario-downloader


Development installation of this project itself
-----------------------------------------------

We're installed with `pipenv <https://docs.pipenv.org/>`_, a handy wrapper
around pip and virtualenv. Install that first with ``pip install
pipenv``. Then run::

  $ PIPENV_VENV_IN_PROJECT=1 pipenv --three
  $ pipenv install --dev

In order to get nicely formatted python files without having to spend manual
work on it, run the following command periodically::

  $ pipenv run black threedi_scenario_downloader

Run the tests regularly. This also checks with pyflakes, black and it reports
coverage. Pure luxury::

  $ pipenv run pytest

The tests are also run automatically `on travis-ci
<https://travis-ci.com/nens/threedi-scenario-downloader>`_, you'll see it in
the pull requests. There's also `coverage reporting
<https://coveralls.io/github/nens/threedi-scenario-downloader>`_ on
coveralls.io.

If you need a new dependency (like `requests`), add it in `setup.py` in
`install_requires`. Afterwards, run install again to actuall install your
dependency::

  $ pipenv install --dev
