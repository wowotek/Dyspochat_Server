#!/usr/bin/python3
import random, sys

_AFFIXES = [
    "A ", "Ab ", "Abu ", "Al ", "Alam ",
    "Bar ", "Bath ", "Bat ", "Bet ", "Bin ",
    "Da ", "Das ", "De", "Degli ", "Dele ", "Del ", "Der ", "Di", "Dos ", "Du",
    "E ", "El ", "Erch ",
    "Fetch ", "Fitz ",
    "i ", "i"
    "Kil ",
    "La ",
    "Le ",
    "Lille ",
    "Lu ",
    "M'", "Mac", "Mc", "Mck", "Mhic", "Mic",
    "Mala ",
    "Mellom ", "Myljom ",
    "Na", "Ned ", "Nedre ", "Neder ", "Nic ", "Ni", "Nord ", "Norr ", "Ny",
    "O ", "Opp", "Ost ",
    "Pour ", "Putra ", "Putri ",
    "Setia ", "Stor ", "Syndre ",
    "Ter ", "Tre ",
    "Ua ", "Ui'", "Upp",
    "Van ", "Verch ", "Vest ", "Vesle ", "Vetle ", "von ", "von und zu ",
    "zu ",
    "I Made ", "I Gusti ", "I Gede ", "Ketut ", "Tjok ", "Tjokorda Istri ", "Ida I Dewa ", "Dewa Agung ", "I Dewa ", "I Dewa Ayu ", "Desak ",
    "I Gusti Ngurah ", "I Gusti Ayu ", "Anak Agung ", "Anak Agung Ayu ", "Anak Agung Istri ", "Tjokorda "
]
_NAMES = [
    'alex', 'alessia', 'alexander', 'ava', 'amelia', 'aiden', 'anthony', 'aurel', 'aurelia', 'avalon', 'avaskyl', "alexeyev", "ali", "adun", "ahmad",
    'brad', 'belford', 'buds', 'bona', 'bandhu', 'budi', 'bambang', 'brian', 'benita',
    'conny', 'cris', 'chris', 'cadell',
    'dennis', 'dolly', 'donnel', 'dewangga', 'diriw',
    'efra', 'essburn', 'emperor', 'ester', 'ernest', 'erlangga', "edo",
    'fris', 'freskel', 'folly', 'felix', 'fiona',
    'gerald', 'gerson', 'garfield', 'gabriele', 'garry', 'gunawan',
    'hansen', 'hansel', 'hans', 'harold', 'hermawan', 'helmi', 'hendri',
    'ivon', 'ivory', 'irvan', 'irvin', 'ignatius', 'immanuel', 'ibrahim', 'ipin',
    'jerry', 'james', 'jason', 'jonathan', 'junio',
    'klein', 'kevin', 'kalvin', 'kurt', 'kunto', 'kentu', 'kabuto',
    'larry', 'lucas', 'laurentius', 'legnin', 'latchuba',
    'mahmud', 'mohammed', 'mubarak', 'mamat', 'maggie', 'milan', 'mindityas',
    'neva', 'nadia', 'nindy', 'nonita', 'novensky', 'ngolan',
    'orlando', 'ovel', 'olivia', 'octa', "o'neil", 'oliver', 'oval', 'opick',
    'picard', 'palulu', 'pamela', 'pipo', 'pipit', 'puspitasari',
    'quinn', 'quinncy', 'quentin', 'qory', 'quaid', 'quade',
    'ronald', 'rachel', 'rando', 'reva', 'riance',
    'stephen', 'steven', 'stephan', 'sterling', 'stirling', 'scarlett', 'samantha', 'stella', 'sadie', 'sophia',
    'theresa', 'theresia', 'timothy', 'tom', 'tiffany', "thalib",
    'ujang', 'uyung', 'upin', 'ucup', 'ucok', 'uut', 'usman', 'udin',
    'vicky', 'victoria', 'vanessa', 'victor', 'valentina', 'valerie',
    'wowotek', 'william', 'weshburn', 'wawan', 'wirid',
    'xavier', 'xander', 'xiomora', 'xavi', 'xyla',
]
_SUFFIXES = [
    "a", "ya", "ac", "ach", "aei", "ago", "aitis", "aite", "aty", "aj", "ak", "an", "al", "and", "ano", "ange", "anu", "ar", "awan",
    "berg", "by", "bee",
    "chi", "chian", "chek", "ckas", "cki", "cock", "cox", 
    "datter", "din", "dotter", "dottir", "dze", "dzki",
    "e", "eanu", "eau", "eault", "ec", "ee", "eff", "eiro", "ek", "ell", "el", "ema", "ems", "enko", "ens", "er", "ese", "ers", "et", "eva", "ez",
    "fia", "fi", "fy", "ffy", "fleth", "felth", "fleet",
    "gil",
    "i", "ia", "ian", "iak", "ic", "ich", "ides", "ier", "ik", "ikh", "in", "ing", "ipa", "is", "iu", "ius", "iv",
    "j",
    "ka", "kan", "ke", "kin", "ko", "kus", "kvist", "kyzy",
    "le", "lein", "li", "lin", "litz",
    "man", "mand", "maz", "men", "man", "ment",
    "ne", "nen", "nik", "nova", "novas", "novo", "ny", "nezhad", "nejad", "nejhad", "nyi",
    "off", "oglu", "ok", "ois", "oy", "on", "onak", "onis", "os", "opoulos", "ot", "ou", "ov", "ouf", "oui", "ovo",
    "pour", "poor", "putra", "putri",
    "quin",
    "s", "sen", "shvili", "skas", "ski", "skiy", "ska", "skoy", "sma", "son", "sson", "stad", "stein", "strom",
    "tae", "tabar", "tzki", "tzky",
    "uk", "ulea", "ulis", "uly", "unas", "uulu", 
    "vich", "vych", "vic", "vicius", "vics", "wala", "wan", "wati", "wi",
    "y", "ycz", "ynas", "ys", "ysz", "za",
    "zadeh", "zadegan",
]
_SURNAME = [
    "Eizenbaums", "Safire", "Reis", "Salim", "Sudono", "Sunyoto", "Morgenstern",
    "Batubara", "Sitohang", "Pandjaitan", "Siregar", "Sitorus", "Sinaga", "Ujung", "Sembiring", "Pohan", "Hasibuan", "Padang Batanghari", "Pane",
    "Asegaf", "Abdat", "Anoez", "Abudan", "Al Abd Baqi", "Abdat", "Anoez", "Abudan", "Abunumay", "Adrebi", "Aglag", "Alabeid", "Algadri", "Al Qadri",
    "Alhasin", "Alisalim", "Almakkawy", "Ambadar", "Arfan", "Arghubi", "Askar", "Assa'di", "Assaidi", "Assaili", "Assegaf", "Assewed", "Assidawi",
    "Assiry", "Assyabibi", "Assyaiban", "Assyiblie", "Attuwi", "Al Abd Baqi", "Al Aidid", "Al Allan/ Alland", "Al Ali Al Hajj", "Al Ali Bin Jabir", "At Tamimi",
    "Al Amar", "Al Amri", "Al Amudi", "Al Askarie", "Al Attas/ Alatas/ Alatthas", "Al Audah", "Al Aulagi", "Al Aydrus", "Al Ba Abud", "Al Ba Faraj",
    "Al Ba Harun", "Al Ba Raqbah", "Al Baar", "Al Bagdadi/ Al Baghdhadhi", "Al Bahar", "Al Baiti", "Al Bajrai", "Al Bakri", "Al Bal Faqih", "Al Baldjoen",
    "Al Balghaist", "Al Balgon", "Al Baljun", "Al Balkhi", "Al Bantan", "Al Bantani", "Al Barak", "Al Barhim", "Al Bas", "Al Batati", "Al Bawahab", "Al Waini",
    "Al Bawazier", "Al Bin Jindan", "Al Bin Sahal", "Al Bin Semit", "Al Bin Yahya", "Al Dzeban", "Al Fad'aq", "Al Fagih", "Al Falugah", "Al Gaiti",
    "Al Habsyie", "Al Haddad", "Al Haddar", "Al Hamid", "Al Hasani", "Al Hassan", "Al Hasyim", "Al Hayaza'", "Al Hayaze", "Al Hilabi", "Al Jabri", "Al Jahwari",
    "Al Jaidi", "Al Jufrie", "Al Junaid", "Al Katiri", "Al Katsiri", "Al Khatib", "Al Kherid", "Al Khubais", "Al Madhir", "Al Mahdali", "Al Makky", "Al Masyhur",
    "Al Mathar", "Al Muchdor", "Al Muhaddam", "Al Munawwar", "Al Musawa", "Al Mutahhar", "Al Nahdi", "Al Naqieb", "Al Qadiri", "Al Rasyidi", "Al Wachdin", "As shatry",
    "Abednego", "Abel", "Abishalom", "Abarua", "Abraham", "Abrahams", "Abrahamsz", "Acher", "Ademiar", "Adeo", "Adjahary", "Adolf", "Adonis", "Adrian", "Adrianz", "Adrians",
    "Adriaansz", "Adrianus", "Adtjas", "Afaratu", "Afdan", "Affifudin", "Afflu", "Afitu", "Aghogo", "Agudjir", "Agustinus", "Agustis", "Agustyen", "Ahab", "Ahad", "Ahar", 
    "Ahiyate", "Ahlaro", "Ahnary", "Ahudora", "Ahuluheluw", "Ahver", "Aihery", "Ailerbitu", "Ailerkora", "Ainoli", "Aipassa", "Airory", "Aitonam", "Ajawaila", "Akasian", "Akbar", 
    "Akel", "Akerina", "Akhir", "Akiaar", "Akiary", "Akihary", "Akipu", "Aklafin", "Akohillo", "Akollo", "Akse", "Aktalora", "Akyuwen", "Al", "Albram", "Al Chatib", 
    "Alain", "Alakaman", "Ambar", "Amboki", "Amergebi", "Amesz", "Ameth", "Amorhosea", "Amos", "Ambrosilla", "Amunnopunjo", "Amuntoda", "Anakotta", "Anakotapary", 
    "Anamova", "Anas", "Andea", "Andies", "Andino", "Andres", "Andrias", "Andries", "Angelbert", "Angels", "Angganois", "Anggoda", "Angkotta", "Angkotamony", "Angkotasan", 
    "Angky", "Angwarmase", "Anidla", "Aninjola", "Anjarang", "belw", "Bachta", "Baco", "Bacory", "Badelwair", "Badmas", "Baersady", "Bager", "Bahasoan", "Bachmid", 
    "Bain", "Barons", "Baros", "Barry", "Bartolomeus", "Barutressy", "Barza", "Basafin", "Basalamah", "Bayan", "Basry", "Bassay", "Basteirn", "Bastian", "Batawi", "Batceran", 
    "Batcori", "Batdjedelik", "Batfeny", "Batfian", "Batfin", "Batfyor", "Batho", "Batidas", "Batkunde", "Batlajery", "Batlayeri", "Batlyol", "Batlyeware", 
    "Batmomolin", "Batserin", "Batsira", "Batsyory", "Battisina", "Batto", "Batwael", "Batuwael", "Batyefwal", "Bazar", "Bazari", "Bazergan", "Beay", "Beffers", "Beilohy", 
    "Beisilla", "Bejarano", "Belay", "Belder", "Belegur", "Belen", "Belena", "Beruat", "Besan", "Bessy", "Betaubun", "Betoky", "Bianchi", "Bicoli", "Biet", "Bilahmar", 
    "Bille", "Bin Agiel", "Binbaso", "Binnendijk", "Bin Sulaiman", "Binsye", "Bin Umar", "Birahy", "Bision", "Blijlevens", "Blukora", "Bobero", "Bobeto", "Boca", "Bochi", 
    "Boften", "Boger", "Bohoekoe Nam Radja", "Boina", "Boinsera", "Boky", "Bolisara", "Bonara", "Bonay", "Bonsalya", "Boogart", "Borges", "Boritnaban", "Borlak", "Bormassa", 
    "Boroson", "Borrel", "Borolla", "Borut", "Bosko", "Bothmir", "Botter", "Boufakar", "Bouwens", "Breekland", "Bremeer", "Bria", "Bruhns", "Bruigom", "Buano", "Buarlely", 
    "Buarnirun", "Buchaer", "Bugal", "Builder", "Buiswarin", "Bukop", "Buloglabna", "Bulohroy", "Bunjanan", "Burnama", "Bwariat", "Caarsten", "Caian", "Callahan", 
    "Calvari", "Calvio", "Camerling", "Canu (Tjanoe)", "Cao", "Capires", "Capobianco", "Carelsz", "Carliano", "Carmiago", "Carolus", "Castera", "Castillo", 
    "Castro", "Cecene", "Ceda", "Chadiman", "Chakenota", "Chatib", "Cheiongers", "Chello", "Chera", "Chevais", "Chostantinus", "Chrisaldo", "Christabel", 
    "Christen", "Christiaan", "Christo", "Christoffel", "Christopher", "Chuleyevo", "Cie", "Claus", "Cobis", "Coendraad", "Cohen", "Collins", "Collouse", 
    "Cols", "Coly", "Comul", "Conoras", "Consina", "Corputty", "Corneille", "Cornelis", "Correa", "Courbois", "Coveka", "Cramer", "Crola", "Cuana", "Cupoano", 
    "Eleujaan", "Elewarin", "Eleuwarin", "Eli", "Elier", "Elmas", "Elanor", "Elath", "El-Betan", "Eliesen", "Elkel", "Elle", "Ellias", "Elfarin", "Elminero", "Elsiba", 
    "Elsoin", "Elsunan", "Eluwart", "Elte", "Elwarin", "Ely", "Elly", "Ellys", "Elyaan", "Embisa", "Emola", "Emor", "Empra", "Emray", "Engel", "Engko", "England", 
    "Engro", "Enrico", "Enos", "Entamoin", "Entaren", "Entero", "Enus", "Eoch", "Erbabley", "Eremerd", "Erlely", "Erloor", "Ernas", "Eropley", "Ersaprosy", "Erwanno", 
    "Esomar", "Esrev", "Esron", "Esserey", "Essy", "Eteva", "Etha", "Etiory", "Etlegar", "Etrial", "Ette", "Etwiory", "Eugara", "Evaay", "Evamutan", "Evert", "Ewaldo", 
    "Eyale", "Eykendorp", "Ezauw", "Fenyapwain", "Feoh", "Fer", "Ferlin", "Ferdinandus", "Fernandez", "Fernando", "Fernayan", "Ferreira", "Fasanlaw", "Fesanrey", 
    "Fifaona", "Fillips", "Filmort", "Firanty", "Firley", "Firloy", "Fitron", "Fiumdity", "Flohr", "Flontin", "Flora", "Floris", "Flory", "Fofid", "Fol", "Folatfindu", 
    "Foor", "Foraly", "Fordatkosu", "Forfan", "Forinti", "Formes", "Forno", "Forwet", "Fower", "Frabes", "Frainuny", "Francis", "Franciz", "Frandescolli", "Frans", 
    "Franciscus", "Franssisco", "Fransz", "Frare", "Freely", "Freitas", "Froim", "Fuarisin", "Fuller", "Fun", "Fursima", "Futraun", "Futural", "Futuray", "Gabian", 
    "Gelfara", "Genno", "George", "Geraldi", "Geras", "Geresi", "Gerrits", "Geslauw", "Ghosaloi", "Gigengack", "Gill", "Gisberthus", "Gisedemo", "Geassa", "Gedoa", "Geers", 
    "Gerrits", "Gerson", "Giay", "Gilbert", "Gimon", "Ginzel", "Gitler", "Giop", "Giovani", "Givano", "Gobuino", "Godlieb", "Godlief", "Goeslaw", "Gogerino", "Gogus", "Gohao", 
    "Gohir", "Goain", "Goleo", "Golf", "Goliho", "Golle", "Golorem", "Gomies", "Gommies", "Gonia", "Gonimasela", "Gonsalves", "Gonzales", "Gordan", "Gorfan", 
    "Gosain", "Gosem", "Gosjen", "Goszal", "Gotterys", "Goulaf", "Graf", "Granada", "Grasselly", "Greni", "Griapon", "Grisel", "Grobbe", "Guraici", "Gudam", "Gurgurem", 
    "Guriton", "Gurium", "Guslao", "Gustam", "Gwedjor", "Habel", "Habibu", "Hadi", "Hadler", "Hahijary", "Hahuly", "Hahury", "Haikutty", "Hair", "Haire", 
    "Hakamuly", "Hakapaä", "Halamury", "Halapiry", "Halattu", "Halawane", "Halawet", "Halirat", "Haliwela", "Hallatu", "Hallauw", "Halos", "Haltere", "Haluly", "Haluna", 
    "Haluruk", "Hamangau", "Hambaly", "Hamdun", "Hameda", "Hamel", "Hammar", "Han", "Hanavi", "Hanca", "Hanegraaf", "Hangewa", "Hanorsian", "Haprekkunarey", "Haratilu", 
    "Harbel", "Harbelubun", "Hardenberg", "Haris", "Harihaya", "Harlen", "Harmen", "Harmusial", "Harnia", "Hartala", "Hartety", "Hartog", "Hartsteen", "Hasbers", 
    "Haspers", "Hassanussy", "Hatalaibessy", "Hatane", "Hatapayo", "Hataul", "Hatharua", "Hathelhela", "Hatlessy", "Hatopa", "Hatsama", "Hattu", "Hatuala", "Hatuleli",
    "Hatuluayo", "Hatumena", "Hommy", "Hong", "Hong", "Honorsian", "Hoor", "Hoppus", "Horaszon", "Hordembun", "Horeyaam", "Horhoruw", "Horosio", "Horsael", "Horsair",
    "Horst", "Horts", "Horu", "Hosea", "Host", "Hotjum", "Huath", "Hüffner", "Huibers", "Huik", "Huily", "Huka", "Hukom", "Hukumahu", "Hukunala", "Hulihulis", "Huliselan",
    "Hulkiawar", "Hully", "Hungan", "Huniake", "Hunila", "Huninhatu", "Hunitetu", "Hunsam", "Hurasan", "Hurlean", "Hurry", "Hursepuny", "Hursina", "Hursup", "Hurta",
    "Hurwiora", "Husein", "Husen", "Hutubessy", "Hutuely", "Huwaa", "Huwae", "Huwaeol", "Intopiana", "Ipaenin", "Ipol", "Irapanussa", "Iraratu", "Irkey", "Iriley",
    "Irloy", "Irmuply", "Isaac", "Iscandario", "Ischa", "Ishak", "Iskiwar", "Ismael", "Isran", "Istia", "Isto", "Italilpessy", "Itamar", "Itapaty", "Itramury", "Iwamony",
    "Iwane", "Iwar", "Iyarmasse", "Iyay", "Iyon", "Izaach", "Izack", "Jacob", "Jacobs", "Jacobus", "Jadera", "Jaflaun", "Jaftoran", "Jahya", "Jallo", "Jalmav", "Jamangun",
    "Jambormias", "Jamco", "Jamlean", "Jamrewav", "Jamsaref", "Jonain", "Jonathan", "Jones", "Jongker", "Jooce", "Joostensz", "Joris", "Jorna", "Joseph", "Jotlely",
    "Jozias", "Juarsa", "Julian", "Julis", "Jurben", "Jurcales", "Jurley", "Justinus",
]

CONFIG = {
    "have_affix": 25,
    "have_suffix": 25,
    "name_reversed": 6.25,
    "have_second_name": 90,
    "have_surname": 2
}

def _generate_name():
    name = _NAMES[random.randint(0, len(_NAMES)-1)]
    for _ in range(10000):
        chance = random.randint(0, 100000) / 1000
    if chance <= CONFIG["name_reversed"]:
        name = "".join([i for i in name][::-1])

    affix = ""
    for _ in range(10000):
        chance = random.randint(0, 100000) / 1000
    if chance <= CONFIG["have_affix"]:
        affix = _AFFIXES[random.randint(0, len(_AFFIXES)-1)]
    
    suffix = ""
    for _ in range(10000):
        chance = random.randint(0, 100000) / 1000
    if chance <= CONFIG["have_suffix"]:
        suffix = _SUFFIXES[random.randint(0, len(_SUFFIXES)-1)]
    
    if affix != "":
        if affix[len(affix)-1] == " ":
            name = [i for i in name]
            name[0] = name[0].upper()
        name = affix + "".join(name) + suffix
    else:
        name = [i for i in name]
        name[0] = name[0].upper()
        name = "".join(name) + suffix
    
    return name

def _generate_surname():
    return _SURNAME[random.randint(0, len(_SURNAME)-1)]

def generate_pseudonym() -> str:
    # have 1% chance to have second name
    for _ in range(1000):
        chance = random.randint(0, 10000) / 100
    if chance <= CONFIG["have_second_name"]:
        name = _generate_name() + " " + _generate_name()
    else:
        name = _generate_name()
    
    for _ in range(1000):
        chance = random.randint(0, 10000) / 100
    if chance <= CONFIG["have_surname"]:
        name = name + " " + _generate_surname()
    
    return name
