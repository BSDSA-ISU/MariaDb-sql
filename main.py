# Semi working main.py, love from Koishi Komeiji

from lib.libraries import SqlServer

sql: SqlServer = SqlServer()

def main():
    while True:
        print("1. input")
        print("2. Delete")
        print("3. Edit")
        print("4. Search")
        print("5. Showall")
        print("6. exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("inserting..\n")

            terminater = True

            while terminater:
                username = input("enter username/email\n>>")
                website = input("enter website\n>>")
                password = input("enter password\n>>")

                sql.insert(username=username, password=password, website=website)

                sql.results(username, password, website)

                x = str(input("success.. you want to enter again(y/n)?"))

                if x.upper() == "Y":
                    continue
                else:
                    terminater = False


        elif choice == '2':
            print("Delete entry row using unique id. warining: This is dangerous and there's no undo button...\n")

            Terminator = True

            while Terminator:
                print("\nList of all passwords:")
                sql.showall()

                try:
                    id = int(input("Enter a row id to delete(type nothing to exit)\n>>"))

                    sql.delete(id)

                except Exception:
                    print("exiting...")

                x = input("want to delete another entry?")

                if x.upper() == 'Y':
                    Terminator = True
                else:
                    Terminator = False

        elif choice == '3':
            sql.showall()
            id = int(input("\nChoose the id to edit\n>>"))

            print("\ninput. Enter provided fields. leave blank so it will not change\n")
            username = input("enter username/email\n>>")
            website = input("enter website\n>>")
            password = input("enter password\n>>")

            if username == "":
                username = None
            if password == "":
                password = None
            if website == '':
                password = None

            sql.edit(id=id, username=username, password=password, website=website)

        elif choice == '4':
            print("Search saved password using a website\n")
            query = input("search query\n>>")
            sql.search(search=query)

        elif choice == '5':
            sql.showall()

        elif choice == '6':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()