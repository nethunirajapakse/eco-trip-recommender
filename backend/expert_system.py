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
        (slot preferred-popularity)
        (slot max-total-user-preference-score))
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
        (slot raw-score)
        (slot normalized-score))
    ''')

    env.build('''
    (defrule recommend-complex
        ?u <- (user
                (activities $?user-acts)
                (preferred-climate ?user-climate)
                (preferred-region ?user-region)
                (preferred-difficulty ?user-difficulty)
                (preferred-popularity ?user-popularity)
                (max-total-user-preference-score ?max-total-user-score))
        ?d <- (destination
                (name ?n)
                (activities $?dest-acts)
                (climate ?dest-climate)
                (region ?dest-region)
                (difficulty ?dest-difficulty)
                (popularity ?dest-popularity))

        ; --- Strict Filtering Conditions ---
        (test (or (eq ?user-climate "any") (eq ?user-climate ?dest-climate)))
        (test (or (eq ?user-region "any") (eq ?user-region ?dest-region)))
        (test (or (eq ?user-difficulty "any") (eq ?user-difficulty ?dest-difficulty)))
        (test (or (eq ?user-popularity "any") (eq ?user-popularity ?dest-popularity)))
        ; --- End Strict Filtering Conditions ---

        =>
        (bind ?activity-matches 0)
        (foreach ?user-act $?user-acts
            (if (member$ ?user-act $?dest-acts)
                then (bind ?activity-matches (+ ?activity-matches 1))))

        ; --- New Rule: If no activity matches, raw-score is 0 and normalization is 0 ---
        (if (> ?activity-matches 0) then
            (bind ?raw-score (* ?activity-matches 10)) ; Higher weight for activity match

            ; Bonus for exact matches
            (if (eq ?user-climate ?dest-climate) then (bind ?raw-score (+ ?raw-score 5)))
            (if (eq ?user-region ?dest-region) then (bind ?raw-score (+ ?raw-score 5)))
            (if (eq ?user-difficulty ?dest-difficulty) then (bind ?raw-score (+ ?raw-score 5)))
            (if (eq ?user-popularity ?dest-popularity) then (bind ?raw-score (+ ?raw-score 5)))

            ; Calculate normalized score based on max_total_user_preference_score
            (bind ?normalized-score 0)
            (if (> ?max-total-user-score 0) then
                (bind ?normalized-score (* (/ ?raw-score (float ?max-total-user-score)) 10.0))
            )
        else
            ; If no activity matches, raw-score and normalized-score are 0
            (bind ?raw-score 0)
            (bind ?normalized-score 0)
        )

        (assert (recommendation
            (name ?n)
            (raw-score ?raw-score)
            (normalized-score ?normalized-score)))
    )
    ''')

    return env

def recommend(activities, climate, region, difficulty, popularity):
    env = setup_environment()

    activity_str = " ".join([f'"{a}"' for a in activities]) if activities else ""
    
    max_total_user_preference_score = (len(activities) * 10)
    
    if climate != "any": max_total_user_preference_score += 5
    if region != "any": max_total_user_preference_score += 5
    if difficulty != "any": max_total_user_preference_score += 5
    if popularity != "any": max_total_user_preference_score += 5

    if max_total_user_preference_score == 0:
        max_total_user_preference_score = 1


    env.assert_string(f'(user (activities {activity_str}) (preferred-climate "{climate}") (preferred-region "{region}") (preferred-difficulty "{difficulty}") (preferred-popularity "{popularity}") (max-total-user-preference-score {max_total_user_preference_score}))')

    env.run()

    results = []
    for fact in env.facts():
        if fact.template.name == 'recommendation':
            normalized_score = round(min(max(fact["normalized-score"], 0), 10), 1)
            results.append({
                "name": fact["name"],
                "raw_score": fact["raw-score"],
                "normalized_score": normalized_score
            })

    results.sort(key=lambda x: x['normalized_score'], reverse=True)

    return results