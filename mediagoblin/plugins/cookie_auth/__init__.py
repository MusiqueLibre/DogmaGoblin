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

import sqlalchemy
from mediagoblin.tools import pluginapi

import  urllib


#connect to the user DB to compare cookies token with user's token
def cookie_check(request):
    if 'sso_authent_coomute[id]' in request.cookies and not 'user_id' in request.session:
        config = pluginapi.get_config('mediagoblin.plugins.cookie_auth')
        user_id = request.cookies['sso_authent_coomute[id]']
        user_token = request.cookies['sso_authent_coomute[token]']

        connection_string = "mysql://"+config['db_user']+":"+urllib.quote_plus(config['db_pass'])+"@localhost/"+config['db']
        engine = sqlalchemy.create_engine(connection_string)
        connection = engine.connect()
        result = connection.execute("select session from users where id = "+unicode(user_id)).first()[0]
        if urllib.unquote(user_token) == result:
            request.session['user_id'] = unicode(user_id)
            request.session.save()
    # delete session if there's one but no cookie
    elif 'user_id' in request.session:
        request.session.delete()
    return request

def auth():
    return True

hooks = {
    'authentication': auth,
    'modify_request': cookie_check,
}
