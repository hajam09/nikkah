from django.db.models import TextChoices, IntegerChoices


class CreatedBy(TextChoices):
    SELF = 'SELF', 'Self'
    PARENTS = 'PARENTS', 'Parents'
    SIBLING = 'SIBLING', 'Sibling'
    RELATIVE = 'RELATIVE', 'Relative'
    FRIEND = 'FRIEND', 'Friend'
    OTHER = 'OTHER', 'Other'


class Gender(TextChoices):
    MALE = 'MALE', 'Male'
    FEMALE = 'FEMALE', 'Female'


class Height(IntegerChoices):
    H_122 = 122, '4\'0" (122 cm)'
    H_124 = 124, '4\'1" (124 cm)'
    H_127 = 127, '4\'2" (127 cm)'
    H_130 = 130, '4\'3" (130 cm)'
    H_132 = 132, '4\'4" (132 cm)'
    H_135 = 135, '4\'5" (135 cm)'
    H_137 = 137, '4\'6" (137 cm)'
    H_140 = 140, '4\'7" (140 cm)'
    H_142 = 142, '4\'8" (142 cm)'
    H_145 = 145, '4\'9" (145 cm)'
    H_147 = 147, '4\'10" (147 cm)'
    H_150 = 150, '4\'11" (150 cm)'
    H_152 = 152, '5\'0" (152 cm)'
    H_155 = 155, '5\'1" (155 cm)'
    H_157 = 157, '5\'2" (157 cm)'
    H_160 = 160, '5\'3" (160 cm)'
    H_163 = 163, '5\'4" (163 cm)'
    H_165 = 165, '5\'5" (165 cm)'
    H_168 = 168, '5\'6" (168 cm)'
    H_170 = 170, '5\'7" (170 cm)'
    H_173 = 173, '5\'8" (173 cm)'
    H_175 = 175, '5\'9" (175 cm)'
    H_178 = 178, '5\'10" (178 cm)'
    H_180 = 180, '5\'11" (180 cm)'
    H_183 = 183, '6\'0" (183 cm)'
    H_185 = 185, '6\'1" (185 cm)'
    H_188 = 188, '6\'2" (188 cm)'
    H_191 = 191, '6\'3" (191 cm)'
    H_193 = 193, '6\'4" (193 cm)'
    H_196 = 196, '6\'5" (196 cm)'
    H_198 = 198, '6\'6" (198 cm)'
    H_201 = 201, '6\'7" (201 cm)'
    H_203 = 203, '6\'8" (203 cm)'
    H_206 = 206, '6\'9" (206 cm)'
    H_208 = 208, '6\'10" (208 cm)'
    H_211 = 211, '6\'11" (211 cm)'
    H_213 = 213, '7\'0" (213 cm)'


class Weight(IntegerChoices):
    W_40 = 40, '40 kg'
    W_41 = 41, '41 kg'
    W_42 = 42, '42 kg'
    W_43 = 43, '43 kg'
    W_44 = 44, '44 kg'
    W_45 = 45, '45 kg'
    W_46 = 46, '46 kg'
    W_47 = 47, '47 kg'
    W_48 = 48, '48 kg'
    W_49 = 49, '49 kg'
    W_50 = 50, '50 kg'
    W_51 = 51, '51 kg'
    W_52 = 52, '52 kg'
    W_53 = 53, '53 kg'
    W_54 = 54, '54 kg'
    W_55 = 55, '55 kg'
    W_56 = 56, '56 kg'
    W_57 = 57, '57 kg'
    W_58 = 58, '58 kg'
    W_59 = 59, '59 kg'
    W_60 = 60, '60 kg'
    W_61 = 61, '61 kg'
    W_62 = 62, '62 kg'
    W_63 = 63, '63 kg'
    W_64 = 64, '64 kg'
    W_65 = 65, '65 kg'
    W_66 = 66, '66 kg'
    W_67 = 67, '67 kg'
    W_68 = 68, '68 kg'
    W_69 = 69, '69 kg'
    W_70 = 70, '70 kg'
    W_71 = 71, '71 kg'
    W_72 = 72, '72 kg'
    W_73 = 73, '73 kg'
    W_74 = 74, '74 kg'
    W_75 = 75, '75 kg'
    W_76 = 76, '76 kg'
    W_77 = 77, '77 kg'
    W_78 = 78, '78 kg'
    W_79 = 79, '79 kg'
    W_80 = 80, '80 kg'
    W_81 = 81, '81 kg'
    W_82 = 82, '82 kg'
    W_83 = 83, '83 kg'
    W_84 = 84, '84 kg'
    W_85 = 85, '85 kg'
    W_86 = 86, '86 kg'
    W_87 = 87, '87 kg'
    W_88 = 88, '88 kg'
    W_89 = 89, '89 kg'
    W_90 = 90, '90 kg'
    W_91 = 91, '91 kg'
    W_92 = 92, '92 kg'
    W_93 = 93, '93 kg'
    W_94 = 94, '94 kg'
    W_95 = 95, '95 kg'
    W_96 = 96, '96 kg'
    W_97 = 97, '97 kg'
    W_98 = 98, '98 kg'
    W_99 = 99, '99 kg'
    W_100 = 100, '100 kg'
    W_101 = 101, '101 kg'
    W_102 = 102, '102 kg'
    W_103 = 103, '103 kg'
    W_104 = 104, '104 kg'
    W_105 = 105, '105 kg'
    W_106 = 106, '106 kg'
    W_107 = 107, '107 kg'
    W_108 = 108, '108 kg'
    W_109 = 109, '109 kg'
    W_110 = 110, '110 kg'
    W_111 = 111, '111 kg'
    W_112 = 112, '112 kg'
    W_113 = 113, '113 kg'
    W_114 = 114, '114 kg'
    W_115 = 115, '115 kg'
    W_116 = 116, '116 kg'
    W_117 = 117, '117 kg'
    W_118 = 118, '118 kg'
    W_119 = 119, '119 kg'
    W_120 = 120, '120 kg'


class MaritalStatus(TextChoices):
    SINGLE = 'SINGLE', 'Single'
    ANNULLED = 'ANNULLED', 'Annulled'
    DIVORCED = 'DIVORCED', 'Divorced'
    SEPARATED = 'SEPARATED', 'Separated'
    WIDOWED = 'WIDOWED', 'Widowed'


class HijabStatus(TextChoices):
    HIJAB = 'HIJAB', 'Hijab'
    NIQAB = 'NIQAB', 'Niqab'
    NONE = 'NONE', 'None'


class PhysicalStatus(TextChoices):
    NORMAL = 'NORMAL', 'Normal'
    HANDICAPPED = 'HANDICAPPED', 'Handicapped'
    DISABLED = 'DISABLED', 'Disabled'


class Madhab(TextChoices):
    HANAFI = 'HANAFI', 'Hanafi'
    SHAFI = 'SHAFI', 'Shafi'
    MALIKI = 'MALIKI', 'Maliki'
    HANBALI = 'HANBALI', 'Hanbali'
    JAFARI = 'JAFARI', "Ja'fari"
    ISMAILI = 'ISMAILI', 'Ismaili'
    ZAYDI = 'ZAYDI', 'Zaydi'
    OTHER = 'OTHER', 'Other'
    PREFER_NOT_TO_SAY = 'PREFER_NOT_TO_SAY', 'Prefer not to say'


class Language(TextChoices):
    ENGLISH = 'ENGLISH', 'English'
    MANDARIN = 'MANDARIN', 'Mandarin Chinese'
    HINDI = 'HINDI', 'Hindi'
    SPANISH = 'SPANISH', 'Spanish'
    ARABIC = 'ARABIC', 'Arabic'
    FRENCH = 'FRENCH', 'French'
    BENGALI = 'BENGALI', 'Bengali'
    PORTUGUESE = 'PORTUGUESE', 'Portuguese'
    RUSSIAN = 'RUSSIAN', 'Russian'
    URDU = 'URDU', 'Urdu'
    INDONESIAN = 'INDONESIAN', 'Indonesian'
    GERMAN = 'GERMAN', 'German'
    JAPANESE = 'JAPANESE', 'Japanese'
    PUNJABI = 'PUNJABI', 'Punjabi'
    SWAHILI = 'SWAHILI', 'Swahili'
    TURKISH = 'TURKISH', 'Turkish'
    PERSIAN = 'PERSIAN', 'Persian'
    KOREAN = 'KOREAN', 'Korean'
    ITALIAN = 'ITALIAN', 'Italian'
    VIETNAMESE = 'VIETNAMESE', 'Vietnamese'
    TAMIL = 'TAMIL', 'Tamil'
    TELUGU = 'TELUGU', 'Telugu'
    THAI = 'THAI', 'Thai'
    DUTCH = 'DUTCH', 'Dutch'
    POLISH = 'POLISH', 'Polish'
    OTHER = 'OTHER', 'Other'


class EatingHabit(TextChoices):
    VEGETARIAN = 'VEGETARIAN', 'Vegetarian'
    NON_VEGETARIAN = 'NON_VEGETARIAN', 'Non-Vegetarian'
    OTHER = 'OTHER', 'Other'
    PREFER_NOT_TO_SAY = 'PREFER_NOT_TO_SAY', 'Prefer not to say'


class SmokingHabit(TextChoices):
    NON_SMOKER = 'NON_SMOKER', 'Non-smoker'
    LIGHT_SOCIAL = 'LIGHT_SOCIAL', 'Light / Social smoker'
    REGULAR = 'REGULAR', 'Regular smoker'


class PrayerFrequency(TextChoices):
    FIVE_TIMES = 'FIVE_TIMES', 'Five times daily'
    MOST_PRAYERS = 'MOST_PRAYERS', 'Most prayers'
    SOMETIMES = 'SOMETIMES', 'Sometimes'
    RARELY = 'RARELY', 'Rarely'
    NOT_PRACTICING = 'NOT_PRACTICING', 'Not currently practicing'
    PREFER_NOT_TO_SAY = 'PREFER_NOT_TO_SAY', 'Prefer not to say'


class QuranReading(TextChoices):
    DAILY = 'DAILY', 'Daily'
    SEVERAL_TIMES_WEEK = 'SEVERAL_TIMES_WEEK', 'Several times a week'
    WEEKLY = 'WEEKLY', 'Weekly'
    OCCASIONALLY = 'OCCASIONALLY', 'Occasionally'
    RAMADAN = 'RAMADAN', 'During Ramadan'
    RARELY = 'RARELY', 'Rarely'
    NOT_CURRENTLY = 'NOT_CURRENTLY', 'Not currently reading'
    PREFER_NOT_TO_SAY = 'PREFER_NOT_TO_SAY', 'Prefer not to say'


class EducationLevel(TextChoices):
    HIGH_SCHOOL = 'HIGH_SCHOOL', 'High School'
    DIPLOMA = 'DIPLOMA', 'Diploma'
    BACHELORS = 'BACHELORS', "Bachelor's"
    MASTERS = 'MASTERS', "Master's"
    PHD = 'PHD', 'PhD'
    ISLAMIC_STUDIES = 'ISLAMIC_STUDIES', 'Islamic Studies'
    OTHER = 'OTHER', 'Other'


class EmploymentStatus(TextChoices):
    EMPLOYED = 'EMPLOYED', 'Employed'
    SELF_EMPLOYED = 'SELF_EMPLOYED', 'Self Employed'
    BUSINESS_OWNER = 'BUSINESS_OWNER', 'Business Owner'
    STUDENT = 'STUDENT', 'Student'
    UNEMPLOYED = 'UNEMPLOYED', 'Unemployed'
    RETIRED = 'RETIRED', 'Retired'


class Industry(TextChoices):
    IT = 'IT', 'Information Technology'
    HEALTHCARE = 'HEALTHCARE', 'Healthcare'
    EDUCATION = 'EDUCATION', 'Education'
    FINANCE = 'FINANCE', 'Finance'
    ENGINEERING = 'ENGINEERING', 'Engineering'
    GOVERNMENT = 'GOVERNMENT', 'Government'
    CONSTRUCTION = 'CONSTRUCTION', 'Construction'
    RETAIL = 'RETAIL', 'Retail'
    MANUFACTURING = 'MANUFACTURING', 'Manufacturing'
    HOSPITALITY = 'HOSPITALITY', 'Hospitality'
    LEGAL = 'LEGAL', 'Legal'
    TRANSPORT = 'TRANSPORT', 'Transport'
    AGRICULTURE = 'AGRICULTURE', 'Agriculture'
    ARTS_MEDIA = 'ARTS_MEDIA', 'Arts and Media'
    CONSULTING = 'CONSULTING', 'Consulting'
    ENERGY_UTILITIES = 'ENERGY_UTILITIES', 'Energy and Utilities'
    ENVIRONMENT = 'ENVIRONMENT', 'Environment'
    INSURANCE = 'INSURANCE', 'Insurance'
    NONPROFIT = 'NONPROFIT', 'Nonprofit'
    REAL_ESTATE = 'REAL_ESTATE', 'Real Estate'
    SCIENCE_RESEARCH = 'SCIENCE_RESEARCH', 'Science and Research'
    TELECOMMUNICATIONS = 'TELECOMMUNICATIONS', 'Telecommunications'
    OTHER = 'OTHER', 'Other'
    PREFER_NOT_TO_SAY = 'PREFER_NOT_TO_SAY', 'Prefer not to say'


class FamilyValue(TextChoices):
    ORTHODOX = 'ORTHODOX', 'Orthodox'
    TRADITIONAL = 'TRADITIONAL', 'Traditional'
    MODERATE = 'MODERATE', 'Moderate'
    LIBERAL = 'LIBERAL', 'Liberal'


class FamilyType(TextChoices):
    JOINT = 'JOINT', 'Joint family'
    NUCLEAR = 'NUCLEAR', 'Nuclear family'
    EXTENDED = 'EXTENDED', 'Extended family'
    SINGLE_PARENT = 'SINGLE_PARENT', 'Single-parent family'


class FamilyStatus(TextChoices):
    LOW_INCOME = 'LOW_INCOME', 'Low income'
    WORKING_CLASS = 'WORKING_CLASS', 'Working class'
    MIDDLE_CLASS = 'MIDDLE_CLASS', 'Middle class'
    UPPER_MIDDLE_CLASS = 'UPPER_MIDDLE_CLASS', 'Upper middle class'
    AFFLUENT = 'AFFLUENT', 'Affluent / Wealthy'
    ELITE = 'ELITE', 'Elite / Extremely wealthy'


class Relationship(TextChoices):
    FATHER = 'FATHER', 'Father'
    BROTHER = 'BROTHER', 'Brother'
    GRANDFATHER = 'GRANDFATHER', 'Grandfather'
    UNCLE = 'UNCLE', 'Uncle'
    OTHER = 'OTHER', 'Other'
