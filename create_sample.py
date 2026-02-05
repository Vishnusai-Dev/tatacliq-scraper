import pandas as pd
import openpyxl

# Create sample data
sample_data = {
    's.no': [1, 2, 3],
    'url': [
        'https://www.tatacliq.com/woodland-green-beige-cotton-regular-fit-checks-shirt/p-mp000000026178350',
        'https://www.tatacliq.com/adidas-white-w-fi-3s-qz-hoodie/p-mp000000023456789',
        'https://www.tatacliq.com/sample-product/p-mp000000011111111'
    ]
}

df = pd.DataFrame(sample_data)
df.to_excel('sample_input.xlsx', index=False, sheet_name='Products')
print("Sample input file created: sample_input.xlsx")
