from zope import interface, schema
from plone.theme.interfaces import IDefaultPloneLayer

from ploudenv.themegallery import themegalleryMessageFactory as _

class IThemeGallerySettingsSchema(interface.Interface):

    tgserver_url = schema.TextLine(
        title=_(u'Server'),
        description=_(u'URL to reach themegallery server'),
        required=True,
        readonly=False,
        default=u"https://ploud.com/",
        )
