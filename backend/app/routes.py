from flask import Blueprint, request, jsonify
from .translator import Translator

# Create blueprint
api_bp = Blueprint('api', __name__)

# Initialize translator
translator = Translator()

@api_bp.route('/translate', methods=['POST'])
def translate_text():
    """
    Endpoint to translate text
    Expected JSON: {
        'text': 'text to translate',
        'source_lang': 'en' or 'auto',
        'target_lang': 'es'
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({
                'error': 'No data provided'
            }), 400
        
        # Extract parameters
        text = data.get('text', '')
        source_lang = data.get('source_lang', 'auto')
        target_lang = data.get('target_lang', 'en')
        
        # Validate text
        if not text:
            return jsonify({
                'error': 'No text provided'
            }), 400
        
        # Validate target language
        if not target_lang:
            return jsonify({
                'error': 'Target language is required'
            }), 400
        
        # Log the request
        print(f"Translation request received:")
        print(f"  Text: '{text}'")
        print(f"  Source: {source_lang}")
        print(f"  Target: {target_lang}")
        
        # Perform translation
        result = translator.translate(text, source_lang, target_lang)
        
        # Check if translation was successful
        if result['success']:
            print(f"Translation successful: '{result['translated_text']}'")
            
            return jsonify({
                'success': True,
                'translated_text': result['translated_text'],
                'source_lang': result['source_lang'],
                'target_lang': result['target_lang']
            }), 200
        else:
            print(f"Translation failed: {result['error']}")
            
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        print(f"Unexpected error in translate endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@api_bp.route('/languages', methods=['GET'])
def get_languages():
    """
    Endpoint to get all supported languages
    """
    try:
        print("Languages request received")
        
        # Get languages from translator
        result = translator.get_languages()
        
        if result['success']:
            print(f"Returning {len(result['languages'])} languages")
            
            return jsonify({
                'success': True,
                'languages': result['languages']
            }), 200
        else:
            print(f"Failed to get languages: {result.get('error')}")
            
            return jsonify({
                'success': False,
                'error': result.get('error', 'Failed to load languages')
            }), 500
            
    except Exception as e:
        print(f"Unexpected error in languages endpoint: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify API is running
    """
    return jsonify({
        'success': True,
        'status': 'healthy',
        'message': 'Translation API is running',
        'version': '1.0.0'
    }), 200


@api_bp.route('/detect', methods=['POST'])
def detect_language():
    """
    Endpoint to detect language of text
    Expected JSON: {
        'text': 'text to detect'
    }
    """
    try:
        data = request.get_json()
        
        if not data or not data.get('text'):
            return jsonify({
                'error': 'No text provided'
            }), 400
        
        text = data.get('text')
        
        # Use translator to detect language (auto translate)
        result = translator.translate(text, 'auto', 'en')
        
        if result['success']:
            return jsonify({
                'success': True,
                'detected_lang': result['source_lang'],
                'text': text
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Error handlers
@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@api_bp.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 'Method not allowed'
    }), 405


@api_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500