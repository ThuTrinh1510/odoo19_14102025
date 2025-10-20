# Stock Valuation 

Our enhanced 'Stock Valuation' module in Odoo provides a detailed guide on how to segregate labour and material costs for stock journal entries associated with Manufacturing Orders.

**Before** 

Odoo's standard settings do not offer a feature to separate labour and material costs in automated stock journal entries. This is what our enhanced module attempts to rectify.

**After**
 
Our enhanced module addresses this issue by introducing an extra function. This includes a 'stock labour valuation account' in the product category, and an automated action for dividing material costs into labour and material upon posting of a manufacturing journal entry. The labour cost is noted in the journal entry using the 'stock labour valuation account', while the material cost is segregated into material and labour costs.

## Manual

### Installing the Module
To begin using this module, just find it in the list of Odoo applications and click 'Install'.

![image1](https://gitlab.com/mjb.customers/out/enroutebizz//raw/18.0/mjb_valuation_mo_split_labor/static/description/image1.png?inline=false)
 
### Setting up product category, Bill of Materials, operations, and work center
Configure your category, Bills of Materials, operations and work center

![image2](https://gitlab.com/mjb.customers/out/enroutebizz//raw/18.0/mjb_valuation_mo_split_labor/static/description/image2.png?inline=false) 
![image3](https://gitlab.com/mjb.customers/out/enroutebizz//raw/18.0/mjb_valuation_mo_split_labor/static/description/image3.png?inline=false) 
![image4](https://gitlab.com/mjb.customers/out/enroutebizz//raw/18.0/mjb_valuation_mo_split_labor/static/description/image4.png?inline=false) 
![image5](https://gitlab.com/mjb.customers/out/enroutebizz//raw/18.0/mjb_valuation_mo_split_labor/static/description/image5.png?inline=false) 
![image6](https://gitlab.com/mjb.customers/out/enroutebizz//raw/18.0/mjb_valuation_mo_split_labor/static/description/image6.png?inline=false)
 
### Manufacturing Order generates a separate line for labour
Manufacturing Order journal entries will now include a separate line for labour costs.

![image7](https://gitlab.com/mjb.customers/out/enroutebizz//raw/18.0/mjb_valuation_mo_split_labor/static/description/image7.png?inline=false) 
![image8](https://gitlab.com/mjb.customers/out/enroutebizz//raw/18.0/mjb_valuation_mo_split_labor/static/description/image8.png?inline=false) 
![image9](https://gitlab.com/mjb.customers/out/enroutebizz//raw/18.0/mjb_valuation_mo_split_labor/static/description/image9.png?inline=false)
  
## Features

#### Separate Line for Labour
Manufacturing Order journal entries will now include a separate line for labour costs.

## About Majorbird
Majorbird is a leading software engineering and consulting firm based in Shenzhen, Guangdong, China. As an official Odoo Silver Partner, we have a proven track record of successfully implementing Odoo in over 30 projects. We understand the importance of ERP systems in today's business world and our goal is to support our customers closely to ensure success in their ERP projects.

[Contact us](https://majorbird.cn/contactus)

![Majorbird logo](https://gitlab.com/mjb.customers/out/enroutebizz//raw/18.0/mjb_valuation_mo_split_labor/static/description/logo.png?inline=false)
![Silver logo](https://gitlab.com/mjb.customers/out/enroutebizz//raw/18.0/mjb_valuation_mo_split_labor/static/description/logo_silver.png?inline=false) 

### Majorbird Vietnam Office
Tower SAV1, The Sun Avenue Apartment, Hochiminh, Vietnam

[https://majorbird.vn/](https://majorbird.vn/)

[odoo@majorbird.cn](mailto:odoo@majorbird.cn?subject=VN%20MODULE%20Stock%20Valuation)

### Majorbird China Office 
深圳市南山区招商街道沿山社区南海大道1079号花园城数码大厦A座201, 518000, Shenzhen, China

[https://majorbird.cn/](https://majorbird.cn/)

[odoo@majorbird.cn](mailto:odoo@majorbird.cn?subject=CN%20MODULE%20Stock%20Valuation)
