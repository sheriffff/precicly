# precicly

Live prediction of bycicle waiting times for Madrid and Barcelona.

To install the conda environment that we're using make sure you have conda (or miniconda) installed. The
description of our environment is on `"./requirements.yml"`. After cloning the repository locally, run
`conda env create --file=requirements.yml` from the root of the repository. That should create an environment
called `precicly` with the same package versioning of our project. 

Currently it's a bit cumbersome but everytime we install a package we would need to do two things:

* Rewrite `requirements.yml` with `conda env export > requirements.yml`
* The other developers have to run `conda env create --file=requirements.yml` to update their own environments

I feel this is a bit cumbersome as I'll always forget but we need to think (or read) of a simple solution, as there probably is.
