from argon2 import PasswordHasher

ph = PasswordHasher()
hashed = ph.hash("joha123")
print(hashed)
# Verificación
ph.verify(hashed, "joha123")
