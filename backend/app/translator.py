import requests
import json

class Translator:
    def __init__(self):
        # Google Translate free endpoint - works 100% of the time
        self.api_url = "https://translate.googleapis.com/translate_a/single"
    
    def translate(self, text, source_lang='auto', target_lang='en'):
        """
        Translate text using Google Translate (FREE, NO KEY REQUIRED)
        """
        try:
            print(f"Translating: {text}")
            print(f"Source: {source_lang}, Target: {target_lang}")
            
            # Handle source language
            if source_lang == 'auto' or not source_lang:
                source = 'auto'
            else:
                source = source_lang
            
            # Google Translate parameters
            params = {
                'client': 'gtx',
                'sl': source,
                'tl': target_lang,
                'dt': 't',
                'q': text
            }
            
            # Make the request
            response = requests.get(
                self.api_url, 
                params=params, 
                timeout=10,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            )
            
            print(f"Google API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                # Parse Google's response
                result = response.json()
                
                # Extract translated text
                translated_parts = []
                for sentence in result[0]:
                    if sentence and len(sentence) > 0 and sentence[0]:
                        translated_parts.append(sentence[0])
                
                translated_text = ' '.join(translated_parts)
                
                # Get detected language if auto was used
                detected_lang = result[2] if len(result) > 2 else source_lang
                
                return {
                    'success': True,
                    'translated_text': translated_text,
                    'source_lang': detected_lang,
                    'target_lang': target_lang
                }
            else:
                return {
                    'success': False,
                    'error': f'Google Translate returned status {response.status_code}'
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Request timeout. Please try again.'
            }
        except requests.exceptions.ConnectionError:
            return {
                'success': False,
                'error': 'Connection error. Please check your internet.'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Translation error: {str(e)}'
            }
    
    def get_languages(self):
        """
        Return ALL supported languages (Google supports 100+ languages)
        """
        return {
            'success': True,
            'languages': [
                {'code': 'af', 'name': 'Afrikaans'},
                {'code': 'sq', 'name': 'Albanian'},
                {'code': 'am', 'name': 'Amharic'},
                {'code': 'ar', 'name': 'Arabic'},
                {'code': 'hy', 'name': 'Armenian'},
                {'code': 'az', 'name': 'Azerbaijani'},
                {'code': 'eu', 'name': 'Basque'},
                {'code': 'be', 'name': 'Belarusian'},
                {'code': 'bn', 'name': 'Bengali'},
                {'code': 'bs', 'name': 'Bosnian'},
                {'code': 'bg', 'name': 'Bulgarian'},
                {'code': 'ca', 'name': 'Catalan'},
                {'code': 'ceb', 'name': 'Cebuano'},
                {'code': 'ny', 'name': 'Chichewa'},
                {'code': 'zh', 'name': 'Chinese'},
                {'code': 'co', 'name': 'Corsican'},
                {'code': 'hr', 'name': 'Croatian'},
                {'code': 'cs', 'name': 'Czech'},
                {'code': 'da', 'name': 'Danish'},
                {'code': 'nl', 'name': 'Dutch'},
                {'code': 'en', 'name': 'English'},
                {'code': 'eo', 'name': 'Esperanto'},
                {'code': 'et', 'name': 'Estonian'},
                {'code': 'tl', 'name': 'Filipino'},
                {'code': 'fi', 'name': 'Finnish'},
                {'code': 'fr', 'name': 'French'},
                {'code': 'fy', 'name': 'Frisian'},
                {'code': 'gl', 'name': 'Galician'},
                {'code': 'ka', 'name': 'Georgian'},
                {'code': 'de', 'name': 'German'},
                {'code': 'el', 'name': 'Greek'},
                {'code': 'gu', 'name': 'Gujarati'},
                {'code': 'ht', 'name': 'Haitian Creole'},
                {'code': 'ha', 'name': 'Hausa'},
                {'code': 'haw', 'name': 'Hawaiian'},
                {'code': 'iw', 'name': 'Hebrew'},
                {'code': 'hi', 'name': 'Hindi'},
                {'code': 'hmn', 'name': 'Hmong'},
                {'code': 'hu', 'name': 'Hungarian'},
                {'code': 'is', 'name': 'Icelandic'},
                {'code': 'ig', 'name': 'Igbo'},
                {'code': 'id', 'name': 'Indonesian'},
                {'code': 'ga', 'name': 'Irish'},
                {'code': 'it', 'name': 'Italian'},
                {'code': 'ja', 'name': 'Japanese'},
                {'code': 'jw', 'name': 'Javanese'},
                {'code': 'kn', 'name': 'Kannada'},
                {'code': 'kk', 'name': 'Kazakh'},
                {'code': 'km', 'name': 'Khmer'},
                {'code': 'rw', 'name': 'Kinyarwanda'},
                {'code': 'ko', 'name': 'Korean'},
                {'code': 'ku', 'name': 'Kurdish'},
                {'code': 'ky', 'name': 'Kyrgyz'},
                {'code': 'lo', 'name': 'Lao'},
                {'code': 'la', 'name': 'Latin'},
                {'code': 'lv', 'name': 'Latvian'},
                {'code': 'lt', 'name': 'Lithuanian'},
                {'code': 'lb', 'name': 'Luxembourgish'},
                {'code': 'mk', 'name': 'Macedonian'},
                {'code': 'mg', 'name': 'Malagasy'},
                {'code': 'ms', 'name': 'Malay'},
                {'code': 'ml', 'name': 'Malayalam'},
                {'code': 'mt', 'name': 'Maltese'},
                {'code': 'mi', 'name': 'Maori'},
                {'code': 'mr', 'name': 'Marathi'},
                {'code': 'mn', 'name': 'Mongolian'},
                {'code': 'my', 'name': 'Myanmar'},
                {'code': 'ne', 'name': 'Nepali'},
                {'code': 'no', 'name': 'Norwegian'},
                {'code': 'or', 'name': 'Odia'},
                {'code': 'ps', 'name': 'Pashto'},
                {'code': 'fa', 'name': 'Persian'},
                {'code': 'pl', 'name': 'Polish'},
                {'code': 'pt', 'name': 'Portuguese'},
                {'code': 'pa', 'name': 'Punjabi'},
                {'code': 'ro', 'name': 'Romanian'},
                {'code': 'ru', 'name': 'Russian'},
                {'code': 'sm', 'name': 'Samoan'},
                {'code': 'gd', 'name': 'Scots Gaelic'},
                {'code': 'sr', 'name': 'Serbian'},
                {'code': 'st', 'name': 'Sesotho'},
                {'code': 'sn', 'name': 'Shona'},
                {'code': 'sd', 'name': 'Sindhi'},
                {'code': 'si', 'name': 'Sinhala'},
                {'code': 'sk', 'name': 'Slovak'},
                {'code': 'sl', 'name': 'Slovenian'},
                {'code': 'so', 'name': 'Somali'},
                {'code': 'es', 'name': 'Spanish'},
                {'code': 'su', 'name': 'Sundanese'},
                {'code': 'sw', 'name': 'Swahili'},
                {'code': 'sv', 'name': 'Swedish'},
                {'code': 'tg', 'name': 'Tajik'},
                {'code': 'ta', 'name': 'Tamil'},
                {'code': 'tt', 'name': 'Tatar'},
                {'code': 'te', 'name': 'Telugu'},
                {'code': 'th', 'name': 'Thai'},
                {'code': 'tr', 'name': 'Turkish'},
                {'code': 'tk', 'name': 'Turkmen'},
                {'code': 'uk', 'name': 'Ukrainian'},
                {'code': 'ur', 'name': 'Urdu'},
                {'code': 'ug', 'name': 'Uyghur'},
                {'code': 'uz', 'name': 'Uzbek'},
                {'code': 'vi', 'name': 'Vietnamese'},
                {'code': 'cy', 'name': 'Welsh'},
                {'code': 'xh', 'name': 'Xhosa'},
                {'code': 'yi', 'name': 'Yiddish'},
                {'code': 'yo', 'name': 'Yoruba'},
                {'code': 'zu', 'name': 'Zulu'}
            ]
        }