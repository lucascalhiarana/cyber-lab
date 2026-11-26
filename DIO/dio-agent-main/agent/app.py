import sqlite3

DB_PATH = "banco_de_dados.db"


def fazer_login(usuario: str, senha: str) -> str:
        """Autentica um usuário sem interpretar os valores como SQL."""
        if not isinstance(usuario, str) or not isinstance(senha, str):
            return "Acesso Negado."

        try:
            conexao = sqlite3.connect(DB_PATH)
            try:
                cursor = conexao.execute(
                    "SELECT 1 FROM usuarios "
                    'WHERE username = ? AND "password" = ? LIMIT 1',
                    (usuario, senha),
                )
                autenticado = cursor.fetchone() is not None
            finally:
                conexao.close()
        except sqlite3.Error:
            # Falha fechada sem expor detalhes internos do banco ao usuário.
            return "Acesso Negado."

        return "Acesso Permitido!" if autenticado else "Acesso Negado."
