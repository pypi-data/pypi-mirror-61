pypublish |License MIT|
==========================

http://python-packaging.readthedocs.io/en/latest/index.html


|PyPI version|

.. |PyPI version| image:: https://badge.fury.io/py/text2img.svg
   :target: https://badge.fury.io/py/text2img

Python library for generate files with jinja and hjson

To update pypi
git add .
git commit -m "7th commit"
git push -u origin master


python2.7 setup.py sdist bdist_wheel
twine upload dist/*


Getting started with the library
--------------------------------

| To use the library, you first need to install it.

::

    pip install bslideshow
    #python -c "import sys; import svgmanager; svgmanager.SvgManager.generate(sys.argv)"
    #python -c "import sys; from text2img import svgmanager; svgmanager.SvgManager.generate(sys.argv)"
    python -c "import sys; from text2img import SvgManager; SvgManager.generate(sys.argv)"
    python -c "import sys; from text2img import SvgManager; SvgManager.generate(sys.argv)" /home/jmramoss/almacen/ORLAS/text2img/text2img/base2.svd
    python -c "import sys; import svgmanager; svgmanager.SvgManager.generate(sys.argv)" /home/jmramoss/almacen/ORLAS/text2img/text2img/base.svd /home/jmramoss/almacen/ORLAS/text2img/text2img/themes.svd /home/jmramoss/text2img_output/clips
    sudo pip install --upgrade text2img




    
    

    

GITHUB
1. Crear repositorio desde panel de control de github
  sbrowser

2. Realizar primer commit (publicar en github)
echo "# bslideshow" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/tuaplicacionpropia/bslideshow.git
git push -u origin master

3. Publicar actualizar en github

git status
git add .
git rm file2delete
git commit -m "commit message"
git push origin master


all together:
git add . && git commit -m "201904131508" && git push origin master


4. Publicar en pypi

#python setup.py register sdist upload
#python2.7 setup.py sdist bdist_wheel

rm -v dist/*
python2.7 setup.py sdist bdist_wheel
twine upload dist/*

all together:
rm -v dist/* && python2.7 setup.py sdist bdist_wheel && twine upload dist/*



5. Actualizar from pypi
#sudo pip2.7 install sbrowser==0.0.16
sudo pip2.7 install --upgrade findfaces

ALL TOGETHER

git add . && git commit -m "201904131508" && git push origin master && rm -v dist/* && python2.7 setup.py sdist bdist_wheel && twine upload dist/*























Every resource exposes the following **methods**:

-  list()
-  search()
-  get()
-  create()
-  update()
-  delete()

To use each resource you will need to create an instance of them,
passing the client as parameter in the constructor.

**Note:** at the moment not all the methods and not all the resources
have been implemented.

Here you can find a couple of examples, but for the complete
documentation you can have a look at the official website
https://developer.toshl.com/docs/

For me
~~~~~~

::

    git status
    git add .
    git rm file2delete
    git commit -m "commit message"
    git push origin master
    python setup.py register sdist upload


Accounts
~~~~~~~~

::

    from toshl.client import ToshlClient, Account

    client = ToshlClient('xxx-xxxxx-xxx-xxxxxx-xxxxxx-xxx-xxxxxx')
    account = Account(client)

    # list all accounts
    account.list()

    # search for a specific account
    account.search('Test Account')

Categories
~~~~~~~~~~

::

    from toshl.client import ToshlClient, Category

    client = ToshlClient('xxx-xxxxx-xxx-xxxxxx-xxxxxx-xxx-xxxxxx')
    category = Category(client)

    # list all categories
    category.list()

    # search for a specific category
    category.search('Test Category')

Entries
~~~~~~~

::

    from toshl.client import ToshlClient, Entry

    client = ToshlClient('xxx-xxxxx-xxx-xxxxxx-xxxxxx-xxx-xxxxxx')
    entry = Entry(client)

    # create an Entry
    json_payload = {
        'amount': -123.68,
        'currency': {
            'code': 'GBP'
        },
        'date': '2016-04-07',
        'account': 'abcd1234',
        'category': 'category-001'
    }

    response = entry.create(json_payload)

Copyright Note
--------------

| **text2img** and its logos, design, text, graphics, and other files, and
  the selection arrangement and organization thereof, are owned by
  http://tuaplicacionpropia.com.
| This is a 3rd party code and I’m not affiliated nor I work for text2img.

.. |License MIT| image:: https://go-shields.herokuapp.com/license-MIT-blue.png

