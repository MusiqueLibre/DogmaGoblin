# -*- coding: utf-8 -*-
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

#FORMS
import wtforms
from mediagoblin.plugins.wtform_html5.wtforms_html5 import (TextField, IntegerField, DateField,
        TextAreaField, DateRange)
#multiple upload
from wtforms.widgets import html_params, HTMLString

from mediagoblin.plugins.dogma_lib.countries import countries_list
from mediagoblin.plugins.dogma_lib.lib import complete_band_list
from mediagoblin.tools.text import tag_length_validator
from mediagoblin.tools.licenses import licenses_as_choices
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from mediagoblin.tools.translate import fake_ugettext_passthrough as _
from cgi import escape
from datetime import date

#
#  fonctions de confort pour allèger le code
#
def DogmaUtilMKBOOK() :
    return _("""You can use
                      <a href="http://daringfireball.net/projects/markdown/basics" target="_blank">
                      Markdown</a> for formatting.""")

# --------

#Custom multiple file input field made by pythonsnake
class LocationInput(object):
    def __call__(self, field, **kwargs):
        if field.flags.required:
            kwargs['required'] = 'required'
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
            #This counter is needed when there's multiple field on the same page so JS can now where it is
            kwargs['data-counter'] = '_0'
        html = [u'<div class="location" id="location_0">\
                <input %s />' % html_params(type="text", name=field.name, class_="city_search city_search_0",  **kwargs)]
        if field.quick_location:
            html.append(u'<button class="button_action copy_band_location" type="button">%s</button>' % field.quick_location)
        html.append(u'<div id="SuggestBoxElement_0"></div>\
                      </div>')
        return HTMLString(u''.join(html))

class LocationField(wtforms.FileField):
    widget = LocationInput()

    def __init__(self,label=None, validators=None,quick_location=None, **kwargs):
        super(LocationField, self).__init__(label, validators, **kwargs)
        self.quick_location = quick_location


class DatePickerInput(object):
    def __call__(self, field, **kwargs):
        if field.flags.required:
            kwargs['required'] = 'required'
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        if field.pattern :
           kwargs['pattern'] = field.pattern

        html = [u'<div class="datePicker  '+field.custom_class+'" data-millis="'+field.millis+'" ></div>\
                <input %s />' % html_params(type="text", name=field.name, class_="date_picker_input",  **kwargs)]
        if field.quick_date:
            html.append(u'<button class="button_action copy_band_date" type="button">%s</button>' % field.quick_date)
        return HTMLString(u''.join(html))

class DatePickerField(wtforms.FileField):
    widget = DatePickerInput()

    def __init__(self,label=None, validators=None,quick_date=None, millis=u'', custom_class=u'', pattern=None, **kwargs):
        super(DatePickerField, self).__init__(label, validators, **kwargs)
        self.quick_date = quick_date
        self.millis = millis
        self.pattern = pattern
        self.custom_class = custom_class



class MultipleFileInput(object):
    def __call__(self, field, **kwargs):
        value = field._value()
        if field.flags.required:
            kwargs['required'] = 'required'
        html = [u'<input %s>' % html_params(name='file[]', id='multi_file_input', type='file', 
                                                  multiple=True, **kwargs)]
        if value:
            kwargs.setdefault('value', value)
        return HTMLString(u''.join(html))

class MultipleFileField(wtforms.FileField):
    widget = MultipleFileInput()


class DateForm(wtforms.Form):
    day =  TextField(_("Day"),
            [wtforms.validators.Required()],
            pattern = "(0[1-9]|[1-9]|[12][0-9]|3[01])"
            )
    """
    month = TextField(_("Month"),
            [wtforms.validators.Required()],
            pattern = "([1-9]|[1-9]|1[012])"
            )
    year =  TextField(_("Year"),
            [wtforms.validators.Required()],
            description = _("year format YYYY"),
            pattern = "(19|20)\d\d",
            )
    """
class LocationForm(wtforms.Form):
    place_0 = LocationField(
            _('City :'),
            [wtforms.validators.Optional()],
            description=_("Type the name of the city and select one in the list (you must select a country first)"),
            quick_location = _("Same location as the band"),
                )
    latitude_0 = wtforms.HiddenField(_('Latitude'),
                  )
    longitude_0 = wtforms.HiddenField(
                  _('Longitude'),
                  )

class DogmaTracks(wtforms.Form):
    title_0 = TextField(
        _('Title'),
        [wtforms.validators.Length(min=0, max=500)],
        description=_(
          "Leave blank if the title is the name of the file."))
    license_0 = wtforms.SelectField(
        _('License'),
        [wtforms.validators.NoneOf('_None', _("you must choose a license"))],
        choices=licenses_as_choices())
    composers_0 = TextField(
        _('Composer(s)'),
        [tag_length_validator],
        description=_(
          "Separate names by commas."))
    authors_0 = TextField(
        _('Author(s)'),
        [tag_length_validator],
        description=_(
          "Separate names by commas."))
    performerNo0_0 = TextField(
        _('Extra Performer'))
    performer_rolesNo0_0 = TextField(
        _('plays'))
    tags_0 = TextField(
        _('Tags for this tracks'),
        [tag_length_validator],
        description=_(
          "Separate tags by commas. (they will be added to the global tags)"))
    description_0 = TextAreaField(
        _('Description of this work'),
        description=DogmaUtilMKBOOK(),
        id="wmd-input_0"
        )

class DogmaTracksGlobal(wtforms.Form):
    composers = TextField(
        _('Composer(s) for ALL tracks'),
        [tag_length_validator],
        description=_(
          "Separate names by commas."))
    authors = TextField(
        _('Author(s) for ALL tracks'),
        [tag_length_validator],
        description=_(
          "Separate names by commas."))
    tags = TextField(
        _('Tags for ALL tracks'),
        [tag_length_validator],
        description=_(
          "Separate tags by commas. Songs' tags will be added to global tags."))
    license = wtforms.SelectField(
        _('License for ALL tracks'),
        [wtforms.validators.Optional()],
        choices=licenses_as_choices())
    tracks = MultipleFileField(_('Tracks'),
            [wtforms.validators.Required()],
            description= _("Use CTRL and/or SHIFT to select multiple items"),
            id="wmd-input")


class BandForm(wtforms.Form):
    country_0 = wtforms.SelectField(
        _('Country'),
        [wtforms.validators.Optional()],
        choices=countries_list())
    internationnal_0 = wtforms.BooleanField(label=_('Long distance collaboration'),
                                            description=_("Members come from multiple countries"))
    Location = wtforms.FormField(LocationForm)
    band_name = TextField(
        _('Name *'),
        [wtforms.validators.Required()]
        )
    band_picture = wtforms.FileField(
                     _('Band picture'),
                     description=_("You can use format *.jpeg or *.jpg filetypes")
                   )
    band_description = TextAreaField(
        _('Description of the band'),
        [wtforms.validators.Required()],
        description=DogmaUtilMKBOOK(),
        id="wmd-input_0"
        )
    band_since = DateField(_('This band started the :'), validators=[DateRange(date(1900,1,1), date.today())])
    
   
class BandSelectForm(wtforms.Form):
    band_select = QuerySelectField(
        _('Bands'),
        allow_blank=True, blank_text=_('-- Select --'), get_label='name')


class MemberForm(wtforms.Form):
    member_username_0 = TextField(
        _('User name *'),
        [wtforms.validators.Required()]
        )
    member_real_name_0 =  TextField(
        _('Real name')
        )
    
    country_0 = wtforms.SelectField(
        _('Country'),
        [wtforms.validators.Optional()],
        choices=countries_list())
    
    Location = wtforms.FormField(LocationForm)

    member_picture_0 = wtforms.FileField(_('Picture'))
    member_description_0 =  wtforms.TextAreaField(
        _('Bio'),
        description=DogmaUtilMKBOOK(),
        id="wmd-input_0"
        )
    
    member_main = wtforms.BooleanField(_('Permanent member'),
            description=_("If the box is checked: the member is listed as band member,\
                          otherwise it is considered as a casual member"),
            default = True)
    member_since_0 = DateField(_('This member joined the band the :'), validators=[DateRange(date(1900,1,1), date.today())])
    '''
    member_since_0 = DatePickerField(_('Member Since'),
            [wtforms.validators.Required()],
            description = _("date format YYYY-MM-DD"),
            quick_date = _("Member since the begining of the band"),
            pattern = "(19|20)\d\d-(0[1-9]|[1-9]|1[012])-(0[1-9]|[1-9]|[12][0-9]|3[01])"
            )
            '''
    member_former_0 = wtforms.BooleanField(_('Former member'),
            description=_("Former members are always listed as band members"),
            default = False)
    member_until_0 = DatePickerField(_('Member until'),
            description = _("date format YYYY-MM-DD"),
            pattern = "(19|20)\d\d-(0[1-9]|[1-9]|1[012])-(0[1-9]|[1-9]|[12][0-9]|3[01])"
            )
        
        
class AlbumForm(wtforms.Form):
    release_date = DateField(_('Album released the :'), validators=[DateRange(date(1900,1,1), date.today())])
    '''
    release_date = DatePickerField(_('Release date of this album *'),
            [wtforms.validators.Required()],
            custom_class=_("album_release")
            )
            '''
    collection_title = TextField(
        _('Album Title'),
        [wtforms.validators.Required(),
        wtforms.validators.Length(min=0, max=500)])
    album_picture = wtforms.FileField(
                    _('Album cover'),
                    description = _("You can only upload *.jpg. An album cover must be a square")
                    )
    collection_description = wtforms.TextAreaField(
        _('Description of this Album'),
        description=DogmaUtilMKBOOK(),
        id="wmd-input_0"
                     )


class MemberRolesInput(object):
    def __call__(self, field, **kwargs):
        if field.millis_until:
            until = 'data-until="'+str(field.millis_until)+'"'
        else:
            until = u''

        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        id_field_name = 'member_'+str(field.count)
        html = [u'<div class="album_member" data-since="'+str(field.millis_since)+'"'+str(until)+'>\
             <input %s />' % html_params(name=field.name, type="text", **kwargs)\
            +'<input %s />' % html_params( name=id_field_name, value=field.member_id, type="hidden")+ '</div>']
        return HTMLString(u''.join(html))

class MemberRolesField(wtforms.FileField):
    widget = MemberRolesInput()

    def __init__(self,label=None, validators=None, count=None,iterable_value = u'', millis_since=u'',\
            millis_until=u'', member_id=u'',  **kwargs):
        super(MemberRolesField, self).__init__(label, validators, **kwargs)
        self.millis_until = millis_until
        self.millis_since = millis_since
        self.member_id = member_id
        self.count= count
        self.iterable_value = iterable_value

class AlbumMembersforms(wtforms.Form):
    roles = MemberRolesField(_('Instrument played * by '),
            [wtforms.validators.Required()],
            count = 0,
            description=_(
              "Separate roles by commas.")
            )


