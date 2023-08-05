Overview
========
ReadIM is a c++ wrapper to load DaVis Images and Vectors DaVis V8. 
ReadIM is a 'low level' interface to C++ libraries provided by LaVision GMBH.

Installation
============
This module is compiled. If there isn't a binary you'll need to have the appropriate build tools installed.


>>> pip install ReadIM

If this fails you will need to compile yourself. Clone the source and run the following.

>>> python setup.py build install
>>> python setup.py test

If the test passes then all should be okay. 


Usage
=====

To load a .vc7 file run::

    >>> vbuff, vatts   =  ReadIM.extra.get_Buffer_andAttributeList('filename.vc7')
    >>> v_array, vbuff = ReadIM.extra.buffer_as_array(vbuff)

similarly for a .im7 file run::

    >>> vbuff, vatts   =  ReadIM.extra.get_Buffer_andAttributeList('filename.im7')
    >>> v_array, vbuff = ReadIM.extra.buffer_as_array(vbuff)


Writing files
-------------
>>> atts = ReadIM.load_AttributeList({'attribute':'value'})
>>> ReadIM.WriteIM7('saved_file.im7', True, buff, atts.next)

Finally, memory cleanup is not automatic. To prevent memory leaks do the following:

>>> del(vbuff)
>>> ReadIM.DestroyBuffer(buff)
>>> ReadIM.DestroyAttributeListSafe(atts)


