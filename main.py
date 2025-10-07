import string #import string module to use string.punctuation
import random # import random module to use random.choice
import hashlib # import hashlib module to use hashlib.sha256
import requests # import requests module to use requests.get
#function to print hello world
def main():
    print("Hello from my password hardening app !")
#function to get dictionary from github this github projects updates the list of comoon o pwned passwords
def getdic():
    try:
        response = requests.get("https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/Language-Specific/Spanish_Pwdb_common-password-list-top-150.txt")
        if(response.status_code == 200): #check if the request was successful
            return response.text 
        else:
            print(f"Error: Unable to fetch file. Status code: {response.status_code}") #print error message if the request was not successful
            return None
    except requests.exceptions.RequestException as e: #catch any exceptions that may occur during the request
        print(f"Error: {e}")
        return None
#function to get hash from user and check if it exists in dictionary
def getcrypted(hash): 
    dictionary_content = getdic() #get dictionary from github
    if dictionary_content:
        dictionary = dictionary_content.splitlines() #split dictionary into lines
        for password in dictionary: #for each password in dictionary
            newhash = hashlib.sha256(password.encode()).hexdigest() #get hash of password
            if(newhash == hash): #check if hash is equal to hash from user
                return "decrypted password: " + password 
    return "password doesn't exist in dictionary" 
#function to check if password is secure
def spcheck(pwd):
    result = True #set result to true by default
    reason = "" #set reason to empty string by default
    if(len(pwd) < 8): #check if password is less than 8 characters
        result = False #set result to false if password is less than 8 characters
        reason += "contraseña corta\n" #add the reason of why the password is not secure
    if ( not(any(c.islower() for c in pwd))): #check if password has at least one lowercase character
        result = False
        reason += "contraseña sin minusculas\n"
    if (not(any(c.isdigit() for c in pwd))): #check if password has at least one digit
        result = False
        reason += "contraseña sin numeros\n" 
    if (not(any(c in string.punctuation for c in pwd))): #check if password has at least one special character
        result = False
        reason += "contraseña sin caracteres especiales\n"
    if (not(any(c.isupper() for c in pwd))): #check if password has at least one uppercase character
        result = False
        reason += "contraseña sin mayusculas\n"
    if(result): #check if password is still secure or if changed to false before
        reason = "contraseña segura" 
    print(reason)#print reason of why the password is not secure
    return result
#function to generate secure password with a custom lenght         
#TODO: add a dictory in the check secure password to be sure that we are don't getting a unsafe password
def genpass():
    psize = 7 #set password size to 7 by default
    while psize < 8: #check if password size is less than 8
        psize = int(input("tamaño de la contraseña a generar (minimo 8): ")) #get password size from user till he chose a safe size
    chars = string.ascii_letters + string.digits + string.punctuation #set characters to use in password
    securepass = False #set securepass to false by default
    while not securepass: #loop the generation of password till the password were secure
        contraseña = ''.join(random.choice(chars) for i in range(psize)) #generate password
        if (any(c.islower() for c in contraseña) 
            and any(c.isupper() for c in contraseña)  
            and sum(c.isdigit() for c in contraseña) >= 2
            and any(c in string.punctuation for c in contraseña)): #check if password is secure
                securepass = True 
    return contraseña 

if __name__ == "__main__":
    #print(spcheck(input("type the password to check: ")))
    #print(genpass()) 
    #print(getdic())
    print(getcrypted(input("type the hash to decrypt: ")))
