""" Test mpl-interactive directive """

import re

from nb2plots.converters import to_pxml


def test_mpl_interactive():
    page = """\
Text here

.. mpl-interactive::

More text here."""
    pxml = to_pxml.from_rst(page)
    assert re.match("""\
<document source=".*?">
    <paragraph>
        Text here
    <mpl_hint>
        <paragraph>
            If running in the IPython console, consider running 
            <literal>
                %matplotlib
             to enable
            interactive plots.  If running in the Jupyter Notebook, use 
            <literal>
                %matplotlib
                inline
            .
    <paragraph>
        More text here.""", pxml)
    page = """\
Text here

.. mpl-interactive::

    Any ReST you *like*.

More text here."""
    pxml = to_pxml.from_rst(page)
    assert re.match("""\
<document source=".*?">
    <paragraph>
        Text here
    <mpl_hint>
        <paragraph>
            Any ReST you 
            <emphasis>
                like
            .
    <paragraph>
        More text here.""", pxml)
