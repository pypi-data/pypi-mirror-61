Poezio OMEMO plugin
###################

This is a `Poezio <https://poez.io>`_ plugin providing OMEMO support. It
distributed separately for licensing reasons.

This plugin is very much **alpha**. It handles encryption and decryption
of OMEMO messages, but doesn't display the encryption state of messages,
and neither does it have a way to do trust management.

Use in poezio
-------------

Once installed (see the `Installation`_ section below), you can add
`omemo` in the `plugin_autoload` configuration. See the Poezio
`documentation
<https://doc.poez.io/plugins/index.html#plugin-autoload>`_ for more
information about autoloading plugins.

License
-------

This plugin is licensed under GPLv3.

Note on the underlying OMEMO library
------------------------------------

As stated in `python-xeddsa's
README <https://github.com/Syndace/python-xeddsa/blob/136b9f12c8286b9463566308963e70f090b60e50/README.md>`_,
(dependency of python-omemo), this library has not undergone any
security audits. If you have the knowledge, any help is welcome.

Please take this into consideration when using this library.

Installation
------------

- ArchLinux (AUR):
   `python-poezio-omemo <https://aur.archlinux.org/packages/python-poezio-omemo>`_, or
   `python-poezio-omemo-git <https://aur.archlinux.org/packages/python-poezio-omemo-git>`_
- PIP: `poezio-omemo`
- Manual: `python3 setup.py install`
