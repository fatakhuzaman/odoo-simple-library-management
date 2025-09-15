from odoo import models, fields, api
from odoo.exceptions import UserError

class LibraryTransaction(models.Model):
    _name = "library.transaction"
    _description = "Library Transaction"

    name = fields.Char(string="Borrower", required=True)
    book_id = fields.Many2one('library.book', string="Book", required=True)
    description = fields.Text(string="Description")
    borrow_date = fields.Datetime(string="Borrow Date")
    return_date = fields.Datetime(string="Return Date")
    lost_date = fields.Datetime(string="Lost Date")
    status = fields.Selection(
        [
            ('borrowed', 'Borrowed'),
            ('returned', 'Returned'),
            ('lost', 'Lost'),
        ],
        string="Status",
        default="borrowed",
        required=True
    )

    @api.model
    def create(self, vals_list):
        book = self.env['library.book'].browse(vals_list['book_id'])
        if book.available <= 0:
            raise UserError("Books are not available for borrowing")

        vals_list['status'] = 'borrowed'
        vals_list['borrow_date'] = fields.Datetime.now()

        book.available -= 1
        book.borrowed += 1

        return super(LibraryTransaction, self).create(vals_list)

    def action_return(self):
        for rec in self:
            if rec.status == 'returned':
                raise UserError("The books has returned")
                
            if rec.status == 'lost':
                rec.book_id.available += 1
                rec.book_id.lost -= 1
            else:
                rec.book_id.available += 1
                rec.book_id.borrowed -= 1

            rec.return_date = fields.Datetime.now()
            rec.status = 'returned'

    def action_lost(self):
        for rec in self:
            if rec.status != 'borrowed':
                raise UserError("Only borrowed books can be marked as lost!")

            rec.lost_date = fields.Datetime.now()
            rec.status = 'lost'

            rec.book_id.borrowed -= 1
            rec.book_id.lost += 1
