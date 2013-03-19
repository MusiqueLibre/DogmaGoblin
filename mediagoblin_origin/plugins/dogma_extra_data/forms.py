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
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from mediagoblin.tools.translate import fake_ugettext_passthrough as _

class BandForm(wtforms.Form):
    band_name = wtforms.TextField(
        _('Name'),
        )
    band_picture = wtforms.FileField(_('Band picture'))
    band_description = wtforms.TextAreaField(
        _('Description of the band'),
        [wtforms.validators.Required()],
        description=_("""You can use
                      <a href="http://daringfireball.net/projects/markdown/basics">
                      Markdown</a> for formatting."""),
        )

class MemberForm(wtforms.Form):
    member_first_name_0 = wtforms.TextField(
        _('First name'),
        [wtforms.validators.Required()],
        )
    member_last_name_0 =  wtforms.TextField(
        _('Last name'),
        [wtforms.validators.Required()],
        )
    member_nickname_0 =  wtforms.TextField(
        _('Nickname'),
        [wtforms.validators.Required()],
        )
    member_roles_0 =  wtforms.TextField(
        _('Role in the band'),
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
    title = wtforms.TextField(
        [wtforms.validators.Required()],
        _('Album Title'),
        )
