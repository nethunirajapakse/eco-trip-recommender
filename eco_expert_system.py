import clips
from eco_knowledge_base import knowledge_base

def setup_environment():
    env = clips.Environment()

    # Define templates
    env.build('''
    (deftemplate user
        (slot activity))
    ''')

    env.build('''
    (deftemplate destination
        (slot name)
        (multislot activities)
        (slot climate)
        (slot region)
        (multislot features))
    ''')

    # Load the knowledge base
    for place in knowledge_base:
        fact = f'''(destination
            (name "{place['location']}")
            (activities {" ".join([f'"{a}"' for a in place['activities']])})
            (climate "{place['climate']}")
            (region "{place['region']}")
            (features {" ".join([f'"{f}"' for f in place['special_features']])})
        )'''
        env.assert_string(fact)

    # Define rule for matching destinations
    env.build('''
    (deftemplate recommendation
        (slot name))
    ''')

    env.build('''
    (defrule recommend
        (user (activity ?a))
        (destination (name ?n) (activities $? ?a $?))
        =>
        (assert (recommendation (name ?n))))
    ''')

    return env


def recommend(activities):
    env = setup_environment()

    # Assert user preferences
    for activity in activities:
        env.assert_string(f'(user (activity "{activity}"))')

    env.run()

    # Collect results from 'recommendation' facts
    results = []
    for fact in env.facts():
        if fact.template.name == 'recommendation':
            results.append({"name": fact["name"]})

    return results


if __name__ == "__main__":
    print("🌿 Welcome to the Eco-Trip Expert System 🌿\n")

    # Get user input
    user_activities = input("Enter your preferred activities (comma separated): ").lower().split(",")
    user_activities = [a.strip() for a in user_activities if a.strip()]

    # Run the expert system
    results = recommend(user_activities)

    if not results:
        print("\n😕 No matching destinations found.")
    else:
        print("\n✅ Inference completed.")
