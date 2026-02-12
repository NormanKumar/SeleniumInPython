import numpy as np
import pandas as pd

arr = np.array([10,20,5,6,200])

print("Array:",arr)
print("Sum",np.sum(arr))
print("Mean",np.mean(arr))
print("Multiply with 2",arr*2)

data={
    "Name":["Kiran","Anita","Ravi"],
    "Age":[25,27,26],
    "City":["Bangalore","Chennai","Hyderabad"]
}
df = pd.DataFrame(data)
print(df)