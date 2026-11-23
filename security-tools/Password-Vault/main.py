
import json
from getpass import getpass

import storage

# Import the cryptographic functions used to protect the vault.
from crypto import (
    generate_salt,
    derive_key,
    encrypt_data,
    decrypt_data,
)

# Import the functions responsible for saving and loading vault data.
from storage import (
    build_vault_data,
    save_vault,
    decode_bytes,
    load_vault,
)

# Import custom exceptions used by the application.
from exceptions import (
    VaultAlreadyExistsError,
    VaultNotFoundError,
)

# Import the secure password generator.
from password_generator import generate_password


def create_vault(master_password: str) -> None:
    """Create a new encrypted vault."""

    # Prevent creating a second vault in the same location.
    if storage.VAULT_PATH.exists():
        raise VaultAlreadyExistsError(
            "Um cofre já existe."
        )

    # Generate a random salt and derive the encryption key.
    salt = generate_salt()
    key = derive_key(master_password, salt)

    # Start the vault with an empty dictionary.
    vault_content = {}

    # Convert the vault dictionary into bytes before encryption.
    plaintext = json.dumps(
        vault_content
    ).encode("utf-8")

    # Encrypt the vault content using the derived key.
    nonce, ciphertext = encrypt_data(
        plaintext,
        key,
    )

    # Build the structure containing the encrypted vault data.
    vault_data = build_vault_data(
        salt,
        nonce,
        ciphertext,
    )

    # Save the encrypted vault to the storage file.
    save_vault(vault_data)


def open_vault(master_password: str) -> dict:
    """Load and decrypt the vault."""

    # Load the encrypted vault data from the storage file.
    vault_data = load_vault()

    # Decode the encrypted values from their stored format.
    salt = decode_bytes(vault_data["salt"])
    nonce = decode_bytes(vault_data["nonce"])
    ciphertext = decode_bytes(
        vault_data["ciphertext"]
    )

    # Derive the encryption key using the master password.
    key = derive_key(
        master_password,
        salt,
    )

    # Decrypt the stored vault content.
    plaintext = decrypt_data(
        nonce,
        ciphertext,
        key,
    )

    # Convert the decrypted bytes back into a dictionary.
    vault_content = json.loads(
        plaintext.decode("utf-8")
    )

    # Ensure that the decrypted content has the expected type.
    if not isinstance(vault_content, dict):
        raise ValueError(
            "Conteúdo do cofre inválido."
        )

    return vault_content


def add_credential(
    vault_content: dict,
    service: str,
    username: str,
    password: str,
) -> dict:
    """Add a credential to the vault dictionary."""

    # Remove unnecessary spaces from the service name.
    service = service.strip()

    # Validate that the service name is not empty.
    if not service:
        raise ValueError(
            "O nome do serviço não pode ficar vazio."
        )

    # Prevent duplicate entries for the same service.
    if service in vault_content:
        raise ValueError(
            "Este serviço já está cadastrado."
        )

    # Store the username and password under the service name.
    vault_content[service] = {
        "username": username,
        "password": password,
    }

    return vault_content


def list_credentials(vault_content: dict) -> list[str]:
    """Return the names of stored services."""

    # Return the service names in alphabetical order.
    return sorted(vault_content.keys())


def get_credential(
    vault_content: dict,
    service: str,
) -> dict:
    """Return a credential for a specific service."""

    # Raise an error if the requested service does not exist.
    if service not in vault_content:
        raise KeyError(
            "Credencial não encontrada."
        )

    # Return the stored username and password.
    return vault_content[service]


def delete_credential(
    vault_content: dict,
    service: str,
) -> dict:
    """Remove a credential from the vault dictionary."""

    # Check whether the requested service exists.
    if service not in vault_content:
        raise KeyError(
            "Credencial não encontrada."
        )

    # Remove the credential from the dictionary.
    del vault_content[service]

    return vault_content


def save_vault_content(
    vault_content: dict,
    master_password: str,
) -> None:
    """Encrypt and save the updated vault content."""

    # Generate a new salt and derive a fresh encryption key.
    salt = generate_salt()
    key = derive_key(
        master_password,
        salt,
    )

    # Serialize the updated dictionary into bytes.
    plaintext = json.dumps(
        vault_content
    ).encode("utf-8")

    # Encrypt the updated vault content.
    nonce, ciphertext = encrypt_data(
        plaintext,
        key,
    )

    # Prepare the encrypted data for storage.
    vault_data = build_vault_data(
        salt,
        nonce,
        ciphertext,
    )

    # Save the encrypted data to the vault file.
    save_vault(vault_data)


def add_credential_to_vault(
    master_password: str,
    service: str,
    username: str,
    password: str,
) -> None:
    """Open the vault, add a credential, and save it."""

    # Decrypt the existing vault content.
    vault_content = open_vault(
        master_password
    )

    # Add the new credential to the dictionary.
    add_credential(
        vault_content,
        service,
        username,
        password,
    )

    # Encrypt and save the updated vault.
    save_vault_content(
        vault_content,
        master_password,
    )


def delete_credential_from_vault(
    master_password: str,
    service: str,
) -> None:
    """Open the vault, remove a credential, and save it."""

    # Decrypt the existing vault content.
    vault_content = open_vault(
        master_password
    )

    # Remove the selected credential.
    delete_credential(
        vault_content,
        service,
    )

    # Encrypt and save the updated vault.
    save_vault_content(
        vault_content,
        master_password,
    )


def show_menu() -> None:
    """Display the main application menu."""

    # Display the available actions in Portuguese.
    print("\n=== COFRE DE SENHAS ===")
    print("1. Adicionar credencial")
    print("2. Listar serviços")
    print("3. Visualizar credencial")
    print("4. Excluir credencial")
    print("5. Gerar senha")
    print("6. Sair")


def run_vault(master_password: str) -> None:
    """Run the vault menu."""

    # Keep displaying the menu until the user chooses to exit.
    while True:
        show_menu()

        # Read the user's menu selection.
        choice = input(
            "Escolha uma opção: "
        ).strip()

        try:
            if choice == "1":
                # Collect the credential information.
                service = input(
                    "Serviço: "
                ).strip()

                username = input(
                    "Usuário: "
                ).strip()

                # Hide the password while the user types it.
                password = getpass(
                    "Senha: "
                )

                # Add the credential and save the vault.
                add_credential_to_vault(
                    master_password,
                    service,
                    username,
                    password,
                )

                print(
                    "Credencial salva com sucesso."
                )

            elif choice == "2":
                # Open the vault and retrieve its services.
                vault_content = open_vault(
                    master_password
                )

                services = list_credentials(
                    vault_content
                )

                # Display a message if the vault has no entries.
                if not services:
                    print(
                        "O cofre está vazio."
                    )
                else:
                    print(
                        "\nServiços cadastrados:"
                    )

                    # Display each stored service.
                    for service in services:
                        print(f"- {service}")

            elif choice == "3":
                # Ask which service the user wants to view.
                service = input(
                    "Nome do serviço: "
                ).strip()

                # Open the vault and retrieve the credential.
                vault_content = open_vault(
                    master_password
                )

                credential = get_credential(
                    vault_content,
                    service,
                )

                # Display the stored username and password.
                print(
                    f"Usuário: {credential['username']}"
                )

                print(
                    f"Senha: {credential['password']}"
                )

            elif choice == "4":
                # Ask which credential should be deleted.
                service = input(
                    "Serviço que deseja excluir: "
                ).strip()

                # Request confirmation before deleting.
                confirmation = input(
                    f"Excluir '{service}'? (s/n): "
                ).strip().lower()

                if confirmation == "s":
                    # Delete the credential and save the vault.
                    delete_credential_from_vault(
                        master_password,
                        service,
                    )

                    print(
                        "Credencial excluída."
                    )
                else:
                    # Cancel the deletion if not confirmed.
                    print(
                        "Exclusão cancelada."
                    )

            elif choice == "5":
                # Ask the user for the desired password length.
                length_input = input(
                    "Tamanho da senha (padrão 20): "
                ).strip()

                # Use 20 characters when no length is provided.
                length = (
                    int(length_input)
                    if length_input
                    else 20
                )

                # Generate and display the new password.
                password = generate_password(
                    length
                )

                print(
                    f"\nSenha gerada: {password}"
                )

            elif choice == "6":
                # Exit the menu and lock the vault.
                print(
                    "Cofre bloqueado. Até logo!"
                )
                break

            else:
                # Handle menu selections that are not available.
                print(
                    "Opção inválida."
                )

        # Handle requests for credentials that do not exist.
        except KeyError:
            print(
                "Credencial não encontrada."
            )

        # Handle invalid values entered by the user.
        except ValueError as error:
            print(
                f"Entrada inválida: {error}"
            )

        # Handle unexpected errors during menu operations.
        except Exception as error:
            from cryptography.exceptions import InvalidTag

            # Detect authentication errors caused by invalid data.
            if isinstance(error, InvalidTag):
                print(
                    "Falha na autenticação do cofre."
                )
            else:
                # Display other unexpected errors.
                print(
                    f"Ocorreu um erro: {error}"
                )


def main() -> None:
    """Start the Password Vault application."""

    # Display the application title.
    print(
        "=== COFRE DE SENHAS ==="
    )

    # Check whether a vault file already exists.
    if not storage.VAULT_PATH.exists():
        print(
            "Nenhum cofre encontrado. Vamos criar um."
        )

        # Ask the user to create and confirm a master password.
        master_password = getpass(
            "Crie sua senha mestra: "
        )

        confirmation = getpass(
            "Confirme sua senha mestra: "
        )

        # Ensure that both passwords match.
        if master_password != confirmation:
            print(
                "As senhas não coincidem."
            )
            return

        # Require a minimum length for the master password.
        if len(master_password) < 12:
            print(
                "Use uma senha mestra com pelo menos "
                "12 caracteres."
            )
            return

        try:
            # Create the encrypted vault.
            create_vault(
                master_password
            )

            print(
                "Cofre criado com sucesso."
            )

            # Open the menu after creating the vault.
            run_vault(
                master_password
            )

        except VaultAlreadyExistsError:
            # Handle the case where a vault already exists.
            print(
                "Já existe um cofre."
            )

        return

    # Ask for the master password when a vault already exists.
    master_password = getpass(
        "Senha mestra: "
    )

    try:
        # Attempt to decrypt the vault using the password.
        open_vault(
            master_password
        )

        print(
            "Cofre desbloqueado."
        )

        # Start the menu after successful authentication.
        run_vault(
            master_password
        )

    except VaultNotFoundError:
        # Handle a missing vault file.
        print(
            "O arquivo do cofre não foi encontrado."
        )

    except Exception as error:
        from cryptography.exceptions import InvalidTag

        # Detect an incorrect password or corrupted data.
        if isinstance(error, InvalidTag):
            print(
                "Senha mestra incorreta "
                "ou cofre corrompido."
            )
        else:
            # Display any other error during vault opening.
            print(
                f"Não foi possível abrir o cofre: {error}"
            )


# Run the application only when this file is executed directly.
if __name__ == "__main__":
    main()
