import logging
_log = logging.getLogger(__name__)
from mediagoblin.tools.response import render_to_response, render_404, redirect

def get_genres():
  _log.debug( 'yes ?')
  return render_to_response(
              request,
              'dogma_genres/submit_add_genre.html',
              {'example' : example,
              })

