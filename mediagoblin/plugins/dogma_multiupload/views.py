import logging
_log = logging.getLogger(__name__)
from mediagoblin.tools.response import render_to_response, render_404, redirect
from mediagoblin.plugins.dogma_multiupload.forms import DogmaMultiuploadForm

def multi_upload_form(request):
  _log.debug( 'yes ?')
  form = DogmaMultiuploadForm(request.form)
  example = 'youpi'
  return render_to_response(
              request,
              'dogma_multiupload/submit.html',
              {'example' : example,
               'form' : form,
              })

def submit(request):
  return
