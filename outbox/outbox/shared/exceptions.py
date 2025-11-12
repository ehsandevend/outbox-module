class OutboxBulkCreateError(Exception):
    """
    Raised when attempting to use bulk_create with a manager that handles outbox events.
    bulk_create does not return object IDs in Oracle, which breaks outbox tracking.
    Developers must use individual save() calls instead.
    """

    pass
