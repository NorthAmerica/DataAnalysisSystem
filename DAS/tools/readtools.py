import os
from django.db import transaction
from .strhelper import GetMiddleStr,GetSqlDateStr
from ..models import Statement,Position_Detail,Position_Summary,Trading_Detail,Close_Detail

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class ReadTxt:

	def reader(self,txtpath):
		'''
		读取TXT的全部内容
		:param txtpath:txt的路径
		:return:队列
		'''
		txt = open(os.path.join(BASE_DIR, '../' + txtpath), 'r', encoding='UTF-8')
		result = []
		for linea in txt.readlines():
			# linea = linea.split(" ")[:-1]
			result.append(linea)
		txt.close()
		return result

	def analyzer(self,results):
		'''
		分行分析TXT的内容
		:param results:队列
		:return:
		'''
		with transaction.atomic():
			sta = Statement()
			for index,line in enumerate(results):
				if index < 2:
					continue
				if index==2:
					sta.account = GetMiddleStr(line,'账户：','\n')
					continue
				if index==3:
					sta.sta_datetime = GetMiddleStr(line,'日期：','\n')
					sta.sta_datetime = GetSqlDateStr(sta.sta_datetime)
						# sta.sta_datetime[:4] + '-' + sta.sta_datetime[4:6] + '-' + sta.sta_datetime[6:8]
					continue
				if  index==6:
					sta.last_statement_fund = GetMiddleStr(line, '上次结算资金：', '\t')
					sta.delivery_charge = GetMiddleStr(line, '交割手续费：', '\n')
					continue
				if  index==7:
					sta.in_or_out = GetMiddleStr(line, '出入金：', '\t')
					sta.final_balance = GetMiddleStr(line, '期末结存：', '\n')
					continue
				if index==8:
					sta.close_break = GetMiddleStr(line, '平仓盈亏：', '\t')
					sta.deposit = GetMiddleStr(line, '保证金占用：', '\n')
					continue
				if  index==9:
					sta.position_break = GetMiddleStr(line, '持仓盈亏：', '\t')
					sta.usable_fund = GetMiddleStr(line, '可用资金：', '\n')
					continue
				if  index==10:
					sta.service_charge = GetMiddleStr(line, '手续费：', '\t')
					sta.risk_degree = GetMiddleStr(line, '风险度：', '%\n')
					# 删除已有的主表Statement以及他的从表
					Statement.objects.filter(account=sta.account).filter(sta_datetime=sta.sta_datetime).delete()
					# 保存新的Statement
					sta.save()
					continue
				if  '持仓明细' in line:
					position_list = ReadTxt.second_analyzer(self,index,results)
					for pstr in position_list:
						pd_model = Position_Detail()
						pl = pstr.split('|')[1:len(pstr.split('|'))-1]
						pd_model.code = pl[0].strip()
						pd_model.exchange = pl[1].strip()
						pd_model.open_date = GetSqlDateStr(pl[2])
						pd_model.investment_type = pl[3].strip()
						pd_model.buy_or_sell = pl[4].strip()
						pd_model.number = pl[5].strip()
						pd_model.open_price = pl[6].strip()
						pd_model.close_price = pl[7].strip()
						pd_model.position_break = pl[8].strip()
						pd_model.deposit = pl[9].strip()
						pd_model.statement = sta
						pd_model.save()

				if  '持仓汇总' in line:
					all_position_list = ReadTxt.second_analyzer(self,index, results)
					for apl in all_position_list:
						ps_model = Position_Summary()
						ps_list = apl.split('|')[1:len(apl.split('|'))-1]
						ps_model.code = ps_list[0].strip()
						ps_model.buy_or_sell = ps_list[1].strip()
						ps_model.number = ps_list[2].strip()
						ps_model.open_avg_price = ps_list[3].strip()
						ps_model.close_price = ps_list[4].strip()
						ps_model.position_break = ps_list[5].strip()
						ps_model.deposit = ps_list[6].strip()
						ps_model.investment_type = ps_list[7].strip()
						ps_model.statement = sta
						ps_model.save()
				if  '成交明细' in line:
					trading_detail = ReadTxt.second_analyzer(self,index, results)
					for td in trading_detail:
						td_model = Trading_Detail()
						td_list = td.split('|')[1:len(td.split('|')) - 1]
						td_model.code = td_list[0].strip()
						td_model.exchange = td_list[1].strip()
						td_model.trading_date = GetSqlDateStr(td_list[2])
						td_model.buy_or_sell = td_list[3].strip()
						td_model.investment_type = td_list[4].strip()
						td_model.trading_price = td_list[5].strip()
						td_model.number = td_list[6].strip()
						td_model.open_close = td_list[7].strip()
						td_model.service_charge = td_list[8].strip()
						td_model.trading_id = td_list[9].strip()
						td_model.statement = sta
						td_model.save()
				if '平仓明细' in line:
					close_detail = ReadTxt.second_analyzer(self,index, results)
					for cd in close_detail:
						cd_model = Close_Detail()
						cd_list = cd.split('|')[1:len(td.split('|')) - 1]
						cd_model.code = cd_list[0].strip()
						cd_model.trading_date = GetSqlDateStr(cd_list[1])
						cd_model.buy_or_sell = cd_list[2].strip()
						cd_model.open_price = cd_list[3].strip()
						cd_model.close_price = cd_list[4].strip()
						cd_model.number = cd_list[5].strip()
						cd_model.open_close = cd_list[6].strip()
						cd_model.close_amount = cd_list[7].strip()
						cd_model.investment_type = cd_list[8].strip()
						cd_model.trading_id = cd_list[9].strip()
						cd_model.statement = sta
						cd_model.save()




	def second_analyzer(self,index,results):
		'''
		二级表分析
		:param index:索引
		:param results:全部队列
		:return:二级表队列
		'''
		begin_index = index + 4
		new_line = results[begin_index:]
		end_index = 0
		for index, position_line in enumerate(new_line):
			if position_line == '-----------------------------------------------------------------------------------------------------------------------\n':
				end_index = begin_index + index
				break
		return results[begin_index:end_index]