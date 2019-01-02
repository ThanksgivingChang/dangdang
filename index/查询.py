from index.models import Product

def dangdang1():
    product=Product.objects.filter(pk=10)
    print(product)

if __name__ == '__main__':
    dangdang1()