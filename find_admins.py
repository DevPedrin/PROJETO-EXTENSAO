import sqlite3

try:
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("SELECT username, email, is_superuser, is_staff, tipo_usuario FROM accounts_user")
    users = cur.fetchall()
    print("\n--- Usuários Cadastrados ---")
    for user in users:
        username, email, is_superuser, is_staff, tipo_usuario = user
        status = []
        if is_superuser: status.append("Superuser")
        if is_staff: status.append("Staff")
        status.append(tipo_usuario)
        print(f"Usuário: {username} | Email: {email} | Nível: {', '.join(status)}")
    print("----------------------------\n")
except Exception as e:
    print("Erro ao ler o banco de dados:", e)
