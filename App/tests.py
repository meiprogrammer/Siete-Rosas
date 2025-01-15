from django.test import TestCase
import unittest
from .views import orderVerify, get_merchant_order
from .models import Pay

# Create your tests here.
## class tests(unittest.TestCase):
    ##def test1(self, request):
        ##""""Verificando a view orderVerify retorna que o merchant_order_id tem o status esperado."""

        ##def orderVerifyTest(request, expected):
        ##    orderVerify(request, "2145127630-5723a164-4e32-4d3e-8e91-100e847a31a3")
            
        ##    if request.get("result") != expected:
        ##        return False
        ##    return True

        ##self.assertTrue(orderVerifyTest(request, "pending"))

   ## def test2(self, request):
    ##    """"Verificando se a views get_merchant_order retornará o merchant_order_id; também verificando se ele existe."""
    ##    get_merchant_order("98476023790")
    ##    if request.get("merchant_order_id"):
    ##        if not Pay.objects.get(get_merchant_order=request.get("merchant_order_id")):
    ##            return False
    ##        return True

   ## if __name__ == "__main__":
    ##    unittest.main()