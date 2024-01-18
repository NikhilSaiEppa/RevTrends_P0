class StringOperations():
    def __init__(self):
        self.input_string=""

    def getString(self):
        self.input_string=input('Enter The String : ')

    def printString(self):
        upper_case=self.input_string.upper()
        print("The Upper Case of String is : ",upper_case)

def testString():
    String_Operation_Object=StringOperations()
    String_Operation_Object.getString()
    String_Operation_Object.printString()
testString()
    