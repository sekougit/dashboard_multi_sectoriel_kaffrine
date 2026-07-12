from utils.google_users import hash_password

password = input("Mot de passe : ")

print("\nHash :")
print(hash_password(password))