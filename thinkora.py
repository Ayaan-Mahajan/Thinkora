import json
from datetime import datetime

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

def decision_scorer():

    print("\n===== DECISION SCORER =====")

    num_criteria = int(input("How many criteria do you want to evaluate? "))

    criteria = []

    for i in range(num_criteria):
        criterion = input(f"Enter Criterion {i+1}: ")
        weight = int(input(f"Importance of {criterion} (1-5): "))

        criteria.append((criterion, weight))

    print("\nYour Criteria:")

    for criterion, weight in criteria:
        print(f"{criterion}: Importance {weight}")
    num_options = int(input("\nHow many options are you comparing? "))

    for i in range(num_options):
        option_name = input(f"\nEnter Option {i+1}: ")

        total_score = 0

        for criterion, importance in criteria:
            score = int(
                   input(
                           f"Rate {option_name} for {criterion} (1-5): "
                    )
             )
            total_score += score * importance
        print(f"{option_name}: Final Score = {total_score}")

def evaluate_decision():
    print("\n===== EVALUATE DECISION =====")
    try:
        
        with open("decisions.json", "r") as file:
            decisions = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        print("No decisions found.")
        return

    if len(decisions) == 0:
        print("No decisions found.")
        return

    print("\nSelect a Decision:")

    for index, decision in enumerate(decisions, start=1):
        print(f"{index}. {decision['Title']}")

    choice = int(input("\nChoose a decision: "))

    selected_decision = decisions[choice - 1]

    print("\nSelected Decision:")
    print(selected_decision["Title"])

    print("\nOptions:")

    for index, option in enumerate(selected_decision["Options"], start=1):
        print(f"{index}. {option}")

    num_criteria = int(
    input("\nHow many criteria matter to you? ")
    )

    criteria = []

    for i in range(num_criteria):
        criterion = input(
              f"Enter Criterion {i+1}: "
         )

        importance = int(
                  input(
                          f"Importance of {criterion} (1-5): "
                  )
        )

        criteria.append((criterion, importance))
    scores = {}

    for option in selected_decision["Options"]:
        print(f"\nEvaluating {option}")

        total_score = 0

        for criterion, importance in criteria:
            score = int(
                   input(
                           f"Rate {option} for {criterion} (1-5): "
                   )
              )

            total_score += score * importance

        scores[option] = total_score
    print("\n===== RESULTS =====")

    for option, score in scores.items():
        print(f"{option}: {score}")

    winner = max(scores, key=scores.get)

    print(f"\n🏆 Recommended Option: {winner}")
    print(f"Score: {scores[winner]}")
    evaluation = {"Date": datetime.now().strftime("%d-%m-%Y %H:%M"), "Winner": winner, "Scores": scores}
    if "Evaluations" not in selected_decision:
        selected_decision["Evaluations"] = []

    selected_decision["Evaluations"].append(evaluation)
    with open("decisions.json", "w") as file:
        json.dump(decisions, file, indent=4)

    print("\nEvaluation saved successfully!")

def view_evaluation_history():

    print("\n===== EVALUATION HISTORY =====")

    try:
        with open("decisions.json", "r") as file:
            decisions = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        print("No decisions found.")
        return

    if len(decisions) == 0:
        print("No decisions found.")
        return

    print("\nSelect a Decision:")

    for index, decision in enumerate(decisions, start=1):
        print(f"{index}. {decision['Title']}")

    try:
        choice = int(input("\nEnter your choice: "))
        if choice < 1 or choice > len(decisions):
            print("Invalid choice.")
            return

    except ValueError:
         print("Please enter a valid number.")
         return

    selected_decision = decisions[choice - 1]

    print("\nSelected Decision:")
    print(selected_decision["Title"])

    if "Evaluations" not in selected_decision:
        print("\nNo evaluations found for this decision.")
        return

    if len(selected_decision["Evaluations"]) == 0:
        print("\nNo evaluations found for this decision.")
        return
    print(f"\nThis decision has been evaluated {len(selected_decision['Evaluations'])} time(s).")

    print("\n===== PAST EVALUATIONS =====")

    for index, evaluation in enumerate(selected_decision["Evaluations"], start=1):
        print(f"\nEvaluation {index}")
        print(f"Date: {evaluation['Date']}")
        print(f"Winner: {evaluation['Winner']}")

        print("\nScores:")

        for option, score in evaluation["Scores"].items():
            print(f"{option}: {score}")

        print("-" * 30)

    if "Final_Choice" in selected_decision:
        print("\n===== FINAL CHOICE =====")
        print(f"Choice: {selected_decision['Final_Choice']}")
        print(f"Date: {selected_decision['Final_Date']}")

    mark_choice = input("\nDo you want to make your final choice? (y/n): ").lower()
    if mark_choice == "y":
        print("\nAvailable Options:")
        for option in selected_decision["Options"]:
            print(f"- {option}")
        final_choice = input( "\nEnter your final choice: ")

        selected_decision["Final_Choice"] = final_choice
        selected_decision["Final_Date"] = datetime.now().strftime("%d-%m-%Y %H:%M")
        with open("decisions.json", "w") as file:
            json.dump(decisions, file, indent=4)
        print("\nFinal choice saved successfully!")

while True:
    print("\n===== THINKORA =====")
    print("1. Add Decision")
    print("2. View Decisions")
    print("3. Evaluate Existing Decision")
    print("4. View Evaluation History")
    print("5. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        add_decision()

    elif choice == 2:
        view_decisions()

    elif choice==3:
        evaluate_decision()

    elif choice == 4:
        view_evaluation_history()

    elif choice == 5:
        print("Thank you for using Thinkora!")
        break

    else:
        print("Invalid choice. Try again.")
