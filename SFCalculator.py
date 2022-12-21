import math

from PyQt5.QtWidgets import (
    QLabel, QWidget, QApplication, 
    QVBoxLayout, QGridLayout, 
    QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from functools import partial
import sys

INT_MAX=0x7f7f7f7f





def plog(func, content):
    print("[{0}]: {1}".format(func, content))




class Sig_Number:
    def __init__(self):
        self.value = "0"                            # value, stored in string, making moving digits easier 
        self.low_decimal = 0                        # Lowest significant decimal, used in addition/subtraction
        self.max_sig_num = 1                        # Maximum number of significant digits, used in multiplication/division
        self.e = 0                                  # Scientific Notation, records the power of 10
        # self.units = {}                           # Units stored in dictionary. not used in calculator, and is not supported by parser yet

    def __init__(self, quant):
        
        self.value = "0"
        self.low_decimal = 0                
        self.max_sig_num = 1                        # Initialize number to have infinte amount of significant digits
        self.e = 0
        # self.units = {}

        self.parse_string()                         # Parse String
        self.to_scientific()                        # Convert to Proper Scientific
        # self.cleanup_units()                      # Cleanup Units
        return



    '''
    Parse String
    - Checks Exact Numbers
    - Parse Scientific Notation
    - 

    The Proper Way to Format a number is as follows:
    "1.259e33"  --[means]--> 1.259 * 10^33
    "_-8_"      --[means]--> [exact number] -8
    '''

    def parse_string(self):
        is_exact = False                                                    # Deal with Exact Numbers
        if arr[0] == "_" and arr[-1] == "_":
            arr = arr[1:len(arr)-1]
            self.low_decimal = -INT_MAX/2
            self.max_sig_num = INT_MAX
            is_exact = True
        if 'e' in arr:                                                      # Deal with Sci Notation
            num = value.split("e")
            if len(num[0]) == 0 or len(num[1] == 0) or len(num) != 2:
                return "INVALID SCI-NOTE"
            arr = num[0]
            self.e = float(num[1])
        if is_exact == True:                                                # Recognize Numbers
            # Deal with Consts
            if arr == "E":
                self.value = str(math.e)
            elif arr == "-E":
                self.value = str(-math.e)
            elif arr == "PI":
                self.value = str(math.pi)
            elif arr == "-PI":
                self.value = str(-math.pi)
            else:
                self.value = arr
                check_result = self.check_and_format_value()
                if check_result != True:
                    return check_result
        else:
            self.value = arr
            check_result = self.check_and_format_value()
            if check_result != True:
                return check_result
            self.low_decimal, self.max_sig_num = self.find_sigfig()
        return True









    def get_string(self):
        num_unit = ""
        div_unit = ""
        for unit in self.units:
            # Deal with more than one dimension units
            if self.units[unit] > 1:
                num_unit += "{0}^{1} ".format(unit, self.units[unit])
            elif self.units[unit] == 1:
                num_unit += "{0}^{1}".format(unit, self.units[unit])
            elif self.units[unit] == -1:
                div_unit += "{0}^{1}".format(unit, self.units[unit])
            else:
                div_unit += "{0}^{1} ".format(unit, self.units[unit])
        print_str = ""

        # Deal with Sign
        if self.sign == -1:
            print_str += "-"

        # Deal with value
        val_str = str(self.value)
        print_n = 0
        for i in range (0,len(val_str)):
            if print_n == self.max_sig_num:
                break
            print_str += val_str[i]
            if val_str[i] != ".":
                print_n += 1
        while print_n < self.max_sig_num:                                       # 
            print_str += "0"
            print_n += 1
        if self.e != 0:                                                         # Deal with Power
            print_str += "e{0}".format(self.e)

        '''
        # Deal with Units
        if len(num_unit):
            print_str += " " + num_unit
        if len(div_unit):
            print_str += "/ " + div_unit
        '''
        '''
        # Deal with Suffix Info
        print_str += " [Sig Digits: {0} / Sig Decimal: {1}]".format(self.max_sig_num, self.low_decimal)
        '''
        return print_str
    def show(self):
        print(self.get_string())

    '''
    def get_sig_fig_indicator(self):
        str = self.get_string()
        numcnt = 0
        sf_str = ""
        for i in range(0,len(str)):
            if str[i] == " ":
                sf_str = "_"*i + " "*(len(str)-1)
                return sf_str
        sf_str = "_"*len(str)
        return sf_str
    '''




    



    def to_scientific(self):
        if self.value < 0:
            self.sign = -1
            self.value *= -1
        while self.value >= 10:
            self.value /= 10
            self.e += 1
            self.low_decimal -= 1
        while self.value < 1 and self.value > 0:
            self.value *= 10
            self.e -= 1
            self.low_decimal += 1
        return




    '''
    def cleanup_units(self):
        for unit in self.units:
            if self.units[unit] == 0:
                self.units.pop(unit, "Desired Unit for Deletion Not Found")
                # del self.units[unit]
        return
    '''



    # Cleanup Functions
    def update_max_signum(self):
        self.max_sig_num = min(self.max_sig_num, abs(self.low_decimal)+1)

    def int_digits(self):
        idig = 0
        tmp = self.value
        while abs(tmp) >= 1:
            tmp /= 10
            idig += 1
        return idig

    def update_low_dec(self):
        # self.low_decimal = min(self.low_decimal, 1-self.max_sig_num)
        self.low_decimal = self.int_digits()-self.max_sig_num


    


    def check_and_format_value(self):
        legal_char = ['0','1','2','3','4','5','6','7','8','9','.','-']
        val = self.value
        sign = 1
        # Check String Format
        dotcnt = 0
        for i in range(0,len(self.value)):                          # Check if unnecessary signs occur
            if self.value[i] == '-' and i != 0:
                return "ERROR UNEXPECTED '-' SIGN"                  # If '-' sign occurs not in the first character
            elif self.value[i] == '.':
                dotcnt += 1
                if dotcnt > 1:
                    return "ERROR UNEXPECTED TOO MANY STRINGS"     # If other characters are in the string
            elif self.value[i] not in legal_char:
                return "ERROR UNEXPECTED CHAR"                      # If other characters are in the string
        if val[0] == '-':                                           # Deal with Sign
            val = val[1:]
            sign = -1
        while val[0] == "0":                                        # Deal with Leading Zeros
            val = val[1:]
        if len(val) == 0:
            val = '0'
        if '.' in val:                                              # Deal with decimal point
            if val[0] == '.':
                val = "0" + val
        if sign == -1:                                              # Cleanup 
            val = '-' + val
        self.value = val
        return True
        

    def find_sigfig(self):
        plog("FindSF", "Finding SF for {0}".format(val))
        value = self.value                                          # Make a copy of value and work on that
        # Format String
        if value[0] == '-':                                         # Deal with Sign
            value = self.value[1:]
        if "." in value:                                            # Deal with Decimals
            n = value.split(".") 
            intprt = n[0]                                               # Deal with Integer Part
            for i in range(0,len(intprt)):                              # First remove all leading zeros
                if intprt[0] == "0": 
                    intprt = intprt[1:]
                else: 
                    break
            max_sigfig = len(intprt)                                    # After removing all zeros, max sig fig update
                                                                        # Deal with Decimal Part
            low_dec = -len(n[1])                                        # Lowest decimal is where the lowest is 
            max_sigfig += len(n[1])                                     # For every digit after decimal, max sigfig counts as one
        
        else:                                                       # If there is no decimal point
            for i in range(0,len(value)-1):                         # First remove all leading zeros
                if value[0] == '0': 
                    value = value[1:]
                else: break
            if len(value) != 0:                                     # If the value is not zero
                if value[len(value)-1] == '0':                      # deal with trailing zeros. 
                    plog("Input {0} has AMBIGUOUS Sig Figs!".format(value))
                for i in range(len(value)-1,-1, -1):
                    if value[i] == '0':                             # For trailing zeros, lowest decimal place ++
                        low_dec += 1
                    else:                                           # Otherwise, break and do max_sigfig
                        break
                max_sigfig = len(value) - low_dec
        if max_sigfig == 0:
            max_sigfig = INT_MAX
        return low_dec, max_sigfig

    def invert_sign(self):
        self.sign *= -1
        return


    # +-*/ Calculations
    def __add__(self, num2):
        # If the units don't match, addition cannot be completed
        if same_unit(self, num2) != True:
            plot("[__add__] Mismatching Units!")
            return False
        # Prep Work
        self.e, num2.e = sync_e(self, num2)                          # Sync the scientific notation so values can be added
        # Update Value
        self.value = self.value * self.sign + num2.value * num2.sign     # Update New Value
        # Sig Fig & Units remains the same
        # Update Sig Fig Info
        self.low_decimal = max(self.low_decimal, num2.low_decimal)       # Addition, uses decimal place rule
        # Clean up
        self.to_scientific()                     # Convert to Proper Sci Notation
        self.update_max_signum()                 # pdate max sig figure count based on decimal place result
        return self

    def __sub__(self, num2):
        # If the units don't match, addition cannot be completed
        if same_unit(self, num2) != True:
            plot("[__sub__] Mismatching Units!")
            return False
        # Prep Work
        self.e, num2.e = sync_e(self, num2)                          # Sync the scientific notation so values can be added
        # Update Value
        self.value = self.value * self.sign - num2.value * num2.sign     # Update New Value
        # Sig Fig & Units remains the same
        self.low_decimal = max(self.low_decimal, num2.low_decimal)       # Update Sig Fig Info --> Subtraction, uses decimal place rule
        # Clean up
        self.to_scientific()                     # Convert to Proper Sci Notation
        self.update_max_signum()                 # pdate max sig figure count based on decimal place result
        return self

    def __mul__(self, num2):
        # Update Value
        self.value *= num2.value
        self.sign *= num2.sign
        self.e += num2.e
        # Update Units
        self.mult_unit(num2)
        # Sig Fig Update
        self.max_sig_num = min(self.max_sig_num, num2.max_sig_num)
        self.update_low_dec()
        self.to_scientific()                     # Convert to Proper Sci Notation
        return self

    def __truediv__(self, num2):
        # Update Value
        self.value /= num2.value
        self.sign *= num2.sign
        self.e -= num2.e
        # Update Units
        self.div_unit(num2)
        # Sig Fig Update
        self.max_sig_num = min(self.max_sig_num, num2.max_sig_num)
        self.update_low_dec()
        self.to_scientific()                     # Convert to Proper Sci Notation
        return self

    '''
    def __pow__(self, num2):
        # Update Value
        self.value *= num2.value
        self.e += num2.e
        # Update Units
        self.mult_unit(num2)
        # Sig Fig Update -- No Need
        self.update_low_dec()
        self.to_scientific()                     # Convert to Proper Sci Notation
        # Cleanup
        return self
    '''


    '''
    # Unit Multiplication and Division
    def mult_unit(self, cdt):
        for unit in cdt.units:
            if self.units[unit] == None:
                self.units[unit] = 0
            self.units[unit] += cdt.units[unit]
        self.cleanup_units()
    def div_unit(self, cdt):
        for unit in cdt.units:
            if self.units[unit] == None:
                self.units[unit] = 0
            self.units[unit] -= cdt.units[unit]
        self.cleanup_units()
    '''


    def val_tenfold(self):
        if '.' in self.value:
            if self.value[0] == '.':                    #

        else:
            self.value += '0'
            

    def sync_e(self, num2):
        while self.e > num2.e:
            self.value_tenfold()
            self.e -= 1
            self.low_decimal += 1
        while self.e < num2.e:
            num2.val_tenfold()
            num2.e -= 1
            num2.low_decimal += 1
        return self, num2

    def same_unit(self, num2):
        # If length is not the same 
        # assuming units have been cleared with cleanup functions
        if len(self.units) != len(num2.units):
            return False
        # If length is the same, check if all units are the same with the same values. 
        for unit in self.units:
            if self.units[unit] != num2.units[unit]: 
                return False
        return True



































class CalculatorBackend:
    def __init__(self):
        self.legal_operators = ['+', '*', '/', '-']
        self.dummy = Sig_Number("0.0")

        
        self.prev_val = self.dummy                              # Prev Value
        self.prev_expr = ""

        # Operation
        self.left_expr = ""
        self.left_val = self.dummy
        self.operator = ""
        self.right_expr = ""
        self.right_val = self.dummy

        # Results
        self.res = self.dummy
        self.res_expr = ""

    def clear_res(self):
        if self.res != self.dummy:
            self.res == self.dummy
            self.res_expr = ""
        

    # Add stuff
    def clear(self):
        self.clear_res()
        self.operator = ""
        self.left_expr = ""
        self.left_val = self.dummy
        self.right_expr = ""
        self.right_val = self.dummy
        return

    def delete(self):
        self.clear_res()
        if self.right_expr != "":
            self.right_expr = ""
            self.left_val = self.dummy
        elif self.operator != "":
            self.operator = ""
        elif self.left_expr != "":
            self.left_expr = ""
            self.left_val = self.dummy

    def apply_prev(self):
        self.clear_res()
        if self.operator != "":
            self.right_val = self.prev_val
            self.right_expr = self.prev_expr
        else:
            self.left_val = self.prev_val
            self.left_expr = self.prev_expr

    def invert_sign(self):
        self.clear_res()
        if self.operator != "" and self.right_val != self.dummy:
            self.right_val.invert_sign()
            if self.right_expr[0] == "-":
                self.right_expr = self.right_expr[1:]
            else:
                self.right_expr = "-" + self.right_expr

        elif self.left_val != self.dummy:
            self.left_val.invert_sign()
            if self.left_expr[0] == "-":
                self.left_expr = self.left_expr[1:]
            else:
                self.left_expr = "-" + self.left_expr

    def def_operator(self, content):
        self.clear_res()
        if self.left_expr != "":
            self.operator = content
        return
    
    def add_number(self, n):
        self.clear_res()
        if self.operator == "":
            self.left_expr += n
            self.left_val = Sig_Number(self.left_expr)
        else:
            self.right_expr += n
            self.right_val = Sig_Number(self.right_expr)
    
    def compute(self):
        if self.left_expr != "" and self.operator != "" and self.right_expr != "":
            if self.operator == "+":
                self.res = self.left_val + self.right_val
            elif self.operator == "-":
                self.res = self.left_val - self.right_val
            elif self.operator == "*":
                self.res = self.left_val * self.right_val
            elif self.operator == "/":
                self.res = self.left_val / self.right_val
            elif self.operator == "^":
                self.res = self.left_val^self.right_val
            self.res_expr = self.res.get_string()
            self.prev_val = self.res
            self.prev_expr = self.res_expr
        else:
            return "ERROR! Invalid Expression"

        # Cleanup
        self.operator = ""
        self.left_expr = ""
        self.left_val = self.dummy
        self.right_expr = ""
        self.right_val = self.dummy
































class Calculator:
    def __init__(self):
        self.app = QApplication([])
        self.log("[Main] Initializing app")
        self.app.setWindowIcon(QIcon("icon.png"))

        # Main View
        self.main_window = QWidget()
        self.main_window.setWindowTitle("Sig Fig Calculator")
        self.main_window.setFixedHeight(720)
        self.main_window.setFixedWidth(480)

        self.main_box_layout = QVBoxLayout()
        self.main_window.setLayout(self.main_box_layout)
        self.calculator = CalculatorBackend()

        print("Backbone Created")

        # Initialize Display and Keyboard Arrangement
        self.add_display()
        self.add_keyboard()

        print("Initialized")
        return 


    '''
    Initialization
    '''
    def add_display(self):
        # Main Digit Display
        self.calc_msg = ""
        self.calc_display = QLineEdit()
        self.calc_display.setAlignment(Qt.AlignRight)
        self.calc_display.setFixedHeight(160)
        self.calc_display.setReadOnly(True)
        self.main_box_layout.addWidget(self.calc_display)

        # Results Display
        self.res_msg = ""
        self.res_display = QLineEdit()
        self.res_display.setAlignment(Qt.AlignRight)
        self.res_display.setFixedHeight(40)
        self.res_display.setReadOnly(True)
        self.main_box_layout.addWidget(self.res_display)

        '''
        # Sig Fig Display
        self.sig_msg = ""
        self.sig_display = QLineEdit()
        self.sig_display.setAlignment(Qt.AlignRight)
        self.sig_display.setFixedHeight(40)
        self.sig_display.setReadOnly(True)
        self.main_box_layout.addWidget(self.sig_display)
        '''

    def add_keyboard(self):
        self.button_map = {}
        self.button_grid = QGridLayout()
        keyboard = [
            ["7", "8", "9", "/", "C"],
            ["4", "5", "6", "*", "<=="],
            ["1", "2", "3", "-", "PREV"],
            ["inv", "0", ".", "+", "="],
        ]
        for row, keys in enumerate(keyboard):
            for col, key in enumerate(keys):
                self.button_map[key] = QPushButton(key)
                self.button_map[key].setFixedSize(80, 100)
                if key == "C":
                    self.button_map[key].clicked.connect(self.clear)
                elif key == "<==":
                    self.button_map[key].clicked.connect(self.delete)
                elif key == "PREV":
                    self.button_map[key].clicked.connect(self.apply_prev)
                elif key == "inv":
                    self.button_map[key].clicked.connect(self.invert_sign)
                elif key in self.calculator.legal_operators:
                    self.button_map[key].clicked.connect(partial(self.def_operator, key))
                elif key == "=":
                    self.button_map[key].clicked.connect(self.show_result)
                else:
                    self.button_map[key].clicked.connect(partial(self.add_number, key))
                self.button_grid.addWidget(self.button_map[key], row, col)

        self.main_box_layout.addLayout(self.button_grid)
        return

    '''
    Display
    '''
    def update_display(self):
        self.calc_msg = self.calculator.left_expr + \
                        self.calculator.operator + \
                        self.calculator.right_expr
        # Results Tab
        self.res_msg = self.calculator.res_expr
        '''
        # Sig Fig Tab
        if self.res_msg != "":
            self.sig_msg = self.calculator.res.get_sig_fig_indicator()
        else:
            self.sig_msg = ""
        '''
        self.calc_display.setText(self.calc_msg)
        self.res_display.setText(self.res_msg)
        # self.sig_display.setText(self.sig_msg)
        self.calc_display.setFocus()


    '''
    Buttons
    '''
    def clear(self):
        self.calculator.clear()
        self.update_display()

    def delete(self):
        self.calculator.delete()
        self.update_display()
    
    def apply_prev(self):
        self.calculator.apply_prev()
        self.update_display()
    
    def invert_sign(self):
        self.calculator.invert_sign()
        self.update_display()
    
    def def_operator(self, content):
        self.calculator.def_operator(content)
        # Update Display
        self.update_display()

    def show_result(self):
        self.calculator.compute()
        self.update_display()

    def add_number(self, n):
        self.calculator.add_number(n)
        self.update_display()


    def run(self):
        self.main_window.show()
        sys.exit(self.app.exec_())

    def log(self,content):
        try:
            print(content)
        except:
            pass
        return



if __name__ == "__main__":
    calc_app = Calculator()
    calc_app.run()