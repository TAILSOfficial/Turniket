"""
Django settings for DjangoQR project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path


# if not hasattr(sys, 'KTSK_Vid_Cap') and os.environ['VIDCAP_RUN'] == 'TRUE':
#     import cv2
#     import time
#     import threading

#     class VideoCamera(object):
#         def __init__(self, cam_id: int):
#             self.video = cv2.VideoCapture(cam_id)
#             self.grabbed, self.frame = self.video.read()
#             threading.Thread(target=self.update, args=()).start()

#         def __del__(self):
#             self.video.release()

#         def get_frame(self):
#             image = self.frame
#             ret, jpeg = cv2.imencode('.jpg', image)
#             return jpeg.tobytes()

#         def update(self):
#             while True:
#                 (self.grabbed, self.frame) = self.video.read()
#                 time.sleep(0.1)

#     setattr(sys, 'KTSK_Vid_Cap', (VideoCamera(0), VideoCamera(1)))

VIDCAP_SERVER_IP = '127.0.0.1'
VIDCAP_0_PORT = 5672
VIDCAP_1_PORT = VIDCAP_0_PORT + 1


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = Path(__file__).resolve().parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-m1d)d(i!!(peri2aa!g-0n9bkcavhaopaduk43cs3i^6!=m^a%'
CIPHER_KEY = b'V6WsODocoiU4hqHS562R_1XvIgwujhcRSUglOeN1360='
IMAGE_PATH = BASE_DIR / 'qr_codes'
SAVE_IMAGE = True

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'video.apps.VideoConfig',
    'downloads.apps.DownloadsConfig',
    'QR_Generator.apps.QrGeneratorConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DjangoQR.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            PROJECT_ROOT / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'DjangoQR.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'PASSWORD': '',
    #     'HOST': '127.0.0.1',
    #     'PORT': '3306',
    #     'USER': 'root',
    #     'NAME': 'skud',
    # },
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    PROJECT_ROOT / "static",
]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'qr_codes'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'