# Create pipy package
---------------------
python setup.py sdist bdist_wheel
twine upload dist/*
