from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_tailwind.layout import Field


from .models import Producto


class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto

        fields = [
            'nombre',
            'descripcion',
            'precio',
            'stock'
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.form_method = 'post'

        self.helper.add_input(
            Submit(
                'submit',
                'Guardar producto',
                css_class='bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-5 rounded-lg'
            )
        )