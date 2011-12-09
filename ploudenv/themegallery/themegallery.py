import tempfile
import simplejson as json
import pprint, urllib, logging
from zope.publisher.browser import BrowserView

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.decode import processInputs
from Products.statusmessages.interfaces import IStatusMessage

import zipfile
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.resource.utils import queryResourceDirectory
from plone.app.theming.interfaces import IThemeSettings
from plone.app.theming.utils import extractThemeInfo
from plone.app.theming.utils import getZODBThemes
from plone.app.theming.utils import getAvailableThemes
from plone.app.theming.utils import applyTheme
from plone.app.theming.utils import getOrCreatePersistentResourceDirectory
from plone.app.theming.plugins.utils import getPluginSettings
from plone.app.theming.plugins.utils import getPlugins
from plone.app.theming.interfaces import THEME_RESOURCE_NAME


logger = logging.getLogger('ploudenv.themegallery')

api = 'https://ploud.com/__rest__/cms/applications'


class PloudThemeGallery(BrowserView):

    error = None

    base_url = 'https://ploud.com/__rest__/cms/content:themes'

    def __call__(self):
        self.update()
        return self.index()

    def load(self):
        data = json.loads(urllib.urlopen(api).read())

        link = ''
        for rec in data:
            if rec['__name__'] == 'themes':
                link = rec['__link__']
                break

        data = json.loads(urllib.urlopen(link).read())

        themes = []
        for rec in data['__contents__']:
            theme_info = json.loads(urllib.urlopen(rec['__link__']).read())
            if 'theme-file' not in theme_info:
                continue

            themes.append(theme_info)

        return themes

    def loadTheme(self, uuid):
        url = '%s/%s/data'%(self.base_url, uuid)

        tfile = tempfile.mkstemp('.zip')[1]

        urllib.urlretrieve(url, tfile)
        return tfile

    def update(self):
        form = self.request.form
        self.settings = getUtility(IRegistry).forInterface(
            IThemeSettings, False)

        if 'form.button.install' in form:
            theme = form.get('theme_uuid', None)

            if theme is not None:
                tfile = self.loadTheme(theme)
                try:
                    themeZip = zipfile.ZipFile(tfile)
                except (zipfile.BadZipfile, zipfile.LargeZipFile,):
                    logger.exception("Could not read zip file")
                    self.error = u"The uploaded file is not a valid Zip archive"
                    return

                if themeZip:
                    try:
                        themeData = extractThemeInfo(themeZip)
                    except (ValueError, KeyError,), e:
                        logger.warn(str(e))
                        self.error = u"The uploaded file does not contain a valid theme archive."

                    else:
                        themeContainer=getOrCreatePersistentResourceDirectory()
                        themeExists = themeData.__name__ in themeContainer

                        if themeExists:
                            del themeContainer[themeData.__name__]

                        themeContainer.importZip(themeZip)
                        themeDirectory = queryResourceDirectory(
                            THEME_RESOURCE_NAME, themeData.__name__)
                        if themeDirectory is not None:
                            plugins = getPlugins()
                            pluginSettings = getPluginSettings(
                                themeDirectory, plugins)
                            if pluginSettings is not None:
                                for name, plugin in plugins:
                                    plugin.onCreated(
                                        themeData.__name__,
                                        pluginSettings[name],
                                        pluginSettings)

                        applyTheme(themeData)
                        self.settings.enabled = True

                        IStatusMessage(self.request).add(
                            "Theme has been installed.")
