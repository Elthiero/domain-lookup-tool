import socket
import re
import csv
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Check if the domain name is valid
def is_valid_domain(domain: str) -> bool:
    """Check if the provided domain is valid."""
    regex = r'^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$'
    return re.match(regex, domain) is not None

# Getting information about the domain
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

# Getting IP address
def get_ip_address(domain: str) -> str:
    """Get the IP address for the given domain."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror as e:
        return f"Error resolving domain: {e}"

# Saving to text file
def save_to_txt(filename: str, content: str) -> None:
    """Save the content to a text file."""
    try:
        with open(f"{filename}.txt", "w") as file:
            file.write(content)
        messagebox.showinfo("Saved", f"The output is saved to {filename}.txt")
    except IOError as e:
        messagebox.showerror("Error", f"Error saving to file: {e}")

# Saving to CSV file
def save_to_csv(filename: str, domain: str, ip_address: str, whois_response: str) -> None:
    """Save the domain information to a CSV file."""
    try:
        with open(f"{filename}.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Domain", "IP Address", "WHOIS Response"])
            writer.writerow([domain, ip_address, whois_response])
        messagebox.showinfo("Saved", f"The output is saved to {filename}.csv")
    except IOError as e:
        messagebox.showerror("Error", f"Error saving to CSV: {e}")

# Perform lookup and update results in the text area
def perform_lookup():
    domain = domain_entry.get().strip()
    
    if not is_valid_domain(domain):
        messagebox.showerror("Invalid Domain", "Please enter a valid domain.")
        return
    
    ip_address = get_ip_address(domain)
    response = lookup(domain)
    
    # Display results
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Domain: {domain}\n")
    result_text.insert(tk.END, f"IP Address: {ip_address}\n")
    result_text.insert(tk.END, "Search Response:\n")
    result_text.insert(tk.END, response)

# Save results based on user's choice
def save_results():
    domain = domain_entry.get().strip()
    if not domain:
        messagebox.showwarning("No Domain", "Please perform a lookup before saving.")
        return

    choice = save_choice.get()
    if choice == 1:
        filename = f"{domain}"
        save_to_txt(filename, result_text.get(1.0, tk.END))
    elif choice == 2:
        filename = f"{domain}"
        save_to_csv(filename, domain, get_ip_address(domain), result_text.get(1.0, tk.END))

# Setting up the GUI
app = tk.Tk()
app.title("Domain Lookup Tool")

# Domain entry
tk.Label(app, text="Enter Domain:").pack(pady=5)
domain_entry = tk.Entry(app, width=60)
domain_entry.pack(pady=5)

# Lookup button
lookup_button = tk.Button(app, text="Lookup Domain", command=perform_lookup)
lookup_button.pack(pady=10)

# Text area for results
result_text = scrolledtext.ScrolledText(app, width=70, height=25)
result_text.pack(pady=10)

# Save options
save_choice = tk.IntVar()
tk.Radiobutton(app, text="Save to text file", variable=save_choice, value=1).pack(anchor=tk.W)
tk.Radiobutton(app, text="Save to CSV file", variable=save_choice, value=2).pack(anchor=tk.W)

# Save button
save_button = tk.Button(app, text="Save Results", command=save_results)
save_button.pack(pady=10)

# Start the GUI event loop
app.mainloop()
