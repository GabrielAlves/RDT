s = "kiro"
s = "gabriel"
s = "00000001"
bit_trocado = "0" if s[-1] == "1" else "1"
s = s[:-1] + bit_trocado
print(s)