=====================
pyams_viewlet package
=====================

These doctests are based on zope.viewlet doctests.

In this implementation of viewlets, we first have to define *viewlet managers*, which are special
content providers which manage a special type of content providers called *viewlets*. Every
viewlets manager handles the viewlets registered for it:

    >>> from pyramid.testing import setUp, tearDown
    >>> config = setUp()

    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)
    >>> from pyams_template import includeme as include_template
    >>> include_template(config)
    >>> from pyams_viewlet import includeme as include_viewlet
    >>> include_viewlet(config)

    >>> from pyams_viewlet.interfaces import IViewletManager

    >>> class ILeftColumn(IViewletManager):
    ...     """Left column viewlet manager"""

We can then create a viewlet manager factory using this interface:

    >>> from pyams_viewlet.manager import ViewletManagerFactory
    >>> LeftColumn = ViewletManagerFactory('left-column', ILeftColumn)

Having the factory, we can instantiate it:

    >>> from zope.interface import implementer, Interface
    >>> @implementer(Interface)
    ... class Content:
    ...     """Content class"""
    >>> content = Content()

    >>> from pyramid.interfaces import IView, IRequest
    >>> from pyramid.testing import DummyRequest
    >>> request = DummyRequest()

    >>> @implementer(IView)
    ... class View:
    ...     def __init__(self, context, request):
    ...         self.context = context
    ...         self.request = request
    >>> view = View(content, request)

    >>> left_column = LeftColumn(content, request, view)

Actually, viewlet manager doesn't render anything:

    >>> left_column.update()
    >>> left_column.render()
    ''

We have to create and register viewlets for the manager:

    >>> from pyams_viewlet.interfaces import IViewlet
    >>> from pyams_viewlet.viewlet import EmptyViewlet
    >>> class TextBox(EmptyViewlet):
    ...     def render(self):
    ...         return '<div class="text">Text box!</div>'
    ...     def __repr__(self):
    ...         return '<TextBox object at %x>' % id(self)

    >>> config.registry.registerAdapter(TextBox,
    ...                                 (Interface, IRequest, IView, ILeftColumn),
    ...                                 IViewlet, name='text-box')

    >>> left_column.render()
    ''

Why is it empty? It's because viewlet managers are memoized on rendering, because they are
generally used only once in a given page, so we have to reset it's state if we want to render it
another time:

    >>> left_column.reset()
    >>> left_column.update()
    >>> left_column.render()
    '<div class="text">Text box!</div>'

After being registered, a viewlet manager (as any registered content provider) can be included
into a Chameleon template easilly:

    >>> from zope.contentprovider.interfaces import IContentProvider
    >>> config.registry.registerAdapter(LeftColumn, (Interface, IRequest, Interface),
    ...                                 IContentProvider, name='left-column')

    >>> from chameleon import PageTemplateFile
    >>> from pyams_viewlet.provider import ProviderExpr

    >>> PageTemplateFile.expression_types['provider'] = ProviderExpr

    >>> import os, tempfile
    >>> temp_dir = tempfile.mkdtemp()
    >>> template = os.path.join(temp_dir, 'template.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write('<div>${structure:provider:left-column}</div>')

    >>> from pyams_template.interfaces import IPageTemplate
    >>> from pyams_template.template import TemplateFactory
    >>> factory = TemplateFactory(template, 'text/html')
    >>> config.registry.registerAdapter(factory, (Interface, IRequest, None), IPageTemplate)
    >>> render = config.registry.getMultiAdapter((content, request, view), IPageTemplate)
    >>> render(**{'context': content, 'request': request, 'view': view})
    '<div><div class="text">Text box!</div></div>'

Just keep in that that we generally use decorators to register viewlets and viewlets managers,
as well as other content providers, to keep the syntax simple and clean.


Test cleanup:

    >>> tearDown()
