## new in jupyter-openbis-extension 0.5.0

- splitted project into jupyter-openbis-server and jupyter-openbis-extension
- jupyter-openbis-server is the Python-part which talks to both openBIS and the Jupyter extension
- jupyter-opnebis-server is also used by the jupyterlab-openbis notebook extension

## new in jupyter-openbis-extension 0.4.0

- made it compatible to pybis-1.9.x
- minor bugfixes and improvements

## new in jupyter-openbis-extension 0.3.0

- removed search-as-you-type feature, as it is not mature yet
- fixed notebook path problem in special environments
- improved download path
- connection dialog: show that connection is being established
- upload dialog: improved file chooser
- upload dialog: save notebook automatically before upload

## new in jupyter-openbis-extension 0.2.4

- improved entity selection
- openBIS History ID support
- warning: there are known bugs in the new search feature which will hopefully be fixed in an
  upcoming release

## new in jupyter-openbis-extension 0.2.2

- fixed link to gitlab project
- fixed setup.py to force tornado=5.1.1

## new in jupyter-openbis-extension 0.2.1

- improved download dialog
- added spinner
- persist values entered in dialog fields

## new in jupyter-openbis-extension 0.2.0

- first version that cleanly works with pip install only
- bugfixes in setup.py
- typos in .json files in jupyter-config
- CHANGELOG added

## new in jupyter-openbis-extension 0.1.0

- separation of connection, down- and upload
- upload let you specify dataset type
- dataset type specific input fields (properties)
- input control for all properties
- checks for missing properties
- downloaded datasets are new parent datasets by default
- simplified way to upload files as part of the new dataset

## new in jupyter-openbis-extension 0.0.1

- first published version
