from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# 上传的结算数据
class Txt_Data(models.Model):
	account = models.CharField(max_length=255, blank=True)
	file_date = models.DateField()
	file = models.FileField(upload_to='DAS/txt/')
	uploaded_date = models.DateTimeField(auto_now_add=True)


#结算单
class Statement(models.Model):
	#账户
	account = models.CharField(max_length=100)
	#日期
	sta_datetime = models.DateField()
	#上次结算资金
	last_statement_fund = models.DecimalField(max_digits=12,decimal_places=2)
	#交割手续费
	delivery_charge = models.DecimalField(max_digits=12,decimal_places=2)
	#出入金
	in_or_out = models.DecimalField(max_digits=12,decimal_places=2)
	#期末结存
	final_balance = models.DecimalField(max_digits=12,decimal_places=2)
	#平仓盈亏
	close_break = models.DecimalField(max_digits=12,decimal_places=2)
	#保证金占用
	deposit = models.DecimalField(max_digits=12,decimal_places=2)
	#持仓盈亏
	position_break = models.DecimalField(max_digits=12,decimal_places=2)
	#可用资金
	usable_fund = models.DecimalField(max_digits=12,decimal_places=2)
	#手续费
	service_charge = models.DecimalField(max_digits=12,decimal_places=2)
	#风险度
	risk_degree = models.DecimalField(max_digits=12,decimal_places=2)
	#作者
	# author = models.ForeignKey(User, on_delete=models.CASCADE)
	#更新日期
	date_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.account

#持仓明细
class Position_Detail(models.Model):
	#合约代码
	code = models.CharField(max_length=100)
	#交易所
	exchange = models.CharField(max_length=100,blank=True)
	#开仓日期
	open_date = models.DateField()
	#投/保
	investment_type = models.CharField(max_length=100,blank=True)
	#买/卖
	buy_or_sell = models.CharField(max_length=100,blank=True)
	#手数
	number = models.IntegerField()
	#开仓价
	open_price = models.DecimalField(max_digits=12,decimal_places=3)
	#结算价
	close_price = models.DecimalField(max_digits=12,decimal_places=3)
	#持仓盈亏
	position_break = models.DecimalField(max_digits=12,decimal_places=2)
	#保证金
	deposit = models.DecimalField(max_digits=12, decimal_places=2)
	#结算单外键
	statement= models.ForeignKey(Statement, on_delete=models.CASCADE)

	def __str__(self):
		return self.statement.account

#持仓汇总
class Position_Summary(models.Model):
	# 合约代码
	code = models.CharField(max_length=100)
	# 买/卖
	buy_or_sell = models.CharField(max_length=100)
	# 手数
	number = models.IntegerField()
	# 开仓均价
	open_avg_price = models.DecimalField(max_digits=12, decimal_places=3)
	# 结算价
	close_price = models.DecimalField(max_digits=12, decimal_places=3)
	# 持仓盯市盈亏
	position_break = models.DecimalField(max_digits=12, decimal_places=2)
	# 保证金
	deposit = models.DecimalField(max_digits=12, decimal_places=2)
	# 投/保
	investment_type = models.CharField(max_length=100)
	# 结算单外键
	statement = models.ForeignKey(Statement, on_delete=models.CASCADE)

	def __str__(self):
		return self.statement.account

#成交明细
class Trading_Detail(models.Model):
	# 合约代码
	code = models.CharField(max_length=100)
	# 交易所
	exchange = models.CharField(max_length=100)
	# 成交日期
	trading_date = models.DateField()
	# 买/卖
	buy_or_sell = models.CharField(max_length=100)
	# 投/保
	investment_type = models.CharField(max_length=100)
	# 成交价
	trading_price = models.DecimalField(max_digits=12, decimal_places=3)
	# 手数
	number = models.IntegerField()
	# 开平方向
	open_close = models.CharField(max_length=100)
	# 手续费
	service_charge = models.DecimalField(max_digits=10, decimal_places=2)
	# 成交编号
	trading_id = models.CharField(max_length=100)
	# 结算单外键
	statement = models.ForeignKey(Statement, on_delete=models.CASCADE)

	def __str__(self):
		return self.statement.account

# 平仓明细
class Close_Detail(models.Model):
	# 合约代码
	code = models.CharField(max_length=100)
	# 成交日期
	trading_date = models.DateField()
	# 买/卖
	buy_or_sell = models.CharField(max_length=100)
	# 开仓价
	open_price = models.DecimalField(max_digits=12, decimal_places=3)
	# 平仓价
	close_price = models.DecimalField(max_digits=12, decimal_places=3)
	# 手数
	number = models.IntegerField()
	# 开平方向
	open_close = models.CharField(max_length=100)
	# 平仓盈亏
	close_amount = models.DecimalField(max_digits=12, decimal_places=2)
	# 投/保
	investment_type = models.CharField(max_length=100)
	# 成交编号
	trading_id = models.CharField(max_length=100)
	# 结算单外键
	statement = models.ForeignKey(Statement, on_delete=models.CASCADE)

	def __str__(self):
		return self.statement.account