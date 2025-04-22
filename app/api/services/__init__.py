from tensorflow.keras.models import load_model
from ...logger import log

log('Loading models...', level='INFO')
squat_model = load_model('app/api/services/squat_model.keras')
bicep_curl_model = load_model('app/api/services/bicep_model.keras')
front_raise_model = load_model('app/api/services/front_raise_model.keras')