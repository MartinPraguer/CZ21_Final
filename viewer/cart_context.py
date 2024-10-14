
from viewer.models import Cart
def cart_count(request):
    if request.user.is_authenticated:
        return {"cart_count": Cart.objects.filter(user=request.user).count() }
    else:
        return {}
