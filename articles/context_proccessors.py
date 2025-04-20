from .models import Category

def navbar_context(request):
    
    return{
        "menu": Category.objects.filter(parent=None),
    }