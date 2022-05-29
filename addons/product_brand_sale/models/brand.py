# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2020-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Midilaj (<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from odoo import models, fields, api


class PosCategory(models.Model):
    _inherit = 'pos.category'
    
    code = fields.Char(string='Code', required=True)
    
    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Brand code must be unique!')
    ]

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brand_id = fields.Many2one('product.brand', string='Brand')
    
    # Onchange brand_id set default_code
    
    @api.onchange('brand_id', 'pos_categ_id')
    def _onchange_brand_id(self):
        for rec in self:
            brand_code = ''
            cat_code = ''
            if rec.brand_id:
                next_num = int(rec.brand_id.product_count) + 1
                brand_code = rec.brand_id.code + (str(next_num).zfill(4))
            if rec.pos_categ_id:
                for cat in rec.pos_categ_id:
                    if cat.code:
                        cat_code += cat.code
            if brand_code and cat_code:
                rec.name = cat_code + '-' + brand_code
    
    
    
class ProductProduct(models.Model):
    _inherit = 'product.product'

    brand_id = fields.Many2one('product.brand', string='Brand')
    
    @api.onchange('brand_id', 'pos_categ_id')
    def _onchange_brand_id(self):
        for rec in self:
            brand_code = ''
            cat_code = ''
            if rec.brand_id:
                next_num = int(rec.brand_id.product_count) + 1
                brand_code = rec.brand_id.code + (str(next_num).zfill(4))
            if rec.pos_categ_id:
                for cat in rec.pos_categ_id:
                    if cat.code:
                        cat_code += cat.code
            if brand_code and cat_code:
                rec.name = cat_code + '-' + brand_code
    
    total_sale_price = fields.Float(string='Total Sale Price', compute='_compute_total_sale_price')
    total_purchase_price = fields.Float(string='Total Purchase Price', compute='_compute_total_sale_price')
    
    def _compute_total_sale_price(self):
        for rec in self:
            sale_price = 0.0
            rec.total_sale_price = rec.lst_price * rec.qty_available
            rec.total_purchase_price = rec.standard_price * rec.qty_available


class BrandProduct(models.Model):
    _name = 'product.brand'

    name = fields.Char(String="Name")
    brand_image = fields.Binary()
    member_ids = fields.One2many('product.template', 'brand_id')
    product_count = fields.Char(String='Product Count', compute='get_count_products', store=True)
    code = fields.Char(String='Code', required=True)
    
    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Brand code must be unique!')
    ]

    @api.depends('member_ids')
    def get_count_products(self):
        self.product_count = len(self.member_ids)


class BrandPivot(models.Model):
    _inherit = 'sale.report'

    brand_id = fields.Many2one('product.brand', string='Brand')

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['brand_id'] = ", t.brand_id as brand_id"
        groupby += ', t.brand_id'
        return super(BrandPivot, self)._query(with_clause, fields, groupby, from_clause)
