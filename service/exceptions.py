class AlreadyValidAT(Exception):
    def __init__(self, original_exception):
        super().__init__(str(original_exception))
        self.original_exception = original_exception

class loginTicketResponseNotFound(Exception):
    pass