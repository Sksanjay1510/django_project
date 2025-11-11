#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from home.models import Product

def create_default_products():
    print("Creating default Tecosoft products...")
    
    # Eagle Pro
    eagle_pro, created = Product.objects.get_or_create(
        name="Eagle Pro",
        defaults={
            'slug': 'eagle-pro',
            'product_type': 'gateway',
            'short_description': 'A robust IIOT gateway for large-scale industrial automation, real-time monitoring, and advanced analytics.',
            'description': '''Join our core development team to architect and build scalable IoT solutions and digital twin platforms that power Industry 4.0 transformations for manufacturing clients worldwide.

The Eagle Pro is designed for enterprise-level industrial operations requiring high-performance processing, advanced analytics, and seamless integration with existing systems.''',
            'price': 2999.00,
            'features': [
                'High-performance processing',
                'Multi-protocol support', 
                'Real-time analytics',
                'Edge AI capabilities',
                'Quad-core ARM processor',
                '8GB RAM, 64GB storage',
                'WiFi 6, 5G ready',
                'Enterprise security'
            ],
            'is_featured': True,
            'is_active': True
        }
    )
    if created:
        print("✓ Created Eagle Pro")
    else:
        print("✓ Eagle Pro already exists")
    
    # Eagle Mini
    eagle_mini, created = Product.objects.get_or_create(
        name="Eagle Mini",
        defaults={
            'slug': 'eagle-mini',
            'product_type': 'gateway',
            'short_description': 'A compact IIOT device for small to medium enterprises, enabling seamless device connectivity and data collection.',
            'description': '''Perfect for small to medium enterprises looking to embrace Industry 4.0 without the complexity of larger systems.

The Eagle Mini offers essential IoT gateway functionality in a compact, cost-effective package that's easy to deploy and manage.''',
            'price': 1299.00,
            'features': [
                'Compact form factor',
                'Low power consumption',
                'Easy installation',
                'Cost-effective',
                'Dual-core processor',
                '2GB RAM, 16GB storage',
                'WiFi 5, 4G LTE',
                'PoE powered'
            ],
            'is_featured': True,
            'is_active': True
        }
    )
    if created:
        print("✓ Created Eagle Mini")
    else:
        print("✓ Eagle Mini already exists")
    
    # Sparrow
    sparrow, created = Product.objects.get_or_create(
        name="Sparrow",
        defaults={
            'slug': 'sparrow',
            'product_type': 'sensor',
            'short_description': 'An agile IIOT sensor node for edge data acquisition, wireless communication, and smart integration.',
            'description': '''The Sparrow sensor network provides flexible, wireless monitoring capabilities for industrial environments where traditional wired solutions are impractical.

Designed for long-term deployment with minimal maintenance, the Sparrow offers reliable data collection in challenging industrial conditions.''',
            'price': 299.00,
            'features': [
                'Wireless connectivity',
                'Battery powered',
                'Multiple sensors',
                'Mesh networking',
                'ARM Cortex-M4',
                '512KB RAM, 4MB flash',
                'LoRaWAN, BLE',
                '5+ year battery life'
            ],
            'is_featured': False,
            'is_active': True
        }
    )
    if created:
        print("✓ Created Sparrow")
    else:
        print("✓ Sparrow already exists")
    
    print(f"\nTotal active products: {Product.objects.filter(is_active=True).count()}")
    print("Default products created successfully!")

if __name__ == '__main__':
    create_default_products()