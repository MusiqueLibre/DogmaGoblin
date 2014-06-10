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

import  urllib

def cookie_check(request):
    print "bouh"
    if 'sso_authent_coomute[id]' in request.cookies:
        print "bouh"
        user_id = request.cookies['sso_authent_coomute[id]']
        user_token = request.cookies['sso_authent_coomute[token]']

        engine = sqlalchemy.create_engine('mysql://yii_user:yii_user@localhost/yii_user')
        connection = engine.connect()
        result = connection.execute("select session from users where id = "+unicode(user_id)).first()[0]
        print urllib.unquote(user_token) + result
        if urllib.unquote(user_token) == result:
            print 'yeah'
            request.session['user_id'] = unicode(user_id)
            request.session.save()
