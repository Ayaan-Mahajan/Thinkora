import json

def add_decision():
    title = input("Decision Title: ")
    deadline = input("Deadline: ")
    importance = input("Importance (Low/Medium/High): ")
    options = []

    num_options = int(input("How many options do you want to add? "))

    for i in range(num_options):
        option = input(f"Enter Option {i+1}: ")
        options.append(option)

    new_decision = {
    "Title": title,
    "Deadline": deadline,
    "Importance": importance,
    "Options": options
     }

    try:
        with open("decisions.json", "r") as file:
               decisions = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        decisions = []

    decisions.append(new_decision)

    with open("decisions.json", "w") as file:
        json.dump(decisions, file, indent=4)

    print("\nDecision saved successfully! ")

def view_decisions():

    try:
        with open("decisions.json", "r") as file:
            decisions = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        print("\nNo decisions found.")
        return

    if len(decisions) == 0:
        print("\nNo decisions found.")
        return

    print("\n===== YOUR DECISIONS =====")

    for index, decision in enumerate(decisions, start=1):

        print(f"\nDecision #{index}")

        print("Title:", decision["Title"])
        print("Deadline:", decision["Deadline"])
        print("Importance:", decision["Importance"])

        print("Options:")

        for option in decision["Options"]:
            print("-", option)

while True:
    print("\n===== THINKORA =====")
    print("1. Add Decision")
    print("2. View Decisions")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_decision()

    elif choice == "2":
        view_decisions()

    elif choice == "3":
        print("Thank you for using Thinkora!")
        break

    else:
        print("Invalid choice. Try again.")
