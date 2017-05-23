from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import json

# Create your models here.
'''
Table 'Cars'
(* Primary Keys)

make (char) | model (char) | year (int) | vehicle_id (int) | style_name (char) | style_spec (char)            | price (int)
            |              |            |          *       |                   |                              |
--------------------------------------------------------------------------------------------------------------------------
 "Jeep"     |   "Patriot"  |  2017      |       430823     |  "Sport Utility"  | "{"Engine(s)": "2.7 Liter"}" |    18000

'''
@python_2_unicode_compatible  # only if you need to support Python 2
class Cars(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=200)
    year = models.IntegerField(default=2017)
    vehicle_id = models.IntegerField(primary_key=True)
    style_name = models.CharField(max_length=200, default="DEFAULT")
    style_spec = models.CharField(max_length=500, default="N/A")
    price = models.IntegerField(default=0)

    def __str__(self):
        try:
            specs = json.loads(str(self.style_spec))
            spec_str = ""
            for spec in specs:
                spec_str += " [ {} : {} ] ".format(spec, specs[spec])
        except:
            spec_str = "[ {} ]".format(self.style_spec)
        s = "{} {} {} {} ({}) price: ${} spec: {}".format(self.year, self.make, self.model, self.style_name, self.vehicle_id, self.price, spec_str)
        return s

