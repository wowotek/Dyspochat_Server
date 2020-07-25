import random

def generate_pseudonym() -> str:
    names = [
        "Alex", "Alessia", "Alexander", "Ava", "Amelia", "Aiden", "Anthony", "Aurel", "Aurelia",
        "Brad", "Belford", "Buds", "Bona", "Bandhu", "Budi", "Bambang", "Brian", "Benita",
        "Conny", "Cris", "Chris", "Cadell",
        "Dennis", "Dolly", "Donnel", "Dewangga",
        "Efra", "Essburn", "Emperor", "Ester", "Ernest", "Erlangga",
        "Fris", "Freskel", "Folly", "Felix", "Fiona",
        "Gerald", "Gerson", "Garfield", "Gabriele", "Garry", "Gunawan",
        "Hansen", "Hansel", "Hans", "Harold",
        "Ivon", "Ivory", "Irvan", "Irvin", "Ignatius", "Immanuel", "Ibrahim", "Ipin",
        "Jerry", "James", "Jason", "Jonathan", "Junio",
        "Klein", "Kevin", "Kalvin", "Kurt",
        "Larry", "Lucas", "Laurentius", "Legnin", "Latchuba",
        "Mahmud", "Mohammed", "Mubarak",
        "Neva", "Nadia", "Nindy", "Nonita", "Novensky", "Ngolan",
        "Orlando", "Ovel", "Olivia", "Octa", "O'neil",
        "Picard", "Palulu", "Pamela", "Pipo", "Pipit", "Puspitasari",
        "Quinn", "Quinncy", "Quentin", "Qory", "Quaid", "Quade",
        "Ronald", "Rachel", "Rando", "Reva", "Riance",
        "Stephen", "Steven", "Stephan", "Sterling", "Stirling", "Scarlett", "Samantha", "Stella", "Sadie", "Sophia",
        "Theresa", "Theresia", "Timothy", "Tom", "Tiffany",
        "Ujang", "Uyung", "Upin",
        "Vicky", "Victoria", "Vanessa", "Victor", "Valentina", "Valerie",
        "Wowotek", "William", "Weshburn", "Wawan",
        "Xavier", "Xander", "Xiomora", "Xavi", "Xyla"
    ]
    ending = ["", "ly", "y", "", "ia", "ny", "er", "r", "", "s", "sy", "", "ox", "my", "ma", "", "mo", "ni", "sky", "", ""]

    # First name 50% change to have ending
    for _ in range(100):
        chance = random.randint(0, 100)
    if chance >= 50:
        first = names[random.randint(0, len(names)-1)]
    else:
        first = names[random.randint(0, len(names)-1)] + ending[random.randint(0, len(ending)-1)]
    # Second name 20% change to have ending
    for _ in range(100):
        chance = random.randint(0, 100)
    if chance >= 80:
        second = names[random.randint(0, len(names)-1)]
    else:
        second = names[random.randint(0, len(names)-1)] + ending[random.randint(0, len(ending)-1)]

    return first + " " + second