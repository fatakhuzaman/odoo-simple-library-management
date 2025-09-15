from odoo import models, fields, api
from odoo.exceptions import UserError

class LibraryBook(models.Model):
    _name = "library.book"
    _description = "Library Book"

    name = fields.Char(string="Title", required=True)
    author = fields.Char(string="Author")
    pages = fields.Integer(string="Pages")
    amount = fields.Integer(string="Amount", default="0")
    available = fields.Integer(string="Available", default="0", readonly=True)
    borrowed = fields.Integer(string="Borrowed", default="0", readonly=True)
    lost = fields.Integer(string="Lost", default="0", readonly=True)
    borrower_ids = fields.One2many('library.transaction', 'book_id', string="Book")

    @api.model
    def create(self, vals_list):
        if vals_list.get("amount"):
            vals_list['available'] = vals_list["amount"]
        return super(LibraryBook, self).create(vals_list)

    def write(self, vals):
        for rec in self:
            if "amount" in vals:
                new_amount = vals["amount"]
                if new_amount < rec.amount:
                    raise UserError("The amount must not be reduced from the previous amount!")
                
                selisih = new_amount - rec.amount
                if selisih > 0:
                    rec.available += selisih

        return super(LibraryBook, self).write(vals)