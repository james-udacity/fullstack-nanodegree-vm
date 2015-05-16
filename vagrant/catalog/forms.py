from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, SelectField, \
    HiddenField


class CreateItemForm(Form):
    """Model for a create and edit item form"""

    _objectId = HiddenField("_id")
    title = TextField("Title")
    description = TextAreaField("Description")
    category = SelectField(u'Category', choices=[])
    submit = SubmitField("Send")


class DeleteForm(Form):
    """Model for a delete item form"""

    btnYes = SubmitField("Confirm")
    btnCancel = SubmitField("Cancel")
