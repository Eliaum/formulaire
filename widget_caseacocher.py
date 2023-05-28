from django import forms

class CustomCheckbox(forms.CheckboxInput):
    def __init__(self, hidden_fields_mapping, *args, **kwargs):
        self.hidden_fields_mapping = hidden_fields_mapping
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        attrs['data-group'] = name  # Ajout de l'attribut data-group
        html = super().render(name, value, attrs, renderer)
        html += f"<script>initCustomCheckbox('{attrs['id']}', {self.hidden_fields_mapping})</script>"
        return html

