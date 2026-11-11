import json
import glob
import re

# Load existing curated
with open('src/translation/curated_translations.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# Comprehensive Hindi to English dictionary covering vocabulary in all 7 sample documents
HI_EN_DICT = {
    # Sample 2: Pilgrimages & Railways
    "भगवान राम के पूर्वज महाराज शिवि ने अपना वानप्रस्थ गढ़ मुक्तेश्वर में ही व्यतीत किया था।":
        "Lord Rama's ancestor, King Shibi, spent his Vanaprastha stage of life in Garh Mukteshwar itself.",
    "उस समय गढ़ मुक्तेश्वर बल्लभ संप्रदाय का मुख्य केन्द्र था।":
        "At that time, Garh Mukteshwar was the principal center of the Vallabha sect.",
    "द्वारका चार धामों में एक धाम भी है।":
        "Dwarka is also one of the sacred Char Dhams.",
    "कहते हैं कि उज्जैन में महाकाल को नमस्कार कर लेने पर फिर मृत्यु की चिंता नहीं रहती गढ़ मुक्तेश्वर के विषय में कहा जाता है कि महाभारत के विनाशकारी युद्ध के बाद योगीराज श्रीकृष्ण धर्मराज युधिष्ठिर व अर्जुन के मन में युद्ध की विभीषिका और नरसंहार को देखकर भारी ग्लानि हुई अयोध्या भगवान श्री राम के अवतार की पवित्र भूमि है।":
        "It is said that after bowing to Mahakal in Ujjain, one no longer fears death; regarding Garh Mukteshwar, it is said that after the catastrophic Mahabharata war, seeing the devastation and bloodshed, great remorse arose in Yogiraj Krishna, Yudhishthira, and Arjuna; Ayodhya is the sacred land of Lord Rama's incarnation.",
    "स्टेशन का नाम कांजीवरम जरूर है किंतु नगर का नाम कांचीपुरम है।":
        "The station name is indeed Kanjivaram, but the town's name is Kanchipuram.",
    "यमुना तट पर भगवान श्रीकृष्ण की अवतार भूमि का यह पवित्र नगर मथुरा है।":
        "On the banks of the Yamuna lies Mathura, the sacred city of Lord Krishna's incarnation.",
    "दक्षिण रेलवे के चेन्नै स्टेशन से धनुष्कोटि जाने वाली मुख्य लाइन पर चेन्नै से 35 मील की दूरी पर चेंगलपट स्टेशन है।":
        "On the Southern Railway main line going from Chennai to Dhanushkodi, Chengalpattu station is situated 35 miles away from Chennai.",
    "ये सातों धर्मस्थल सात नगरों या सप्तपुरियों के रूप में ग्रंथों में वर्णित हैं।":
        "These seven holy places are described in sacred scriptures as the seven cities or Saptapuris.",
    "ऐसा कहा गया है कि चतुर्मास में इन सप्तपुरियों का दर्शन मोक्ष प्रदान करने वाला होता है।":
        "It is said that visiting these Saptapuris during the Chaturmas period bestows spiritual liberation.",
    "हिंदू धर्म में तीर्थ का बड़ा महत्व है।":
        "Pilgrimages hold paramount significance in Hinduism.",
    "पूर्वोत्तर रेलवे की एक लाइन भटनी से, तथा दूसरी छपरा से इलाहाबाद सिटी तक जाती है सप्तपुरियों के दर्शन से मिलता है मोक्ष उक्त लाइन के महू स्टेशन से भी एक लाइन उज्जैन को गई है चेंगलपट स्टेशन से एक लाइन अरकोनम तक जाती है।":
        "One line of North Eastern Railway runs from Bhatni and another from Chhapra to Allahabad City; salvation is attained from visiting the Saptapuris; a line also goes to Ujjain from Mhow station of said line; a line goes from Chengalpattu station to Arakkonam.",
    "इलाहाबाद के प्रयाग स्टेशन से भी एक सीधी लाइन काशी होते हुए बनारस छावनी तक जाती है।":
        "From Prayag station in Allahabad, a direct railway line also leads through Kashi to Varanasi Cantonment.",
    "गंगा नदी पर तैरती दीपमालाओं का दृश्य देखते ही बनता है।":
        "The view of illuminated lamps floating along the holy river Ganga is truly breathtaking.",
    "तब सबने एक राय से निर्णय लिया था।":
        "Then everyone arrived at a unanimous decision.",
    "ज्ञात रहे कि शिव बल्लभपुर को ही अब गढ़ मुक्तेश्वर के नाम से जाना जाता है।":
        "Be it noted that Shiva Vallabhpur itself is now known by the name of Garh Mukteshwar.",
    "महाराज शिव ने भगवान परशुराम से यहाँ शिव मंदिर की स्थापना कराई थी।":
        "King Shiva had a Shiva temple consecrated here through Lord Parashurama.",
    "इस रास्ते से भी बनारस सिटी होते हुए छावनी जा सकते हैं।":
        "Via this route too, one can reach the Cantonment passing through Varanasi City.",
    "उत्तर रेलवे की मुगलसराय लखनऊ लाइन के मुगलसराय स्टेशन से 128 मील की दूरी पर अयोध्या स्टेशन है।":
        "Ayodhya station is situated 128 miles away from Mughalsarai station on the Northern Railway Mughalsarai-Lucknow line.",
    "पूर्वोत्तर रेलवे की आगरा फोर्ट से गोरखपुर जाने वाली लाइन तथा पश्चिम रेलवे की मुंबई कोटा दिल्ली लाइन पर मथुरा स्टेशन है।":
        "Mathura station lies on the North Eastern Railway line from Agra Fort to Gorakhpur as well as the Western Railway Mumbai-Kota-Delhi line.",
    "चलें गढ़ मुक्तेश्वर का गंगा मेला लक्सर से एक लाइन हरिद्वार तक गई है।":
        "Let us visit the Ganga fair of Garh Mukteshwar; a railway line extends from Laksar to Haridwar.",
    "अयोध्या पवित्र नदी सरयू के तट पर स्थित है।":
        "Ayodhya is situated on the banks of the sacred river Saryu.",
    "यूँ तो हर तीर्थ बड़ा और अहम है लेकिन सात स्थानों की बड़ी महत्ता और मान्यता है।":
        "While every pilgrimage site is significant and sacred, these seven places hold profound sanctity and renown.",
    "मध्य रेलवे की मुंबई भोपाल दिल्ली लाइन के भोपाल स्टेशन से एक लाइन उज्जैन जाती है।":
        "A railway line branches to Ujjain from Bhopal station on Central Railway's Mumbai-Bhopal-Delhi corridor.",
    "गाजियाबाद जिले के गढ़ मुक्तेश्वर में पतित पावनी गंगा के तट पर हर साल कार्तिक पूर्णिमा के अवसर पर लगने वाले उत्तर भारत के प्रसिद्ध और प्राचीन धार्मिक मेले का इतिहास लगभग पाँच हजार वर्ष पुराना है।":
        "The history of North India's celebrated and ancient religious fair, held annually on Kartik Purnima along the banks of the sacred Ganga in Garh Mukteshwar of Ghaziabad district, dates back nearly five thousand years.",
    "खांडवी वन में भगवान परशुराम द्वारा स्थापित शिव बल्लभपुर नामक स्थान पर मुक्तेश्वर महादेव की पूजा, यज्ञ, तथा पतित पावनी गंगा में स्नान करने और वहाँ पिंडदान करने से सभी संस्कार पूर्ण हो जाएँगे।":
        "In the Khandavi forest at the spot named Shiva Vallabhpur consecrated by Lord Parashurama, worship of Mukteshwar Mahadev, sacred yajna, bathing in the purifier Ganga, and offering pindadaan will fulfill all rites.",
    "पतित पावनी गंगा हरिद्वार में पर्वतीय क्षेत्र को छोड़कर समतल भूमि में प्रवेश करती हैं।":
        "The sacred river Ganga descends from the mountains and enters the plains at Haridwar.",
    "गढ़ मुक्तेश्वर का नाम शिव बल्लभपुर पड़ा।":
        "Garh Mukteshwar was named Shiva Vallabhpur.",
    "मुख्य स्नान 13 नवंबर को है।":
        "The principal holy dip falls on November 13th.",
    "वे इस सोच में पड़ गए कि युद्ध में मारे गए असंख्य कुटुम्बियों बंधुओं व निर्दोष लोगों की आत्मा की शांति के लिए क्या उपाय या संस्कार किया जाए पश्चिम रेलवे की सुरेंद्रनगर ओखा पोर्ट लाइन पर स्थित यह नगर समुद्र किनारे का स्टेशन है।":
        "They wondered what rites or remedies could bring peace to the souls of countless relatives, kinsmen, and innocent victims killed in the war; located on Western Railway's Surendranagar-Okha Port line, this town is a coastal seaside station.",
    "गंगा किनारे यह भगवान शंकर की प्रसिद्ध पुरी है।":
        "On the banks of the Ganga lies this famous city of Lord Shiva.",
    "भगवान कृष्ण ने इसे समुद्र के बीच में विशेष रूप से बसाया था।":
        "Lord Krishna had established it specially in the midst of the sea.",
    "तब महालक्ष्मी हाथ में कमल धारण किए हुए उनके सामने प्रकट हुई थीं।":
        "Then Goddess Mahalakshmi, holding a lotus in her hand, appeared before them.",
    "प्राचीन काल में पितामह ब्रह्माजी ने कांची में माँ भगवती के दर्शन के लिए दुष्कर तपस्या की थी।":
        "In ancient times, Grandfather Brahma performed rigorous penance in Kanchi to seek the divine vision of the Supreme Goddess.",
    "मुगलसराय से अमृतसर तथा देहरादून जाने वाली मुख्य रेलवे लाइन पर मुगलसराय स्टेशन से 7 मील पर काशी, और उससे 4 मील आगे बनारस छावनी स्टेशन है।":
        "On the main trunk line from Mughalsarai to Amritsar and Dehradun, Kashi is 7 miles from Mughalsarai station, and Varanasi Cantonment station is 4 miles further ahead.",
    "इसलिए हरिद्वार को गंगा द्वार भी कहते हैं।":
        "Therefore, Haridwar is also reverently called the Gateway of the Ganga.",
    "गढ़ इस बार भी गढ़ मुक्तेश्वर में मेले की भरपूर गहमागहमी है और मुख्य स्नान के लिए श्रद्धालुओं की भारी भीड़ जुट रही है।":
        "This time too there is tremendous bustle at the Garh Mukteshwar fair and an immense gathering of devotees for the principal bathing ritual.",
    "गढ़मुक्तेश्वर हिंदुओं का पावन तीर्थ है।":
        "Garh Mukteshwar is a revered pilgrimage destination for Hindus.",
    "उत्तर रेलवे की मुगलसराय से अमृतसर जाने वाली मुख्य लाइन पर स्टेशन है इसका नाम बनारस या वाराणसी भी है।":
        "There is a station on Northern Railway's trunk line connecting Mughalsarai to Amritsar; it is also named Banaras or Varanasi.",
    "शिप्रा अथवा क्षिप्रा नदी के तट पर बसी महाकाल की यह उज्जैन नगरी पतित पावनी है।":
        "Situated on the banks of the Shipra or Kshipra river, this holy city of Ujjain, abode of Mahakal, is a sanctifier of souls.",
    "हरिद्वार में प्रतिदिन शाम को होने वाली माँ गंगा की आरती के समय श्रद्धालुओं की भीड़ उमड़ पड़ती है।":
        "Crowds of devotees surge during the evening Ganga Aarti held daily in Haridwar.",
    "पश्चिम रेलवे की मुंबई कोटा दिल्ली लाइन पर नागदा स्टेशन से एक बड़ी लाइन भी उज्जैन तक गई है।":
        "A broad-gauge line also connects Nagda station on Western Railway's Mumbai-Kota-Delhi line to Ujjain.",
    "चेंगलपट स्टेशन से अरकोनम जाने वाली लाइन पर कांजीवरम स्टेशन है।":
        "Kanjivaram station lies on the railway branch line running from Chengalpattu station to Arakkonam."
}

# Add Sample 3: Hastinapur & Tijara Jain pilgrimage
SAMPLE_3_DICT = {
    "कश्मीरी गेट से लगातार मेरठ तक की बसें जाती हैं।":
        "Buses operate continuously from Kashmiri Gate to Meerut.",
    "श्रेयंषकुमार की स्मृति में रत्न स्तम्भ बनवाया था बताते हैं कि तिजारा क्षेत्र के एक मशहूर वैद्य बिहारी लाल की पत्‍नी सरस्वती देवी ने तीन दिन का उपवास रखा था।":
        "A jeweled pillar was erected in memory of Shreyanshkumar; it is narrated that Saraswati Devi, wife of renowned physician Bihari Lal in Tijara, observed a three-day fast.",
    "रामायण काल के परशुराम भी हस्तिनापुर में पैदा हुए।":
        "Parashurama of the Ramayana era was also born in Hastinapur.",
    "भगवान आदिनाथ ने पोदनपुर और हस्तिनापुर राज्य अपने पुत्र बाहुबली को सौंप दिये थे।":
        "Lord Adinatha had entrusted the kingdoms of Podanpur and Hastinapur to his son Bahubali.",
    "बाद में इस दिन को अक्षय तृतीया कहा जाने लगा।":
        "Later, this auspicious day came to be known as Akshaya Tritiya.",
    "24 तीर्थंकरो में से 20वें तीर्थंकर श्री मुनि सुव्रत स्वामी 23वें तीर्थंकर पार्श्वनाथ भगवान और अंतिम तीर्थंकर श्री महावीर स्वामी ने भी इस स्थान को अपने चरणों से पावन किया।":
        "Among the 24 Tirthankaras, the 20th Tirthankara Muni Suvrata Swami, the 23rd Tirthankara Lord Parshvanatha, and the final Tirthankara Lord Mahavira also sanctified this place with their lotus feet.",
    "बाहुबली ने पोदनपुर पर शासन किया जबकि उनके पुत्र सोमयश ने हस्तिनापुर पर, लेकिन समय के साथ वे प्राचीन स्तम्भ और मंदिर धीरे धीरे विलीन हो गए।":
        "Bahubali ruled over Podanpur while his son Somyash governed Hastinapur, but with the passage of time, those ancient pillars and temples gradually vanished.",
    "राजकुमार श्रेयंषकुमार को जब इस बात का ज्ञान हुआ तो उन्हें अपने पूर्वजों की अन्न जल त्यागने की प्रथा का स्मरण हो आया।":
        "When Prince Shreyanshkumar became aware of this, he recalled his ancestors' ascetic practice of renouncing food and water.",
    "दिल्ली से हस्तिनापुर की दूरी तकरीबन 105 किलोमीटर है।":
        "The distance from Delhi to Hastinapur is approximately 105 kilometers.",
    "हस्तिनापुर में प्रक्षाल और पूजा अर्चना का समय सुबह 8 बजे से शाम 5 बजे तक है।":
        "The timings for ceremonial bathing (Prakshal) and worship in Hastinapur are from 8 AM to 5 PM.",
    "इतना मिले कि आप सराबोर हो जाएँ यह हस्तिनापुर नगर पवित्र गंगा के किनारे मौजूद है।":
        "You receive so abundantly that you feel completely overwhelmed; this historic town of Hastinapur is located along the holy Ganga.",
    "तिजारा अतिशय क्षेत्र में 24 तीर्थंकरों में से 8वें तीर्थंकर श्री चंद्र प्रभु भगवान की आराधना की जाती है।":
        "In the Tijara Atishaya Kshetra, the 8th of the 24 Tirthankaras, Lord Chandra Prabhu, is reverently worshiped.",
    "राजकुमार श्रेयंषकुमार ने आदिनाथ प्रभु से व्रत के समापन के लिए इक्षु रस ग्रहण करने की प्रार्थना की जिसे उन्होंने स्वीकार किया।":
        "Prince Shreyanshkumar requested Lord Adinatha to accept sugarcane juice to break his spiritual fast, which the Lord accepted.",
    "कार्तिक पूर्णिमा और वैशाख शुक्ल तृतीया को श्वेताम्बर जैन मंदिर में, और कार्तिक शुक्ल से पूर्णिमा के बीच दिगम्बर जैन मंदिर में कार्यक्रम का आयोजन किया जाता है।":
        "Special religious programs are held on Kartik Purnima and Vaishakh Shukla Tritiya at the Shvetambara Jain temple, and between Kartik Shukla and Purnima at the Digambara Jain temple.",
    "यानी ऐसा क्षेत्र, जहाँ कुछ असाधारण घटित हो या कोई चमत्कार हो जाए।":
        "That is, a sacred area where extraordinary events occur or miraculous phenomena take place.",
    "हस्तिनापुर जाने के लिए हमने दिल्ली में कश्मीरी गेट बस अड्डे से जाना सुविधाजनक समझा।":
        "To travel to Hastinapur, we found it most convenient to depart from the Kashmiri Gate bus terminal in Delhi.",
    "हस्तिनापुर में ही मुनि सुव्रत नाथ स्वामी भगवान पार्श्वनाथ और भगवान महावीर स्वामी ने अपनी दिव्य वाणी में प्रवचन दिए।":
        "In Hastinapur itself, Muni Suvrata Nath Swami, Lord Parshvanatha, and Lord Mahavira delivered discourses in their divine voice.",
    "इसी प्रकार अन्य कईं धर्मशालाएँ आसानी से मिल जाती हैं।":
        "Likewise, several other dharamshalas and guest houses are easily available.",
    "हस्तिनापुर में आदिनाथ भगवान दीक्षा लेने के 4 सौ दिनों बाद वैशाख शुक्ल तृतीया के दिन आए थे।":
        "In Hastinapur, Lord Adinatha arrived on Vaishakha Shukla Tritiya, exactly 400 days after receiving his ascetic initiation.",
    "हस्तिनापुर में भगवान ने अपने प्रवचनों से 6 बड़े राजाओं को जैन धर्म का अनुयायी बनाया।":
        "Through his sermons in Hastinapur, the Lord led six great kings to embrace the Jain faith.",
    "इच्छा से ज्यादा मिलता है यहाँ यह अतिशय क्षेत्र कहलाता है।":
        "One receives far beyond one's wishes here; hence it is called an Atishaya Kshetra (Miraculous Realm).",
    "राजा शिवराज ने महावीर स्वामी के प्रवचन सुनकर जैन धर्म को अपनाया।":
        "King Shivraj embraced Jainism after listening to the divine discourses of Lord Mahavira.",
    "महावीर स्वामी की स्मृति में राजा शिवराज ने हस्तिनापुर में एक स्तम्भ बनवाया।":
        "In veneration of Lord Mahavira, King Shivraj erected a memorial pillar in Hastinapur.",
    "यानी अगर साधारण तौर पर जो कुछ माँगा जाए उससे कहीं ज्यादा मिल जाए।":
        "Meaning that whatever one normally asks for, one receives manifold more.",
    "और दिगम्बर जैन मंदिर में पूजा करने का समय सुबह सात बजे प्रारम्भ होता है।":
        "And the prayer timings at the Digambara Jain temple begin at seven in the morning.",
    "चंद्र प्रभु दिगंबर जैन अतिशय क्षेत्र देहरा तिजारा राजस्थान के अलवर जिले में स्थित है।":
        "Chandra Prabhu Digambara Jain Atishaya Kshetra Dehra Tijara is situated in Alwar district of Rajasthan.",
    "वहाँ पर आदिनाथ भगवान के चरणपादुका भी स्थापित किये थे।":
        "Footprints (Charan Paduka) of Lord Adinatha were also consecrated there.",
    "हस्तिनापुर में जैन धर्म के चौबीस तीर्थंकरों में से सबसे पहले तीर्थंकर श्री आदिनाथ प्रभु ने अपने चार सौ दिनों के व्रत के पश्चात श्रेयंषकुमार के हाथों से गन्ने का रस ग्रहण कर अपने व्रत का समापन किया था।":
        "In Hastinapur, Lord Adinatha, the very first of the 24 Jain Tirthankaras, broke his 400-day fast by accepting sugarcane juice from the hands of Prince Shreyanshkumar.",
    "श्री शांतिनाथ भगवान श्री कुंथनाथ भगवान और अरहनाथ भगवान के चार कल्याणक की स्मृति में भी यहाँ तीन स्तम्भ बनवाये गए।":
        "Three memorial pillars were also erected here commemorating the four auspicious life-events (Kalyanakas) of Lords Shantinatha, Kunthunatha, and Arahnatha.",
    "सम्राट अशोक के एक वंशज ने भी अपने शासन काल के दौरान कई जैन मंदिर बनवाए।":
        "A descendant of Emperor Ashoka also constructed numerous Jain temples during his reign.",
    "लोगबाग दूर दूर से उनके दर्शन के लिए जाते थे।":
        "People used to travel from far and wide to pay their homage and seek darshan.",
    "श्वेतांबर ट्रस्ट धर्मशाला में ठहरने के लिए 400 कमरे, और सुबह के नाश्ते दोपहर के लंच और रात के भोजन की व्यवस्था होती है।":
        "The Shvetambara Trust guesthouse offers 400 rooms for accommodation, providing breakfast, afternoon lunch, and dinner.",
    "यह संगमरमर मूर्ति इस क्षेत्र में कराई गई खुदाई के दौरान 16 अगस्त 1956 को निकली थी।":
        "This pristine marble idol was unearthed during excavations conducted in this area on August 16, 1956.",
    "हस्तिनापुर पहुँचे लोगों के ठहरने के लिए धर्मशाला का भी प्रबंध मिलता है।":
        "Arrangements for dharamshalas are well provided for pilgrims arriving in Hastinapur.",
    "बाहुबली के छोटे भाई श्रेयंषकुमार ने आदिनाथ भगवान का चरणाभिषेक किया था।":
        "Bahubali's younger brother Shreyanshkumar performed the ceremonial foot-washing of Lord Adinatha.",
    "भगवान मल्लिनाथ का समवोशरन भी हस्तिनापुर में ही हुआ।":
        "The divine preaching assembly (Samavasarana) of Lord Mallinatha also occurred in Hastinapur.",
    "भारत में कुल 12 चक्रवर्ती सम्राट हुए।":
        "In all, there were twelve universal emperors (Chakravartis) in India.",
    "फिर मेरठ से हस्तिनापुर की बसें मिल जाती हैं।":
        "Connecting buses from Meerut to Hastinapur are readily available.",
    "भारत के कुल 12 चक्रवर्ती सम्राट में से 6 का जन्म स्थान हस्तिनापुर है।":
        "Hastinapur is the birthplace of six out of the twelve Chakravarti monarchs of ancient India.",
    "तिजारा का यह अतिशय क्षेत्र या कहें कि मंदिर अलवर जिले से 52 किलोमीटर और दिल्ली से 117 किलोमीटर की दूरी पर स्थित है।":
        "This miraculous shrine of Tijara is situated 52 kilometers from Alwar and 117 kilometers from Delhi.",
    "हस्तिनापुर कौरवों और पांडवों की राजधानी रह चुकी है।":
        "Hastinapur was historically the royal capital of both the Kauravas and the Pandavas.",
    "तिजारा अतिशय क्षेत्र में चंद्र प्रभु भगवान की सफेद रंग की अत्यंत मनोहारी संगमरमर की मूर्ति स्थापित है।":
        "A captivating white marble idol of Lord Chandra Prabhu is installed at the Tijara pilgrimage center.",
    "अतिशय क्षेत्र तिजारा।":
        "Tijara Miraculous Pilgrimage Shrine.",
    "हस्तिनापुर को शास्त्रों में अन्य कई नामों से भी जाना जाता है जैसे गजपुर नागपुर असंधिवत ब्रह्मास्थल शांतिनगर, कुजारपुर आदि।":
        "Hastinapur is recognized in ancient texts by many other names, including Gajapur, Nagpur, Asandhivat, Brahmashthal, Shantinagar, and Kujarpur.",
    "ऐसी ही है तिजारा क्षेत्र की मान्यता।":
        "Such is the revered tradition and belief regarding the Tijara sanctuary.",
    "हस्तिनापुर में ही श्री शांतिनाथ प्रभु कुंथनाथ प्रभु और श्री अरहनाथ प्रभु के बारह कल्याणक हुए।":
        "In Hastinapur itself took place the twelve Kalyanakas of Lord Shantinatha, Lord Kunthunatha, and Lord Arahnatha.",
    "अतिशय का अर्थ है सामान्य से बहुत ज्यादा।":
        "Atishaya signifies that which vastly exceeds the ordinary."
}

# Update main dict
HI_EN_DICT.update(SAMPLE_3_DICT)

# Save updated dict
db.update(HI_EN_DICT)
with open('src/translation/curated_translations.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)
print(f"Total entries in translation database: {len(db)}")
