from flask import Flask, request, jsonify
from flask_cors import CORS
from backend.expert_system import recommend
from backend.knowledge_base import knowledge_base

app = Flask(__name__)
CORS(app)  

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    """
    API endpoint to get destination recommendations
    Expected JSON body:
    {
        "activities": ["hiking", "photography"],
        "climate": "any",
        "region": "any",
        "difficulty": "any",
        "popularity": "any"
    }
    """
    try:
        data = request.get_json()
        
        activities = data.get('activities', [])
        climate = data.get('climate', 'any')
        region = data.get('region', 'any')
        difficulty = data.get('difficulty', 'any')
        popularity = data.get('popularity', 'any')
        
        if not activities or len(activities) == 0:
            return jsonify({
                'error': 'Please provide at least one activity'
            }), 400
        
        results = recommend(activities, climate, region, difficulty, popularity)
      
        enriched_results = []
        for result in results:
            destination = next(
                (place for place in knowledge_base 
                 if place['location'].lower() == result['name'].lower()),
                None
            )
            
            if destination:
                enriched_results.append({
                    'name': result['name'].title(),
                    'score': result['score'],
                    'climate': destination['climate'].title(),
                    'region': destination['region'].title(),
                    'features': destination['special_features'],
                    'activities': destination['activities'],
                    'difficulty': destination['difficulty'].title(),
                    'popularity': destination['popularity'].title()
                })
            else:
                enriched_results.append({
                    'name': result['name'].title(),
                    'score': result['score'],
                    'climate': 'Unknown',
                    'region': 'Unknown',
                    'features': [],
                    'activities': [],
                    'difficulty': 'Unknown',
                    'popularity': 'Unknown'
                })
        
        return jsonify({
            'success': True,
            'results': enriched_results,
            'count': len(enriched_results)
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/destinations', methods=['GET'])
def get_all_destinations():
    """
    API endpoint to get all available destinations
    """
    try:
        destinations = [
            {
                'name': place['location'].title(),
                'activities': place['activities'],
                'climate': place['climate'].title(),
                'region': place['region'].title(),
                'features': place['special_features'],
                'difficulty': place['difficulty'].title(),
                'popularity': place['popularity'].title()
            }
            for place in knowledge_base
        ]
        
        return jsonify({
            'success': True,
            'destinations': destinations,
            'count': len(destinations)
        })
    
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'CeylonWild API is running'
    })

if __name__ == '__main__':
    print("🌿 Starting CeylonWild API Server...")
    print("📍 API will be available at http://localhost:5000")
    print("🔗 React app should connect to this URL")
    app.run(debug=True, port=5000)