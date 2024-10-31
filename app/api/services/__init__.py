from tensorflow.keras.models import load_model
from ...logger import log

log('Loading squat model...', level='INFO')
squat_model = load_model('app/api/services/squat_model.keras')
