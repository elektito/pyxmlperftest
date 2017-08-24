This program benchmarks a few XML parsing libraries available to
Python programmers. In particular, it compares [lxml][1] with some of
the modules in the [xml][2] package in Python standard library.

You need to pass at least one XML file as test input:

    $ ./pyxmlperftest.py 1.xml 2.xml 3.xml

Sample final results:

    Results:
       xml.dom.minidom: 7.49 MBps
       lxml.etree: 89.63 MBps
       xml.etree.ElementTree.iterparse: 31.77 MBps
       xml.etree.ElementTree: 58.43 MBps
       xml.sax: 25.68 MBps

From what I've seen so far, `lxml` is superior to all other options by
a wide margin, will `minidom` is the slowest option by far.

This is not a very scientific benchmark, so take the results with a
grain of salt.


[1]: http://lxml.de/
[2]: https://docs.python.org/3/library/xml.html
