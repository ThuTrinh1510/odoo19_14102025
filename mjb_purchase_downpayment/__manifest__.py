# -*- coding: utf-8 -*-
{
    'name': 'MJB - Purchase Downpayment',
    "version": "19.0.0.2",
    'author': 'Majorbird',
    'website': 'https://majorbird.cn',
    'category': 'Inventory/Purchase',
    'summary': 'Purchase DownPayment',
    'description':
    '''
        This module contain some functions:\n
        1. add downpayment on purchase\n
    ''',
    'depends': [
        'base','purchase'
    ],
    'data': [
        'security/ir.model.access.csv',

        'wizard/purchase_make_invoice_advance_views.xml',
        'views/res_config_setting_views.xml',
        'views/purchase.xml',
    ],
    'css': [],
    'js': [],
    "_documentation":
    {
        "banner": "banner.png",
        "icon": "icon.png",
        "excerpt": "Effortless Purchase Downpayment Management",
        "summary": "Welcome to the Purchase Downpayment Manager module. This tool streamlines the purchase process by allowing you to easily add downpayments to your purchase orders. It simplifies financial transactions and enhances transparency in your procurement operations.",
        "issue": "Solving Downpayment Challenges",
        "solution": "The Purchase Downpayment module is designed to address the challenges associated with adding downpayments to purchase orders. It provides a user-friendly interface for managing advance payments and simplifies financial control during procurement.",
        "manual": [
            {
                "title": "Installation",
                "description": "Locate the module in the application list and proceed with clicking 'Install'!",
                "images": ["image1.png"]
            },
            {
                "title": "Managing Downpayments",
                "description": "Open the purchase order where you've added a downpayment, review and edit downpayment details if necessary.",
                "images": ["image3.png","image2.png","image4.png"]
            }
        ],
        "features": [
            {
                "title": "Streamlined Downpayment Handling",
                "description": "Effortlessly add downpayments to purchase orders, enhancing financial control and transparency."
            }
        ]
    },
    'images': ['static/description/banner_slide.gif'],
    'demo': [],
    'application': False,
    'license': 'OPL-1',
    "installable": True,  
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
