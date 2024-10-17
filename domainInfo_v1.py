import socket       #socket module, which provides access to the BSD socket interface, enabling network communication
import re           #provides regular expression matching operations similar to those found in Perl
import csv          #to work with csv 


#function to check if the domain is valid
def is_valid_domain(domain: str) -> bool:
    """Check if the provided domain is valid."""
    regex = r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$'
    return re.match(regex, domain) is not None


#function which perform the lookup and return the reponse
def lookup(domain: str):
    """Perform a WHOIS lookup for the given domain."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("whois.iana.org", 43))
    s.send(f"{domain}\r\n".encode())
    response = s.recv(4096).decode()
    s.close()
    return response




#main function where we are getting input, checking the domain, getting information, and displaying
def main():

    #getting domain name to search
    domain = input("Enter a domain to lookup (e.g., google.com): ").strip()

    #checking if the domain name is valid
    if not is_valid_domain(domain):
        print("Invalid domain format. Please enter a valid domain.")
        return
    
    #looking up the domain and saving the response
    response = lookup(domain)
    print(response)

    choice = int(input(" DO you want to save it to text?\n 1. for Yes\n 2. for NO\n :"))
    if choice == 1:
        filename = input("Enter a name for the file:")
        f = open(f"{filename}.txt","w")
        f.write(response)
        f.close()
        print(f"The output of {domain} is saved to {filename}.txt" )
    else:
        print("Thanks for using our search program...")


if __name__ == "__main__":
    main()