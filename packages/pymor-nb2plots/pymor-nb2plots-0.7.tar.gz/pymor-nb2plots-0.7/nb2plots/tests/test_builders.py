""" Tests for Markdown and other builders
"""
from __future__ import unicode_literals

from os.path import join as pjoin, isfile
import re

from nb2plots.testing import PlotsBuilder


class TestMarkdownBuild(PlotsBuilder):
    """ Markdown builder without specified base URL
    """

    builder = 'markdown'

    rst_sources = {'a_page': """\
.. _a-ref:

################
Refereed section
################

This section refers to :ref:`itself <a-ref>`.

It also refers forward to the :ref:`next section <b-ref>`.

Then, and finally, it refers to itself with its own name: :ref:`a-ref`.

.. _b-ref:

##########
Rerefereed
##########

This section refers to this document at :doc:`a_page`, and with an
explicit title, to :doc:`this document <a_page>`.

Then to :doc:`a_page`.  Again to :doc:`another doc <a_page>`.

Now :download:`a_page.rst`.

Then :download:`another page <a_page.rst>`.

.. code-links::

Then `a link <https://another-place.com/page.html>`_.

Again, we :doc:`link to another doc <subdir1/b_page>`.""",
                   'subdir1/b_page': """\
############
Another page
############

Here is another page.

It refers to :doc:`/a_page`.""",
                   'subdir2/c_page': """\
############
Further page
############

Here is further page.

It refers to :doc:`../a_page`.

It also refers to :doc:`/subdir1/b_page`."""}

    def test_output(self):
        assert self.get_built_file('contents.md').strip() == ''
        assert self.get_built_file('a_page.md') == """\
## Refereed section

This section refers to itself.

It also refers forward to the next section.

Then, and finally, it refers to itself with its own name: Refereed section.

## Rerefereed

This section refers to this document at Refereed section, and with an
explicit title, to this document.

Then to Refereed section.  Again to another doc.

Now `a_page.rst`.

Then `another page`.

Then [a link](https://another-place.com/page.html).

Again, we link to another doc.
"""
        assert self.get_built_file(pjoin('subdir1', 'b_page.md')) == """\
## Another page

Here is another page.

It refers to Refereed section.
"""
        assert self.get_built_file(pjoin('subdir2', 'c_page.md')) == """\
## Further page

Here is further page.

It refers to Refereed section.

It also refers to Another page.
"""


class TestBasedMarkdownBuild(TestMarkdownBuild):
    """ Markdown builder with specified base URL
    """

    conf_source = ('master_doc = "contents"\n'
                   'extensions = ["nb2plots"]\n'
                   'markdown_http_base = "https://dynevor.org"')

    def test_output(self):
        assert self.get_built_file('contents.md').strip() == ''
        expected_re = r"""## Refereed section

This section refers to \[itself\]\(https://dynevor.org/a_page.html#a-ref\)\.

It also refers forward to the \[next section\]\(https://dynevor.org/a_page.html#b-ref\)\.

Then, and finally, it refers to itself with its own name: \[Refereed section\]\(https://dynevor.org/a_page\.html#a-ref\)\.

## Rerefereed

This section refers to this document at \[Refereed section\]\(https://dynevor\.org/a_page\.html\), and with an
explicit title, to \[this document\]\(https://dynevor\.org/a_page.html\)\.

Then to \[Refereed section\]\(https://dynevor\.org/a_page.html\)\.  Again to \[another doc\]\(https://dynevor\.org/a_page.html\)\.

Now \[a_page\.rst\]\(https://dynevor.org/_downloads/([a-f0-9]+/)?a_page.rst\)\.

Then \[another page\]\(https://dynevor\.org/_downloads/([a-f0-9]+/)?a_page.rst\)\.

Then \[a link\]\(https://another-place.com/page.html\)\.

Again, we \[link to another doc\]\(https://dynevor.org/subdir1/b_page\.html\)\.
"""
        actual = self.get_built_file('a_page.md')
        assert re.match(expected_re, actual)
        assert self.get_built_file(pjoin('subdir1', 'b_page.md')) == """\
## Another page

Here is another page.

It refers to [Refereed section](https://dynevor.org/a_page.html).
"""
        assert self.get_built_file(pjoin('subdir2', 'c_page.md')) == """\
## Further page

Here is further page.

It refers to [Refereed section](https://dynevor.org/a_page.html).

It also refers to [Another page](https://dynevor.org/subdir1/b_page.html).
"""


class TestPythonBuild(PlotsBuilder):
    """ Python builder without specified base URL
    """

    builder = 'python'

    rst_sources = {'a_page': """\
.. _a-ref:

A section
=========

Some text

This section refers to :ref:`itself <a-ref>`.

.. nbplot::

    >>> a = 1
"""}

    def test_output(self):
        assert self.get_built_file('contents.py').strip() == ''
        assert self.get_built_file('a_page.py') == """\
# ## A section
#
# Some text
#
# This section refers to itself.

a = 1
"""


class TestBasedPythonBuild(TestPythonBuild):
    """ Python builder with specified base URL
    """

    conf_source = ('master_doc = "contents"\n'
                   'extensions = ["nb2plots"]\n'
                   'markdown_http_base = "https://dynevor.org"')

    def test_output(self):
        assert self.get_built_file('contents.py').strip() == ''
        assert self.get_built_file('a_page.py') == """\
# ## A section
#
# Some text
#
# This section refers to [itself](https://dynevor.org/a_page.html#a-ref).

a = 1
"""


class TestLatexBuild(PlotsBuilder):
    """ Test LaTeX build

    In particular, test that code outputs in a subdirectory work without
    raising an error.
    """

    builder = 'latex'

    rst_sources = {'foo/a_page': """\
A section
=========

.. code-links::
"""}

    toctree_pages = list(rst_sources)

    def test_output(self):
        for suffix in ('.py', '.ipynb', '_full.ipynb'):
            assert isfile(pjoin(self.out_dir, 'foo', 'a_page' + suffix))
