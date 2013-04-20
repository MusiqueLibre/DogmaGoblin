# GNU MediaGoblin -- federated, autonomous media hosting
# Copyright (C) 2011, 2012 MediaGoblin contributors.  See AUTHORS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import wtforms
from mediagoblin.tools.text import tag_length_validator
from mediagoblin.tools.licenses import licenses_as_choices
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from mediagoblin.tools.translate import fake_ugettext_passthrough as _
#multiple upload
from wtforms.widgets import html_params, HTMLString
from cgi import escape

#Custom multiple file input field made by pythonsnake

class MultipleFileInput(object):
    def __call__(self, field, **kwargs):
        value = field._value()
        html = [u'<input %s>' % html_params(name='file[]', id='multi_file_input', type='file', multiple=True, style="display: none;", **kwargs)]
        html.append(u'<input %s>' % html_params(class_="button_action", id="multi_browse",  type="button", value="Browse...", \
                     style="width:auto;", **kwargs))
        if value:
            kwargs.setdefault('value', value)
        return HTMLString(u''.join(html))

class MultipleFileField(wtforms.FileField):
    widget = MultipleFileInput()

class DogmaSubmitFormTrack(wtforms.Form):
    title_0 = wtforms.TextField(
        _('Title'),
        [wtforms.validators.Length(min=0, max=500)],
        description=_(
          "Leave empty to use the file's name."))
    license_0 = wtforms.SelectField(
        _('License'),
        [wtforms.validators.Optional(),],
        choices=licenses_as_choices())
    tags_0 = wtforms.TextField(
        _('Tags for this tracks'),
        [tag_length_validator],
        description=_(
          "Separate tags by commas. (they will be added to the global tags)"))
    description_0 = wtforms.TextAreaField(
        _('Description of this work'),
        description=_("""You can use
                      <a href="http://daringfireball.net/projects/markdown/basics">
                      Markdown</a> for formatting."""))

class DogmaSubmitFormGlobal(wtforms.Form):
    tags = wtforms.TextField(
        _('Tags for ALL tracks'),
        [tag_length_validator],
        description=_(
          "Separate tags by commas."))
    license = wtforms.SelectField(
        _('License for ALL tracks'),
        [wtforms.validators.Optional()],
        choices=licenses_as_choices())
    file = MultipleFileField(_('File'))


class BandForm(wtforms.Form):
    band_virtual = wtforms.BooleanField(
        _('Nope, this is a virtual band'),
        description=_("There is no location for this band, its members comes from different places")
        )
    band_name = wtforms.TextField(
        _('Name *'),
        [wtforms.validators.Required()],
        )
    band_picture = wtforms.FileField(_('Band picture'))
    band_description = wtforms.TextAreaField(
        _('Description of the band'),
        description=_("""You can use
                      <a href="http://daringfireball.net/projects/markdown/basics">
                      Markdown</a> for formatting."""),
        )
class BandSelectForm(wtforms.Form):
    band_select = QuerySelectField(
        _('Bands'),
        allow_blank=True, blank_text=_('-- Select --'), get_label='name')

class MemberForm(wtforms.Form):
    member_first_name_0 = wtforms.TextField(
        _('First name'),
        )
    member_last_name_0 =  wtforms.TextField(
        _('Last name'),
        )
    member_nickname_0 =  wtforms.TextField(
        _('Nickname'),
        )
    member_roles_0 =  wtforms.TextField(
        _('Role in the band *'),
        [wtforms.validators.Required()],
        description=_("Use commas to separate roles")
        )
    member_picture_0 = wtforms.FileField(_('Picture'))
    member_description_0 =  wtforms.TextAreaField(
        _('Bio'),
        description=_("""You can use
                      <a href="http://daringfireball.net/projects/markdown/basics">
                      Markdown</a> for formatting."""),
        )
        
class AlbumForm(wtforms.Form):
    collection_title = wtforms.TextField(
        _('Album Title'),
        [wtforms.validators.Length(min=0, max=500)])
    album_cover = wtforms.FileField(_('Album cover'))
    collection_description = wtforms.TextAreaField(
        _('Description of this Album'),
        description=_("""You can use
                      <a href="http://daringfireball.net/projects/markdown/basics">
                      Markdown</a> for formatting."""))
