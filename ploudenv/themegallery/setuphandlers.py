# -*- coding: utf-8 -*-
import logging
from Products.CMFCore.utils import getToolByName

PROFILE_ID = 'profile-ploudenv.themegallery:default'

def add_registry(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('ploudenv.themegallery')
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')
    logger.info("Imported Registry settings")

def setupVarious(context):
    """Import step for configuration that is not handled in xml files.
    """
    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('ploudenv.themegallery.various.txt') is None:
        return
    logger = context.getLogger('ploudenv.themegallery')
    site = context.getSite()

