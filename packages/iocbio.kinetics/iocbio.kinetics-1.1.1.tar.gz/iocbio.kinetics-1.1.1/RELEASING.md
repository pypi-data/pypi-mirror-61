## Making packages

### Adjust version number

emacs packaging/conda/meta.yaml setup.py

git status
git add packaging/conda/meta.yaml setup.py
git commit -m "bump version"
git push origin master

### PyPi

For making source package, run

```
python3 setup.py sdist
```

For upload to PyPI:

```
twine upload dist/iocbio.kinetics-1.0.0.tar.gz
```

### Make release at Gitlab

Go to https://gitlab.com/iocbio/kinetics/tags and make a new release
with Changelog


### Anaconda

For Conda packages, install conda (miniconda3 or anaconda3), `conda-build`. Assuming that 
miniconda3 is installed at home, run from the project root directory

```
. ~/miniconda3/etc/profile.d/conda.sh
python3 setup.py sdist
(cd packaging/conda && conda build -c anaconda -c conda-forge . && conda index ~/miniconda3/conda-bld/noarch)
```


When package is ready, upload it with (replace version numbers accordingly)

```
~/miniconda3/bin/anaconda login
~/miniconda3/bin/anaconda upload -u iocbio --thumbnail ~/miniconda3/conda-bld/noarch/.icons/iocbio.kinetics-1.0.0-py_1.tar.bz2.png ~/miniconda3/conda-bld/noarch/iocbio.kinetics-1.0.0-py_1.tar.bz2
```
