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
from __future__ import unicode_literals
import logging
import os.path

from sqlalchemy import func
#TODO: We should be able to import this via 'mediagoblin.db'
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import cast, desc
from sqlalchemy.types import Float

from mediagoblin.decorators import active_user_from_url
from mediagoblin.db.base import Session
from mediagoblin.db.models import User, MediaTag, MediaEntry, Tag
from mediagoblin.tools import pluginapi
from mediagoblin.tools.response import render_to_response, render_404
from mediagoblin.tools.template import render_template

_log = logging.getLogger(__name__)

class TagCloud(object):
    _setup_plugin_called = 0

    @classmethod
    def setup_plugin(cls):
        """Set up this plugin during 'setup' hook"""
        global _log
        classpath = '{0}:{1}'.format(cls.__module__, cls.__name__)
        if cls._setup_plugin_called:
            _log.info("'{0}' plugin was already set up.".format(classpath))
            return

        _log.debug("'{0}' plugin set up.".format(classpath))
        cls._setup_plugin_called += 1

        routes = [
            # endpoint in the form of e.g.
            # 'mediagoblin.plugins.tagcloud:render_tag_cloud
            ('mediagoblin.plugins.tag_cloud',
             '/u/<string:user>/tags/',
             '{0}:render_tag_cloud'.format(cls.__module__)),
            ]
        pluginapi.register_routes(routes)

        templatedir = os.path.dirname(__file__)
        templatedir = os.path.join(templatedir, 'templates')
        pluginapi.register_template_path(templatedir)

def get_tagcloud_databak(user, limit=None):
    """Return the number of tags, as well as [(freq,value),...] tuples

    :param limit: If set, limit returned values to <n> entries"""
    # Get number of Tags from a given user
    if user:
        num_tags = Session.query(func.count(MediaTag.id)).join(MediaEntry).\
            filter(MediaEntry.uploader==user.id)
    else:
        num_tags = Session.query(func.count(MediaTag.id)).join(MediaEntry)
        
    if limit:
        num_tags = num_tags.order_by(desc('count_1')).limit(limit)
    num_tags = num_tags.scalar()

    # Get tuples of (tag, frequency) where frequency is the share of this tag
    # among users tags as integer. Sorted in decreasing frequency

    if user:
        tags = Session.query(MediaTag.name, 100*func.count()/num_tags).join(Tag).\
            join(MediaEntry).filter(MediaEntry.uploader==user.id).\
            group_by(Tag.id, MediaTag.name).order_by(func.count().desc())
    else:
        tags = Session.query(MediaTag.name, 100*func.count()/num_tags).join(Tag).\
            join(MediaEntry).group_by(Tag.id, MediaTag.name).order_by(func.count().desc())

    if limit:
        tags = tags.limit(limit)

    final_tags_count = tags.count()
    return final_tags_count, tags


@active_user_from_url
def render_tag_cloud(request, url_user=None, limit=None):
    """Render a users tag cloud on a separate page"""
    num_tags, tags = get_tagcloud_data(url_user, limit)
    return render_to_response(request,
                              'tagcloud/user_tag_cloud.html',
                              {'user': url_user, 'tags': tags, 'num_tags': tags.count()})

def tag_cloud_html(request, url_user=None, limit=5):
    """Return the HTML of the tagcloud body

    This is appropriate output for plugins to use, directly inserting html.
    :param limit: If set, limit returned values to <n> entries"""
    num_tags, tags = get_tagcloud_data(url_user, limit)
    return render_template(request, 'tagcloud/tag_cloud_include.html',
                          {'user': url_user, 'tags': tags, 'num_tags': tags.count()})

def tag_cloud_context(context, user=None, limit=None):
    context['final_tags_count'], context['tags'] = get_tagcloud_data(user, limit)
    return context


hooks = {
    'setup': TagCloud.setup_plugin,
    'profile_html': tag_cloud_html,
    }
