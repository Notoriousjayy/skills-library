def get_invoice(db, requested_invoice_id, current_user):
    return db.get_invoice(requested_invoice_id)  # No owner/tenant filter
