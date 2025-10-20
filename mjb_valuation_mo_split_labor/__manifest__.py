{
    "name": "Stock Valuation",
    "author": "Majorbird",
    "version": "0.1",
    "category": "Inventory/Inventory",
    "summary": "By using this module, the labour cost is calculated by time spent on operations multiplied by the workcentre's hourly rate. Material costs are accounted separately.",
    "website": "majorbird.cn",
    "depends": [
        "base",
        "stock",
        "account",
        "mrp",
        "mrp_maintenance",
        "base_automation",
        "stock_account",
        "mrp_workorder",
        'hr_hourly_cost'
    ],
    "data": [
        'data/action.xml',
        'data/base_automation.xml',
        'views/hr_employee.xml',
        'views/product_category_views.xml',
    ],
    "_documentation": {
        "banner": "banner.jpg",
        "icon": "icon.png",
        "excerpt": "Our enhanced 'Stock Valuation' module in Odoo provides a detailed guide on how to segregate labour and material costs for stock journal entries associated with Manufacturing Orders.",
        "summary": "Odoo's standard settings allow for automated stock journal entries based on the set-up valuation, or input accounts either on product category or stock location. This feature automatically activates whenever a product is manufactured. But one main issue is that the labour cost and the material cost are not differentiated in these entries. Our enhanced solution module makes it possible to separate these costs. The labour cost is calculated by time spent on operations multiplied by the workcentre's hourly rate. Material costs are accounted separately.vFor this module to work efficiently, one has to set up labour cost account, and the input/output/stock valuation for FIFO/Automated stock products on all product categories.",
        "issue": "Odoo's standard settings do not offer a feature to separate labour and material costs in automated stock journal entries. This is what our enhanced module attempts to rectify.",
        "solution": "Our enhanced module addresses this issue by introducing an extra function. This includes a 'stock labour valuation account' in the product category, and an automated action for dividing material costs into labour and material upon posting of a manufacturing journal entry. The labour cost is noted in the journal entry using the 'stock labour valuation account', while the material cost is segregated into material and labour costs.",
        "manual": [
            {
                "title": "Installing the Module",
                "description": "To begin using this module, just find it in the list of Odoo applications and click 'Install'.",
                "images": ["image1.png"],
            },
            {
                "title": "Setting up product category, Bill of Materials, operations, and work center",
                "description": "Configure your category, Bills of Materials, operations and work center",
                "images": ["image2.png", "image3.png", "image4.png","image6.png"],
            },
            {
                "title": "Manufacturing Order generates a separate line for labour",
                "description": "Manufacturing Order journal entries will now include a separate line for labour costs.",
                "images": ["image7.png", "image8.png"],
            },
        ],

        "features": [
            {
                "title": "Separate Line for Labour",
                "description": "Manufacturing Order journal entries will now include a separate line for labour costs.",
            },
        ],
    },
    'images': ['static/description/banner_slide.gif'],
    "license": "OPL-1",
    "installable": True,
}
