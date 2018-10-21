# coding:utf-8
import csv
import os
import pandas as pd

# 读入所有店铺交易数据
results_list = []
# 从inputfiles里面逐个读出文件信息
for (root, dirs, files) in os.walk('C:/Users/Administrator/Desktop/inputfiles/'):
    for file in files:
        filename = os.path.join(root, file)
        portion = os.path.splitext(file)
        csv_reader = csv.reader(open(filename, encoding='utf-8'))
        count = 0
        # 除了前7行 其他的信息存起来
        for row in csv_reader:
            count += 1
            if count > 8:
                row6 = row[6]
                if row6 == "":
                    row6 = "0"
                results_list.append([portion[0], row[2], row[4], int(row6.replace(',', '')), \
                                     float(row[12].replace(',', '')), float(row[13].replace(',', '')), \
                                     float(row[14].replace(',', '')), float(row[15].replace(',', '')), \
                                     float(row[16].replace(',', '')), float(row[17].replace(',', '')), \
                                     float(row[18].replace(',', '')), float(row[19].replace(',', '')), \
                                     float(row[20].replace(',', '')), float(row[21].replace(',', '')), \
                                     float(row[22].replace(',', ''))])
# 给results_list添加标题行
all_data = pd.DataFrame(results_list, index=None, columns=['dianpu', 'type', 'sku', 'quantity', \
                                                           'product_sales', 'shipping_credits', 'gift_wrap_credits', \
                                                           'promotional_rebates', 'sales_tax_collected', \
                                                           'Marketplace_Facilitator_Tax', 'selling_fees', 'fba_fees', \
                                                           'other_transaction_fees', 'other', 'total'])

df = all_data.copy()

# 销售量计算：type==Order,quantity的和
quantity_sales = df.loc[df.type == 'Order', ['dianpu', 'type', 'sku', 'quantity']]
quantity_sales.rename(columns={'quantity': '销售量'}, inplace=True)

# 退款量计算：“Refund”-“product sales”金额为0的数量，（问题：如何减“product sales”金额为0的数量）
quantity_refund = df.loc[df.type == 'Refund', ['dianpu', 'type', 'sku', 'quantity']]
quantity_refund.rename(columns={'quantity': '退款量'}, inplace=True)

df2 = df.loc[df.product_sales == 0, ['dianpu', 'type', 'sku', 'quantity', 'product_sales']]
quantity_refund1 = df2.loc[df2.type == 'Refund', ['dianpu', 'type', 'sku', 'quantity']]
quantity_refund1.rename(columns={'quantity': '减退款量 '}, inplace=True)

# 收入类-收到运费
income_shipping_credits = df.loc[:, ['dianpu', 'type', 'sku', 'shipping_credits']]
income_shipping_credits.rename(columns={'shipping_credits': '运费'}, inplace=True)

# 收入类-销售收入
income_product_sales = df.loc[:, ['dianpu', 'type', 'sku', 'product_sales']]
income_product_sales.rename(columns={'product_sales': '商品价格'}, inplace=True)

# 收入类-折扣:促销返点
income_promotional_rebates = df.loc[:, ['dianpu', 'type', 'sku', 'promotional_rebates']]
income_promotional_rebates.rename(columns={'promotional_rebates': '促销返点'}, inplace=True)

# 收入类-折扣:销售税
income_sales_tax_collected = df.loc[:, ['dianpu', 'type', 'sku', 'sales_tax_collected']]
income_sales_tax_collected.rename(columns={'sales_tax_collected': '销售税'}, inplace=True)

# 收入类-折扣:平台服务税
income_Marketplace_Facilitator_Tax = df.loc[:, ['dianpu', 'type', 'sku', 'Marketplace_Facilitator_Tax']]
income_Marketplace_Facilitator_Tax.rename(columns={'Marketplace_Facilitator_Tax': '平台服务税'}, inplace=True)

# 店内费用类-佣金
sellingfees = df.loc[:, ['dianpu', 'type', 'sku', 'selling_fees']]
sellingfees.rename(columns={'selling_fees': '佣金'}, inplace=True)

# 店内费用类-亚马逊物流基础服务费
fba = df.loc[:, ['dianpu', 'type', 'sku', 'fba_fees']]
fba.rename(columns={'fba_fees': '亚马逊物流基础服务费'}, inplace=True)

# 店内费用类-广告费用
other_transaction = df.loc[:, ['dianpu', 'type', 'sku', 'other_transaction_fees']]
other_transaction.rename(columns={'other_transaction_fees': '广告费用'}, inplace=True)

# 店内费用类-其他：订单
order_other = df.loc[df.type == 'Order', ['dianpu', 'type', 'sku', 'other']]
order_other.rename(columns={'other': '其他_订单'}, inplace=True)

# 店内费用类-其他：服务费
service_fee_other = df.loc[df.type == 'Service Fee', ['dianpu', 'type', 'sku', 'other']]
service_fee_other.rename(columns={'other': '其他：服务费'}, inplace=True)

# 店内费用类-其他：其他：退货
refund_other = df.loc[df.type == 'Refund', ['dianpu', 'type', 'sku', 'other']]
refund_other.rename(columns={'other': '其他：退货'}, inplace=True)

# 店内费用类-其他：其他：清算
adjustment_other = df.loc[df.type == 'Adjustment', ['dianpu', 'type', 'sku', 'other']]
adjustment_other.rename(columns={'other': '其他：清算'}, inplace=True)

# 店内费用类-其他：其他：闪电交易费
lightning_Deal_Fee_other = df.loc[df.type == 'Lightning Deal Fee', ['dianpu', 'type', 'sku', 'other']]
lightning_Deal_Fee_other.rename(columns={'other': '其他：闪电交易费'}, inplace=True)

# 店内费用类-其他：其他：Debt
debt_other = df.loc[df.type == 'Debt', ['dianpu', 'type', 'sku', 'other']]
debt_other.rename(columns={'other': '其他：Debt'}, inplace=True)

# 店内费用类-其他：其他：退款
chargeback_Refund_other = df.loc[df.type == 'Chargeback Refund', ['dianpu', 'type', 'sku', 'other']]
chargeback_Refund_other.rename(columns={'other': '其他：退款'}, inplace=True)

# 店内费用类-其他：其他：FBA 库存费
FBA_Inventory_Fee_other = df.loc[df.type == 'FBA Inventory Fee', ['dianpu', 'type', 'sku', 'other']]
FBA_Inventory_Fee_other.rename(columns={'other': '其他：FBA 库存费'}, inplace=True)

# 店内费用类-包装费
gift_wrap_credits_fees = df.loc[:, ['dianpu', 'type', 'sku', 'gift_wrap_credits']]
gift_wrap_credits_fees.rename(columns={'gift_wrap_credits': '包装费'}, inplace=True)

# 其他：提款
tixian = df.loc[df.type == 'Transfer', ['dianpu', 'type', 'sku', 'total']]
tixian.rename(columns={'total': '其他:提款'}, inplace=True)

# 销售净额
xiaoshoue = df.loc[df.type != 'Transfer', ['dianpu', 'type', 'sku', 'total']]
xiaoshoue.rename(columns={'total': '销售净额'}, inplace=True)

concat_all = pd.concat([quantity_sales, quantity_refund, quantity_refund1, income_shipping_credits, \
                        income_product_sales, income_promotional_rebates, income_sales_tax_collected, \
                        income_Marketplace_Facilitator_Tax, sellingfees, fba, other_transaction, \
                        order_other, service_fee_other, refund_other, adjustment_other, \
                        lightning_Deal_Fee_other, debt_other, chargeback_Refund_other, FBA_Inventory_Fee_other, \
                        gift_wrap_credits_fees, xiaoshoue, tixian]).fillna(0)


sales_statistics = concat_all.groupby(['dianpu','sku'])['销售净额','销售量','退款量','减退款量 ','运费','商品价格',\
                                                 '促销返点','销售税','平台服务税','佣金','亚马逊物流基础服务费',\
                                                 '广告费用','其他_订单','其他：服务费','其他：退货','其他：清算',\
                                                 '其他：闪电交易费','其他：Debt','其他：退款','其他：FBA 库存费',\
                                                 '包装费','其他:提款'].sum()

sales_statistics.to_csv('C:/Users/Administrator/Desktop/result.csv')

print('done...')
exit(0)
