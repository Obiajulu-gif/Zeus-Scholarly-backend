from flask import Flask, jsonify, request
from flask_cors import CORS
from serpapi import GoogleSearch
import requests
from datetime import datetime
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
CORS(app)
API_KEY = os.getenv("API_KEY")

@app.route('/api/countries', methods=['GET'])
def get_countries():
    try:
        response = requests.get("https://restcountries.com/v3.1/all")
        response.raise_for_status()  # Raise an exception for HTTP errors

        countries_data = response.json()

        countries_data.sort(key=lambda country: country['name']['common'])

        countries = [{"name": country['name']['common']} for country in countries_data]
        return jsonify(countries)
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/scholarships', methods=['GET'])
def get_scholarships():
    selected_country = request.args.get('selectedCountry', 'usa')
    selected_degree = request.args.get('selectedDegree', 'master')
    api_key = os.getenv("api_key")
    page = int(request.args.get('page', 1))

    params = {
        "api_key": api_key,
        "engine": "google",
        "q": f"{selected_degree} degree scholarships in {selected_country}",
        "start": (page - 1) * 10,
    }

    try:
        current_date = datetime.now()
        search = GoogleSearch(params)
        result = search.get_dict()
        organic_results = result.get('organic_results', [])

        scholarships_data = [
            {
                "source": result.get("source"),  
                "link": result.get("link"),
                "favicon": result.get("favicon"),  
                "snippet": result.get("snippet"),
                "date": current_date.strftime("%d %B %Y") if result.get("date") is None else result.get("date"),
            }
            for result in organic_results
        ]

        total_results = result.get('search_information', {}).get('total_results', 0)
        return jsonify({"scholarships": scholarships_data, "totalResults": total_results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    title = request.args.get('title', 'software developer')
    location = request.args.get('location', 'nigeria')
    page = request.args.get('page', 1)

    job_params = {
        "api_key": API_KEY,
        "engine": "google_jobs",
        "google_domain": "google.com",
        "q": f"{title} in {location}",
        "start": (int(page) - 1) * 10,
    }

    try:
        job_search = GoogleSearch(job_params)
        job_results = job_search.get_dict().get('jobs_results', [])
        return jsonify({"jobs": job_results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/news', methods=['GET'])
def get_news():
    query = request.args.get('query', 'latest news')
    page = request.args.get('page', 1)

    news_params = {
        "api_key": API_KEY,
        "engine": "google_news",
        "q": query,
        "start": (int(page) - 1) * 10,
    }

    try:
        news_search = GoogleSearch(news_params)
        news_results = news_search.get_dict().get('news_results', [])
        return jsonify({"news": news_results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/internships', methods=['GET'])
def get_internships():
    discipline = request.args.get('discipline', default='software engineer') 
    location = request.args.get('location', default='nigeria')
    state = request.args.get('state', default='lagos')

    api_key = os.getenv("API_KEY")

    internship_params = {
        "api_key": api_key,
        "engine": "google_jobs",
        "q": f"{discipline} internship in {state} {location}",
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en"
    }
    
    try:
        internship_search = GoogleSearch(internship_params)
        result = internship_search.get_dict()
        internship_results = result.get('jobs_results', [])
        return jsonify({"internships": internship_results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/research-grants', methods=['GET'])
def get_research_grants():
    query = request.args.get('query', 'current research grants for master and phd students')
    page = request.args.get('page', 1)

    params = {
        "api_key": API_KEY,
        "engine": "google",
        "q": query,
        "start": (int(page) - 1) * 10,
    }

    try:
        search = GoogleSearch(params)
        result = search.get_dict()
        organic_results = result.get('organic_results', [])

        research_grants_data = [
            {
                "source": result.get("source"),
                "link": result.get("link"),
                "favicon": result.get("favicon"),
                "snippet": result.get("snippet"),
                "date": result.get("date"),
            }
            for result in organic_results
        ]

        return jsonify({"research_grants": research_grants_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

 
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
