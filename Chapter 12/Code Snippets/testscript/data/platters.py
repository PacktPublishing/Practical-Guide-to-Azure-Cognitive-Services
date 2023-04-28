
platters = {
    'pasta_with_shellfish': {
        'attributes': {
            'qty':10, 
            'cuisine':'italian',
            'price':8
        },
        'dietary_attributes': {
            'vegan': False,
            'low_carb': False,
            'high_protein': False,
            'vegetarian': False,
            'low_fat': True,
            'low_sodium': True
        }
    },
    'sushi': {
        'attributes': {
            'qty':25, 
            'cuisine':'asian',
            'price':20
        }, 
        'dietary_attributes': {
            'vegan': False,
            'low_carb': True,
            'high_protein': True,
            'vegetarian': False,
            'low_fat': False,
            'low_sodium': False
        }
    },
    'seafood_salad': {
        'attributes': {
            'qty': 15,
            'cuisine': 'american',
            'price': 10
        }, 
        'dietary_attributes': {
            'vegan': False,
            'low_carb': False,
            'high_protein': True,
            'vegetarian': False,
            'low_fat': False,
            'low_sodium': False
        }
    },
    'lobster_rolls': {
        'attributes' : {
            'qty': 10,
            'cuisine': 'american',
            'price': 25
        }, 
        'dietary_attributes': {
            'vegan': True, 
            'low_carb': False,
            'high_protein': True,
            'vegetarian': True,
            'low_fat': False, 
            'low_sodium': False
        }
    },
    'vegetable_platter': {
        'attributes': {
            'qty': 50,
            'cuisine': 'american', 
            'price': 8
        },
        'dietary_attributes': {
            'vegan': True,
            'low_carb': True,
            'high_protein': False,
            'vegetarian': True,
            'low_fat': True,
            'low_sodium': True
        }
    }
}

def get_platters() -> dict:
    return platters