from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True,
                        primary_key=True
                    )
                ),
                (
                    'uuid', models.CharField(
                        default='46845ca5-d94d-4669-9d7b-7886e2bac036',
                        max_length=48, editable=False
                    )
                ),
                (
                    'label', models.CharField(
                        default='Uninitialized document',
                        help_text='The name of the document', max_length=255,
                        verbose_name='Label', db_index=True
                    )
                ),
                (
                    'description', models.TextField(
                        null=True, verbose_name='Description', blank=True
                    )
                ),
                (
                    'date_added', models.DateTimeField(
                        auto_now_add=True, verbose_name='Added'
                    )
                ),
                (
                    'language', models.CharField(
                        default='eng', max_length=8, verbose_name='Language',
                        choices=[
                            ('aar', 'Afar'), ('abk', 'Abkhazian'),
                            ('ace', 'Achinese'), ('ach', 'Acoli'),
                            ('ada', 'Adangme'), ('ady', 'Adyghe; Adygei'),
                            ('afa', 'Afro-Asiatic languages'),
                            ('afh', 'Afrihili'), ('afr', 'Afrikaans'),
                            ('ain', 'Ainu'), ('aka', 'Akan'),
                            ('akk', 'Akkadian'), ('alb', 'Albanian'),
                            ('ale', 'Aleut'), ('alg', 'Algonquian languages'),
                            ('alt', 'Southern Altai'), ('amh', 'Amharic'),
                            ('ang', 'English, Old (ca. 450-1100)'),
                            ('anp', 'Angika'), ('apa', 'Apache languages'),
                            ('ara', 'Arabic'),
                            (
                                'arc',
                                'Official Aramaic (700-300 BCE); Imperial '
                                'Aramaic (700-300 BCE)'
                            ),
                            ('arg', 'Aragonese'), ('arm', 'Armenian'),
                            ('arn', 'Mapudungun; Mapuche'), ('arp', 'Arapaho'),
                            ('art', 'Artificial languages'), ('arw', 'Arawak'),
                            ('asm', 'Assamese'),
                            ('ast', 'Asturian; Bable; Leonese; Asturleonese'),
                            ('ath', 'Athapascan languages'),
                            ('aus', 'Australian languages'), ('ava', 'Avaric'),
                            ('ave', 'Avestan'), ('awa', 'Awadhi'),
                            ('aym', 'Aymara'), ('aze', 'Azerbaijani'),
                            ('bad', 'Banda languages'),
                            ('bai', 'Bamileke languages'), ('bak', 'Bashkir'),
                            ('bal', 'Baluchi'), ('bam', 'Bambara'),
                            ('ban', 'Balinese'), ('baq', 'Basque'),
                            ('bas', 'Basa'), ('bat', 'Baltic languages'),
                            ('bej', 'Beja; Bedawiyet'), ('bel', 'Belarusian'),
                            ('bem', 'Bemba'), ('ben', 'Bengali'),
                            ('ber', 'Berber languages'), ('bho', 'Bhojpuri'),
                            ('bih', 'Bihari languages'), ('bik', 'Bikol'),
                            ('bin', 'Bini; Edo'), ('bis', 'Bislama'),
                            ('bla', 'Siksika'), ('bnt', 'Bantu languages'),
                            ('bos', 'Bosnian'), ('bra', 'Braj'),
                            ('bre', 'Breton'), ('btk', 'Batak languages'),
                            ('bua', 'Buriat'), ('bug', 'Buginese'),
                            ('bul', 'Bulgarian'), ('bur', 'Burmese'),
                            ('byn', 'Blin; Bilin'), ('cad', 'Caddo'),
                            ('cai', 'Central American Indian languages'),
                            ('car', 'Galibi Carib'),
                            ('cat', 'Catalan; Valencian'),
                            ('cau', 'Caucasian languages'),
                            ('ceb', 'Cebuano'), ('cel', 'Celtic languages'),
                            ('cha', 'Chamorro'), ('chb', 'Chibcha'),
                            ('che', 'Chechen'), ('chg', 'Chagatai'),
                            ('chi', 'Chinese'), ('chk', 'Chuukese'),
                            ('chm', 'Mari'), ('chn', 'Chinook jargon'),
                            ('cho', 'Choctaw'),
                            ('chp', 'Chipewyan; Dene Suline'),
                            ('chr', 'Cherokee'),
                            (
                                'chu',
                                'Church Slavic; Old Slavonic; Church '
                                'Slavonic; Old Bulgarian; Old Church Slavonic'
                            ),
                            ('chv', 'Chuvash'), ('chy', 'Cheyenne'),
                            ('cmc', 'Chamic languages'), ('cop', 'Coptic'),
                            ('cor', 'Cornish'), ('cos', 'Corsican'),
                            ('cpe', 'Creoles and pidgins, English based'),
                            ('cpf', 'Creoles and pidgins, French-based'),
                            ('cpp', 'Creoles and pidgins, Portuguese-based'),
                            ('cre', 'Cree'),
                            ('crh', 'Crimean Tatar; Crimean Turkish'),
                            ('crp', 'Creoles and pidgins'),
                            ('csb', 'Kashubian'),
                            ('cus', 'Cushitic languages'), ('cze', 'Czech'),
                            ('dak', 'Dakota'), ('dan', 'Danish'),
                            ('dar', 'Dargwa'),
                            ('day', 'Land Dayak languages'),
                            ('del', 'Delaware'),
                            ('den', 'Slave (Athapascan)'), ('dgr', 'Dogrib'),
                            ('din', 'Dinka'),
                            ('div', 'Divehi; Dhivehi; Maldivian'),
                            ('doi', 'Dogri'), ('dra', 'Dravidian languages'),
                            ('dsb', 'Lower Sorbian'), ('dua', 'Duala'),
                            ('dum', 'Dutch, Middle (ca. 1050-1350)'),
                            ('dut', 'Dutch; Flemish'), ('dyu', 'Dyula'),
                            ('dzo', 'Dzongkha'), ('efi', 'Efik'),
                            ('egy', 'Egyptian (Ancient)'), ('eka', 'Ekajuk'),
                            ('elx', 'Elamite'), ('eng', 'English'),
                            ('enm', 'English, Middle (1100-1500)'),
                            ('epo', 'Esperanto'), ('est', 'Estonian'),
                            ('ewe', 'Ewe'), ('ewo', 'Ewondo'),
                            ('fan', 'Fang'), ('fao', 'Faroese'),
                            ('fat', 'Fanti'), ('fij', 'Fijian'),
                            ('fil', 'Filipino; Pilipino'), ('fin', 'Finnish'),
                            ('fiu', 'Finno-Ugrian languages'), ('fon', 'Fon'),
                            ('fre', 'French'),
                            ('frm', 'French, Middle (ca. 1400-1600)'),
                            ('fro', 'French, Old (842-ca. 1400)'),
                            ('frr', 'Northern Frisian'),
                            ('frs', 'Eastern Frisian'),
                            ('fry', 'Western Frisian'), ('ful', 'Fulah'),
                            ('fur', 'Friulian'), ('gaa', 'Ga'),
                            ('gay', 'Gayo'), ('gba', 'Gbaya'),
                            ('gem', 'Germanic languages'), ('geo', 'Georgian'),
                            ('ger', 'German'), ('gez', 'Geez'),
                            ('gil', 'Gilbertese'),
                            ('gla', 'Gaelic; Scottish Gaelic'),
                            ('gle', 'Irish'), ('glg', 'Galician'),
                            ('glv', 'Manx'),
                            ('gmh', 'German, Middle High (ca. 1050-1500)'),
                            ('goh', 'German, Old High (ca. 750-1050)'),
                            ('gon', 'Gondi'), ('gor', 'Gorontalo'),
                            ('got', 'Gothic'),
                            ('grb', 'Grebo'),
                            ('grc', 'Greek, Ancient (to 1453)'),
                            ('gre', 'Greek, Modern (1453-)'),
                            ('grn', 'Guarani'),
                            ('gsw', 'Swiss German; Alemannic; Alsatian'),
                            ('guj', 'Gujarati'), ('gwi', "Gwich'in"),
                            ('hai', 'Haida'),
                            ('hat', 'Haitian; Haitian Creole'),
                            ('hau', 'Hausa'), ('haw', 'Hawaiian'),
                            ('heb', 'Hebrew'), ('her', 'Herero'),
                            ('hil', 'Hiligaynon'),
                            (
                                'him',
                                'Himachali languages; Western Pahari '
                                'languages'
                            ),
                            ('hin', 'Hindi'), ('hit', 'Hittite'),
                            ('hmn', 'Hmong; Mong'), ('hmo', 'Hiri Motu'),
                            ('hrv', 'Croatian'), ('hsb', 'Upper Sorbian'),
                            ('hun', 'Hungarian'), ('hup', 'Hupa'),
                            ('iba', 'Iban'), ('ibo', 'Igbo'),
                            ('ice', 'Icelandic'), ('ido', 'Ido'),
                            ('iii', 'Sichuan Yi; Nuosu'),
                            ('ijo', 'Ijo languages'), ('iku', 'Inuktitut'),
                            ('ile', 'Interlingue; Occidental'),
                            ('ilo', 'Iloko'),
                            (
                                'ina',
                                'Interlingua (International Auxiliary '
                                'Language Association)'
                            ),
                            ('inc', 'Indic languages'),
                            ('ind', 'Indonesian'),
                            ('ine', 'Indo-European languages'),
                            ('inh', 'Ingush'), ('ipk', 'Inupiaq'),
                            ('ira', 'Iranian languages'),
                            ('iro', 'Iroquoian languages'),
                            ('ita', 'Italian'), ('jav', 'Javanese'),
                            ('jbo', 'Lojban'), ('jpn', 'Japanese'),
                            ('jpr', 'Judeo-Persian'), ('jrb', 'Judeo-Arabic'),
                            ('kaa', 'Kara-Kalpak'), ('kab', 'Kabyle'),
                            ('kac', 'Kachin; Jingpho'),
                            ('kal', 'Kalaallisut; Greenlandic'),
                            ('kam', 'Kamba'), ('kan', 'Kannada'),
                            ('kar', 'Karen languages'), ('kas', 'Kashmiri'),
                            ('kau', 'Kanuri'), ('kaw', 'Kawi'),
                            ('kaz', 'Kazakh'), ('kbd', 'Kabardian'),
                            ('kha', 'Khasi'), ('khi', 'Khoisan languages'),
                            ('khm', 'Central Khmer'),
                            ('kho', 'Khotanese;Sakan'),
                            ('kik', 'Kikuyu; Gikuyu'), ('kin', 'Kinyarwanda'),
                            ('kir', 'Kirghiz; Kyrgyz'), ('kmb', 'Kimbundu'),
                            ('kok', 'Konkani'), ('kom', 'Komi'),
                            ('kon', 'Kongo'), ('kor', 'Korean'),
                            ('kos', 'Kosraean'), ('kpe', 'Kpelle'),
                            ('krc', 'Karachay-Balkar'), ('krl', 'Karelian'),
                            ('kro', 'Kru languages'), ('kru', 'Kurukh'),
                            ('kua', 'Kuanyama; Kwanyama'), ('kum', 'Kumyk'),
                            ('kur', 'Kurdish'), ('kut', 'Kutenai'),
                            ('lad', 'Ladino'), ('lah', 'Lahnda'),
                            ('lam', 'Lamba'), ('lao', 'Lao'),
                            ('lat', 'Latin'), ('lav', 'Latvian'),
                            ('lez', 'Lezghian'),
                            ('lim', 'Limburgan; Limburger; Limburgish'),
                            ('lin', 'Lingala'), ('lit', 'Lithuanian'),
                            ('lol', 'Mongo'), ('loz', 'Lozi'),
                            ('ltz', 'Luxembourgish; Letzeburgesch'),
                            ('lua', 'Luba-Lulua'), ('lub', 'Luba-Katanga'),
                            ('lug', 'Ganda'),
                            ('lui', 'Luiseno'), ('lun', 'Lunda'),
                            ('luo', 'Luo (Kenya and Tanzania)'),
                            ('lus', 'Lushai'), ('mac', 'Macedonian'),
                            ('mad', 'Madurese'), ('mag', 'Magahi'),
                            ('mah', 'Marshallese'), ('mai', 'Maithili'),
                            ('mak', 'Makasar'), ('mal', 'Malayalam'),
                            ('man', 'Mandingo'), ('mao', 'Maori'),
                            ('map', 'Austronesian languages'),
                            ('mar', 'Marathi'), ('mas', 'Masai'),
                            ('may', 'Malay'), ('mdf', 'Moksha'),
                            ('mdr', 'Mandar'), ('men', 'Mende'),
                            ('mga', 'Irish, Middle (900-1200)'),
                            ('mic', "Mi'kmaq; Micmac"),
                            ('min', 'Minangkabau'),
                            ('mis', 'Uncoded languages'),
                            ('mkh', 'Mon-Khmer languages'),
                            ('mlg', 'Malagasy'), ('mlt', 'Maltese'),
                            ('mnc', 'Manchu'), ('mni', 'Manipuri'),
                            ('mno', 'Manobo languages'), ('moh', 'Mohawk'),
                            ('mol', 'Moldavian; Moldovan'),
                            ('mon', 'Mongolian'), ('mos', 'Mossi'),
                            ('mul', 'Multiple languages'),
                            ('mun', 'Munda languages'), ('mus', 'Creek'),
                            ('mwl', 'Mirandese'), ('mwr', 'Marwari'),
                            ('myn', 'Mayan languages'), ('myv', 'Erzya'),
                            ('nah', 'Nahuatl languages'),
                            ('nai', 'North American Indian languages'),
                            ('nap', 'Neapolitan'), ('nau', 'Nauru'),
                            ('nav', 'Navajo; Navaho'),
                            ('nbl', 'Ndebele, South; South Ndebele'),
                            ('nde', 'Ndebele, North; North Ndebele'),
                            ('ndo', 'Ndonga'),
                            (
                                'nds',
                                'Low German; Low Saxon; German, Low; Saxon, '
                                'Low'
                            ),
                            ('nep', 'Nepali'), ('new', 'Nepal Bhasa; Newari'),
                            ('nia', 'Nias'),
                            ('nic', 'Niger-Kordofanian languages'),
                            ('niu', 'Niuean'),
                            ('nno', 'Norwegian Nynorsk; Nynorsk, Norwegian'),
                            (
                                'nob',
                                'Bokm\xe5l, Norwegian; Norwegian Bokm\xe5l'
                            ),
                            ('nog', 'Nogai'), ('non', 'Norse, Old'),
                            ('nor', 'Norwegian'),
                            ('nqo', "N'Ko"),
                            ('nso', 'Pedi; Sepedi; Northern Sotho'),
                            ('nub', 'Nubian languages'),
                            (
                                'nwc',
                                'Classical Newari; Old Newari; Classical '
                                'Nepal Bhasa'
                            ),
                            ('nya', 'Chichewa; Chewa; Nyanja'),
                            ('nym', 'Nyamwezi'),
                            ('nyn', 'Nyankole'), ('nyo', 'Nyoro'),
                            ('nzi', 'Nzima'), ('oci', 'Occitan (post 1500)'),
                            ('oji', 'Ojibwa'), ('ori', 'Oriya'),
                            ('orm', 'Oromo'), ('osa', 'Osage'),
                            ('oss', 'Ossetian; Ossetic'),
                            ('ota', 'Turkish, Ottoman (1500-1928)'),
                            ('oto', 'Otomian languages'),
                            ('paa', 'Papuan languages'),
                            ('pag', 'Pangasinan'), ('pal', 'Pahlavi'),
                            ('pam', 'Pampanga; Kapampangan'),
                            ('pan', 'Panjabi; Punjabi'),
                            ('pap', 'Papiamento'), ('pau', 'Palauan'),
                            ('peo', 'Persian, Old (ca. 600-400 B.C.)'),
                            ('per', 'Persian'),
                            ('phi', 'Philippine languages'),
                            ('phn', 'Phoenician'),
                            ('pli', 'Pali'), ('pol', 'Polish'),
                            ('pon', 'Pohnpeian'), ('por', 'Portuguese'),
                            ('pra', 'Prakrit languages'),
                            (
                                'pro',
                                'Proven\xe7al, Old (to 1500); Occitan, Old '
                                '(to 1500)'
                            ),
                            ('pus', 'Pushto; Pashto'),
                            ('qaa-qtz', 'Reserved for local use'),
                            ('que', 'Quechua'), ('raj', 'Rajasthani'),
                            ('rap', 'Rapanui'),
                            ('rar', 'Rarotongan; Cook Islands Maori'),
                            ('roa', 'Romance languages'), ('roh', 'Romansh'),
                            ('rom', 'Romany'), ('rum', 'Romanian'),
                            ('run', 'Rundi'),
                            ('rup', 'Aromanian; Arumanian; Macedo-Romanian'),
                            ('rus', 'Russian'), ('sad', 'Sandawe'),
                            ('sag', 'Sango'),
                            ('sah', 'Yakut'),
                            ('sai', 'South American Indian languages'),
                            ('sal', 'Salishan languages'),
                            ('sam', 'Samaritan Aramaic'),
                            ('san', 'Sanskrit'), ('sas', 'Sasak'),
                            ('sat', 'Santali'), ('scn', 'Sicilian'),
                            ('sco', 'Scots'), ('sel', 'Selkup'),
                            ('sem', 'Semitic languages'),
                            ('sga', 'Irish, Old (to 900)'),
                            ('sgn', 'Sign Languages'), ('shn', 'Shan'),
                            ('sid', 'Sidamo'),
                            ('sin', 'Sinhala; Sinhalese'),
                            ('sio', 'Siouan languages'),
                            ('sit', 'Sino-Tibetan languages'),
                            ('sla', 'Slavic languages'),
                            ('slo', 'Slovak'), ('slv', 'Slovenian'),
                            ('sma', 'Southern Sami'),
                            ('sme', 'Northern Sami'),
                            ('smi', 'Sami languages'),
                            ('smj', 'Lule Sami'), ('smn', 'Inari Sami'),
                            ('smo', 'Samoan'), ('sms', 'Skolt Sami'),
                            ('sna', 'Shona'), ('snd', 'Sindhi'),
                            ('snk', 'Soninke'), ('sog', 'Sogdian'),
                            ('som', 'Somali'), ('son', 'Songhai languages'),
                            ('sot', 'Sotho, Southern'),
                            ('spa', 'Spanish; Castilian'),
                            ('srd', 'Sardinian'), ('srn', 'Sranan Tongo'),
                            ('srp', 'Serbian'), ('srr', 'Serer'),
                            ('ssa', 'Nilo-Saharan languages'),
                            ('ssw', 'Swati'), ('suk', 'Sukuma'),
                            ('sun', 'Sundanese'), ('sus', 'Susu'),
                            ('sux', 'Sumerian'), ('swa', 'Swahili'),
                            ('swe', 'Swedish'), ('syc', 'Classical Syriac'),
                            ('syr', 'Syriac'),
                            ('tah', 'Tahitian'), ('tai', 'Tai languages'),
                            ('tam', 'Tamil'), ('tat', 'Tatar'),
                            ('tel', 'Telugu'), ('tem', 'Timne'),
                            ('ter', 'Tereno'), ('tet', 'Tetum'),
                            ('tgk', 'Tajik'), ('tgl', 'Tagalog'),
                            ('tha', 'Thai'), ('tib', 'Tibetan'),
                            ('tig', 'Tigre'), ('tir', 'Tigrinya'),
                            ('tiv', 'Tiv'), ('tkl', 'Tokelau'),
                            ('tlh', 'Klingon; tlhIngan-Hol'),
                            ('tli', 'Tlingit'),
                            ('tmh', 'Tamashek'), ('tog', 'Tonga (Nyasa)'),
                            ('ton', 'Tonga (Tonga Islands)'),
                            ('tpi', 'Tok Pisin'), ('tsi', 'Tsimshian'),
                            ('tsn', 'Tswana'), ('tso', 'Tsonga'),
                            ('tuk', 'Turkmen'), ('tum', 'Tumbuka'),
                            ('tup', 'Tupi languages'), ('tur', 'Turkish'),
                            ('tut', 'Altaic languages'), ('tvl', 'Tuvalu'),
                            ('twi', 'Twi'), ('tyv', 'Tuvinian'),
                            ('udm', 'Udmurt'), ('uga', 'Ugaritic'),
                            ('uig', 'Uighur; Uyghur'), ('ukr', 'Ukrainian'),
                            ('umb', 'Umbundu'), ('und', 'Undetermined'),
                            ('urd', 'Urdu'), ('uzb', 'Uzbek'),
                            ('vai', 'Vai'), ('ven', 'Venda'),
                            ('vie', 'Vietnamese'), ('vol', 'Volap\xfck'),
                            ('vot', 'Votic'), ('wak', 'Wakashan languages'),
                            ('wal', 'Wolaitta; Wolaytta'), ('war', 'Waray'),
                            ('was', 'Washo'), ('wel', 'Welsh'),
                            ('wen', 'Sorbian languages'), ('wln', 'Walloon'),
                            ('wol', 'Wolof'), ('xal', 'Kalmyk; Oirat'),
                            ('xho', 'Xhosa'), ('yao', 'Yao'),
                            ('yap', 'Yapese'), ('yid', 'Yiddish'),
                            ('yor', 'Yoruba'), ('ypk', 'Yupik languages'),
                            ('zap', 'Zapotec'),
                            ('zbl', 'Blissymbols; Blissymbolics; Bliss'),
                            ('zen', 'Zenaga'),
                            ('zgh', 'Standard Moroccan Tamazight'),
                            ('zha', 'Zhuang; Chuang'),
                            ('znd', 'Zande languages'), ('zul', 'Zulu'),
                            ('zun', 'Zuni'),
                            ('zxx', 'No linguistic content; Not applicable'),
                            (
                                'zza',
                                'Zaza; Dimili; Dimli; Kirdki; Kirmanjki; '
                                'Zazaki'
                            )
                        ]
                    )
                ),
            ],
            options={
                'ordering': ['-date_added'],
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentPage',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True,
                        primary_key=True
                    )
                ),
                (
                    'content', models.TextField(
                        null=True, verbose_name='Content', blank=True
                    )
                ),
                (
                    'page_label', models.CharField(
                        max_length=40, null=True, verbose_name='Page label',
                        blank=True
                    )
                ),
                (
                    'page_number', models.PositiveIntegerField(
                        default=1, verbose_name='Page number',
                        editable=False, db_index=True
                    )
                ),
            ],
            options={
                'ordering': ['page_number'],
                'verbose_name': 'Document page',
                'verbose_name_plural': 'Document pages',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentPageTransformation',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True,
                        primary_key=True
                    )
                ),
                (
                    'order', models.PositiveIntegerField(
                        default=0, null=True, verbose_name='Order',
                        db_index=True, blank=True
                    )
                ),
                (
                    'transformation', models.CharField(
                        max_length=128, verbose_name='Transformation',
                        choices=[
                            ('resize', 'Resize'), ('rotate', 'Rotate'),
                            ('zoom', 'Zoom')
                        ]
                    )
                ),
                (
                    'arguments', models.TextField(
                        blank=True, help_text="Use dictionaries to indentify "
                        "arguments, example: {'degrees':90}", null=True,
                        verbose_name='Arguments', validators=[]
                    )
                ),
                (
                    'document_page', models.ForeignKey(
                        verbose_name='Document page',
                        to='documents.DocumentPage'
                    )
                ),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Document page transformation',
                'verbose_name_plural': 'Document page transformations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True,
                        primary_key=True
                    )
                ),
                (
                    'name', models.CharField(
                        unique=True, max_length=32, verbose_name='Name'
                    )
                ),
                (
                    'ocr', models.BooleanField(
                        default=True, verbose_name='Automatically queue '
                        'newly created documents for OCR.'
                    )
                ),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Document type',
                'verbose_name_plural': 'Documents types',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentTypeFilename',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True,
                        primary_key=True
                    )
                ),
                (
                    'filename', models.CharField(
                        max_length=128, verbose_name='Filename', db_index=True
                    )
                ),
                (
                    'enabled', models.BooleanField(
                        default=True, verbose_name='Enabled'
                    )
                ),
                (
                    'document_type', models.ForeignKey(
                        related_name='filenames',
                        verbose_name='Document type',
                        to='documents.DocumentType'
                    )
                ),
            ],
            options={
                'ordering': ['filename'],
                'verbose_name': 'Document type quick rename filename',
                'verbose_name_plural': 'Document types quick rename filenames',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentVersion',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True,
                        primary_key=True
                    )
                ),
                (
                    'timestamp', models.DateTimeField(
                        auto_now_add=True, verbose_name='Timestamp'
                    )
                ),
                (
                    'comment', models.TextField(
                        verbose_name='Comment', blank=True
                    )
                ),
                (
                    'file', models.FileField(
                        upload_to='2a2af9b3-8079-4753-9863-f1c342ec0d06',
                        storage=FileSystemStorage(),
                        verbose_name='File'
                    )
                ),
                (
                    'mimetype', models.CharField(
                        max_length=255, null=True, editable=False, blank=True
                    )
                ),
                (
                    'encoding', models.CharField(
                        max_length=64, null=True, editable=False, blank=True
                    )
                ),
                (
                    'checksum', models.TextField(
                        verbose_name='Checksum', null=True, editable=False,
                        blank=True
                    )
                ),
                (
                    'document', models.ForeignKey(
                        related_name='versions', verbose_name='Document',
                        to='documents.Document'
                    )
                ),
            ],
            options={
                'verbose_name': 'Document version',
                'verbose_name_plural': 'Document version',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RecentDocument',
            fields=[
                (
                    'id', models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True,
                        primary_key=True
                    )
                ),
                (
                    'datetime_accessed', models.DateTimeField(
                        auto_now=True, verbose_name='Accessed', db_index=True
                    )
                ),
                (
                    'document', models.ForeignKey(
                        editable=False, to='documents.Document',
                        verbose_name='Document'
                    )
                ),
                (
                    'user', models.ForeignKey(
                        editable=False, to=settings.AUTH_USER_MODEL,
                        verbose_name='User'
                    )
                ),
            ],
            options={
                'ordering': ('-datetime_accessed',),
                'verbose_name': 'Recent document',
                'verbose_name_plural': 'Recent documents',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='documenttypefilename',
            unique_together=set([('document_type', 'filename')]),
        ),
        migrations.AddField(
            model_name='documentpage',
            name='document_version',
            field=models.ForeignKey(
                related_name='pages', verbose_name='Document version',
                to='documents.DocumentVersion'
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='document_type',
            field=models.ForeignKey(
                related_name='documents', verbose_name='Document type',
                to='documents.DocumentType'
            ),
            preserve_default=True,
        ),
    ]
