Messaging
#########

The tdf.extensionuploadcenter Plone add-on use some of the Plone messaging
implementations to create messages to the site admin, reviewers and the
owner / creator of extensions / extension projects.

Messages To The Site-Admininstrator / Administrator
***************************************************

- The site-administrator / admininstrator get an e-mail once a new extension
  project or small extension project have been added to the Extension Center.
- If the project owner submit her / his project / small project for
  publication, the site-administrator / administrator get an e-mail about
  this event.
- Once the text of a published project or small project change the
  site-administrator / administrator will get an e-mail with the complete
  text of the project / small project summary and its description. Thus
  he get an information, if the text of the project / small project
  changes into a direction that has not been reviewed.

If the form field 'contactForCenter' in the Extension Center contains an
e-mail address the above messages will be send to this address. Otherwise
the e-mail goes to the e-mail address of the Plone site.



Messages To The Project Owner
*****************************

- Once a workflow status of her / his project(s) / small project(s) change
  the project / small project owner will get a message (e-mail) which
  inform her / him about this new status.
- The project owner will get an e-mail once an extension release or a linked
  extension release have been added to her / his project(s).
- Once the site-administrator / administrator of the Plone site adds a new
  LibreOffice (product) version to the form field 'Available Versions' the
  owner of a project will get an e-mail to inform her / him about this
  event. The message ask the owner to update the versions list of the
  (linked) releases of his project(s). The owner of a small extension
  project will also get such message and should update the versions
  information on her / his small project(s).


Messages To A Possible Information Hub Of Extension Releases
************************************************************

It is possible to create a hub outside of the Plone site, that drives the
Extension Center, which could get an e-mail for every new published extension
(linked) release. This e-mail could be parsed and used to inform the user
of the product about new (linked) releases from inside LibreOffice (the
product).




