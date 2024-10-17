import socket
import re
import csv

#checking if domain name is valid
def is_valid_domain(domain: str) -> bool:
    """Check if the provided domain is valid."""
    regex = r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$'
    return re.match(regex, domain) is not None

#getting information about domain
def lookup(domain: str) -> str:
    """Perform a WHOIS lookup for the given domain."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("whois.iana.org", 43))
            s.send(f"{domain}\r\n".encode())
            response = s.recv(4096).decode()
        return response
    except socket.error as e:
        return f"Error connecting to WHOIS server: {e}"

#getting Ip address
def get_ip_address(domain: str) -> str:
    """Get the IP address for the given domain."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror as e:
        return f"Error resolving domain: {e}"

#saving to text file
def save_to_txt(filename: str, content: str) -> None:
    """Save the content to a text file."""
    try:
        with open(f"{filename}.txt", "w") as file:
            file.write(content)
        print(f"The output is saved to {filename}.txt")
    except IOError as e:
        print(f"Error saving to file: {e}")

def save_to_csv(filename: str, domain: str, ip_address: str, whois_response: str) -> None:
    """Save the domain information to a CSV file."""
    try:
        with open(f"{filename}.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Domain", "IP Address", "WHOIS Response"])
            writer.writerow([domain, ip_address, whois_response])
        print(f"The output is saved to {filename}.csv")
    except IOError as e:
        print(f"Error saving to CSV: {e}")

def main():
    while True:
        domain = input("Enter a domain to lookup (e.g., google.com): ").strip()
        
        if not is_valid_domain(domain):
            print("Invalid domain format. Please enter a valid domain.")
            continue
        
        print(f"\nDomain name is : {domain}")

        ip_address = get_ip_address(domain)
        print(f"IP Address: {ip_address}\n")

        response = lookup(domain)
        print("Search Response:")
        print(response)

        while True:
            try:
                choice = int(input("Do you want to save it?\n1. Save to text file\n2. Save to CSV\n3. No\n: "))
                if choice == 1:
                    filename = input("Enter a name for the text file: ").strip()
                    save_to_txt(filename, response)
                    break
                elif choice == 2:
                    filename = input("Enter a name for the CSV file: ").strip()
                    save_to_csv(filename, domain, ip_address, response)
                    break
                elif choice == 3:
                    break
                else:
                    print("Please enter 1, 2, or 3.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Ask the user if they want to lookup another domain
        another = input("\nDo you want to lookup another domain? (yes/no): ").strip().lower()
        if another != 'yes':
            print("Thanks for using our search program...")
            break

if __name__ == "__main__":
    main()
