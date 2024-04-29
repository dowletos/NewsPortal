from django_filters import FilterSet,ModelMultipleChoiceFilter
from .models import  *



class ProductFilter(FilterSet):

    material=ModelMultipleChoiceFilter(field_name='productmaterial__material',
    queryset=Material.objects.all(),
    label='Material')



    class Meta:
        model=Product
        fields={

            'name':['icontains'],
            'quantity':['gt'],
            'price':[
                'lt',
                'gt'
                ],
        }
