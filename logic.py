from data import COURSES, ACTIVITIES, ALUMNI_TRAJECTORIES


def get_recommendations(profile, career_key):
    recommended_courses    = [c for c in COURSES     if career_key in c["career_relevance"]]
    recommended_activities = [a for a in ACTIVITIES  if career_key in a["career_relevance"]]
    alumni                 = [a for a in ALUMNI_TRAJECTORIES if a["career"] == career_key]

    return {
        "courses":    recommended_courses[:5],
        "activities": recommended_activities[:5],
        "alumni":     alumni,
    }
