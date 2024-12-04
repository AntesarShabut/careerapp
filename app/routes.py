from flask import Flask, url_for, render_template, request, redirect, session, request, jsonify
from app import app
import json
import urllib.parse
from wtforms.fields.html5 import IntegerRangeField
from .forms import SkillsForm
from .helpers import get_soft_skills_data, format_anon_user, get_role, format_skills, process_session_data
import recommender.recommender as rc
import job_info.job_descriptions as get_job_desc
import job_info.job_skills as get_job_skills
import sys
#import serpstack as ss
#from app import mongo

@app.route('/')
def home():
    """ route for the home view
    """
    return render_template('home.html', page_name="Home")

@app.route('/details')
def details():
    """route for details"""
    return render_template('details.html', page_name="Details")

@app.route('/familiarity')
def familiarity():
    """route for familiarity"""
    return render_template('familiarity.html', page_name="Familiarity")

@app.route('/familiar_roles')
def familiar_roles():
    """route for familiarity"""
    return render_template('familiar-roles.html', page_name="familiar_roles")

@app.route('/career_likelyhood')
def career_likelyhood():
    """route for familiarity"""
    return render_template('career-likelyhood.html', page_name="career_likelyhood")



@app.route('/skills_assessment', methods=['GET', 'POST'])
def skills_assessment():
    """ route for entering soft skills"""
    # get soft skills categories data
    soft_skills_data = get_soft_skills_data()
    class F(SkillsForm):
        pass
    for skill in soft_skills_data:
        setattr(F, skill["term"], IntegerRangeField(skill["label"], 
            default=0) )
    form = F(username='anonymous')
    if request.method == 'POST' and form.validate():
        session['FORMDATA'] = request.form.to_dict()
        # generate recommendations
        return redirect(url_for('results'))
    else:
        return render_template('skills-assessment.html', page_name='Soft Skills', form=form)
    # return render_template('skills-assessment.html', page_name="skills_assessment")

    

@app.route('/job_results')
def job_results():
    # ##define users array from anonymous form data
    # if session.get('FORMDATA', None):
    #     # create user from form data
    #     anon_user = format_anon_user( session.get('FORMDATA') )
    #     # initialise graph
    #     G = rc.initialise_graph([anon_user])
    #     # get job match data
    #     matches = [m[0] for m in rc.n_best_matches(G, 'anonymous', 10)]
    #     data = []
    #     for match in matches:
    #         role = get_role(match)
    #         skills = format_skills( rc.get_skills(G, match) )
    #         data.append({"title": match, "description": role['snippet'], "skills": skills, "url": role['Url']})
    #         # print(role['Url'],None)
    #     # send match data to template
        return render_template('job-results.html') 
    # else:
    #     return redirect(url_for('skills_assessment'))
    # return render_template('job-results.html', page_name="results")




# @app.route('/about')
# def about():
#     """ route for the about view
#     """
#     return render_template('about.html', page_name="About")

# @app.route('/contact')
# def contact():
#     """ route for the contact view
#     """
#     return render_template('contact.html', page_name="Contact")

# @app.route('/faqs')
# def faqs():
#     """ route for the faqs view
#     """
#     return render_template('faqs.html', page_name="FAQ's")

# @app.route('/myskills', methods=['GET', 'POST'])
# def skills_profile():
#     """ route for entering soft skills
#     """
#     # get soft skills categories data
#     soft_skills_data = get_soft_skills_data()
#     class F(SkillsForm):
#         pass
#     for skill in soft_skills_data:
#         setattr(F, skill["term"], IntegerRangeField(skill["label"], 
#             default=0) )
#     form = F(username='anonymous')
#     if request.method == 'POST' and form.validate():
#         session['FORMDATA'] = request.form.to_dict()
#         # generate recommendations
#         return redirect(url_for('matches'))
#     else:
#         return render_template('skills_profile.html', page_name='Soft Skills', form=form)

# @app.route('/matches')
# def matches():
#     """ route which displays role matches for user """
#     # define users array from anonymous form data
#     if session.get('FORMDATA', None):
#         # create user from form data
#         anon_user = format_anon_user( session.get('FORMDATA') )
#         # initialise graph
#         G = rc.initialise_graph([anon_user])
#         # get job match data
#         matches = [m[0] for m in rc.n_best_matches(G, 'anonymous', 10)]
#         data = []
#         for match in matches:
#             role = get_role(match)
#             skills = format_skills( rc.get_skills(G, match) )
#             data.append({"title": match, "description": role['snippet'], "skills": skills, "url": role['Url']})
#             print(role['Url'],None)
#         # send match data to template
#         return render_template('matches.html', page_name='My Matches', matches=data) 
#     else:
#         return redirect(url_for('skills_profile'))
    
@app.route('/results')
def results():


    # Rows represent jobs, columns represent skills, values represent importance level of each skill (1-10 scale)
    job_attributes = np.array([
        [8, 2, 6, 7, 5],  # Developer: JavaScript, Teamwork, Problem-solving, Creativity, Communication
        [3, 9, 5, 8, 6],  # Designer
        [7, 4, 9, 3, 4],  # Data Analyst
        [6, 5, 4, 8, 7],  # Project Manager
        [4, 6, 3, 5, 9],  # QA Tester
    ])

    # Define job titles for example
    job_titles = ["Developer", "Designer", "Data Analyst", "Project Manager", "QA Tester"]

    # Example user profile from the questionnaire
    user_profile = np.array([7, 8, 5, 6, 7])

    # Content-Based Filtering via cosine similarity
    similarity_scores = cosine_similarity([user_profile], job_attributes)[0]

    # Sort jobs by similarity score (similarity_score ranks lowest to highest so reverse it)
    recommended_job_indices = np.argsort(-similarity_scores)
    recommended_jobs = [(job_titles[i], similarity_scores[i]) for i in recommended_job_indices]

    # Display recommendations and similarity scores
    print("Recommended jobs for the user based on content-based filtering:")
    for job, score in recommended_jobs:
        print(f"{job}: Similarity Score {score * 100:.2f}%")
    return render_template('results.html', page_name='Results')

@app.route('/matches_temp')
def matches_temp():
    session_data = request.args.get('session_data', '{}')
    decoded_session_data = urllib.parse.unquote(session_data)
    
    print("Debug: Decoded session_data:", decoded_session_data)

    try:
        session_data = json.loads(decoded_session_data)
        print("Debug: Parsed session_data:", session_data)
    except json.JSONDecodeError:
        print("Debug: Failed to parse session_data. Using empty dict.")
        session_data = {}

    try:
        # Initialize the graph
        G = rc.initialise_graph([session_data])
        print("Debug: Nodes in G:", G.nodes(data=True))
        print("Debug: Edges in G:", G.edges(data=True))

        # Find matches
        matches = [m[0] for m in rc.n_best_matches(G, "anonymous", 10)]
        print("Debug: Matches:", matches)

        # Format match data
        data = []
        for match in matches:
            role = get_role(match)
            skills = rc.get_skills(G, match)
            formatted_skills = format_skills(skills)
            data.append({
                "title": match,
                "description": role.get('snippet', 'No description available'),
                "skills": formatted_skills,
                "url": role.get('Url', '#')
            })
        print("Debug: Data for template:", data)

    except Exception as e:
        print("Debug: Error in match processing:", str(e))
        data = []

    return render_template(
        'matches-temp.html',
        page_name='My Matches',
        matches=data,
        session_data=session_data
    )

@app.route('/process-data', methods=['POST'])
def process_data():

    try:
        data = request.json  # Parse incoming JSON
        if not data:
            return jsonify({"error": "No data received"}), 400

        user_skills = data.get('userSkills')  # Extract userSkills
        if not user_skills:
            return jsonify({"error": "No user skills provided"}), 400

        # Store in session
        session['userSkills'] = user_skills

        # Process the session data
        session_data = process_session_data(user_skills)
        if isinstance(session_data, str):  # Check if an error message was returned
            return jsonify({"error": session_data}), 400

        return jsonify({"session_data": session_data})
    except Exception as e:
        # Catch any unexpected errors
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500