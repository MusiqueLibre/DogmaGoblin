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

class DogmaTracks(wtforms.Form):
    title_0 = wtforms.TextField(
        _('Title'),
        [wtforms.validators.Length(min=0, max=500)],
        description=_(
          "Leave empty to use the file's name."))
    license_0 = wtforms.SelectField(
        _('License'),
        [wtforms.validators.NoneOf('_None', _(u"You must select a licence !"))],
        choices=licenses_as_choices())
    composers_0 = wtforms.TextField(
        _('Composer(s)'),
        [tag_length_validator],
        description=_(
          "Separate names by commas."))
    authors_0 = wtforms.TextField(
        _('Author(s)'),
        [tag_length_validator],
        description=_(
          "Separate names by commas."))
    performerNo0_0 = wtforms.TextField(
        _('Extra Performer'))
    performer_rolesNo0_0 = wtforms.TextField(
        _('plays'))
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

class DogmaTracksGlobal(wtforms.Form):
    composers = wtforms.TextField(
        _('Composer(s) for ALL tracks'),
        [tag_length_validator],
        description=_(
          "Separate names by commas."))
    authors = wtforms.TextField(
        _('Author(s) for ALL tracks'),
        [tag_length_validator],
        description=_(
          "Separate names by commas."))
    tags = wtforms.TextField(
        _('Tags for ALL tracks'),
        [tag_length_validator],
        description=_(
          "Separate tags by commas. Songs' tags will be added to global tags."))
    license = wtforms.SelectField(
        _('License for ALL tracks'),
        [wtforms.validators.Optional()],
        choices=licenses_as_choices())
    tracks = MultipleFileField(_('Tracks'),
            description= _("Use CTRL and/or SHIFT to select multiple items"))


class BandForm(wtforms.Form):
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

class DatePickerInput(object):
    def __call__(self, field, **kwargs):
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        html = [u'<div class="datePicker dateUnprocessed '+field.custom_class+'" data-millis="'+field.millis+'" >\
                <input %s />' % html_params(type="hidden", name=field.name, class_="date_picker_input",  **kwargs)]
        if field.quick_date:
            html.append(u'<button class="button_action copy_band_date" type="button">%s</button>' % field.quick_date)
        html.append(u'</div>')
        return HTMLString(u''.join(html))

class DatePickerField(wtforms.FileField):
    widget = DatePickerInput()

    def __init__(self,label=None, validators=None,quick_date=None, millis=u'', custom_class=u'', **kwargs):
        super(DatePickerField, self).__init__(label, validators, **kwargs)
        self.quick_date = quick_date
        self.millis = millis
        self.custom_class = custom_class

class MemberForm(wtforms.Form):
    member_username_0 = wtforms.TextField(
        _('User name *'),
        [wtforms.validators.Required()]
        )
    member_real_name_0 =  wtforms.TextField(
        _('Real name')
        )
    member_picture_0 = wtforms.FileField(_('Picture'))
    member_description_0 =  wtforms.TextAreaField(
        _('Bio'),
        description=_("""You can use
                      <a href="http://daringfireball.net/projects/markdown/basics">
                      Markdown</a> for formatting."""),
        )
    member_since_0 = DatePickerField(_('Member Since'),
            [wtforms.validators.Required()],
            quick_date = _("Member since the begining of the band"),
            )
    member_former_0 = wtforms.BooleanField(_('Former member'))
    member_until_0 = DatePickerField(_('Member until'))
        
class AlbumForm(wtforms.Form):
    release_date = DatePickerField(_('Release date of this album *'),
            [wtforms.validators.Required()],
            custom_class=_("album_release")
            )
    collection_title = wtforms.TextField(
        _('Album Title'),
        [wtforms.validators.Required(),
        wtforms.validators.Length(min=0, max=500)])
    album_cover = wtforms.FileField(_('Album cover'))
    collection_description = wtforms.TextAreaField(
        _('Description of this Album'),
        description=_("""You can use
                      <a href="http://daringfireball.net/projects/markdown/basics">
                      Markdown</a> for formatting."""))
