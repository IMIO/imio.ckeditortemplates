# -*- coding: utf-8 -*-
from collective.ckeditortemplates.setuphandlers import FOLDER
from plone import api
from plone.app.textfield.value import RichTextValue


IMAGES_FOLDER = 'images'

def setupTemplates(context):
    if context.readDataFile('imio.ckeditortemplates.txt') is None:
        return

    site = context.getSite()
    types = api.portal.get_tool(name="portal_types")
    types.getTypeInfo('cktemplatefolder').filter_content_types = False
    cktfolder = getattr(site, FOLDER)
    if not cktfolder.get(IMAGES_FOLDER):
        api.content.create(
            type='Folder',
            title=IMAGES_FOLDER,
            container=cktfolder)

    types.getTypeInfo('cktemplatefolder').filter_content_types = True

    templates = {
            u'Pésentation service': presentationservice(),
            u'Présentation élu': presentationelu()}

    for key in templates.keys():
        if not cktfolder.get(key):
            rtv = RichTextValue(templates[key])
            template = api.content.create(
                    type="cktemplate",
                    title=key,
                    content=rtv,
                    container=cktfolder)
            state = api.content.transition(obj=template, transition='enable')



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
<p class="horloge">&nbsp;</p>
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
<div class="bloc-main"><img alt="" class="image-left-border" src="++resource++imio.ckeditortemplates/photo-exemple.jpg" style="height:125px; width:125px" />
<div class="bloc-content">

<h2>Nom</h2>
<p>Fonction</p>
<p class="adresse">&nbsp;</p>
<p class="telephone">&nbsp;</p>
<p class="mail">&nbsp;</p>
</div>

<div class="bloc-content">
<h3>Attributions</h3>
<ul>
    <li>&nbsp;</li>
    <li>&nbsp;</li>
    <li>&nbsp;</li>
</ul>
</div>
<div class="clear">&nbsp;</div>
</div>
'''
    return text
