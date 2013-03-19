import wtforms

from mediagoblin.tools.text import tag_length_validator
from mediagoblin.tools.translate import fake_ugettext_passthrough as _
from mediagoblin.tools.licenses import licenses_as_choices


class DogmaMultiuploadForm(wtforms.Form):
    file = wtforms.FileField(_('File'))
    title = wtforms.TextField(
        _('Title'),
        [wtforms.validators.Length(min=0, max=500)])
    description = wtforms.TextAreaField(
        _('Description of this work'),
        description=_("""You can use
                      <a href="http://daringfireball.net/projects/markdown/basics">
                      Markdown</a> for formatting."""))
    tags = wtforms.TextField(
        _('Tags'),
        [tag_length_validator],
        description=_(
          "Separate tags by commas."))
    license = wtforms.SelectField(
        _('License'),
        [wtforms.validators.Optional(),],
        choices=licenses_as_choices())

class AddCollectionForm(wtforms.Form):
    title = wtforms.TextField(
        _('Title'),
        [wtforms.validators.Length(min=0, max=500), wtforms.validators.Required()])
    description = wtforms.TextAreaField(
        _('Description of this collection'),
        description=_("""You can use
                      <a href="http://daringfireball.net/projects/markdown/basics">
                      Markdown</a> for formatting."""))
