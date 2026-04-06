import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_django_api.settings')
print('DJANGO_SETTINGS_MODULE', os.environ['DJANGO_SETTINGS_MODULE'])
import django
django.setup()
print('django setup complete')
import blogapp.serializers as s
print('loaded', s)
print('has BlogSerializer', hasattr(s, 'BlogSerializer'))
print('attrs', [a for a in dir(s) if 'Blog' in a])
