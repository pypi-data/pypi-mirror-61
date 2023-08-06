==================
PyAMS_i18n package
==================


Introduction
------------

This package is composed of a set of utility functions, usable into any Pyramid application, which
allows to provide translations to any property using custom I18n schema fields.


Site upgrade
------------

PyAMS_i18n provides a site generation utility, which automatically create a negotiator utility:

    >>> from pyramid.testing import setUp, tearDown, DummyRequest
    >>> config = setUp()
    >>> config.registry.settings['zodbconn.uri'] = 'memory://'

    >>> from pyramid_zodbconn import includeme as include_zodbconn
    >>> include_zodbconn(config)
    >>> from pyams_utils import includeme as include_utils
    >>> include_utils(config)
    >>> from pyams_site import includeme as include_site
    >>> include_site(config)
    >>> from pyams_i18n import includeme as include_i18n
    >>> include_i18n(config)


Using negotiator
----------------

A negotiator is a registered utility which can be used to define how language selection is made;
several policies are available, between:

 - browser: used language is based on browser's settings, transmitted into requests headers

 - session: the session is stored into a user's attribute which is stored into it's session

 - server: the language is extrated from server settings.

You can also choose to select a "combined" policy, which will scan several options before chossing
a language, for example "session -> browser -> server" (which is the default).

    >>> from zope.traversing.interfaces import BeforeTraverseEvent
    >>> from pyramid.threadlocal import manager
    >>> from pyams_utils.registry import handle_site_before_traverse, get_local_registry
    >>> from pyams_site.generations import upgrade_site

    >>> request = DummyRequest(headers={'Accept-Language': 'en'})
    >>> app = upgrade_site(request)
    Upgrading PyAMS timezone to generation 1...
    Upgrading PyAMS I18n to generation 1...

    >>> handle_site_before_traverse(BeforeTraverseEvent(app, request))
    >>> manager.push({'request': request, 'registry': config.registry})

    >>> 'Language negotiator' in app.getSiteManager()
    True
    >>> negotiator = app.getSiteManager()['Language negotiator']
    >>> negotiator.policy
    'session --> browser --> server'
    >>> negotiator.server_language
    'en'
    >>> negotiator.offered_languages
    {'en'}

PyAMS_i18n also defines request properties, like locale and localizer:

    >>> loc = request.localizer
    >>> loc
    <pyramid.i18n.Localizer object at 0x...>
    >>> loc.locale_name
    'en'


Languages vocabularies
----------------------

There are two defined vocabularies concerning languages; the first on called "Offered languages",
provides a list of languages which can be selected as "server" policies, or which can be selected
when you need to provide translations of a given content:

    >>> from zope.schema.vocabulary import getVocabularyRegistry
    >>> from pyams_i18n.interfaces import OFFERED_LANGUAGES_VOCABULARY_NAME

    >>> context = {}
    >>> registry = getVocabularyRegistry()

    >>> from pyams_i18n.interfaces import INegotiator
    >>> config.registry.registerUtility(negotiator, INegotiator)
    >>> negotiator.offered_languages =  {'en', 'fr', 'es'}
    >>> languages = registry.get(context, OFFERED_LANGUAGES_VOCABULARY_NAME)
    >>> languages
    <...I18nOfferedLanguages object at 0x...>
    >>> len(languages)
    3
    >>> languages.getTermByToken('en').value
    'en'
    >>> languages.getTermByToken('en').title
    'English'
    >>> languages.getTermByToken('fr').value
    'fr'
    >>> languages.getTermByToken('fr').title
    'French'

When languagas have been selected for a given I18n content manager, you can select which languages
are selected for a given content using another vocabulary:

    >>> from pyams_i18n.interfaces import CONTENT_LANGUAGES_VOCABULARY_NAME
    >>> languages = registry.get(context, CONTENT_LANGUAGES_VOCABULARY_NAME)
    >>> languages
    <...I18nContentLanguages object at 0x...>
    >>> len(languages)
    1

There is only one language actually in this vocabulary, which is the server language:

    >>> languages.getTerm('en').title
    'English'
    >>> languages.getTerm('fr').title
    Traceback (most recent call last):
    ...
    LookupError: fr

We first have to create a I18n manager, which will be the parent of our future context:

    >>> from zope.interface import alsoProvides
    >>> from pyams_i18n.content import I18nManagerMixin

    >>> manager = I18nManagerMixin()
    >>> manager.languages = ['en', 'fr']

    >>> from zope.container.contained import Contained
    >>> context = Contained()
    >>> context.__parent__ = manager
    >>> languages = registry.get(context, CONTENT_LANGUAGES_VOCABULARY_NAME)
    >>> languages
    <...I18nContentLanguages object at 0x...>
    >>> len(languages)
    2
    >>> [t.value for t in languages]
    ['en', 'fr']
    >>> languages.getTerm('en').title
    'English'
    >>> languages.getTerm('fr').title
    'French'

Server language is automatically added to content available languages, always in first place:

    >>> manager.languages = ['fr', 'es']
    >>> languages = registry.get(context, CONTENT_LANGUAGES_VOCABULARY_NAME)
    >>> languages
    <...I18nContentLanguages object at 0x...>
    >>> len(languages)
    3
    >>> [t.value for t in languages]
    ['en', 'fr', 'es']


Using I18n manager
------------------

The I18n manager is used to define, in any context, the set of languages which are "offered" for
translation; as providing translations is overloading the user interface while not being used
very often, if only by defining this at the manager level that you can really activate
translations.

    >>> from pyams_i18n.content import I18nManagerMixin
    >>> class MyI18nManager(I18nManagerMixin):
    ...     """Custom I18n manager class"""

    >>> i18n_manager = MyI18nManager()
    >>> i18n_manager.languages = ['fr', 'en', 'es']

Manager provides the full ordered list of available languages; server's language as defined into
negotiator settings is always set first, as a default fallback language, even if not included
into languages list:

    >>> i18n_manager.get_languages()
    ['en', 'es', 'fr']

    >>> i18n_manager.languages = ['fr', 'es']
    >>> i18n_manager.get_languages()
    ['en', 'es', 'fr']

I18n manager is a base class for many contents handling translations.


Translated properties
---------------------

After setting server settings, it's time to create custom interfaces to handle translated
properties:

    >>> from zope.interface import implementer, Interface
    >>> from zope.schema.fieldproperty import FieldProperty
    >>> from pyams_i18n.schema import I18nTextLineField, I18nTextField, I18nHTMLField

    >>> class IMyI18nContent(Interface):
    ...     text_line = I18nTextLineField(title="Text line field")
    ...     text = I18nTextField(title="Text field")
    ...     html = I18nHTMLField(title="HTML field")

    >>> @implementer(IMyI18nContent)
    ... class MyI18nContent:
    ...     text_line = FieldProperty(IMyI18nContent['text_line'])
    ...     text = FieldProperty(IMyI18nContent['text'])
    ...     html = FieldProperty(IMyI18nContent['html'])

    >>> my_content = MyI18nContent()

Instance attributes are then set as mappings, where keys are the language codes and values are
classic values matching each field type:

    >>> value = {'en': "Invalid text line\n", 'fr': "Ligne de texte valide"}
    >>> IMyI18nContent['text_line'].validate(value)
    Traceback (most recent call last):
    ...
    zope.schema._bootstrapinterfaces.WrongContainedType: ([ConstraintNotSatisfied('Invalid text line\n', '')], 'text_line')

    >>> value = {'en': "Text line", 'fr': "Ligne de texte"}
    >>> IMyI18nContent['text_line'].validate(value)

    >>> my_content.text_line = value


Getting translated values
-------------------------

The :py:class:`II18n <pyams_i18n.interfaces.II18n>` interface is used to query an I18n value; the
returned value is trying to match browser settings with offered languages: if a requested language
is not defined or have an empty value, the value defined for the default server language will be
used:

    >>> from pyams_i18n.interfaces import II18n
    >>> i18n = II18n(my_content)
    >>> i18n.query_attribute('text_line', request=request)
    'Text line'

Of course, we can change browser settings to get another translated value:

    >>> request = DummyRequest(headers={'Accept-Language': 'fr, en-US;q=0.9'})
    >>> i18n.query_attribute('text_line', request=request)
    'Ligne de texte'

    >>> request = DummyRequest(headers={'Accept-Language': 'es, en-US;q=0.9'})
    >>> i18n.query_attribute('text_line', request=request)
    'Text line'

It's also possible to get any translated value "as is", without using request headers, eventually
by providing a default value:

    >>> i18n.get_attribute('text_line', request=request) is None
    True
    >>> i18n.get_attribute('text_line', lang='es') is None
    True
    >>> i18n.get_attribute('text_line', lang='es', default='Linea de texto')
    'Linea de texto'
    >>> i18n.get_attribute('text_line', lang='fr', request=request)
    'Ligne de texte'

Another option is to use a request or session parameter to define user's language; this can be
helpful, for example when you want to preview your web site in different languages, without the
need to modify your browser settings (this feature is used by PyAMS_content package):

    >>> request = DummyRequest(params={'lang': 'fr'})
    >>> i18n.query_attribute('text_line', request=request)
    'Ligne de texte'

    >>> request = DummyRequest()
    >>> request.session['language'] = 'fr'
    >>> i18n.query_attribute('text_line', request=request)
    'Ligne de texte'


I18n TALES expression
---------------------

An "i18n:" TALES expression is available to get I18n attributes directly from Chameleon templates;
this test is using PyAMS_template template factory, but this should work with any Chameleon
template:

    >>> import os
    >>> from tempfile import mkdtemp
    >>> temp_dir = mkdtemp()
    >>> template = os.path.join(temp_dir, 'template.pt')
    >>> with open(template, 'w') as file:
    ...     _ = file.write('<div>${i18n:context.text_line}</div>')

    >>> from pyramid.interfaces import IRequest
    >>> from pyams_template.interfaces import IContentTemplate
    >>> from pyams_template.template import TemplateFactory, get_content_template
    >>> factory = TemplateFactory(template, 'text/html')
    >>> config.registry.registerAdapter(factory, (Interface, IRequest, Interface), IContentTemplate)

    >>> from pyams_utils.adapter import ContextRequestAdapter
    >>> @implementer(Interface)
    ... class MyContentView(ContextRequestAdapter):
    ...     template = get_content_template()
    ...     def __call__(self):
    ...         return self.template(**{'context': self.context, 'request': self.request})

    >>> my_view = MyContentView(my_content, request)
    >>> print(my_view())
    <div>Ligne de texte</div>

Using a different request setting should return another result:

    >>> request = DummyRequest()
    >>> my_view = MyContentView(my_content, request)
    >>> print(my_view())
    <div>Text line</div>

Another option is to use the "i18n" TALES extension, as provided my PyAMS_utils; the benefit of
this method is that it also provides a default value is requested property doesn't exist:

    >>> with open(template, 'w') as file:
    ...     _ = file.write("<div>${tales:i18n(context, 'missing_property', 'Default value')}</div>")
    >>> factory = TemplateFactory(template, 'text/html')
    >>> config.registry.registerAdapter(factory, (Interface, IRequest, Interface), IContentTemplate)

    >>> my_view = MyContentView(my_content, request)
    >>> print(my_view())
    <div>Default value</div>


Tests cleanup:

    >>> tearDown()
