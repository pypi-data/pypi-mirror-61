DOM query
===========

CSS selector syntax for python minidom and DOM implementations.

Short example
-------------

Provided an HTML file *sample.html* the following code will query
some elements and return them as *minidom* *Elements*.
In case of multiple elements (*select_all*) a simple python *list*
is returned (instead of a minidom *NodeList*).

.. code-block:: python

    from xml.dom.minidom import parse
    from dom_query import select, select_all

    tree = parse("test/html/sample.html")

    # Title element
    title = select(tree, "title")

    # Every P element
    paragraphs = select_all(tree, "p")

    # Element with type P and ID equal to "summary"
    summary = select(tree, "p#summary")

    # Every element with class "wide"
    wide_elements = select_all(tree, ".wide")

Supported CSS syntax
--------------------

Only a subset of CSS syntax is supported:

- Compound selectors (comma separator),
- element type and id,
- classes presence,
- attributes match (presence and all the other operators),
- combinators (descendant, sibling, subsequent, child).

Some supported selectors:

.. code-block:: css

    p#abstract[lang|=en]
    p[data-user="john"]
    div > p + p, article > p + p
    script[type="text/data"]
    header > li ul, footer > li ul
    section h1 ~ p, article h2 ~ p

Internals and implementation
----------------------------

Every query is compiled and cached for subsequent use.

Lexer
^^^^^

The first stage is tokenization (*lexer.py lexer*) which is loosely
based on the
`W3C selector lexer <https://www.w3.org/TR/selectors-3/#lex>`_.
The differences are mainly to make the tokenizer compatible with
regular expressions and to strip every unnecessary features.

Parser
^^^^^^

Then follows the parsing stage (*parser.py parse*) which produce a
simple AST from the tokens. The parser is, just like the tokenizer, a
simplified version of the standard one. It is a single function which
implements a descent parser. The AST is a tuple of tuples and maps in
a relatively close way the given query.

Compiler
^^^^^^^^

The last stage is the compiler (*compiler.py compile*). It translates
the AST into a sequence of simple actions to be performed in order to
select the matching elements.
Once compiled it is saved in cache and will be reused whenever the same
query is seen again.

Virtual machine
^^^^^^^^^^^^^^^

The opcodes are executed by (*vm.py execute*). This function takes a
starting element, a sequence of opcodes, and an *api*.
The api is dict-like object. Every key corresponds to a function which
implements an opcode. The default api is *minidom_api.py api*.

DOM API
^^^^^^^

Every function in the api is either a filter (actual filtering of nodes)
or a generator (combinators expansion). The only two opcodes which don't
follows this rule are *YIELD* (return elements found so far) and *RESET*
(reload the original element node after a CSS comma).

In case of other *dom* implementations it *should* be sufficient to
write a new api and pass it to *execute* (or *select\**) upon querying.

Code quality and stability
--------------------------

The code is far from complete.
It is tested but there are minor issues (attribute match doesn't follow
the specs verbatim).

Feel free to contribute.
