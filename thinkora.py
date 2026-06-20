import json
from datetime import datetime

def invalid_choice():
    print("Invalid choice.")

##########################################
# DECISION MANAGEMENT
##########################################
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
    "Options": options,
    "Evaluations": [],
    "Reflections": []
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

##########################################
# EVALUATIONS
##########################################
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
    if "Reflections" not in selected_decision:
        selected_decision["Reflections"] = []

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
    evaluation = {"Date": datetime.now().strftime("%d-%m-%Y %H:%M"), "Winner": winner, "Scores": scores, "Criteria": criteria}
    if "Evaluations" not in selected_decision:
        selected_decision["Evaluations"] = []

    selected_decision["Evaluations"].append(evaluation)
    with open("decisions.json", "w") as file:
        json.dump(decisions, file, indent=4)

    print("\nEvaluation saved successfully!")
    add_reflection = input(
    "\nWould you like to add a reflection? (y/n): "
    ).lower()
    if add_reflection == "y":
        reflection = input("\nEnter your reflection: ")
        selected_decision["Reflections"].append(
               {
                       "Date": datetime.now().strftime("%d-%m-%Y %H:%M"),
                       "Note": reflection
                }
           )
        with open("decisions.json", "w") as file:
            json.dump(decisions, file, indent=4)
        print("\nReflection saved successfully!")

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
            invalid_choice()
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

##########################################
# REFLECTIONS
##########################################
def view_reflections():

    print("\n===== VIEW REFLECTIONS =====")

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
    if "Reflections" not in selected_decision:
        selected_decision["Reflections"] = []
    if len(selected_decision["Reflections"]) == 0:
        print("\nNo reflections found.")
        return
    print("\n===== REFLECTIONS =====")
    print(f"\nDecision: {selected_decision['Title']}")
    for index, reflection in enumerate(selected_decision["Reflections"], start=1):
        print(f"\nReflection {index}")
        print(f"Date: {reflection['Date']}")
        print("Note:")
        print(reflection["Note"])
        print("\n" + "-" * 40)

##########################################
# ANALYTICS
##########################################
def decision_analytics():

    print("\n===== DECISION ANALYTICS =====")
    try:
        with open("decisions.json", "r") as file:
            decisions = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        print("No decisions found.")
        return

    if len(decisions) == 0:
        print("No decisions found.")
        return
    total_decisions = len(decisions)
    total_evaluations = 0
    total_reflections = 0
    final_choices = 0
    for decision in decisions:
        if "Evaluations" in decision:
            total_evaluations += len(decision["Evaluations"])
        if "Reflections" in decision:
            total_reflections += len(decision["Reflections"])
        if "Final_Choice" in decision:
            final_choices += 1
    if total_decisions > 0:
        average_evaluations = (total_evaluations / total_decisions)
    else:
        average_evaluations = 0
    print(f"\nTotal Decisions: {total_decisions}")

    print(
        f"Total Evaluations: {total_evaluations}"
    )

    print(
        f"Total Reflections: {total_reflections}"
    )

    print(
        f"Final Choices Made: {final_choices}"
    )

    print(
        f"Average Evaluations per Decision: "
        f"{average_evaluations:.2f}"
    )
    
def decision_patterns():
    final_choices=0
    high_importance_decisions = 0
    high_importance_reflections = 0
    high_importance_evaluations = 0
    high_importance_final_choices = 0
    print("\n===== DECISION PATTERNS =====")
    try:
        with open("decisions.json", "r") as file:
            decisions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No decisions found.")
        return
    if len(decisions) == 0:
        print("No decisions found.")
        return
    total_evaluations = 0
    reflected_decisions = 0
    total_decisions = len(decisions)
    for decision in decisions:
        if "Evaluations" in decision:
            total_evaluations += len(decision["Evaluations"])
        if ("Reflections" in decision and len(decision["Reflections"]) > 0):
            reflected_decisions += 1
        if "Final_Choice" in decision:
            final_choices += 1
        if decision["Importance"] == "High":
            high_importance_decisions += 1

            if "Evaluations" in decision:
                high_importance_evaluations += len(decision["Evaluations"])
            if ("Reflections" in decision and len(decision["Reflections"]) > 0):
                high_importance_reflections += 1
            if "Final_Choice" in decision:
                high_importance_final_choices += 1
                
    average_evaluations = ( total_evaluations / total_decisions)
    if average_evaluations >= 3:
        decision_style = "Analytical Thinker"
    elif reflected_decisions >= (total_decisions / 2):
        decision_style = "Reflective Thinker"
    elif average_evaluations <= 1:
        decision_style = "Fast Decider"
    else:
        decision_style = "Balanced Thinker"
    print(
           f"\n[Decision Style]\n "
           f"{decision_style}"
    )
    if average_evaluations <= 1:
        confidence_pattern = ("You generally trust your initial judgment.")
    elif average_evaluations <= 3:
        confidence_pattern = ("You usually seek some reassurance before deciding.")
    else:
        confidence_pattern = ("You often revisit decisions to gain certainty before committing.")
    print(
           f"\n[Confidence Pattern]\n"
           f"{confidence_pattern}"
    )
    commitment_rate = (final_choices / total_decisions) * 100
    if commitment_rate >= 75:
        commitment_pattern = ("You usually follow through and commit to your decisions.")
    elif commitment_rate >= 40:
        commitment_pattern = ("You finalize some decisions while leaving others open." )
    else:
        commitment_pattern = ("You often keep your options open and delay commitment.")
    print(
           f"\n[Commitment Pattern]\n"
           f"{commitment_pattern}"
     )

    print(
           f"Commitment Rate: "
           f"{commitment_rate:.2f}%"
     )
    reflection_rate = (reflected_decisions / total_decisions) * 100
    if reflection_rate >= 70:
        self_awareness = ("High")
    elif reflection_rate >= 40:
        self_awareness = ("Moderate")
    else:
        self_awareness = ("Developing")
    print("\n[Self-Awareness Level]")
    print(
           f"{self_awareness}"
    )

    print(
           f"Reflection Rate: "
          f"{reflection_rate:.2f}%"
     )
    if high_importance_decisions == 0:
        major_detector = ("You haven't recorded any High Importance decisions yet.")
    else:
        avg_high_evaluations = (high_importance_evaluations / high_importance_decisions)
        high_reflection_rate = (high_importance_reflections / high_importance_decisions ) * 100
        high_commitment_rate = (high_importance_final_choices / high_importance_decisions ) * 100
        if avg_high_evaluations >= 3:
            major_detector = ("You spend extra time evaluating major decisions before committing.")
        elif high_reflection_rate >= 50:
            major_detector = ("You often reflect deeply on important life choices.")
        elif high_commitment_rate >= 75:
            major_detector = ("You trust yourself and commit confidently to major decisions.")
        else:
            major_detector = ("You approach major decisions thoughtfully while balancing action and reflection.")
    print("\n[Major Decision Detector]")
    print(major_detector)

    if (decision_style == "Analytical Thinker" and reflection_rate >= 50):
        personalized_insight = (
                "You are highly reflective and analytical. "
                "You invest significant effort into understanding "
                "important choices before acting."
         )
    elif (decision_style == "Fast Decider" and commitment_rate < 50):
        personalized_insight = (
                "You tend to trust your instincts while keeping "
                "options open. You may benefit from committing "
                "more confidently once you've made a choice."
        )
    elif (decision_style == "Balanced Thinker" and commitment_rate >= 50):
        personalized_insight = (
                "You balance thought and action well. "
                "You reflect on experiences and usually "
                "commit once you feel prepared."
        )
    else:
        personalized_insight = (
                "You may benefit from trusting yourself more often. "
                "Your tendency to revisit major decisions suggests "
                "a desire for certainty before acting."
        )
    print("\n[Thinkora Insight]")
    print(personalized_insight)

def top_priorities():

    print("\n===== TOP PRIORITIES =====")
    try:
        with open("decisions.json", "r") as file:
            decisions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No decisions found.")
        return
    if len(decisions) == 0:
        print("No decisions found.")
        return
    priority_counts = {}
    for decision in decisions:
        if "Evaluations" in decision:
            for evaluation in decision["Evaluations"]:
                if "Criteria" in evaluation:
                    for criterion, importance in evaluation["Criteria"]:
                        if criterion not in priority_counts:
                            priority_counts[criterion] = 0
                        priority_counts[criterion] += 1
    print()
    for criterion, count in priority_counts.items():
        if count == 1:
            print(f"{criterion}: {count} time")
        else:
            print(f"{criterion}: {count} times")

    most_valued = max(priority_counts, key=priority_counts.get)
    print("\nMost Valued Criterion:")
    print(most_valued)

def recommendation_trust():
    print("\n===== RECOMMENDATION TRUST =====")
    try:
        with open("decisions.json", "r") as file:
            decisions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No decisions found.")
        return
    if len(decisions) == 0:
        print("No decisions found.")
        return
    recommendations_followed = 0
    recommendations_ignored = 0
    for decision in decisions:
        total_recommendations = ( recommendations_followed + recommendations_ignored)
        if ("Final_Choice" in decision and "Evaluations" in decision and len(decision["Evaluations"]) > 0):
            latest_evaluation = decision["Evaluations"][-1]
            recommended_option = latest_evaluation["Winner"]
            final_choice = decision["Final_Choice"]
            if recommended_option == final_choice:
                recommendations_followed += 1
            else:
                recommendations_ignored += 1
    if total_recommendations == 0:
        print("No finalized decisions with recommendations found.")
        return
    else:
        trust_score = ( recommendations_followed / total_recommendations) * 100
    print(
           f"\nRecommendations Followed: "
           f"{recommendations_followed}"
    )

    print(
           f"Recommendations Ignored: "
           f"{recommendations_ignored}"
    )

    print(
            f"\nTrust Score: "
            f"{trust_score:.2f}%"
    )

def overthinking_detector():

    print("\n===== OVERTHINKING DETECTOR =====")
    try:
        with open("decisions.json", "r") as file:
            decisions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No decisions found.")
        return
    if len(decisions) == 0:
        print("No decisions found.")
        return
    overthinking_detected = False
    for decision in decisions:
        if "Evaluations" in decision:
            evaluation_count = len(decision["Evaluations"])
            if evaluation_count >= 5:
                print(
                       f"\nDecision: "
                       f"{decision['Title']}" )

                print(
                       f"Evaluations: "
                       f"{evaluation_count}" )

                print(
                       "\n⚠️ Thinkora Insight:")

                print(
                       "You may be seeking certainty "
                       "rather than clarity.")

                print(
                       "Consider whether additional "
                       "evaluations would truly "
                       "change your outcome.")
                overthinking_detected = True
            elif evaluation_count >= 3:
                print(
                f"\nDecision: "
                f"{decision['Title']}")

                print(
                f"Evaluations: "
                f"{evaluation_count}")

                print(
                "\n🤔 Thinkora Insight:")

                print(
                "You approach this decision "
                "carefully before committing.")
                overthinking_detected = True
            elif evaluation_count >= 1:
                print(
                f"\nDecision: "
                f"{decision['Title']}")

                print(
                f"Evaluations: "
                f"{evaluation_count}")

                print(
                "\n✅ Thinkora Insight:")

                print(
                "You explored your options "
                "without getting stuck in "
                "analysis.")
                overthinking_detected = True
    if overthinking_detected == False:
        print("No evaluated decisions found.")

def decision_growth():

    print("\n===== DECISION GROWTH INSIGHTS =====")
    try:
        with open("decisions.json", "r") as file:
            decisions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No decisions found.")
        return
    if len(decisions) == 0:
        print("No decisions found.")
        return
    reflected_decisions = 0
    finalized_decisions = 0
    total_evaluations = 0
    recommendations_followed = 0
    recommendations_total = 0
    for decision in decisions:
        if ("Reflections" in decision and len(decision["Reflections"]) > 0):
            reflected_decisions += 1
        if "Evaluations" in decision:
            total_evaluations += len(decision["Evaluations"])
        if "Final_Choice" in decision:
            finalized_decisions += 1
        if ("Final_Choice" in decision and "Evaluations" in decision and len(decision["Evaluations"]) > 0):
            latest_evaluation = decision["Evaluations"][-1]
            recommendations_total += 1
            if (latest_evaluation["Winner"]== decision["Final_Choice"]):
                recommendations_followed += 1
    if finalized_decisions == 0:
        print("Not enough decision history yet.")
        return
    reflection_rate = (reflected_decisions / len(decisions)) * 100
    avg_evaluations = (total_evaluations / finalized_decisions)
    if recommendations_total > 0:
        trust_rate = (recommendations_followed / recommendations_total) * 100
    else:
        trust_rate = 0
    if reflection_rate >= 50:
        print(
        "\n📝 You regularly reflect on "
        "your decisions and learn "
        "from them.")
    else:
        print(
        "\n📝 You could benefit from "
        "reflecting more often on "
        "important choices." )
    if avg_evaluations <= 2:
        print(
        "⚡ You tend to make decisions "
        "efficiently without excessive "
        "analysis.")
    elif avg_evaluations <= 4:
        print(
        "🤔 You balance careful thinking "
        "with action.")
    else:
        print(
        "🚨 You often spend a lot of time "
        "evaluating before deciding.")
    if trust_rate >= 75:
        print(
        "🤝 You trust your decision "
        "process and commit confidently.")
    elif trust_rate >= 50:
        print(
        "🤝 You sometimes trust your "
        "recommendations while leaving "
        "room for intuition.")
    else:
        print(
        "🤝 You frequently override "
        "recommendations and rely on "
        "personal judgment.")
    print(
    "\n🌱 Thinkora Insight:")
    print(
    "Your decision-making journey "
    "is evolving. Every choice "
    "helps you understand yourself "
    "a little better.")

def record_outcome():

    print("\n===== RECORD DECISION OUTCOME =====")
    try:
        with open("decisions.json", "r") as file:
            decisions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No decisions found.")
        return
    if len(decisions) == 0:
        print("No decisions found.")
        return
    has_evaluated_decision = False
    print("\n===== SELECT A DECISION =====")
    for index, decision in enumerate(decisions, start=1):
        if ("Evaluations" in decision and len(decision["Evaluations"]) > 0):
            has_evaluated_decision = True
        if "Outcome" in decision:
            status = "📝 Outcome Recorded"
        elif "Final_Choice" in decision:
            status = "✓ Finalized"
        elif ("Evaluations" in decision and len(decision["Evaluations"]) > 0 ):
            status = "✓ Evaluated"

        else:
            status = "⚠ Not evaluated"
        print(
        f"{index}. "
        f"{decision['Title']} "
        f"{status}")
    if has_evaluated_decision == False:
        print("No evaluated decisions found.")
        return
    
    choice = int(
    input("\nChoose a decision: "))
    selected_decision = decisions[choice - 1]
    if ("Evaluations" not in selected_decision or len(selected_decision["Evaluations"]) == 0):
        print("\nThis decision hasn't been evaluated yet.")
        return
    if "Outcome" in selected_decision:
        overwrite = input("\nAn outcome already exists. Overwrite? (y/n): ").lower()
        if overwrite != "y":
            print("Outcome not updated.")
            return
        
    print("\nHow do you feel about this decision now?")
    print("1. Very Happy")
    print("2. Mostly Happy")
    print("3. Neutral")
    print("4. Slightly Regretful")
    print("5. Strongly Regretful")
    rating = int(input("\nChoose a rating: "))
    add_note = input("\nWould you like to reflect on this outcome? (y/n): ").lower()
    note = ""
    if add_note == "y":
        if rating <= 2:
            note = input(
            "\nWhat made this decision work out well?\n> " )
        elif rating == 3:
            note = input(
            "\nLooking back, what would you do differently?\n> ")
        else:
            note = input(
            "\nWhat lesson will you carry into future decisions?\n> ")
    outcome = {
    "Date": datetime.now().strftime("%d-%m-%Y %H:%M"),
    "Rating": rating,
    "Note": note}
    selected_decision["Outcome"] = outcome
    with open("decisions.json", "w") as file:
        json.dump( decisions,  file,  indent=4)
    print(
    "\nOutcome recorded successfully!")

def outcome_insights():

    print("\n===== DECISION OUTCOME INSIGHTS =====")
    try:
        with open("decisions.json", "r") as file:
            decisions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No decisions found.")
        return
    if len(decisions) == 0:
        print("No decisions found.")
        return
    satisfied = 0
    neutral = 0
    regretful = 0
    for decision in decisions:
        if "Outcome" in decision:
            rating = decision["Outcome"]["Rating"]

            if rating <= 2:
                satisfied += 1
            elif rating == 3:
                neutral += 1
            else:
                regretful += 1

    total_outcomes = ( satisfied + neutral  + regretful)
    if total_outcomes == 0:
        print(
        "No recorded outcomes found.")
        return
    print(
    f"\nSatisfied Decisions: "
    f"{satisfied}")
    print(
    f"\nNeutral Decisions: "
    f"{neutral}")
    print(
    f"\nRegretful Decisions: "
    f"{regretful}")

    if satisfied >= neutral and satisfied >= regretful:
        print(
        "\n🌟 Thinkora Insight:")
        print(
        "Most of your past decisions "
        "have worked out well." )
        print(
        "You appear to trust your values "
        "and commit to choices that align "
        "with what matters to you." )
        print(
        "Keep balancing reflection "
        "with action.")
    elif neutral >= satisfied and neutral >= regretful:
        print(
        "\n🌱 Thinkora Insight:")
        print(
        "Many of your decisions led "
        "to mixed outcomes." )
        print(
        "You may benefit from identifying "
        "which criteria truly predict "
        "satisfaction for you.")
    else:
        print(
        "\n🧠 Thinkora Insight:")
        print(
        "Several decisions resulted "
        "in regret." )
        print(
        "Consider reflecting more deeply "
        "before committing to future choices.")
        print(
        "Every regret carries a lesson." )

def decision_timeline():

    print("\n===== DECISION TIMELINE =====")
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
        print(
            f"{index}. "
            f"{decision['Title']}"
        )

    choice = int( input("\nChoose a decision: "))
    selected_decision = decisions[ choice - 1  ]
    print(
        f"\nDecision:\n"
        f"{selected_decision['Title']}")
    timeline_events = 0
    if "Evaluations" in selected_decision:
        for index, evaluation in enumerate( selected_decision["Evaluations"], start=1):
            timeline_events += 1  
            if index == 1:
                event = "Evaluated"
            else:
                event = "Re-evaluated"
            print(
            f"\n{evaluation['Date']}")
            print(
            f"→ {event}")
            print(
            f"Winner: "
            f"{evaluation['Winner']}")
            
    if "Reflections" in selected_decision:
        for reflection in selected_decision["Reflections"]:
            timeline_events += 1  
            print(
            f"\n{reflection['Date']}")
            print(
            "→ Reflection")
            print(
            f"\"{reflection['Note']}\"")
            
    if "Final_Choice" in selected_decision:
        timeline_events += 1
        print(
        f"\n{selected_decision['Final_Date']}")
        print(
        "→ Final Choice")
        print(
        f"{selected_decision['Final_Choice']}")
        
    if "Outcome" in selected_decision:
        timeline_events += 1
        outcome = selected_decision["Outcome"]
        print(
        f"\n{outcome['Date']}")
        print(
        "→ Outcome")
        rating = outcome["Rating"]
        if rating == 1:
            feeling = "😁 Very Happy"
        elif rating == 2:
            feeling = "😊 Mostly Happy"
        elif rating == 3:
            feeling = "😐 Neutral"
        elif rating == 4:
            feeling = "😕 Slightly Regretful"
        else:
            feeling = "😔 Strongly Regretful"
        print(feeling)
        if outcome["Note"] != "":
            print(
            "\nOutcome Reflection:")
            print(
            f"\"{outcome['Note']}\"")
    if timeline_events == 0:
        print(
        "\nThis decision has not developed yet.")
        print(
        "Start by evaluating your options "
        "to begin building its timeline." )

def decision_personality():

    print("\n===== YOUR DECISION PROFILE =====")
    try:
        with open("decisions.json", "r") as file:
            decisions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No decisions found.")
        return
    if len(decisions) == 0:
        print("No decisions found.")
        return
    total_evaluations = 0
    evaluated_decisions = 0
    reflections = 0
    finalized = 0
    satisfied = 0
    neutral = 0
    regretful = 0
    recommendations_followed = 0
    recommendations_ignored = 0
    for decision in decisions:
        if ( "Evaluations" in decision and len(decision["Evaluations"]) > 0 ):
            evaluated_decisions += 1
            total_evaluations += len( decision["Evaluations"])
        if "Reflections" in decision:
            reflections += len(decision["Reflections"])
        if "Final_Choice" in decision:
            finalized += 1
            if ("Evaluations" in decision and len(decision["Evaluations"]) > 0):
                latest_winner = decision["Evaluations"][-1]["Winner"]
                if (latest_winner== decision["Final_Choice"]):
                    recommendations_followed += 1
                else:
                    recommendations_ignored += 1
        if "Outcome" in decision:
            rating = decision["Outcome"]["Rating"]
            if rating <= 2:
                satisfied += 1
            elif rating == 3:
                neutral += 1
            else:
                regretful += 1
    if evaluated_decisions > 0:
        average_evaluations = (
        total_evaluations
        / evaluated_decisions)
    else:
        average_evaluations = 0
    if average_evaluations <= 2:
        evaluation_style = "Decisive"
    elif average_evaluations <= 4:
        evaluation_style = "Thoughtful"
    else:
        evaluation_style = "Analytical"

    if finalized > 0:
        reflection_ratio = (
        reflections
        / finalized )
    else:
        reflection_ratio = 0
    if reflection_ratio >= 1:
        reflection_style = "Reflective"
    elif reflection_ratio >= 0.5:
        reflection_style = "Self-aware"
    else:
        reflection_style = "Action-oriented"

    trust_total = (
    recommendations_followed
    + recommendations_ignored)
    if trust_total > 0:
        trust_percentage = (
        recommendations_followed
        / trust_total
    ) * 100
    else:
        trust_percentage = 0
    if trust_percentage >= 80:
        commitment_style = "Conviction Driven"
    elif trust_percentage >= 50:
        commitment_style = "Balanced Explorer"
    else:
        commitment_style = "Independent Thinker"

    if (satisfied >= neutral and satisfied >= regretful):
        outcome_style = ("Optimistic Decision Maker" )
    elif (neutral >= satisfied and neutral >= regretful):
        outcome_style = (
        "Adaptive Learner")
    else:
        outcome_style = (
        "Growth-Seeking Rebuilder")

    print(
    f"\n🧠 Evaluation Style: "
    f"{evaluation_style}")
    print(
    f"🪞 Reflection Style: "
    f"{reflection_style}")
    print(
    f"🎯 Commitment Style: "
    f"{commitment_style}")
    print(
    f"🌱 Outcome Pattern: "
    f"{outcome_style}")

    if ( evaluation_style == "Thoughtful"  and reflection_style == "Reflective"):
        personality = "Reflective Strategist"
    elif ( evaluation_style == "Decisive" and commitment_style == "Conviction Driven"):
        personality = "Confident Executor"
    elif (evaluation_style == "Analytical" and reflection_style == "Reflective"):
        personality = "Insightful Analyst"
    elif (commitment_style == "Independent Thinker"):
        personality = "Independent Pathfinder"
    else:
        personality = "Adaptive Decision Maker"
    print(
    f"\n🏆 Your Thinkora Personality:")
    print(
    f"✨ {personality}")

    print("\nStrengths:")
    if evaluation_style != "Decisive":
        print(
        "✓ You carefully consider your options.")
    if reflection_style == "Reflective":
        print(
        "✓ You actively learn from experience.")
    if commitment_style == "Conviction Driven":
        print(
        "✓ You trust your judgment and commit." )
    if outcome_style == "Optimistic Decision Maker":
        print(
        "✓ Your decisions tend to satisfy you.")

    print("\nWatch Outs:")
    watch_outs = 0
    if evaluation_style == "Analytical":
        print(
        "⚠ Avoid chasing perfect certainty.")
        watch_outs += 1
    if commitment_style == "Independent Thinker":
        print(
        "⚠ Stay open to outside perspectives.")
        watch_outs += 1
    if outcome_style == "Growth-Seeking Rebuilder":
        print(
        "⚠ Be kind to yourself when reflecting on regrets.")
        watch_outs += 1
    if reflection_style == "Action-oriented":
        print(
        "⚠ Consider reflecting more often.")
        watch_outs += 1

    if watch_outs == 0:
        print(
        "✓ No major blind spots detected.")
        print(
        "Continue balancing reflection "
        "with decisive action.")

def regret_pattern_analysis():

    print(
        "\n===== REGRET PATTERN ANALYSIS =====")
    try:
        with open("decisions.json", "r") as file:
            decisions = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(
        "No decisions found.")
        return
    if len(decisions) == 0:
        print(
        "No decisions found.")
        return
    regret_count = 0
    regret_reasons = {}
    for decision in decisions:
        if "Outcome" in decision:
            rating = decision["Outcome"]["Rating"]
            if rating >= 4:
                regret_count += 1
                importance = decision.get("Importance", "Unknown")
                regret_reasons[importance] = regret_reasons.get( importance, 0) + 1
    if regret_count == 0:
        print(
        "\n🎉 No regret patterns detected.")
        print(
        "Your recorded decisions have generally aligned with your expectations.")
        print(
        "\n🧠 Thinkora Insight:")
        print(
        "You appear to make decisions that align well with your values and expectations. Continue balancing reflection with decisive action.")
        return
    most_common_regret = max(
    regret_reasons,
    key=regret_reasons.get)
    regret_frequency = regret_reasons[
    most_common_regret]
    print(
    f"\nMost regrets occurred in "
    f"{most_common_regret}-importance decisions.")
    print(
    f"Occurrences: {regret_frequency}")
    if most_common_regret == "High":
        insight = (
        "You tend to regret high-stakes decisions. "
        "Slow down, gather information, and avoid rushing major choices.")
    elif most_common_regret == "Medium":
        insight = (
        "Some mid-level decisions may benefit from a bit more reflection "
        "before committing.")
    elif most_common_regret == "Low":
        insight = (
        "Minor decisions appear to create unnecessary regret. "
        "Trust yourself more on low-risk choices.")
    else:
        insight = (
        "Regret patterns are emerging, but more data is needed "
        "to draw stronger conclusions.")
    print("\n🧠 Thinkora Insight:")
    print(insight)

##########################################
# BEHAVIORAL INTELLIGENCE
##########################################
def decision_streak_system():
    print("\n===== DECISION STREAK =====")
    try:
        with open("decisions.json", "r") as file:
            decisions = json.load(file)
    except ( FileNotFoundError,  json.JSONDecodeError):
        print("No decisions found.")
        return
    if len(decisions) == 0:
        print("No decisions found.")
        return
    reflection_streak = 0
    evaluation_streak = 0
    outcome_streak = 0
    longest_reflection = 0
    longest_evaluation = 0
    longest_outcome = 0
    for decision in decisions:
        if ("Reflections" in decision  and  len(decision["Reflections"]) > 0):
            reflection_streak += 1
        else:
            reflection_streak = 0
        if (reflection_streak>longest_reflection):
            longest_reflection = (reflection_streak)
        if ("Evaluations" in decision and len(decision["Evaluations"]) > 0):
            evaluation_streak += 1
        else:
            evaluation_streak = 0
        if (evaluation_streak>longest_evaluation):
            longest_evaluation = evaluation_streak
        if "Outcome" in decision:
            outcome_streak += 1
        else:
            outcome_streak = 0
        if (outcome_streak>longest_outcome):
            longest_outcome = outcome_streak
    print()
    print(
            f"🪞 Longest Reflection Streak: {longest_reflection}")
    print(
            f"🧠 Longest Evaluation Streak: {longest_evaluation}")
    print(
            f"🎯 Longest Outcome Streak: {longest_outcome}")
    print()
    print("===== THINKORA INSIGHT =====")
    print()
    if longest_reflection >= 5:
        print("🌱 You consistently reflect on your decisions.")
    else:
        print("🪞 Consider reflecting more frequently after making decisions." )
    if longest_evaluation >= 5:
        print("🧠 Structured decision-making seems to be a strong habit.")
    else:
        print("📋 Try evaluating decisions more often.")
    if longest_outcome >= 5:
        print("🎯 You do a good job learning from outcomes.")
    else:
        print("📈 Tracking outcomes can help you grow as a decision-maker.")
    print()
    if (longest_reflection >= 5 and longest_outcome >= 5):
        print( "🏆 Thinkora Observation: You appear to have strong decision-learning habits.")
    elif longest_reflection >= 5:
        print("✨ Thinkora Observation: Reflection seems to be one of your strengths.")
    else:
        print( "🚀 Thinkora Observation: There is plenty of room to strengthen your decision habits.")

def bias_detector():

    print(

        "\n===== DECISION BIAS DETECTOR =====")
    try:
        with open("decisions.json", "r" ) as file:
            decisions = json.load(file)
    except ( FileNotFoundError, json.JSONDecodeError):
        print("No decisions found." )
        return
    analysis_paralysis = 0
    recommendation_avoidance = 0
    reflection_neglect = 0
    impulsive_commitment = 0
    outcome_neglect = 0
    for decision in decisions:

        if ("Evaluations" in decision and len(decision["Evaluations"]) >= 2):
            analysis_paralysis += 1
        if ("Final_Choice" in decision and "Evaluations" in decision and len(  decision["Evaluations"]) > 0):
            latest_winner = (decision["Evaluations"][-1]["Winner"])
            if latest_winner != decision["Final_Choice"]:
                recommendation_avoidance += 1
        if ("Final_Choice" in decision and( "Reflections" not in decision or len(decision["Reflections"]) == 0)):
            reflection_neglect += 1
        if ("Final_Choice" in decision and( "Evaluations" not in decision or len(decision["Evaluations"]) == 0)):
            impulsive_commitment += 1
        if ("Final_Choice" in decision and "Outcome" not in decision):
            outcome_neglect += 1
    print()
    print("Potential Biases:\n")
    if analysis_paralysis > 0:
        print(
        "✓ Analysis Paralysis")
    if (
        analysis_paralysis == 0
        and
        recommendation_avoidance == 0
        and
        reflection_neglect == 0
        and
        impulsive_commitment == 0
        and
        outcome_neglect == 0):
        print( "🎉 No significant biases detected." )
    print()
    print( "===== THINKORA OBSERVATION =====")
    print()
    if analysis_paralysis > 0:
        print("🧠 You occasionally revisit decisions multiple times before committing.")
    if recommendation_avoidance > 0:
        print("📋 You sometimes trust your own judgment over Thinkora recommendations.")
    if reflection_neglect > 0:
        print("🪞 Consider reflecting more often after making decisions.")
    if (analysis_paralysis == 0 and recommendation_avoidance == 0 and reflection_neglect == 0 and impulsive_commitment == 0 and outcome_neglect == 0):
        print("✨ Your recent decisions appear balanced and intentional.")

def wisdom_summary():
    print("\n===== THINKORA WISDOM SUMMARY =====")
    try:
        with open("decisions.json", "r") as file:
            decisions = json.load(file)
    except (FileNotFoundError,  json.JSONDecodeError):
        print("No decisions found.")
        return
    if len(decisions)==0:
        print( "No decisions found." )
        return
    total_decisions = len(decisions)
    outcomes = 0
    reflections = 0
    evaluations = 0
    for decision in decisions:
        if "Outcome" in decision:
            outcomes += 1
        if ( "Reflections" in decision and len( decision["Reflections"]) > 0):
            reflections += 1
        if ("Evaluations" in decision and len(decision["Evaluations"]) > 0):
            evaluations += 1
    print()
    print(f"Decisions Made : {total_decisions}")
    print(f"Decisions Evaluated : {evaluations}")
    print(f"Decisions Reflected On : {reflections}")
    print(f"Outcomes Recorded : {outcomes}")
    reflection_rate = (reflections/total_decisions)*100
    evaluation_rate = ( evaluations/total_decisions)*100
    outcome_rate=(outcomes/total_decisions)*100
    print()
    print(f"Reflection Rate : {reflection_rate:.1f}%")
    print(f"Evaluation Rate : {evaluation_rate:.1f}%")
    print(f"Outcome Rate : {outcome_rate:.1f}%")
    print()
    print("===== THINKORA OBSERVATION =====")
    print()
    if reflection_rate >= 70:
        print( "🌱 Strongest Trait : Reflective Decision Maker")
    elif evaluation_rate >= 70:
        print("🧠 Strongest Trait : Analytical Decision Maker")
    elif outcome_rate >= 70:
        print("🎯 Strongest Trait : Learning From Experience")
    else:
        print( "🚀 Strongest Trait : Developing Decision Habits")
    print()
    print("===== THINKORA WISDOM =====")
    print()
    if (reflection_rate >= 70 and outcome_rate >= 70):
        print("🏆 You appear to be developing strong decision-learning habits.")
    elif reflection_rate >= 70:
        print("🌱 Reflection seems to be one of your greatest strengths.")
    elif evaluation_rate >= 70:
        print("🧠 You tend to approach decisions analytically.")
    elif outcome_rate >= 70:
        print("🎯 You actively learn from past experiences.")
    else:
        print("🚀 You're steadily building better decision habits over time.")

##########################################
# MENUS
##########################################
def analytics_menu():

    while True:

        print("\n===== ANALYTICS =====")

        print("1. Decision Analytics")

        print("2. Decision Patterns")

        print("3. Top Priorities")

        print("4. Recommendation Trust Score")

        print("5. Overthinking Detector")

        print("6. Decision Growth Insights")

        print("7. Back")


        choice = input(

            "\nEnter your choice: ")
        if choice == "1":
            decision_analytics()
        elif choice == "2":
            decision_patterns()
        elif choice == "3":
            top_priorities()
        elif choice == "4":
            recommendation_trust()
        elif choice == "5":
            overthinking_detector()
        elif choice == "6":
            decision_growth()
        elif choice == "7":
            break
        else:
            print("Invalid choice.")

def insights_menu():

    while True:

        print("\n===== DECISION INSIGHTS =====")

        print("1. Outcome Insights")

        print("2. Decision Timeline")

        print("3. Personality Profile")

        print("4. Regret Pattern Analysis")

        print("5. Back")


        choice = input(

            "\nEnter your choice: ")
        if choice == "1":
            outcome_insights()
        elif choice == "2":
            decision_timeline()
        elif choice == "3":
            decision_personality()
        elif choice == "4":
            regret_pattern_analysis()
        elif choice == "5":
            break
        else:
            print( "Invalid choice." )

def behavioral_menu():

    while True:

        print("\n===== BEHAVIORAL INTELLIGENCE =====")

        print("1. Decision Streak System")

        print("2. Decision Bias Detector")

        print("3. Decision Wisdom Summary")

        print("4. Back")


        choice = input(

            "\nEnter your choice: ")
        if choice == "1":
            decision_streak_system()
            
        elif choice == "2":
            bias_detector()
            
        elif choice == "3":
            wisdom_summary()
            
        elif choice == "4":
            break
            
        else:
            print( "Invalid choice." )
        
def main_menu():
    while True:
        print("\n===== THINKORA =====")
        print("1. Add Decision")
        print("2. View Decisions")
        print("3. Evaluate Existing Decision")
        print("4. View Evaluation History")
        print("5. View Reflections")
        print("6. Analytics")
        print("7. Record Decision Outcome")
        print("8. Decision Insights")
        print("9. Behavorial Intelligence")
        print("10. Exit")

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
            view_reflections()

        elif choice == 6:
            analytics_menu()
            
        elif choice==7:
            record_outcome()

        elif choice == 8:
            insights_menu()

        elif choice == 9:
            behavioral_menu()
            
        elif choice == 10:
            print("Thank you for using Thinkora!")
            break

        else:
            invalid_choice()

if __name__ == "__main__":
    main_menu()
