# -*- coding: utf-8 -*-

import sqlite3
from werkzeug.security import generate_password_hash


topic = [
    ' Arts ',
    ' Business ',
    ' Company News ',
    ' Entertainment ',
    ' Environment ',
    ' Health News ',
    ' Lifestyle ',
    ' Media ',
    ' Money ',
    ' Most Read Articles ',
    ' Oddly Enough ',
    ' Pictures ',
    ' People ',
    ' Politics ',
    ' Science ',
    ' Sports ',
    ' Technology ',
    ' Top News ',
    ' US News ',
    ' World ',
    ' Bankruptcy ',
    ' Bonds ',
    ' Deals ',
    ' Economy ',
    ' Global Markets ',
    ' Hedge Funds ',
    ' Hot Stocks ',
    ' Mergers & Acquisitions ',
    ' Regulatory News ',
    ' Summit News ',
    ' US Dollar Report ',
    ' US Markets ',
    ' Basic Materials  ',
    ' Cyclical Consumer Goods ',
    ' Energy  ',
    ' Financials  ',
    ' Healthcare ',
    ' Industrials ',
    ' Media Diversified ',
    ' Utilities ',
    ' Financial Regulatory Forum ',
    ' Global Investing ',
    ' MediaFile ',
    ' Newsmaker ',
    ' Unstructured Finance ',
    ' Breakingviews Video ',
    ' Business Video ',
    ' Business Travel Video ',
    ' Entertainment Video ',
    ' Environment Video ',
    ' Lifestyle Video ',
    ' Most Watched Video ',
    ' Most Recent Video ',
    ' Personal Finance ',
    ' Politics Video ',
    ' Small Business ',
    ' Technology Video ',
    ' Top News Video ',
    ' World News ']

countries = [
    " Afghanistan ",
    " Albania ",
    " Algeria ",
    " Andorra ",
    " Angola ",
    " Antigua and Barbuda ",
    " Argentina ",
    " Armenia ",
    " Australia ",
    " Austria ",
    " Azerbaijan ",
    " Bahamas, The ",
    " Bahrain ",
    " Bangladesh ",
    " Barbados ",
    " Belarus ",
    " Belgium ",
    " Belize ",
    " Benin ",
    " Bhutan ",
    " Bolivia ",
    " Bosnia and Herzegovina ",
    " Botswana ",
    " Brazil ",
    " Brunei ",
    " Bulgaria ",
    " Burkina Faso",
    " Burma ",
    " Burundi ",
    " Cambodia ",
    " Cameroon ",
    " Canada[Note 12] ",
    " Cape Verde ",
    " Central African Republic ",
    " Chad ",
    " Chile ",
    " China ",
    " Colombia ",
    " Comoros ",
    " Congo, Republic of the",
    " Costa Rica ",
    " Croatia ",
    " Cuba ",
    " Cyprus ",
    " Czech Republic ",
    " Denmark ",
    " Djibouti ",
    " Dominica ",
    " Dominican Republic ",
    " East Timor ",
    " Ecuador ",
    " Egypt ",
    " El Salvador ",
    " Equatorial Guinea ",
    " Eritrea ",
    " Estonia ",
    " Ethiopia ",
    " Fiji ",
    " Finland ",
    " France ",
    " Gabon ",
    " Gambia  Gambia, The ",
    " Georgia ",
    " Germany ",
    " Ghana ",
    " Greece ",
    " Grenada ",
    " Guatemala ",
    " Guinea ",
    " Guinea-Bissau ",
    " Guyana ",
    " Haiti ",
    " Honduras ",
    " Hungary ",
    " Iceland ",
    " India ",
    " Indonesia ",
    " Iran ",
    " Iraq ",
    " Ireland ",
    " Israel ",
    " Italy ",
    " Ivory Coast ",
    " Jamaica ",
    " Japan ",
    " Jordan ",
    " Kazakhstan ",
    " Kenya ",
    " Kiribati ",
    " Korea, North ",
    " Korea, South ",
    " Kuwait ",
    " Kyrgyzstan ",
    " Laos ",
    " Latvia ",
    " Lebanon ",
    " Lesotho ",
    " Liberia ",
    " Libya ",
    " Liechtenstein ",
    " Lithuania ",
    " Luxembourg ",
    " Macedonia ",
    " Madagascar ",
    " Malawi ",
    " Malaysia ",
    " Maldives ",
    " Mali ",
    " Malta ",
    " Marshall Islands ",
    " Mauritania ",
    " Mauritius ",
    " Mexico ",
    " Micronesia",
    " Moldova ",
    " Monaco ",
    " Mongolia ",
    " Montenegro ",
    " Morocco ",
    " Mozambique ",
    " Myanmar",
    " Namibia ",
    " Nauru ",
    " Nepal ",
    " Netherlands ",
    " New Zealand ",
    " Nicaragua ",
    " Niger ",
    " Nigeria ",
    " Norway ",
    " Oman ",
    " Pakistan ",
    " Palau ",
    " Palestine ",
    " Panama ",
    " Papua New Guinea ",
    " Paraguay ",
    " Peru ",
    " Philippines ",
    " Poland ",
    " Portugal ",
    " Qatar ",
    " Romania ",
    " Russia ",
    " Rwanda ",
    " Saint Kitts and Nevis ",
    " Saint Lucia ",
    " Saint Vincent and the Grenadines ",
    " Samoa ",
    " San Marino ",
    " Saudi Arabia ",
    " Senegal ",
    " Serbia ",
    " Seychelles ",
    " Sierra Leone ",
    " Singapore ",
    " Slovakia ",
    " Slovenia ",
    " Solomon Islands ",
    " Somalia ",
    " South Africa ",
    " South Sudan ",
    " Spain ",
    " Sri Lanka ",
    " Sudan ",
    " Suriname ",
    " Swaziland ",
    " Sweden ",
    " Switzerland ",
    " Syria ",
    " Tajikistan ",
    " Tanzania ",
    " Thailand ",
    " Togo ",
    " Tonga ",
    " Trinidad and Tobago ",
    " Tunisia ",
    " Turkey ",
    " Turkmenistan ",
    " Tuvalu ",
    " Uganda ",
    " Ukraine ",
    " United Arab Emirates ",
    " United Kingdom ",
    " United States ",
    " Uruguay ",
    " Uzbekistan ",
    " Vanuatu ",
    " Vatican City ",
    " Venezuela ",
    " Vietnam ",
    " Yemen ",
    " Zambia ",
    " Zimbabwe ",
    " Abkhazia ",
    " Cook Islands ",
    " Kosovo ",
    " Nagorno-Karabakh ",
    " Niue ",
    " Northern Cyprus ",
    " Sahrawi Arab Democratic Republic ",
    " Somaliland ",
    " South Ossetia ",
    " Taiwan ",
    " Transnistria "

]

language = [
    " Acèh ",
    " Afrikaans ",
    " Alemannisch ",
    " አማርኛ ",
    " Ænglisc ",
    " العربية ",
    " Aragonés ",
    " ܐܪܡܝܐ ",
    " Armãneashti ",
    " Arpetan ",
    " অসমীয়া ",
    " Asturianu ",
    " Avañe'ẽ ",
    " Aymar aru ",
    " Azərbaycanca ",
    " Bamanankan ",
    " বাংলা ",
    " Bân-lâm-gú ",
    " Basa Banyumasan ",
    " Башҡортса ",
    " Беларуская ",
    " Беларуская (тарашкевіца)‎ ",
    " bh:भाषा ",
    " Български ",
    " Boarisch ",
    " བོད་ཡིག ",
    " Bosanski ",
    " Brezhoneg ",
    " Буряад ",
    " Català ",
    " Чӑвашла ",
    " Cebuano ",
    " Čeština ",
    " Chamoru ",
    " ChiShona ",
    " Cymraeg ",
    " Dansk ",
    " Deitsch ",
    " Deutsch ",
    " ދިވެހިބަސް ",
    " Eesti ",
    " Ελληνικά ",
    " Emiliàn e rumagnòl ",
    " Español ",
    " Esperanto ",
    " Euskara ",
    " فارسی ",
    " Fiji Hindi ",
    " Føroyskt ",
    " Français ",
    " Frysk ",
    " Furlan ",
    " Gaeilge ",
    " Gaelg ",
    " Gàidhlig ",
    " Galego ",
    " 贛語 ",
    " گیلکی ",
    " ગુજરાતી ",
    " 客家語/Hak-kâ-ngî ",
    " 한국어 ",
    " Հայերեն ",
    " हिन्दी ",
    " Hrvatski ",
    " Ido ",
    " Ilokano ",
    " Bahasa Indonesia ",
    " Interlingua ",
    " Interlingue ",
    " Iñupiak ",
    " Ирон ",
    " IsiXhosa ",
    " Íslenska ",
    " Italiano ",
    " עברית ",
    " Basa Jawa ",
    " Kalaallisut ",
    " ಕನ್ನಡ ",
    " Къарачай-малкъар ",
    " ქართული ",
    " Қазақша ",
    " Kernowek ",
    " Kiswahili ",
    " Коми ",
    " Kongo ",
    " Kreyòl ayisyen ",
    " Kurdî ",
    " Кыргызча ",
    " Ladino ",
    " Лезги ",
    " ລາວ ",
    " Latgaļu ",
    " Latina ",
    " Latviešu ",
    " Lëtzebuergesch ",
    " Lietuvių ",
    " Limburgs ",
    " Lingála ",
    " Lojban ",
    " Lumbaart ",
    " Magyar ",
    " Македонски ",
    " Malagasy ",
    " മലയാളം ",
    " मराठी ",
    " مصرى ",
    " مازِرونی ",
    " Bahasa Melayu ",
    " Baso Minangkabau ",
    " Mìng-dĕ̤ng-ngṳ̄ ",
    " Монгол ",
    " မြန်မာဘာသာ ",
    " Nāhuatl ",
    " Nederlands ",
    " Nedersaksies ",
    " नेपाली ",
    " नेपाल भाषा ",
    " 日本語 ",
    " Napulitano ",
    " Nordfriisk ",
    " Norfuk / Pitkern ",
    " Norsk bokmål ",
    " Norsk nynorsk ",
    " Nouormand ",
    " Novial ",
    " Occitan ",
    " Олык марий ",
    " ଓଡ଼ିଆ ",
    " Oʻzbekcha/ўзбекча ",
    " ਪੰਜਾਬੀ ",
    " پنجابی ",
    " Papiamentu ",
    " پښتو ",
    " Перем Коми ",
    " ភាសាខ្មែរ ",
    " Picard ",
    " Piemontèis ",
    " Tok Pisin ",
    " Plattdüütsch ",
    " Polski ",
    " Português ",
    " Ripoarisch ",
    " Română ",
    " Romani ",
    " Rumantsch ",
    " Runa Simi ",
    " Русиньскый ",
    " Русский ",
    " Саха тыла ",
    " Sámegiella ",
    " Gagana Samoa ",
    " संस्कृतम् ",
    " Sardu ",
    " Scots ",
    " Seeltersk ",
    " Sesotho ",
    " Shqip ",
    " Sicilianu ",
    " සිංහල ",
    " Simple English ",
    " Slovenčina ",
    " Slovenščina ",
    " Словѣньскъ / ⰔⰎⰑⰂⰡⰐⰠⰔⰍⰟ ",
    " Ślůnski ",
    " کوردی ",
    " Sranantongo ",
    " Српски / srpski ",
    " Srpskohrvatski / српскохрватски ",
    " Basa Sunda ",
    " Suomi ",
    " Svenska ",
    " Tagalog ",
    " தமிழ் ",
    " Татарча/tatarça ",
    " తెలుగు ",
    " ไทย ",
    " Тоҷикӣ ",
    " ᏣᎳᎩ ",
    " Türkçe ",
    " Türkmençe ",
    " Українська ",
    " اردو ",
    " Vèneto ",
    " Vepsän kel’ ",
    " Tiếng Việt ",
    " Volapük ",
    " Võro ",
    " Walon ",
    " 文言 ",
    " Winaray ",
    " Wolof ",
    " 吴语 ",
    " ייִדיש ",
    " Yorùbá ",
    " 粵語 ",
    " Zazaki ",
    " Zeêuws ",
    " Žemaitėška ",
    " 中文 ",
    " मैथिली "
]

db = sqlite3.connect('app.db')
db.text_factory = str
for t in topic:
    print t.strip()
    db.execute('INSERT INTO category(name) VALUES (?)', (t.strip(),))
    db.commit()

for t in countries:
    print t.strip()
    db.execute('INSERT INTO country(name) VALUES (?)', (t.strip(),))
    db.commit()

for t in language:
    print t.strip()
    db.execute('INSERT INTO language(language) VALUES (?)', (t.strip(),))
    db.commit()

try:
    db.execute('INSERT INTO feed(name, url, category, country, language) VALUES (?,?,?,?,?)',
               ('ESA Netherlands', 'http://www.esa.int/rssfeed/Netherlands', 15, 125, 114))
except BaseException as e:
    print e, ' pushing feed failed'

db.execute('INSERT INTO user(nickname, email, password, role, status) VALUES (?,?,?,?,?)',
           ('Admin', 'admin@busieslist.com',
            generate_password_hash('admin'), 0, 2))
db.commit()

db.close()