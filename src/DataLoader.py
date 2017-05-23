import numpy as np
import pandas as pd

class Dataset(object):

    def __init__(self, dataRoot):
	self.dataRoot = dataRoot
        self.goods = None
   	self.orders = None
	self.orderedProductsTrain = None
	self.orderedProductsPrior = None

    ######## GET METHODS #########
    def GetMergedProductTable(self):
        return self.goods

    def GetOrders(self):
        return self.orders

    def GetOrderedProducts_Train(self):
	return self.orderedProductsTrain

    def GetOrderedProducts_Prior(self):
	return self.orderedProductsPrior

    ######## LOAD METHODS ########
    def LoadAll(self):
	return self.LoadMergedProductTable().LoadOrders().LoadOrderedProducts_Train().LoadOrderedProducts_Prior()

    # Load a product table joined with the department and the aisle
    def LoadMergedProductTable(self):
	print "Loading Merged Product Table"    	

	aisles = pd.read_csv(self.dataRoot + 'aisles.csv', engine='c')
	print('Total aisles: {}'.format(aisles.shape[0]))
	aisles.head()

	departments = pd.read_csv(self.dataRoot + 'departments.csv', engine='c')
	print('Total departments: {}'.format(departments.shape[0]))
	departments.head()

	products = pd.read_csv(self.dataRoot + 'products.csv', engine='c')
	print('Total products: {}'.format(products.shape[0]))
	products.head(5)

	# combine aisles, departments and products (left joined to products)
	goods = pd.merge(left=pd.merge(left=products, right=departments, how='left'), right=aisles, how='left')
	# to retain '-' and make product names more "standard"
	goods.product_name = goods.product_name.str.replace(' ', '_').str.lower() 

	goods.head()
        self.goods = goods

  	print "Finished Loading Merged Product Table"
	return self

    
    def LoadOrders(self):
	print "Loading Orders"
  	
	orders = pd.read_csv(self.dataRoot + 'orders.csv', engine='c', dtype={'order_id' : np.int32,
									      'user_id' : np.int32,
 									      'order_number' : np.int32,
									      'order_dow' : np.int8,
									      'order_hour_of_day': np.int8,
									      'days_since_prior_order' : np.float16})

	print ('Total orders: {}'.format(orders.shape[0]))
	orders.head()

	self.orders = orders

	print "Finished Loading Orders"
	return self


    def LoadOrderedProducts_Train(self):
	print "Loading Ordered Products Train Set"
  	
	ordersTrain = pd.read_csv(self.dataRoot + 'order_products__train.csv', engine='c', dtype={'order_id' : np.int32,
												  'product_id' : np.int32,
												  'order_number' : np.int32,
												  'add_to_cart_order' : np.int16,
												  'reordered': np.int8})

	print ('Total ordered products in train set: {}'.format(ordersTrain.shape[0]))
	ordersTrain.head()
	self.orderedProductsTrain = ordersTrain

	print "Finished Loading Training Set"
	return self


    def LoadOrderedProducts_Prior(self):
	print "Loading Ordered Products Prior set"
  	
	ordersPrior = pd.read_csv(self.dataRoot + 'order_products__prior.csv', engine='c', dtype={'order_id' : np.int32,
												  'product_id' : np.int32,
												  'order_number' : np.int32,
												  'add_to_cart_order' : np.int16,
												  'reordered': np.int8})

	print ('Total ordered products in prior set: {}'.format(ordersPrior.shape[0]))
	ordersPrior.head()
	self.orderedProductsTrain = ordersPrior

	print "Finished Loading Prior Set"
	return self
