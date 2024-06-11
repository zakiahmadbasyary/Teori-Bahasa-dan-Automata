import re

class ValidasiEmail:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = 'start'
        self.bagian_lokal = ''
        self.bagian_domain = ''
        self.bagian_TDL =''
        self.valid=True

    def prosesDFA(self, symbol):
        if self.state == 'start':
            if re.match(r'[a-zA-Z0-9._%+-]', symbol):
                self.state = 'local'
                self.bagian_lokal += symbol
            else:
                self.valid =False

        elif self.state == 'local':
            if symbol == '@':
                if self.bagian_lokal:  
                    self.state = 'at'
            elif re.match(r'[a-zA-Z0-9._%+-]', symbol):
                self.bagian_lokal += symbol
            else:
                self.valid =False 

        elif self.state == 'at':
            if re.match(r'[a-z0-9]', symbol):
                self.state = 'domain'
                self.bagian_domain += symbol
            else:
                self.valid =False

        elif self.state == 'domain':
            if re.match(r'[a-z0-9]', symbol):
                self.bagian_domain += symbol
            elif symbol == '.': 
                self.state = 'dot'
            else:
               self.valid =False 

        elif self.state =='dot':
            if re.match(r'[a-zA-Z]', symbol):
                self.state="TLD"
                self.bagian_TDL += symbol
            else:
                self.valid =False 
        
        elif self.state =='TLD':
            if re.match(r'[a-zA-Z.]', symbol):
                self.bagian_TDL += symbol
                self.valid=True
            else:
                self.valid=True

    def prosesInput(self, input):
        self.reset()
        for symbol in input:
            if(self.valid):
                self.prosesDFA(symbol)
        return (self.state == 'TLD' and self.valid )

# Inisialisasi DFA Email Validator
dfa = ValidasiEmail()


email_pengguna = input("Masukkan Email yang akan divalidasi: ")
alamat_email=[]
alamat_email.append(email_pengguna)

for email in alamat_email:
    if dfa.prosesInput(email):
        print(f"Alamat email '{email}' valid")
    else:
        print(f"Alamat email '{email}' tidak valid")
        print(f"Email Valid : Bagian_lokal@bagian_domain.bagian_TDL")
