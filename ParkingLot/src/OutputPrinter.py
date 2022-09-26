class OutputPrinter:

    def welcome(self):
        self.print_message("Welcome to AG's Parking lot.")

    def end(self):
        self.print_message("Thanks for using Go-Jek Parking lot service.")

    def not_found(self):
        self.print_message("Not found")

    def status_header(self):
        self.print_message("Slot No.    Registration No    Colour")

    def parkinglot_full(self):
        self.print_message("Sorry, parking lot is full")

    def parkinglot_empty(self):
        self.print_message("Parking lot is empty")

    def invalid_file(self):
        self.print_message("Invalid file given.")

    def print_message(self, message):
        print(message)
