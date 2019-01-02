from index.models import Product,AddProduct

class CartItem():
    '''描述一个购物车的订单项'''
    def __init__(self, product, amount):
        self.product = product
        self.amount = amount
    def getSubTotal(self):
        return self.product.addproduct.dangdang_price*self.amount
    # def setAmount(self,value):
    #     self.amount = value


class Cart():
    '''描述一个购物车：
    属性：
        购物车应该有一个列表存储订单项
        购物车应该提供一个列表存储删除的订单项
        购物车能够返回所有订单项金额的总计
        购物车能够返回所有订单项的优惠总计
    方法：
        购物车应提供一个方法添加订单项
        购物车应该提供一个方法删除订单项，并存储删除的订单项
        购物车应该提供一个方法恢复删除的订单项
        购物车应该提供一个方法计算所有订单项金额的总计
        购物车应该提供一个方法计算所有订单项的优惠总计
        购物车应该提供一个方法彻底删除订单项
    '''
    def __init__(self):
        '''初始化购物车'''
        self.cartItems = []
        self.uncartItems = []
        self.totalMoney = 0
        self.saveMoney = 0

    def addCartItem(self,product,amount):
        '''添加订单项'''
        self.cartItem=CartItem(product=product,amount=amount)
        if self.cartItems:
            for one in self.cartItems:
                if one.product.id == self.cartItem.product.id:
                    one.amount += amount
                    return
            else:
                self.cartItems.append(self.cartItem)
        else:
            self.cartItems.append(self.cartItem)

    def subCartItem(self,product):
        '''删除订单项'''
        self.delitem=0
        self.n = 0
        for one in self.cartItems:
            if one.product.id == product.id:
                self.delitem=self.cartItems.pop(self.n)
            self.n += 1
        else:
            if self.delitem:
                if self.uncartItems:
                    for sec in self.uncartItems:
                        if sec.product.id == product.id:
                            sec.amount += self.delitem.amount
                            return
                    else:
                        self.uncartItems.append(self.delitem)
                else:
                    self.uncartItems.append(self.delitem)

    def delCartItem(self, product):
        '''彻底删除订单项'''
        for one in self.uncartItems:
            if one.product.id == product.id:
                self.uncartItems.remove(one)

    def reCartItem(self,product):
        '''恢复订单项'''
        self.reitem=0
        self.n=0
        for one in self.uncartItems:
            if one.product.id == product.id:
                self.reitem=self.uncartItems.pop(self.n)
            self.n += 1
        else:
            if self.reitem:
                if self.cartItems:
                    for sec in self.cartItems:
                        if sec.product.id == product.id:
                            sec.amount += self.reitem.amount
                            return
                    else:
                        self.cartItems.append(self.reitem)
                else:
                    self.cartItems.append(self.reitem)

    def setCartItem(self,cartItem,amount):
        '''修改订单项'''
        for one in self.cartItems:
            if one.product.id == cartItem.product.id:
                one.amount = amount
                # print(one.amount)

    def getTotalMoney(self):
        '''获取订单总额'''
        self.totalMoney = 0
        if self.cartItems:
            for one in self.cartItems:
                self.totalMoney += one.product.addproduct.dangdang_price*one.amount
            return self.totalMoney

    def getSaveMoney(self):
        '''获取订单节省金额'''
        self.totalMoney = 0
        self.saveMoney = 0
        self.middleware=0
        if self.cartItems:
            for one in self.cartItems:
                # print(one.product.addproduct.dangdang_price,type(one.product.addproduct.dangdang_price))
                # print(one.amount,type(one.amount))
                self.totalMoney += one.product.addproduct.dangdang_price*one.amount
                self.middleware += one.product.addproduct.price*one.amount
            self.saveMoney = self.middleware - self.totalMoney
            return self.saveMoney











