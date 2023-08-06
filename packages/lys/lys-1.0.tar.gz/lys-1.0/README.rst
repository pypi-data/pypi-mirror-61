Lys
===
.. image:: https://img.shields.io/pypi/v/lys.svg
    :target: https://pypi.python.org/pypi/lys
.. image:: https://travis-ci.org/mdamien/lys.svg?branch=master
    :target: https://travis-ci.org/mdamien/lys

*Simple HTML templating for Python*

.. code:: python

    from lys import L

    print(L.body / (
        L.h1 / 'What is love ?',
        L.ul / (
            L.li / 'Something in the air',
            L.li / 'You can\'t catch it',
            L.li / (
                L.a(href="https://en.wikipedia.org/wiki/Love") / 'Keep trying'
            ),
        ),
    ))

To install, :code:`pip3 install lys`

A few more tricks:

.. code:: python

    # raw() to mark the content as already escaped
    from lys import raw
    L.p / raw('<script>alert("boo")</script>')

    # attributes '_' are replaced with '-'
    L.button(data_id="123") / 'click me'
    # => <button data-id="123">click me</button>

    # shortcut to add classes and ids easily
    L.button('#magic-button.very-big', onclick='add_it()') / 'Magic !'

    # one easy way to do loops and ifs
    (
        L.h1 / 'Welcome',
        (L.ul / (
            'Try one of our recipes:',
            (L.li / (
                L.a(href=recipe.link) / recipe.name
            ) for recipe in recipes)
        ) if len(recipes) > 0 else ''),
    )

**Inspiration** : `pyxl <https://github.com/dropbox/pyxl>`_, `React <https://facebook.github.io/react/>`_
