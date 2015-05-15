from flask_wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, SelectField, \
    HiddenField

class CreateItemForm(Form):
    _objectId = HiddenField("_id")
    title = TextField("Title")
    description = TextAreaField("Description")
    category = SelectField(u'Category', choices=[])
    submit = SubmitField("Send")

class DeleteForm(Form):
    btnYes = SubmitField("Confirm")
    btnCancel = SubmitField("Cancel")
