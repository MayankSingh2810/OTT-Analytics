import random

# ==========================================================
# USER BEHAVIOUR PROFILES
# ==========================================================

USER_PROFILES = {

    "Casual":{

        "weight":35,

        "monthly_watch_range":(15,50),

        "completion_range":(35,70),

        "preferred_devices":[
            "Mobile",
            "Tablet"
        ],

        "preferred_genres":[
            "Comedy",
            "Romance",
            "Animation"
        ]

    },

    "Regular":{

        "weight":40,

        "monthly_watch_range":(60,140),

        "completion_range":(70,90),

        "preferred_devices":[
            "Laptop",
            "Smart TV"
        ],

        "preferred_genres":[
            "Drama",
            "Thriller",
            "Crime"
        ]

    },

    "Binge":{

        "weight":20,

        "monthly_watch_range":(180,350),

        "completion_range":(90,100),

        "preferred_devices":[
            "Smart TV"
        ],

        "preferred_genres":[
            "Action",
            "Sci-Fi",
            "Thriller"
        ]

    },

    "Family":{

        "weight":5,

        "monthly_watch_range":(40,90),

        "completion_range":(75,100),

        "preferred_devices":[
            "Smart TV"
        ],

        "preferred_genres":[
            "Family",
            "Kids",
            "Animation"
        ]

    }

}

# ==========================================================

def assign_profile():

    names = list(USER_PROFILES.keys())

    weights = [
        USER_PROFILES[p]["weight"]
        for p in names
    ]

    profile = random.choices(
        names,
        weights=weights,
        k=1
    )[0]

    return profile


# ==========================================================

def get_profile(profile_name):

    return USER_PROFILES[profile_name]