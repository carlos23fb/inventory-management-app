from .models import ItemQuantity
import pandas as pd

data = ItemQuantity.objects.all().va
df = pd.DataFrame(data)
