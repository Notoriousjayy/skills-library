def get_invoice(db, requested_invoice_id, current_user):
    return db.get_invoice_for_owner(requested_invoice_id, current_user.id)
