"""
Matching engine.

Two things are computed for every profile <-> posting pair:

1. Skill gap analysis (the main, human-readable result):
   - which required skills the person already has (matched_skills)
   - which required skills they're missing (missing_skills)
   - a match_percentage based on required-skill coverage
   - a plain-English feedback message telling them what to learn next

2. A secondary semantic_score (TF-IDF + cosine similarity) that also takes
   bio/description text into account, used only for ranking/ordering when
   percentages tie - not shown as the headline number.
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.models.profile import Profile
from app.models.posting import Posting


def _parse_skills(skills_str):
    """'Python, Flask , SQL' -> ['python', 'flask', 'sql'] - cleaned, lowercased, deduped."""
    if not skills_str:
        return []
    seen = []
    for raw in skills_str.split(","):
        skill = raw.strip().lower()
        if skill and skill not in seen:
            seen.append(skill)
    return seen


def _profile_text(profile):
    skills = profile.skills or "" if profile else ""
    bio = profile.bio or "" if profile else ""
    return f"{skills} {skills} {bio}"


def _posting_text(posting):
    skills = posting.required_skills or "" if posting else ""
    desc = posting.description or "" if posting else ""
    return f"{skills} {skills} {desc}"


def _semantic_score(doc_a, doc_b):
    if not doc_a.strip() or not doc_b.strip():
        return 0.0
    vectorizer = TfidfVectorizer()
    try:
        matrix = vectorizer.fit_transform([doc_a, doc_b])
    except ValueError:
        return 0.0
    return round(float(cosine_similarity(matrix[0], matrix[1])[0][0]), 4)


def _feedback_message(percentage, missing):
    if not missing:
        return "You match 100% of the required skills for this role. Great fit!"
    if percentage == 0:
        return (
            "You don't currently match any of the required skills for this role. "
            f"Focus on learning: {', '.join(missing)}."
        )
    return (
        f"Your skills match {percentage}% of this role's requirements. "
        f"To improve your employability for this role, work on: {', '.join(missing)}."
    )


def _gap_analysis(profile, posting):
    user_skills = _parse_skills(profile.skills if profile else "")
    required_skills = _parse_skills(posting.required_skills if posting else "")

    if not required_skills:
        return {
            "match_percentage": 0.0,
            "matched_skills": [],
            "missing_skills": [],
            "feedback": "This posting doesn't list specific required skills yet.",
            "semantic_score": 0.0,
        }

    matched = [s for s in required_skills if s in user_skills]
    missing = [s for s in required_skills if s not in user_skills]
    percentage = round(len(matched) / len(required_skills) * 100, 1)

    return {
        "match_percentage": percentage,
        "matched_skills": matched,
        "missing_skills": missing,
        "feedback": _feedback_message(percentage, missing),
        "semantic_score": _semantic_score(_profile_text(profile), _posting_text(posting)),
    }


def score_user_against_posting(user_id, posting_id):
    profile = Profile.query.filter_by(user_id=user_id).first()
    posting = Posting.query.get(posting_id)
    return _gap_analysis(profile, posting)


def rank_postings_for_user(user_id, limit=10):
    profile = Profile.query.filter_by(user_id=user_id).first()
    if not profile:
        return []

    postings = Posting.query.all()
    scored = []
    for posting in postings:
        analysis = _gap_analysis(profile, posting)
        scored.append({**posting.to_dict(), **analysis})

    scored.sort(key=lambda p: (p["match_percentage"], p["semantic_score"]), reverse=True)
    return scored[:limit]


def rank_candidates_for_posting(posting_id, limit=10):
    posting = Posting.query.get(posting_id)
    if not posting:
        return []

    profiles = Profile.query.all()
    scored = []
    for profile in profiles:
        analysis = _gap_analysis(profile, posting)
        scored.append({
            "user_id": profile.user_id,
            "profile": profile.to_dict(),
            **analysis,
        })

    scored.sort(key=lambda p: (p["match_percentage"], p["semantic_score"]), reverse=True)
    return scored[:limit]