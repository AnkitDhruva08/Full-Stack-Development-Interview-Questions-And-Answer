"""
Data Encapsulation:
--------------------------------
=>The Process of Hiding the confidential Information / Data / Methods from external Programmers / end users is called Data Encapsulation.
=>The Purpose of Encapsulation concept is that "To Hide Confidental Information / Features of Class (Data Members and Methods  ) ".
=>Data Encapsulation can be applied in two levels. They are
		a) At Data Members Level
		b) At Methods Level
		
=>To implement Data Encapsulation in python programming, The Data Members , Methods   must be preceded with double under score ( _ _ )
"""


# Simple Encapsulation cl;arification 
class Account:
    def __init__(self, bank_name, ac_no, ifsc_code, salary):
        self.bank_name = bank_name
        self.__ac_no = ac_no            # private
        self.__ifsc_code = ifsc_code    # private

        # salary handling
        if salary > 6000:
            self.__salary = salary      # private
            self._salary = None
        else:
            self._salary = salary       # protected
            self.__salary = None

    # --- Getter Methods ---
    def get_account_no(self):
        return self.__ac_no 
    
    def get_ifsc_code(self):
        return self.__ifsc_code
    
    def get_salary(self):
        if self.__salary is not None:
            return f"(Private) {self.__salary}"
        elif self._salary is not None:
            return f"(Protected) {self._salary}"
        return "No Salary Set"

    # --- Setter Method ---
    def set_salary(self, salary):
        if salary > 6000:
            self.__salary = salary
            self._salary = None
        else:
            self._salary = salary
            self.__salary = None







