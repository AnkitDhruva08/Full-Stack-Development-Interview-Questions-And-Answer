class Account1:
    def __getaccountdet(self):    # private method
        self.acno = 34567
        self.cname = "Rossum"
        self.bal = 34.56
        self.bname = "SBI"
        self.pin = 1234
        self.pincode = 4444444

    # public method to access private method
    def show_account(self):
        # call the private method inside
        self.__getaccountdet()
        return {
            "Account Number": self.acno,
            "Customer Name": self.cname,
            "Balance": self.bal,
            "Branch": self.bname,
            "PIN": self.pin,
            "Pincode": self.pincode
        }