# -*- coding: utf-8 -*-
from collective.ckeditortemplates.setuphandlers import FOLDER
from plone import api
from plone.app.textfield.value import RichTextValue
from plone.uuid.interfaces import ATTRIBUTE_NAME
import logging
logger = logging.getLogger("imio.ckeditortemplates setup")

IMAGES_FOLDER = 'images'


def setupTemplates(context):
    if context.readDataFile('imio.ckeditortemplates.txt') is None:
        return

    site = context.getSite()
    types = api.portal.get_tool(name="portal_types")
    types.getTypeInfo('cktemplatefolder').filter_content_types = False
    cktfolder = getattr(site, FOLDER)
    import ipdb; ipdb.set_trace()
    try:
        api.content.transition(obj=cktfolder,
                               transition='publish_and_hide')
    except api.exc.InvalidParameterError:
        logger.info("No publish_and_hide workflow")

    if not cktfolder.get(IMAGES_FOLDER):
        folder_images = api.content.create(
            type='Folder',
            title=IMAGES_FOLDER,
            container=cktfolder,
            language='fr')

        add_images(folder_images)

    types.getTypeInfo('cktemplatefolder').filter_content_types = True

    templates = [
        {'id': 'presentation-elu',
         'title': u'Présentation élu',
         'text': presentationelu()},
        {'id': 'presentation-service',
         'title': u'Présentation service',
         'text': presentationservice()}
    ]

    for template in templates:
        if not cktfolder.get(template['id']):
            rtv = RichTextValue(template['text'])
            template = api.content.create(type="cktemplate",
                                          id=template['id'],
                                          title=template['title'],
                                          content=rtv,
                                          container=cktfolder,
                                          language='fr')
            try:
                api.content.transition(obj=template, transition='enable')
            except api.exc.InvalidParameterError:
                logger.info("No enable workflow")

    """ Allow figcaption as valid tag in portal_transforms safe_html"""

    from Products.PortalTransforms.Transform import make_config_persistent

    pt = api.portal.get_tool(name='portal_transforms')
    tid = 'safe_html'
    if tid not in pt.objectIds():
        return
    trans = pt[tid]
    tconfig = trans._config

    validtags = tconfig['valid_tags']
    validtags.update({'figcaption': 1})

    make_config_persistent(tconfig)
    trans._p_changed = True
    trans.reload()


def add_images(folder_images):
    images = [
        {'name': 'adresse.png', 'uuid': '62c875a43fca465aa7960312ec74cadr'},
        {'name': 'courriel.png', 'uuid': '9b2970be20414acd81a7ee1d85732cou'},
        {'name': 'fax.png', 'uuid': '922d4db790524e40865a72be3253fax'},
        {'name': 'femme.png', 'uuid': 'f3961428681843f386f83a6ef173fem'},
        {'name': 'gsm.png', 'uuid': '5716be3bb02246a097b752a92d4agsm'},
        {'name': 'homme.png', 'uuid': 'a0adc656cdc94b18821fb84fc9dfhom'},
        {'name': 'horloge.png', 'uuid': '13a4a96fc0254fbfbaf7d7b20cd5hor'},
        {'name': 'lien.png', 'uuid': '6b334453028e4fb385bd9c4ee46clie'},
        {'name': 'pdf-1.png', 'uuid': '1a3e3bfbab544f009faa7d527a0pdf'},
        {'name': 'photo-exemple.jpg', 'uuid': 'f52fb2d7b47648b288a7ff897b5ppho'},
        {'name': 'telephone.png', 'uuid': '3592b8b7a4f44b8c9d9c04595a0tel'},
        {'name': 'localisation.png', 'uuid': '4b73aff9d5dc47df8e84998c8aec8357'},
    ]
    import os
    from imio.ckeditortemplates import interfaces
    package_path = os.path.dirname(interfaces.__file__)
    for image in images:
        if not folder_images.get(image):
            img_path = os.sep.join([package_path, "browser", "static", image['name']])
            img_file = open(img_path, 'r')
            img = api.content.create(type="Image",
                                     title=image['name'],
                                     image=img_file,
                                     container=folder_images,
                                     language='fr')
            img._setUID(image['uuid'])
            if api.content.get_uuid(obj=img) != image['uuid']:
                # its a dexterity content
                setattr(img, ATTRIBUTE_NAME, image['uuid'])
            img.reindexObject()


def presentationservice():
    text = '''
<div class="infos-service">
<div class="coordonnees">
<p class="adresse">&nbsp;</p>
<p class="homme">&nbsp;</p>
<p class="telephone">&nbsp;</p>
<p class="fax">&nbsp;</p>
<p class="mail">&nbsp;</p>
<p class="lien">&nbsp;</p>
</div>
<div class="horaire">
<p>&nbsp;</p>
</div>
<div class="clear">&nbsp;</div>
</div>
<h2>Membres du service</h2>
<p>&nbsp;</p>
<h2>Missions</h2>
<p>&nbsp;</p>
<p>&nbsp;</p>
'''
    return text


def presentationelu():
    text = '''
<div class="bloc-main-2">
<h2>Nom</h2>
<p class="elu-fonction">Fonction</p>
<img alt="" class="image-left" height="125" src="++resource++imio.ckeditortemplates/photo-exemple.jpg" style="width: 125px; height: 125px;" width="125" />
<p class="adresse">&nbsp;</p>
<p class="telephone">&nbsp;</p>
<p class="mail">&nbsp;</p>
<p class="elu-attribution">Attributions</p>
</div>
'''
    return text
