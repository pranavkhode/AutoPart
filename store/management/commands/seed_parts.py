from django.core.management.base import BaseCommand
from store.models import Part


class Command(BaseCommand):
    help = 'Seed the product catalog for the AutoPart store.'

    def handle(self, *args, **options):
        parts_data = [
            {
                'name': 'Synthetic Engine Oil 5W-40 (4L)',
                'category': 'Engine',
                'price': 899.00,
                'part_number': 'AP-ENG-101',
                'stock': 45,
                'rating': 4.9,
                'icon': '⚙️',
                'description': 'Premium fully synthetic oil providing superior thermal stability and sludge protection for high-revving engines.'
            },
            {
                'name': 'Carbon Ceramic Front Brake Pads',
                'category': 'Brakes',
                'price': 1299.00,
                'part_number': 'AP-BRK-202',
                'stock': 30,
                'rating': 4.8,
                'icon': '🛑',
                'description': 'Ultra-low dust, noiseless ceramic formula engineered for supreme stopping power and extended rotor life.'
            },
            {
                'name': 'Heavy-Duty 12V 65Ah Car Battery',
                'category': 'Electrical',
                'price': 5499.00,
                'part_number': 'AP-ELE-303',
                'stock': 18,
                'rating': 4.9,
                'icon': '🔋',
                'description': 'Maintenance-free silver-alloy battery with high cold cranking amps (CCA) for instant starts in all climates.'
            },
            {
                'name': 'High-Flow Performance Air Filter',
                'category': 'Filters',
                'price': 499.00,
                'part_number': 'AP-FLT-404',
                'stock': 50,
                'rating': 4.7,
                'icon': '🌪️',
                'description': 'Multi-density cotton gauze filter providing up to 50% more airflow while trapping 99% of dust particles.'
            },
            {
                'name': 'Full Projector LED Matrix Headlight Set',
                'category': 'Lighting',
                'price': 1899.00,
                'part_number': 'AP-LGT-505',
                'stock': 22,
                'rating': 4.9,
                'icon': '💡',
                'description': 'Crystal-white 6000K daylight beam headlights with integrated dynamic daytime running lights (DRL).'
            },
            {
                'name': 'Laser-Iridium Spark Plugs (Pack of 4)',
                'category': 'Engine',
                'price': 599.00,
                'part_number': 'AP-ENG-106',
                'stock': 60,
                'rating': 4.8,
                'icon': '⚡',
                'description': 'Fine-wire iridium tip ensures maximum spark efficiency, faster acceleration, and optimal fuel economy.'
            },
            {
                'name': 'Gas-Charged Front Shock Absorbers',
                'category': 'Suspension',
                'price': 2799.00,
                'part_number': 'AP-SUS-601',
                'stock': 15,
                'rating': 4.8,
                'icon': '🔩',
                'description': 'Nitrogen gas-pressurized damping system delivering exceptional road handling and plush ride comfort.'
            },
            {
                'name': 'Dual European Disc Horn (115 dB)',
                'category': 'Electrical',
                'price': 799.00,
                'part_number': 'AP-ELE-308',
                'stock': 35,
                'rating': 4.7,
                'icon': '📢',
                'description': 'Robust weatherproof horn producing a commanding twin-tone sound for unmatched highway safety.'
            },
            {
                'name': 'Slotted & Ventilated Brake Rotors (Pair)',
                'category': 'Brakes',
                'price': 2199.00,
                'part_number': 'AP-BRK-209',
                'stock': 20,
                'rating': 4.9,
                'icon': '🔘',
                'description': 'Precision cross-drilled and slotted rotors for rapid heat dissipation and zero brake fade under heavy braking.'
            },
            {
                'name': 'Activated Carbon Cabin AC Filter',
                'category': 'Filters',
                'price': 649.00,
                'part_number': 'AP-FLT-410',
                'stock': 40,
                'rating': 4.6,
                'icon': '🍃',
                'description': 'Eliminates 99.7% of allergens, smog, pollen, and airborne odors inside your car\'s ventilation system.'
            },
            {
                'name': 'Dynamic Sequential LED Tail Light',
                'category': 'Lighting',
                'price': 2399.00,
                'part_number': 'AP-LGT-511',
                'stock': 14,
                'rating': 4.9,
                'icon': '🚨',
                'description': 'Smoked lens rear tail lights featuring modern flowing sequential turn indicators and bright brake lamps.'
            },
            {
                'name': 'Aerodynamic All-Season Wiper Blades (Set)',
                'category': 'Accessories',
                'price': 699.00,
                'part_number': 'AP-ACC-701',
                'stock': 55,
                'rating': 4.7,
                'icon': '🌧️',
                'description': 'Silicone coated beam blades that wipe streak-free and resist extreme heat, sub-zero cold, and UV damage.'
            },
        ]

        for item in parts_data:
            Part.objects.update_or_create(
                part_number=item['part_number'],
                defaults=item,
            )

        self.stdout.write(self.style.SUCCESS(f'Seeded {Part.objects.count()} parts.'))
