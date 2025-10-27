import clips
from knowledge_base import knowledge_base

def setup_environment():
    env = clips.Environment()

    env.build('''
    (deftemplate user
        (multislot activities)
        (slot preferred-climate)
        (slot preferred-region)
        (slot preferred-difficulty)
        (slot preferred-popularity))
    ''')

    env.build('''
    (deftemplate destination
        (slot name)
        (multislot activities)
        (slot climate)
        (slot region)
        (multislot features)
        (slot difficulty)
        (slot popularity))
    ''')

    for place in knowledge_base:
        fact = f'''(destination
            (name "{place['location']}")
            (activities {" ".join([f'"{a}"' for a in place['activities']])})
            (climate "{place['climate']}")
            (region "{place['region']}")
            (features {" ".join([f'"{f}"' for f in place['special_features']])})
            (difficulty "{place['difficulty']}")
            (popularity "{place['popularity']}")
        )'''
        env.assert_string(fact)

    env.build('''
    (deftemplate recommendation
        (slot name)
        (slot score)) ; Add a score to rank recommendations
    ''')

    env.build('''
    (defrule recommend-complex
        ?u <- (user
                (activities $?user-acts)
                (preferred-climate ?user-climate)
                (preferred-region ?user-region)
                (preferred-difficulty ?user-difficulty)
                (preferred-popularity ?user-popularity))
        (destination
                (name ?n)
                (activities $?dest-acts)
                (climate ?dest-climate)
                (region ?dest-region)
                (difficulty ?dest-difficulty)
                (popularity ?dest-popularity))

        ; --- Strict Filtering Conditions ---
        ; Only assert recommendation if preferences match exactly, or if user selected "any"
        (test (or (eq ?user-climate "any") (eq ?user-climate ?dest-climate)))
        (test (or (eq ?user-region "any") (eq ?user-region ?dest-region)))
        (test (or (eq ?user-difficulty "any") (eq ?user-difficulty ?dest-difficulty)))
        (test (or (eq ?user-popularity "any") (eq ?user-popularity ?dest-popularity)))
        ; --- End Strict Filtering Conditions ---

        =>
        (bind ?score 0)

        ; Activity match (count common activities) - still a scoring factor
        (bind ?activity-matches 0)
        (foreach ?user-act $?user-acts
            (if (member$ ?user-act $?dest-acts)
                then (bind ?activity-matches (+ ?activity-matches 1))))
        (bind ?score (+ ?score (* ?activity-matches 10))) ; Higher weight for activity match

        ; Optional: Add a small bonus for exact matches even if not strictly filtered,
        ; to help rank results that pass the strict filter.
        (if (eq ?user-climate ?dest-climate) then (bind ?score (+ ?score 5)))
        (if (eq ?user-region ?dest-region) then (bind ?score (+ ?score 5)))
        (if (eq ?user-difficulty ?dest-difficulty) then (bind ?score (+ ?score 5)))
        (if (eq ?user-popularity ?dest-popularity) then (bind ?score (+ ?score 5)))

        (assert (recommendation (name ?n) (score ?score)))
    )
    ''')

    return env

def recommend(activities, climate, region, difficulty, popularity):
    env = setup_environment()

    activity_str = " ".join([f'"{a}"' for a in activities]) if activities else ""
    env.assert_string(f'(user (activities {activity_str}) (preferred-climate "{climate}") (preferred-region "{region}") (preferred-difficulty "{difficulty}") (preferred-popularity "{popularity}"))')

    env.run()

    results = []
    for fact in env.facts():
        if fact.template.name == 'recommendation':
            results.append({"name": fact["name"], "score": fact["score"]})

    results.sort(key=lambda x: x['score'], reverse=True)

    return results
