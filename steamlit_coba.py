import re
import streamlit as st

class ValidasiEmail:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = 'mulai'
        self.bagian_lokal = ''
        self.bagian_domain = ''
        self.bagian_TLD = ''
        self.valid = True

    def prosesDFA(self, simbol):
        if self.state == 'mulai':
            if re.match(r'[a-zA-Z0-9._%+-]', simbol):
                self.state = 'lokal'
                self.bagian_lokal += simbol
            else:
                self.valid = False

        elif self.state == 'lokal':
            if simbol == '@':
                if self.bagian_lokal:  
                    self.state = 'at'
            elif re.match(r'[a-zA-Z0-9._%+-]', simbol):
                self.bagian_lokal += simbol
            else:
                self.valid = False 

        elif self.state == 'at':
            if re.match(r'[a-z0-9]', simbol):
                self.state = 'domain'
                self.bagian_domain += simbol
            else:
                self.valid = False

        elif self.state == 'domain':
            if re.match(r'[a-z0-9]', simbol):
                self.bagian_domain += simbol
            elif simbol == '.': 
                self.state = 'dot'
            else:
                self.valid = False 

        elif self.state == 'dot':
            if re.match(r'[a-zA-Z]', simbol):
                self.state = "TLD"
                self.bagian_TLD += simbol
            else:
                self.valid = False 
        
        elif self.state == 'TLD':
            if re.match(r'[a-zA-Z.]', simbol):
                self.bagian_TLD += simbol
                self.valid = True
            else:
                self.valid = False

    def prosesInput(self, masukan):
        self.reset()
        for simbol in masukan:
            if self.valid:
                self.prosesDFA(simbol)
        return self.state == 'TLD' and self.valid

# Inisialisasi DFA Validasi Email
dfa = ValidasiEmail()

# Kode Streamlit
st.title("Validator Email")
st.subheader("Email yang valid yaitu : ")
st.text("lokal@domain.TopLevelDomain")
st.text("1. Bagian Lokal dapat berisi huruf alphabet a-z atau A-Z, dan juga dapat berisi angka, dan simbol _ % - + .")
st.text("2. Setelah bagian lokal harus terdapat at (@)")
st.text("3. Bagian Domain dapat berisi huruf alphabet a-z atau A-Z, dan juga dapat berisi angka, dan simbol _ % - + .")
st.text("4. Setelah bagain domain, harus diikuti dengan dot (.)")
st.text("5. Bagian Top Level Domain dapat berisi huruf alphabet a-z atau A-Z, dan simbol titik(.)")
st.text("6. Email yang valid harus berurutan")
st.subheader("Contoh: ")
st.text("zakibasyary@gmail.com")
email_pengguna = st.text_input("Masukkan Email yang akan divalidasi:")

if email_pengguna:
    if dfa.prosesInput(email_pengguna):
        st.success(f"Alamat email '{email_pengguna}' valid")
    else:
        st.error(f"Alamat email '{email_pengguna}' tidak valid")
        st.info("Format Email Valid : bagian_lokal@bagian_domain.bagian_TLD")
