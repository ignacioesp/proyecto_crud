from django import forms

from .models import Producto

INPUT_CLASSES = (
    "w-full rounded-lg border border-gray-300 px-4 py-3 "
    "focus:outline-none focus:ring-2 focus:ring-blue-500"
)

# Reglas de negocio acordadas para la validación en el servidor
NOMBRE_MIN = 3
STOCK_MAX = 100_000


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nombre", "descripcion", "precio", "stock", "skills"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": INPUT_CLASSES}),
            "descripcion": forms.Textarea(attrs={"class": INPUT_CLASSES, "rows": 4}),
            "precio": forms.NumberInput(attrs={"class": INPUT_CLASSES, "step": "0.01", "min": "0"}),
            "stock": forms.NumberInput(attrs={"class": INPUT_CLASSES, "min": "0"}),
            "skills": forms.CheckboxSelectMultiple(attrs={"class": "space-y-2"}),
        }

    def clean_nombre(self):
        # CharField ya aplica strip(), así que "   " llega vacío y se rechaza como obligatorio.
        nombre = self.cleaned_data["nombre"]
        if len(nombre) < NOMBRE_MIN:
            raise forms.ValidationError(
                f"El nombre debe tener al menos {NOMBRE_MIN} caracteres."
            )
        return nombre

    def clean_precio(self):
        precio = self.cleaned_data["precio"]
        if precio < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return precio

    def clean_stock(self):
        stock = self.cleaned_data["stock"]
        if stock < 0:
            raise forms.ValidationError("El stock no puede ser negativo.")
        if stock > STOCK_MAX:
            raise forms.ValidationError(
                f"El stock no puede superar {STOCK_MAX} unidades."
            )
        return stock