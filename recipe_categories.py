"""
Recipe Categories Dictionary
This file contains a comprehensive hierarchical structure of recipe categories.
"""

RECIPE_CATEGORIES = {
    'Breakfast & Brunch': {
        'Hot Breakfast': [
            'pancake',
            'waffle',
            'french toast',
            'omelette',
            'eggs benedict',
            'porridge'
        ],
        'Cold Breakfast': [
            'cereal',
            'granola',
            'yogurt parfait',
            'smoothie bowl'
        ],
        'Breakfast Sandwiches': [
            'bagel',
            'croissant',
            'breakfast burrito'
        ],
        'Breakfast Pastries': [
            'muffin',
            'scone',
            'danish'
        ]
    },
    'Appetizers & Snacks': {
        'Dips & Spreads': [
            'hummus',
            'guacamole',
            'salsa',
            'pate'
        ],
        'Finger Foods': [
            'wings',
            'nachos',
            'spring rolls',
            'tapas'
        ],
        'Soups & Broths': [
            'soup',
            'broth',
            'chowder',
            'bisque'
        ],
        'Salads': [
            'green salad',
            'pasta salad',
            'potato salad',
            'coleslaw'
        ]
    },
    'Main Dishes': {
        'Meat Dishes': {
            'Chicken': [
                'roast chicken',
                'chicken curry',
                'fried chicken'
            ],
            'Beef': [
                'steak',
                'beef stew',
                'hamburger',
                'meatloaf'
            ],
            'Pork': [
                'pork chop',
                'ham',
                'bacon',
                'pulled pork'
            ],
            'Lamb': [
                'lamb chop',
                'rack of lamb',
                "shepherd's pie"]
        },
        'Seafood'
        :
            {
                'Fish': [
                    'salmon',
                    'tuna',
                    'cod',
                    'halibut'
                ],
                'Shellfish': [
                    'shrimp',
                    'crab',
                    'lobster',
                    'mussels'
                ],
                'Mixed Seafood': [
                    'paella',
                    'seafood stew',
                    'fish soup'
                ]
            },
        'Vegetarian'
        :
            {
                'Tofu & Tempeh': [
                    'tofu stir-fry',
                    'tempeh curry'
                ],
                'Bean & Lentil': [
                    'bean stew',
                    'lentil soup',
                    'chickpea curry'
                ],
                'Vegetable Mains': [
                    'ratatouille',
                    'vegetable lasagna'
                ]
            },
        'Pasta & Noodles'
        :
            {
                'Italian Pasta': [
                    'spaghetti',
                    'lasagna',
                    'fettuccine'
                ],
                'Asian Noodles': [
                    'ramen',
                    'udon',
                    'pad thai'
                ],
                'Other Noodles': [
                    'mac and cheese',
                    'noodle casserole'
                ]
            }
    },
    'Side Dishes'
    :
        {
            'Grains': [
                'rice',
                'quinoa',
                'couscous',
                'pilaf'
            ],
            'Potatoes': [
                'mashed',
                'roasted',
                'french fries',
                'hash browns'
            ],
            'Vegetables': [
                'roasted vegetables',
                'steamed veggies',
                'grilled vegetables'
            ],
            'Breads': [
                'dinner rolls',
                'garlic bread',
                'cornbread',
                'naan'
            ]
        },
    'Desserts'
    :
        {
            'Cakes': {
                'Layer Cakes': [
                    'chocolate cake',
                    'vanilla cake',
                    'carrot cake'
                ],
                'Cheesecakes': [
                    'classic cheesecake',
                    'fruit cheesecake'
                ],
                'Special Cakes': [
                    'birthday cake',
                    'wedding cake',
                    'bundt cake'
                ]
            },
            'Cookies & Bars': [
                'chocolate chip cookies',
                'brownies',
                'cookie bars'
            ],
            'Pies & Tarts': [
                'apple pie',
                'fruit tart',
                'cream pie'
            ],
            'Puddings & Custards': [
                'bread pudding',
                'custard',
                'mousse'
            ],
            'Frozen Desserts': [
                'ice cream',
                'sorbet',
                'frozen yogurt'
            ]
        },
    'Beverages'
    :
        {
            'Hot Drinks': [
                'coffee',
                'tea',
                'hot chocolate',
                'mulled wine'
            ],
            'Cold Drinks': [
                'smoothie',
                'juice',
                'iced tea',
                'lemonade'
            ],
            'Cocktails': [
                'margarita',
                'mojito',
                'sangria'
            ],
            'Mocktails': [
                'virgin mojito',
                'fruit punch',
                'smoothie'
            ]
        },
    'Ethnic Cuisine'
    :
        {
            'Italian': [
                'pasta',
                'pizza',
                'risotto',
                'osso buco'
            ],
            'French': [
                'coq au vin',
                'ratatouille',
                'beef bourguignon'
            ],
            'Mexican': [
                'tacos',
                'enchiladas',
                'tamales',
                'fajitas'
            ],
            'Indian': [
                'curry',
                'biryani',
                'tandoori',
                'dal'
            ],
            'Chinese': [
                'stir-fry',
                'dim sum',
                'fried rice',
                'dumplings'
            ],
            'Japanese': [
                'sushi',
                'ramen',
                'tempura',
                'teriyaki'
            ],
            'Thai': [
                'pad thai',
                'curry',
                'tom yum',
                'satay'
            ],
            'Mediterranean': [
                'hummus',
                'falafel',
                'kebab',
                'moussaka'
            ],
            'Middle Eastern': [
                'shawarma',
                'tabbouleh',
                'fattoush',
                'dolma'
            ]
        },
    'Special Diet'
    :
        {
            'Vegetarian': [
                'vegetable curry',
                'veggie burger',
                'vegetable stir-fry'
            ],
            'Vegan': [
                'vegan chili',
                'vegan cake',
                'vegan pasta'
            ],
            'Gluten-Free': [
                'gluten-free bread',
                'gluten-free pasta'
            ],
            'Keto': [
                'keto bread',
                'keto dessert',
                'keto snack'
            ],
            'Low-Carb': [
                'cauliflower rice',
                'zucchini noodles'
            ],
            'Paleo': [
                'paleo bread',
                'paleo dessert',
                'paleo snack'
            ]
        },
    'Baking'
    :
        {
            'Breads': [
                'sourdough',
                'whole wheat',
                'rye bread',
                'baguette'
            ],
            'Pastries': [
                'croissant',
                'danish',
                'puff pastry'
            ],
            'Quick Breads': [
                'banana bread',
                'zucchini bread',
                'muffins'
            ],
            'Pies & Tarts': [
                'pie crust',
                'tart shell',
                'quiche'
            ]
        },
    'Seasonal'
    :
        {
            'Spring': [
                'spring salad',
                'asparagus dishes',
                'Easter dishes'
            ],
            'Summer': [
                'barbecue',
                'grilled dishes',
                'summer salads'
            ],
            'Fall': [
                'pumpkin dishes',
                'apple dishes',
                'Thanksgiving'
            ],
            'Winter': [
                'winter soups',
                'holiday dishes',
                'Christmas'
            ]
        },
    'Breakfast & Brunch'
    :
        {
            'Hot Breakfast': {
                'Egg Dishes': [
                    'omelette',
                    'scrambled eggs',
                    'eggs benedict',
                    'frittata'
                ],
                'Griddle Favorites': [
                    'pancakes',
                    'waffles',
                    'french toast',
                    'crepes'
                ],
                'Hot Cereals': [
                    'porridge',
                    'oatmeal',
                    'cream of wheat',
                    'grits'
                ],
                'Breakfast Meats': [
                    'bacon',
                    'sausage',
                    'ham',
                    'canadian bacon'
                ]
            },
            'Cold Breakfast': {
                'Cold Cereals': [
                    'granola',
                    'muesli',
                    'cereal bowls'
                ],
                'Yogurt Dishes': [
                    'yogurt parfait',
                    'fruit and yogurt',
                    'overnight oats'
                ],
                'Smoothie Bowls': [
                    'acai bowl',
                    'protein smoothie bowl',
                    'fruit smoothie bowl'
                ],
                'Fruit Dishes': [
                    'fruit salad',
                    'fruit and cheese plate'
                ]
            },
            'Breakfast Sandwiches': {
                'Classic': [
                    'egg sandwich',
                    'breakfast burrito',
                    'bagel sandwich'
                ],
                'Croissant Based': [
                    'croissant sandwich',
                    'pain au chocolat'
                ],
                'Healthy Options': [
                    'whole grain wrap',
                    'protein sandwich'
                ]
            },
            'Breakfast Pastries': {
                'Sweet': [
                    'muffins',
                    'scones',
                    'danish',
                    'cinnamon rolls'
                ],
                'Savory': [
                    'cheese scones',
                    'savory muffins',
                    'breakfast pockets'
                ]
            }
        },
    'Appetizers & Starters'
    :
        {
            'Cold Appetizers': {
                'Dips & Spreads': [
                    'hummus',
                    'guacamole',
                    'salsa',
                    'tzatziki'
                ],
                'Cheese Plates': [
                    'cheese board',
                    'charcuterie',
                    'antipasto'
                ],
                'Vegetable Platters': [
                    'crudités',
                    'vegetable dips'
                ],
                'Cold Seafood': [
                    'shrimp cocktail',
                    'smoked salmon',
                    'ceviche'
                ]
            },
            'Hot Appetizers': {
                'Finger Foods': [
                    'wings',
                    'mozzarella sticks',
                    'spring rolls'
                ],
                'Stuffed Items': [
                    'stuffed mushrooms',
                    'jalapeño poppers'
                ],
                'Fried Appetizers': [
                    'calamari',
                    'tempura',
                    'croquettes'
                ],
                'Baked Appetizers': [
                    'bruschetta',
                    'flatbreads',
                    'quesadillas'
                ]
            },
            'Soups & Broths': {
                'Clear Soups': [
                    'consommé',
                    'bone broth',
                    'vegetable broth'
                ],
                'Cream Soups': [
                    'cream of mushroom',
                    'potato soup',
                    'bisque'
                ],
                'Chunky Soups': [
                    'minestrone',
                    'vegetable soup',
                    'chowder'
                ],
                'Cold Soups': [
                    'gazpacho',
                    'vichyssoise',
                    'cold cucumber soup'
                ]
            },
            'Salads': {
                'Green Salads': [
                    'garden salad',
                    'caesar salad',
                    'greek salad'
                ],
                'Grain Salads': [
                    'quinoa salad',
                    'couscous salad',
                    'rice salad'
                ],
                'Protein Salads': [
                    'chicken salad',
                    'tuna salad',
                    'egg salad'
                ],
                'Vegetable Salads': [
                    'coleslaw',
                    'potato salad',
                    'bean salad'
                ]
            }
        },
    'Main Courses'
    :
        {
            'Meat Dishes': {
                'Beef': {
                    'Steaks': [
                        'ribeye',
                        'filet mignon',
                        'sirloin',
                        't-bone'
                    ],
                    'Ground Beef': [
                        'hamburgers',
                        'meatloaf',
                        'meatballs'
                    ],
                    'Roasts': [
                        'prime rib',
                        'pot roast',
                        'beef wellington'
                    ],
                    'Stews': [
                        'beef stew',
                        'beef bourguignon',
                        'goulash'
                    ]
                },
                'Pork': {
                    'Chops': [
                        'pork chops',
                        'stuffed pork chops'
                    ],
                    'Roasts': [
                        'pork loin',
                        'pork tenderloin',
                        'ham'
                    ],
                    'Ground Pork': [
                        'sausages',
                        'pork meatballs'
                    ],
                    'Ribs': [
                        'baby back ribs',
                        'spare ribs',
                        'country ribs'
                    ]
                },
                'Poultry': {
                    'Chicken': [
                        'roast chicken',
                        'fried chicken',
                        'chicken curry'
                    ],
                    'Turkey': [
                        'roast turkey',
                        'turkey breast',
                        'ground turkey'
                    ],
                    'Duck': [
                        'roast duck',
                        'duck breast',
                        'duck confit'
                    ],
                    'Game Birds': [
                        'quail',
                        'pheasant',
                        'cornish hen'
                    ]
                },
                'Lamb': {
                    'Chops': [
                        'lamb chops',
                        'rack of lamb'
                    ],
                    'Roasts': [
                        'leg of lamb',
                        'lamb shoulder'
                    ],
                    'Ground Lamb': [
                        'lamb meatballs',
                        'shepherd',
                        'lamb stew',

                    ]},
                'Game Meats':

                    {

                        'Venison': [
                            'venison steak',
                            'venison stew'
                        ],
                        'Rabbit': [
                            'rabbit stew',
                            'braised rabbit'
                        ],
                        'Wild Boar': [
                            'wild boar ragù',
                            'wild boar roast'
                        ],
                        'Bison': [
                            'bison burger',
                            'bison steak'
                        ]
                    }
            },
            'Seafood'
            :
                {
                    'Fish': {
                        'Fatty Fish': [
                            'salmon',
                            'tuna',
                            'mackerel',
                            'trout'
                        ],
                        'White Fish': [
                            'cod',
                            'halibut',
                            'sea bass',
                            'tilapia'
                        ],
                        'Flat Fish': [
                            'sole',
                            'flounder',
                            'plaice'
                        ],
                        'Fresh Water Fish': [
                            'catfish',
                            'perch',
                            'bass'
                        ]
                    },
                    'Shellfish': {
                        'Crustaceans': [
                            'shrimp',
                            'crab',
                            'lobster',
                            'crayfish'
                        ],
                        'Mollusks': [
                            'mussels',
                            'clams',
                            'oysters',
                            'scallops'
                        ],
                        'Cephalopods': [
                            'squid',
                            'octopus',
                            'cuttlefish'
                        ]
                    },
                    'Mixed Seafood': {
                        'Stews': [
                            'bouillabaisse',
                            'cioppino',
                            'seafood stew'
                        ],
                        'Paella': [
                            'seafood paella',
                            'mixed paella'
                        ],
                        'Pasta': [
                            'seafood pasta',
                            'frutti di mare'
                        ]
                    }
                },
            'Vegetarian & Vegan'
            :
                {
                    'Plant-Based Proteins': {
                        'Tofu Dishes': [
                            'tofu stir-fry',
                            'tofu scramble',
                            'mapo tofu'
                        ],
                        'Tempeh': [
                            'tempeh stir-fry',
                            'tempeh bacon',
                            'tempeh curry'
                        ],
                        'Seitan': [
                            'seitan steak',
                            'seitan stir-fry',
                            'seitan roast'
                        ],
                        'TVP': [
                            'vegetarian chili',
                            'vegetarian bolognese'
                        ]
                    },
                    'Legume Based': {
                        'Bean Dishes': [
                            'black bean burgers',
                            'refried beans',
                            'bean stew'
                        ],
                        'Lentil Dishes': [
                            'lentil soup',
                            'dal',
                            'lentil loaf'
                        ],
                        'Chickpea Dishes': [
                            'falafel',
                            'chickpea curry',
                            'hummus'
                        ]
                    },
                    'Vegetable Mains': {
                        'Stuffed Vegetables': [
                            'stuffed peppers',
                            'stuffed zucchini'
                        ],
                        'Vegetable Gratins': [
                            'eggplant parmesan',
                            'vegetable gratin'
                        ],
                        'Roasted Vegetables': [
                            'roasted vegetable medley',
                            'buddha bowls'
                        ]
                    }
                },
            'Pasta & Noodles'
            :
                {
                    'Italian Pasta': {
                        'Long Pasta': [
                            'spaghetti',
                            'fettuccine',
                            'linguine'
                        ],
                        'Short Pasta': [
                            'penne',
                            'rigatoni',
                            'fusilli'
                        ],
                        'Stuffed Pasta': [
                            'ravioli',
                            'tortellini',
                            'cannelloni'
                        ],
                        'Baked Pasta': [
                            'lasagna',
                            'baked ziti',
                            'pasta al forno'
                        ]
                    },
                    'Asian Noodles': {
                        'Chinese': [
                            'lo mein',
                            'chow mein',
                            'dan dan noodles'
                        ],
                        'Japanese': [
                            'ramen',
                            'udon',
                            'soba'
                        ],
                        'Korean': [
                            'japchae',
                            'ramyeon'
                        ],
                        'Southeast Asian': [
                            'pad thai',
                            'pancit',
                            'mie goreng'
                        ]
                    }
                }
        },
    'Side Dishes'
    :
        {
            'Starches': {
                'Potatoes': {
                    'Mashed': [
                        'classic mashed',
                        'garlic mashed',
                        'loaded mashed'
                    ],
                    'Roasted': [
                        'roast potatoes',
                        'hasselback potatoes'
                    ],
                    'Fried': [
                        'french fries',
                        'home fries',
                        'potato wedges'
                    ],
                    'Gratins': [
                        'potato gratin',
                        'scalloped potatoes'
                    ]
                },
                'Rice': {
                    'White Rice': [
                        'steamed rice',
                        'jasmine rice',
                        'basmati rice'
                    ],
                    'Brown Rice': [
                        'steamed brown rice',
                        'brown rice pilaf'
                    ],
                    'Wild Rice': [
                        'wild rice blend',
                        'wild rice pilaf'
                    ],
                    'Rice Dishes': [
                        'risotto',
                        'rice pilaf',
                        'fried rice'
                    ]
                },
                'Other Grains': {
                    'Quinoa': [
                        'quinoa pilaf',
                        'quinoa salad'
                    ],
                    'Couscous': [
                        'moroccan couscous',
                        'israeli couscous'
                    ],
                    'Ancient Grains': [
                        'farro',
                        'barley',
                        'bulgur'
                    ]
                }
            },
            'Vegetables': {
                'Roasted': [
                    'roasted root vegetables',
                    'roasted brussels sprouts'
                ],
                'Steamed': [
                    'steamed broccoli',
                    'steamed carrots'
                ],
                'Sautéed': [
                    'sautéed mushrooms',
                    'sautéed spinach'
                ],
                'Grilled': [
                    'grilled vegetables',
                    'grilled corn'
                ]
            }
        },
    'Desserts & Baking'
    :
        {
            'Cakes': {
                'Layer Cakes': {
                    'Classic': [
                        'chocolate cake',
                        'vanilla cake',
                        'carrot cake'
                    ],
                    'Special': [
                        'red velvet',
                        'black forest',
                        'opera cake'
                    ],
                    'Wedding': [
                        'tiered cake',
                        'fondant cake'
                    ],
                    'Holiday': [
                        'christmas cake',
                        'birthday cake'
                    ]
                },
                'Cheesecakes': {
                    'Baked': [
                        'new york cheesecake',
                        'basque cheesecake'
                    ],
                    'No-Bake': [
                        'no-bake cheesecake',
                        'chocolate cheesecake'
                    ],
                    'Flavored': [
                        'fruit cheesecake',
                        'specialty cheesecake'
                    ]
                },
                'Other Cakes': {
                    'Pound Cakes': [
                        'classic pound cake',
                        'marble cake'
                    ],
                    'Bundt Cakes': [
                        'bundt cake variations'
                    ],
                    'Coffee Cakes': [
                        'streusel coffee cake',
                        'fruit coffee cake'
                    ],
                    'Sheet Cakes': [
                        'texas sheet cake',
                        'birthday sheet cake'
                    ]
                }
            },
            'Cookies & Bars': {
                'Drop Cookies': {
                    'Classic': [
                        'chocolate chip',
                        'oatmeal raisin',
                        'sugar cookies'
                    ],
                    'Special': [
                        'snickerdoodles',
                        'peanut butter cookies'
                    ],
                    'Holiday': [
                        'christmas cookies',
                        'gingerbread'
                    ]
                },
                'Bar Cookies': {
                    'Brownies': [
                        'classic brownies',
                        'fudge brownies'
                    ],
                    'Blondies': [
                        'butterscotch blondies',
                        'white chocolate'
                    ],
                    'Other Bars': [
                        'lemon bars',
                        'seven layer bars'
                    ]
                },
                'Specialty Cookies': {
                    'Sandwich': [
                        'macarons',
                        'whoopie pies',
                        'oreo-style'
                    ],
                    'Shaped': [
                        'shortbread',
                        'biscotti',
                        'spritz cookies'
                    ],
                    'No-Bake': [
                        'no-bake cookies',
                        'rice krispie treats'
                    ]
                }
            },
            'Pies & Tarts': {
                'Fruit Pies': {
                    'Single Crust': [
                        'pumpkin pie',
                        'custard pie'
                    ],
                    'Double Crust': [
                        'apple pie',
                        'cherry pie',
                        'berry pie'
                    ],
                    'Crumb Top': [
                        'dutch apple pie',
                        'crumble top pie'
                    ]
                },
                'Cream Pies': {
                    'Custard Based': [
                        'banana cream',
                        'coconut cream'
                    ],
                    'Chocolate': [
                        'chocolate cream',
                        'french silk'
                    ],
                    'Other': [
                        'key lime pie',
                        'lemon meringue'
                    ]
                },
                'Tarts': {
                    'Sweet': [
                        'fruit tart',
                        'chocolate tart'
                    ],
                    'Savory': [
                        'quiche',
                        'vegetable tart'
                    ],
                    'Mini': [
                        'tartlets',
                        'mini pies'
                    ]
                }
            },
            'Bread Baking': {
                'Yeast Breads': {
                    'White Breads': [
                        'french bread',
                        'italian bread'
                    ],
                    'Whole Grain': [
                        'whole wheat',
                        'multigrain'
                    ],
                    'Enriched': [
                        'brioche',
                        'challah',
                        'babka'
                    ]
                },
                'Quick Breads': {
                    'Sweet': [
                        'banana bread',
                        'zucchini bread'
                    ],
                    'Savory': [
                        'beer bread',
                        'cheese bread'
                    ],
                    'Muffins': [
                        'blueberry muffins',
                        'corn muffins'
                    ]
                },
                'Specialty Breads': {
                    'Flatbreads': [
                        'naan',
                        'pita',
                        'focaccia'
                    ],
                    'Sourdough': [
                        'sourdough bread',
                        'sourdough variations'
                    ],
                    'Artisan': [
                        'artisan loaves',
                        'specialty shapes'
                    ]
                }
            }
        },
    'Beverages'
    :
        {
            'Hot Drinks': {
                'Coffee': {
                    'Brewed': [
                        'drip coffee',
                        'french press',
                        'pour over'
                    ],
                    'Espresso Based': [
                        'latte',
                        'cappuccino',
                        'americano'
                    ],
                    'Specialty': [
                        'turkish coffee',
                        'vietnamese coffee'
                    ]
                },
                'Tea': {
                    'Black Tea': [
                        'english breakfast',
                        'earl grey'
                    ],
                    'Green Tea': [
                        'sencha',
                        'matcha'
                    ],
                    'Herbal': [
                        'chamomile',
                        'mint tea',
                        'rooibos'
                    ]
                },
                'Hot Chocolate': {
                    'Classic': [
                        'hot cocoa',
                        'drinking chocolate'
                    ],
                    'Flavored': [
                        'peppermint hot chocolate',
                        'mexican hot chocolate'
                    ],
                    'Special': [
                        'white hot chocolate',
                        'spiced hot chocolate'
                    ]
                }
            },
            'Cold Drinks': {
                'Smoothies': {
                    'Fruit': [
                        'berry smoothie',
                        'tropical smoothie'
                    ],
                    'Green': [
                        'green smoothie',
                        'vegetable blend'
                    ],
                    'Protein': [
                        'protein smoothie',
                        'meal replacement'
                    ]
                },
                'Iced Drinks': {
                    'Iced Coffee': [
                        'cold brew',
                        'iced latte'
                    ],
                    'Iced Tea': [
                        'sweet tea',
                        'iced green tea'
                    ],
                    'Frozen': [
                        'frappuccino',
                        'slushie'
                    ]
                },
                'Fresh Juices': {
                    'Fruit Juices': [
                        'orange juice',
                        'apple juice'
                    ],
                    'Vegetable Juices': [
                        'green juice',
                        'carrot juice'
                    ],
                    'Mixed': [
                        'juice blends',
                        'detox juices'
                    ]
                }
            },
            'Cocktails': {
                'Classic': {
                    'Gin Based': [
                        'martini',
                        'gin and tonic',
                        'negroni'
                    ],
                    'Whiskey Based': [
                        'old fashioned',
                        'manhattan',
                        'whiskey sour'
                    ],
                    'Vodka Based': [
                        'moscow mule',
                        'cosmopolitan'
                    ],
                    'Rum Based': [
                        'mojito',
                        'daiquiri',
                        'piña colada'
                    ]
                },
                'Modern': {
                    'Signature': [
                        'custom cocktails',
                        'house specials'
                    ],
                    'Molecular': [
                        'foam drinks',
                        'smoking cocktails'
                    ],
                    'Fusion': [
                        'asian-inspired',
                        'latin fusion'
                    ]
                }
            },
            'Mocktails': {
                'Virgin Classics': [
                    'virgin mojito',
                    'shirley temple'
                ],
                'Wellness Drinks': [
                    'kombucha',
                    'kefir',
                    'probiotic drinks'
                ],
                'Special Occasion': [
                    'non-alcoholic champagne',
                    'party punches'
                ]
            }
        },
    'World Cuisines'
    :
        {
            'European': {
                'Italian': {
                    'Pasta': [
                        'pasta dishes',
                        'risotto'
                    ],
                    'Pizza': [
                        'neapolitan',
                        'sicilian'
                    ],
                    'Regional': [
                        'tuscan',
                        'sicilian',
                        'northern'
                    ]
                },
                'French': {
                    'Classic': [
                        'coq au vin',
                        'beef bourguignon'
                    ],
                    'Pastry': [
                        'croissants',
                        'eclairs'
                    ],
                    'Regional': [
                        'provençal',
                        'alsatian'
                    ]
                },
                'Mediterranean': {
                    'Greek': [
                        'moussaka',
                        'souvlaki',
                        'spanakopita'
                    ],
                    'Spanish': [
                        'paella',
                        'tapas',
                        'gazpacho'
                    ],
                    'Turkish': [
                        'kebab',
                        'pide',
                        'lahmacun'
                    ]
                }
            },
            'Asian': {
                'East Asian': {
                    'Chinese': {
                        'Cantonese': [
                            'dim sum',
                            'stir-fry'
                        ],
                        'Sichuan': [
                            'mapo tofu',
                            'kung pao'
                        ],
                        'Other Regions': [
                            'northern',
                            'eastern'
                        ]
                    },
                    'Japanese': {
                        'Sushi': [
                            'nigiri',
                            'maki',
                            'sashimi'
                        ],
                        'Noodles': [
                            'ramen',
                            'udon',
                            'soba'
                        ],
                        'Other': [
                            'tempura',
                            'teriyaki',
                            'donburi'
                        ]
                    },
                    'Korean': {
                        'BBQ': [
                            'bulgogi',
                            'galbi'
                        ],
                        'Stews': [
                            'kimchi jjigae',
                            'sundubu'
                        ],
                        'Other': [
                            'bibimbap',
                            'japchae'
                        ]
                    }
                },
                'Southeast Asian': {
                    'Thai': [
                        'pad thai',
                        'curry',
                        'tom yum'
                    ],
                    'Vietnamese': [
                        'pho',
                        'banh mi',
                        'spring rolls'
                    ],
                    'Malaysian': [
                        'laksa',
                        'rendang',
                        'satay'
                    ]
                },
                'South Asian': {
                    'Indian': {
                        'North Indian': [
                            'butter chicken',
                            'naan'
                        ],
                        'South Indian': [
                            'dosa',
                            'idli',
                            'sambar'
                        ],
                        'Other Regions': [
                            'bengali',
                            'gujarati'
                        ]
                    },
                    'Pakistani': [
                        'biryani',
                        'karahi',
                        'nihari'
                    ],
                    'Sri Lankan': [
                        'curry',
                        'hoppers',
                        'kottu'
                    ]
                }
            },
            'Americas': {
                'North American': {
                    'American': [
                        'burgers',
                        'hot dogs',
                        'mac and cheese'
                    ],
                    'Southern': [
                        'fried chicken',
                        'bbq',
                        'soul food'
                    ],
                    'Tex-Mex': [
                        'tacos',
                        'fajitas',
                        'enchiladas'
                    ]
                },
                'Latin American': {
                    'Mexican': [
                        'authentic mexican',
                        'street food'
                    ],
                    'Brazilian': [
                        'feijoada',
                        'pão de queijo'
                    ],
                    'Peruvian': [
                        'ceviche',
                        'lomo saltado'
                    ]
                }
            },
            'African': {
                'North African': [
                    'moroccan',
                    'egyptian',
                    'tunisian'
                ],
                'West African': [
                    'nigerian',
                    'ghanaian',
                    'senegalese'
                ],
                'East African': [
                    'ethiopian',
                    'eritrean',
                    'somali'
                ]
            },
            'Middle Eastern': {
                'Lebanese': [
                    'hummus',
                    'tabbouleh',
                    'shawarma'
                ],
                'Persian': [
                    'kebab',
                    'tahdig',
                    'ghormeh sabzi'
                ],
                'Turkish': [
                    'pide',
                    'lahmacun',
                    'kebab'
                ]
            }
        },
    'Special Diets'
    :
        {
            'Vegetarian & Vegan': {
                'Vegetarian Mains': {
                    'Protein Rich': [
                        'bean dishes',
                        'lentil dishes',
                        'tofu dishes'
                    ],
                    'Veggie Based': [
                        'stuffed vegetables',
                        'vegetable curries'
                    ],
                    'Meat Alternatives': [
                        'seitan dishes',
                        'tempeh dishes'
                    ]
                },
                'Vegan Specific': {
                    'Dairy Alternatives': [
                        'vegan cheese',
                        'vegan milk',
                        'vegan butter'
                    ],
                    'Egg Alternatives': [
                        'vegan egg substitutes',
                        'aquafaba recipes'
                    ],
                    'Vegan Baking': [
                        'vegan cakes',
                        'vegan cookies',
                        'vegan breads'
                    ]
                }
            },
            'Gluten-Free': {
                'Breads & Baking': {
                    'Breads': [
                        'gluten-free bread',
                        'flatbreads'
                    ],
                    'Pastries': [
                        'gluten-free pastries',
                        'pies'
                    ],
                    'Desserts': [
                        'cakes',
                        'cookies',
                        'brownies'
                    ]
                },
                'Main Dishes': {
                    'Pasta Alternatives': [
                        'zoodles',
                        'rice noodles',
                        'quinoa pasta'
                    ],
                    'Grain Alternatives': [
                        'cauliflower rice',
                        'quinoa dishes'
                    ]
                }
            },
            'Keto & Low-Carb': {
                'Keto Mains': {
                    'Meat Based': [
                        'fatty meats',
                        'bacon dishes'
                    ],
                    'Seafood': [
                        'fatty fish',
                        'shellfish'
                    ],
                    'Vegetarian': [
                        'low-carb vegetarian'
                    ]
                },
                'Keto Sides': {
                    'Vegetables': [
                        'cauliflower dishes',
                        'zucchini dishes'
                    ],
                    'Salads': [
                        'keto salads',
                        'low-carb slaws'
                    ]
                },
                'Keto Desserts': {
                    'Sweet Treats': [
                        'keto cookies',
                        'keto cakes'
                    ],
                    'Fat Bombs': [
                        'chocolate fat bombs',
                        'nut butter bombs'
                    ]
                }
            },
            'Paleo': {
                'Mains': [
                    'meat dishes',
                    'fish dishes',
                    'egg dishes'
                ],
                'Sides': [
                    'vegetable sides',
                    'fruit dishes'
                ],
                'Snacks': [
                    'nuts and seeds',
                    'paleo bars'
                ]
            },
            'Whole30': {
                'Compliant Meals': [
                    'approved proteins',
                    'vegetable dishes'
                ],
                'Whole30 Sides': [
                    'compliant sides',
                    'salads'
                ],
                'Sauces & Dressings': [
                    'compliant sauces',
                    'dressings'
                ]
            }
        },
    'Seasonal & Holiday'
    :
        {
            'Spring': {
                'Easter': {
                    'Main Dishes': [
                        'ham',
                        'lamb'
                    ],
                    'Side Dishes': [
                        'spring vegetables',
                        'potato dishes'
                    ],
                    'Desserts': [
                        'easter cookies',
                        'spring cakes'
                    ]
                },
                'Spring Produce': {
                    'Asparagus Dishes': [
                        'roasted asparagus',
                        'asparagus soup'
                    ],
                    'Pea Recipes': [
                        'fresh pea dishes',
                        'pea soup'
                    ],
                    'Spring Greens': [
                        'salad greens',
                        'spring herbs'
                    ]
                }
            },
            'Summer': {
                'Grilling & BBQ': {
                    'Meats': [
                        'grilled steaks',
                        'bbq chicken'
                    ],
                    'Seafood': [
                        'grilled fish',
                        'shrimp skewers'
                    ],
                    'Vegetables': [
                        'grilled vegetables',
                        'corn on the cob'
                    ]
                },
                'Summer Produce': {
                    'Tomato Dishes': [
                        'fresh tomato recipes',
                        'gazpacho'
                    ],
                    'Corn Recipes': [
                        'corn dishes',
                        'corn salads'
                    ],
                    'Berry Dishes': [
                        'berry desserts',
                        'fresh fruit dishes'
                    ]
                },
                'Picnic & Outdoor': {
                    'Portable Mains': [
                        'sandwiches',
                        'wraps'
                    ],
                    'Salads': [
                        'potato salad',
                        'pasta salad'
                    ],
                    'Snacks': [
                        'portable snacks',
                        'finger foods'
                    ]
                }
            },
            'Fall': {
                'Thanksgiving': {
                    'Turkey': [
                        'roast turkey',
                        'turkey alternatives'
                    ],
                    'Side Dishes': [
                        'stuffing',
                        'cranberry sauce'
                    ],
                    'Desserts': [
                        'pumpkin pie',
                        'apple pie'
                    ]
                },
                'Fall Produce': {
                    'Pumpkin': [
                        'pumpkin dishes',
                        'pumpkin desserts'
                    ],
                    'Apple': [
                        'apple recipes',
                        'apple desserts'
                    ],
                    'Root Vegetables': [
                        'root vegetable dishes'
                    ]
                }
            },
            'Winter': {
                'Christmas': {
                    'Main Dishes': [
                        'roasts',
                        'ham'
                    ],
                    'Side Dishes': [
                        'christmas sides',
                        'roasted vegetables'
                    ],
                    'Desserts': [
                        'christmas cookies',
                        'fruit cake'
                    ]
                },
                'New Year': {
                    'Party Food': [
                        'appetizers',
                        'finger foods'
                    ],
                    'Traditional': [
                        'lucky foods',
                        'new year dishes'
                    ]
                },
                'Winter Comfort': {
                    'Soups & Stews': [
                        'hearty soups',
                        'winter stews'
                    ],
                    'Casseroles': [
                        'winter casseroles',
                        'baked dishes'
                    ],
                    'Hot Drinks': [
                        'hot chocolate',
                        'mulled drinks'
                    ]
                }
            }
        },
    'Preserves & Canning'
    :
        {
            'Jams & Jellies': {
                'Fruit Jams': {
                    'Berry': [
                        'strawberry jam',
                        'raspberry jam'
                    ],
                    'Stone Fruit': [
                        'peach jam',
                        'plum jam'
                    ],
                    'Citrus': [
                        'marmalade',
                        'citrus preserves'
                    ]
                },
                'Specialty Preserves': {
                    'Herb Infused': [
                        'herb jams',
                        'savory preserves'
                    ],
                    'Exotic': [
                        'tropical fruit jams',
                        'unique combinations'
                    ]
                }
            },
            'Pickles & Ferments': {
                'Pickled Vegetables': {
                    'Cucumber Pickles': [
                        'dill pickles',
                        'bread & butter'
                    ],
                    'Other Vegetables': [
                        'pickled carrots',
                        'pickled peppers'
                    ]
                },
                'Fermented Foods': {
                    'Vegetables': [
                        'sauerkraut',
                        'kimchi'
                    ],
                    'Other': [
                        'kombucha',
                        'fermented drinks'
                    ]
                }
            },
            'Sauces & Condiments': {
                'Tomato Based': [
                    'tomato sauce',
                    'salsa',
                    'ketchup'
                ],
                'Fruit Based': [
                    'chutneys',
                    'fruit sauces'
                ],
                'Specialty': [
                    'relishes',
                    'mustards'
                ]
            }
        },
    'Sauces & Condiments'
    :
        {
            'Basic Sauces': {
                'Mother Sauces': {
                    'White Sauces': [
                        'bechamel',
                        'veloute'
                    ],
                    'Brown Sauces': [
                        'espagnole',
                        'demi-glace'
                    ],
                    'Other Classics': [
                        'hollandaise',
                        'tomato sauce'
                    ]
                },
                'Pan Sauces': [
                    'wine reduction',
                    'cream sauce',
                    'butter sauce'
                ],
                'Emulsified Sauces': [
                    'mayonnaise',
                    'aioli',
                    'vinaigrette'
                ]
            },
            'World Sauces': {
                'Asian': {
                    'Chinese': [
                        'sweet & sour',
                        'hoisin',
                        'oyster sauce'
                    ],
                    'Japanese': [
                        'teriyaki',
                        'ponzu',
                        'katsu sauce'
                    ],
                    'Southeast Asian': [
                        'peanut sauce',
                        'fish sauce',
                        'curry paste'
                    ]
                },
                'European': {
                    'Italian': [
                        'pesto',
                        'marinara',
                        'alfredo'
                    ],
                    'French': [
                        'remoulade',
                        'bearnaise',
                        'roux based'
                    ]
                },
                'Latin': [
                    'mole',
                    'chimichurri',
                    'sofrito'
                ]
            },
            'Condiments': {
                'Table Condiments': [
                    'ketchup',
                    'mustard',
                    'relish'
                ],
                'Spreads': [
                    'hummus',
                    'tapenade',
                    'compound butter'
                ],
                'Spice Blends': [
                    'dry rubs',
                    'seasoning mixes'
                ]
            }
        },
    'Techniques & Methods'
    :
        {
            'Cooking Methods': {
                'Dry Heat': {
                    'Baking': [
                        'bread baking',
                        'pastry techniques'
                    ],
                    'Roasting': [
                        'meat roasting',
                        'vegetable roasting'
                    ],
                    'Grilling': [
                        'direct heat',
                        'indirect heat'
                    ]
                },
                'Moist Heat': {
                    'Boiling': [
                        'pasta cooking',
                        'vegetable blanching'
                    ],
                    'Steaming': [
                        'dim sum',
                        'vegetable steaming'
                    ],
                    'Braising': [
                        'meat braising',
                        'vegetable braising'
                    ]
                },
                'Fat-Based': {
                    'Sautéing': [
                        'pan frying',
                        'stir-frying'
                    ],
                    'Deep Frying': [
                        'batters',
                        'breading techniques'
                    ],
                    'Confit': [
                        'meat confit',
                        'vegetable confit'
                    ]
                }
            },
            'Preparation Methods': {
                'Knife Skills': {
                    'Basic Cuts': [
                        'dice',
                        'julienne',
                        'chiffonade'
                    ],
                    'Butchery': [
                        'meat cutting',
                        'fish filleting'
                    ],
                    'Specialty': [
                        'garnishes',
                        'decorative cuts'
                    ]
                },
                'Mixing Methods': {
                    'Baking': [
                        'creaming',
                        'folding',
                        'kneading'
                    ],
                    'General': [
                        'emulsifying',
                        'blending',
                        'whipping'
                    ]
                }
            },
            'Advanced Techniques': {
                'Molecular Gastronomy': [
                    'spherification',
                    'foams',
                    'gels'
                ],
                'Fermentation': [
                    'bread',
                    'vegetables',
                    'beverages'
                ],
                'Smoking & Curing': [
                    'meat smoking',
                    'fish curing'
                ]
            }
        }
}


def get_ingredient_categories(categories):
    """
    Extracts a dictionary of ingredient categories from the given recipe categories.

    Args:
        categories: The dictionary containing the recipe categories.

    Returns:
        A dictionary where keys are category names and values are sets of ingredients.
    """
    ingredient_categories = {}
    for category_name, subcategories in categories.items():
        if isinstance(subcategories, dict):  # If it's a nested dictionary
            ingredient_categories[category_name] = set()
            for sub_category_name, ingredients in subcategories.items():
                ingredient_categories[category_name].update(ingredients)
        else:
            ingredient_categories[category_name] = set(subcategories)

    return ingredient_categories


# Get the ingredient categories
ingredient_categories = get_ingredient_categories(RECIPE_CATEGORIES)

# Print the ingredient categories
for category, ingredients in ingredient_categories.items():
    print(f"{category}: {sorted(list(ingredients))}")