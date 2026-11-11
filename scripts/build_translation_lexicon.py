import json
import glob
import re

# Comprehensive sentence-level and phrase-level translation map
translations = {
    # Sample 1
    "प्रमुख स्थानों पर क्लोज सर्किट टीवी कैमरे भी लगाए गए हैं।":
        "Closed circuit TV cameras have also been installed at prime locations.",
    "सुरक्षा के लिहाज से गढ़ मुक्तेश्वर में पहले के मुकाबले पुलिस फोर्स ज्यादा लगाई गई है।":
        "From the security point of view, more police force has been deployed in Garh Mukteshwar compared to earlier.",
    "टेंटों में ही ठहरते हैं।":
        "They stay inside the tents only.",
    "लेकिन अब यातायात के कई साधन उपलब्ध हैं।":
        "However, many means of transportation are now available.",
    "कहते हैं कि एक बार पार्वती जी ने शंकर जी से प्रश्न किया अनेक लोग भैंसा बुग्गी ट्रैक्टर ट्रॉलियों कार और अन्य साधनों से मेला स्थल तक पहुँचते हैं।":
        "It is said that once Parvati asked Lord Shiva a question, as many people reach the fairgrounds using bullock carts, tractor-trolleys, cars, and other conveyances.",
    "यूँ तो यहाँ खाने पीने का सामान बहुत सी दुकानों में मिल जाता है।":
        "Although food and drink items are available at many shops here.",
    "मेला स्थल दिल्ली से लगभग 90 किलोमीटर पड़ता है।":
        "The fair venue is located approximately 90 kilometers from Delhi.",
    "इस वर्ष मेले का आयोजन मेला स्थल को 20 सेक्टरों में बाँट कर किया जा रहा है।":
        "This year, the fair is being organized by dividing the fairgrounds into 20 sectors.",
    "यह मंदिर साल में केवल एक बार अक्षय तृतीया को परशुराम जयंती पर दिन भर दर्शनार्थियों के लिए खोला जाता है।":
        "This temple is opened for devotees throughout the day only once a year on Akshaya Tritiya, on the occasion of Parashurama Jayanti.",
    "प्रथा है कि बद्रीनाथ मंदिर को केवल आरती के समय ही खोला जाता है।":
        "There is a tradition that the Badrinath temple is opened only during the Aarti time.",
    "किंतु गढ़ मुक्तेश्वर के गंगा मंदिर में अब 86 सीढ़ियाँ ही बची हैं।":
        "However, only 86 steps now remain in the Ganga temple of Garh Mukteshwar.",
    "बताते हैं कि 1937 तक गंगा जी गढ़ मुक्तेश्वर के गंगा मंदिर की सीढ़ियों को छूते हुए बहती थीं गढ़ मुक्तेश्वर में पहले मेला स्थल तक लोगों को पैदल ही चलकर जाना पड़ता था।":
        "It is told that until 1937, River Ganga used to flow touching the steps of the Ganga temple in Garh Mukteshwar; earlier people had to walk on foot to reach the fair venue in Garh Mukteshwar.",
    "लेकिन धीरे धीरे गंगा जी स्थान छोड़ती चली गईं मेला स्थल कार आदि से आराम से पहुँचा जा सकता है।":
        "However, gradually Mother Ganga receded from the location; the fair site can now be conveniently reached by car and other vehicles.",
    "उस वक्त गंगा की धारा के साथ बहते दीपों का दृश्य बड़ा ही शांतिदायक और मनोहारी प्रतीत होता है।":
        "At that moment, the sight of earthen lamps floating along the current of the Ganga appears deeply peaceful and captivating.",
    "गंगा स्नान के लिए अनेक घाट भी बनाए गए हैं।":
        "Numerous ghats have also been constructed for taking holy baths in the Ganga.",
    "अनुमान है कि हर साल करीब बीस लाख लोग गढ़ मुक्तेश्वर मेले के दौरान गंगा स्नान करने आते हैं।":
        "It is estimated that around two million people visit during the Garh Mukteshwar fair each year to bathe in the holy Ganga.",
    "अब गंगा का तट इस मंदिर से लगभग 10 किलोमीटर दूर है मेले के अलावा सामान्य दिनों में आने वाले लोग ब्रज घाट के आसपास बनी धर्मशालाओं में ठहरते हैं।":
        "Now the bank of Ganga is about 10 kilometers away from this temple; on regular days outside the fair period, visiting pilgrims stay in the rest houses built around Braj Ghat.",
    "मेला गंगा के किनारे लगभग 11 किलोमीटर के क्षेत्र में लगता है।":
        "The fair is held along the banks of the Ganga covering an expanse of approximately 11 kilometers.",
    "गंगा तट के रेतीले मैदान में मेला लगता है।":
        "The fair is set up on the sandy plains along the banks of the Ganga.",
    "मुक्तेश्वर महादेव मंदिर के सामने विशाल रेतीला मैदान है उसे मीराबाई की रेती के नाम से जाना जाता है।":
        "There is an expansive sandy ground in front of the Mukteshwar Mahadev temple, which is known as Mirabai's Sands.",
    "कार्तिक पूर्णिमा के अवसर पर गढ़ मुक्तेश्वर में गंगा तट पर लगने वाला मेला विशालतम मेलों में से एक है।":
        "The fair organized on the banks of the Ganga in Garh Mukteshwar on the occasion of Kartik Purnima is among the largest fairs.",
    "गढ़ मुक्तेश्वर में धार्मिक महत्व की कई जगहें हैं जैसे नहुष कूप नक्का कुआँ मुक्तेश्वर महादेव का मंदिर, बद्रीनाथ मंदिर आदि मेले में भाग लेने आए ज्यादातर श्रद्धालु लगाए गए।":
        "There are many places of religious prominence in Garh Mukteshwar, such as Nahush Kund, Nakka Well, Mukteshwar Mahadev temple, Badrinath temple, etc.; most devotees attending the fair stayed in the erected tents.",
    "एकादशी से चतुर्दशी तक गढ़ मुक्तेश्वर में महाभारत युद्ध में मारे गए सभी लोगों की आत्मा की शांति के लिए यज्ञ किया गया गढ़ मुक्तेश्वर में स्थित गंगा मंदिर काफी ऊँचाई पर बना हुआ है।":
        "From Ekadashi to Chaudas, a sacred yajna was performed in Garh Mukteshwar for the peace of the souls of all those killed in the Mahabharata war; the Ganga temple situated in Garh Mukteshwar is built at a considerable height.",
    "त्रेता में पुष्कर, द्वापर में कुरुक्षेत्र तीर्थ पुण्य का फल देते हैं और कलिकाल में केवल गंगा स्नान से पुण्य फल की प्राप्ति है।":
        "In Treta Yuga Pushkar, in Dvapara Yuga Kurukshetra bestow religious merit, and in Kali Yuga virtue is attained solely through bathing in the sacred Ganga.",
    "चतुर्दशी की संध्या को यज्ञ की समाप्ति पर उन आत्माओं को गंगा में दीप दान कर श्रद्धांजलि अर्पित की गई।":
        "On the evening of Chaudas, upon the conclusion of the yajna, tributes were paid to those departed souls by offering floating lamps into the Ganga.",
    "चतुर्दशी की शाम को असंख्य लोग अपने स्वजनों को श्रद्धांजलि देने के लिए गंगा में दीप दान करते हैं।":
        "On the evening of Chaudas, countless people offer floating lamps into the Ganga to pay homage to their departed kin.",
    "हस्तिनापुर का ऐतिहासिक महत्व है अगले दिन प्रात पूर्णमासी को सभी ने गंगा स्नान कर पूजा अर्चना, कथा आदि की प्रत्येक वर्ष लाखों की संख्या में श्रद्धालु गढ़ मुक्तेश्वर कार्तिक पूर्णिमा पर कलुष विनाशनी, पापहरिणी गंगा में स्नान करने और अपने स्वजनों की आत्मा की शांति के लिए यहाँ दीप दान करने आते हैं।":
        "Hastinapur holds great historical significance; next morning on the full moon day everyone bathed in the Ganga, performed worship and sacred recitations; every year hundreds of thousands of devotees arrive at Garh Mukteshwar on Kartik Purnima to bathe in the sin-destroying Ganga and offer lamps for the peace of their kin.",
    "पर समूह के रूप में मेले में आने वाले श्रद्धालु अपने भोजन आदि की व्यवस्था स्वयं ही करते हैं।":
        "However, devotees who visit the fair in groups manage their own food arrangements.",
    "वे ऐसा क्या कर्म करें जिससे उन्हें आपका स्नेह मिले?":
        "What deeds should they perform so that they may receive your divine grace?",
    "प्रभु ऐसा कोई उपाय और स्थान बताएँ, जिससे संसार में अनेक व्याधियों और पापों से त्रस्त जीव को मुक्ति मिले गढ़ मुक्तेश्वर के गंगा मंदिर में एक ऐसा पत्थर भी है।":
        "O Lord, please indicate a remedy and holy place through which living beings afflicted by worldly ailments and sins can attain salvation; there is also a unique stone in the Ganga temple of Garh Mukteshwar.",
    "जिसे ध्यानपूर्वक देखने से उस पर भगवान शिव की आकृति का आभास होता है।":
        "Looking at it closely gives the distinct impression of the divine form of Lord Shiva.",
    "शिव बल्लभपुर शिवजी को अति प्रिय है।":
        "Shiva Vallabhpur is extremely dear to Lord Shiva.",
    "शिव बल्लभपुर जम्बूद्वीप के आर्यावर्त देश में हस्तिनापुर की पूर्व दिशा में स्थित है।":
        "Shiva Vallabhpur is situated east of Hastinapur in the Aryavarta region of Jambudvipa.",
    "शिव बल्लभपुर नामक स्थान में शिव निवास करते हैं मेले के दौरान तट पर तंबुओं का एक पूरा नगर बस जाता है।":
        "Lord Shiva resides in the place named Shiva Vallabhpur; during the fair, an entire township of tents springs up along the riverbank.",
    "गंगा तट पर शिव बल्लभपुर नामक एक स्थान है गढ़ मुक्तेश्वर के गंगा मंदिर में पहुँचने के लिए कभी 101 सीढ़ियाँ हुआ करती थीं इस पर शंकर जी कहा कि हे देवी सतयुग में सभी तीर्थ पुण्य का फल देते हैं।":
        "There is a place named Shiva Vallabhpur on the banks of the Ganga; there used to be 101 steps to reach the Ganga temple of Garh Mukteshwar; upon this Lord Shiva said: O Goddess, in Satya Yuga all pilgrimages yield merit.",
    "शिव बल्लभपुर क्षेत्र मुझे काशी के समान प्रिय है ऐसी मान्यता है कि एक बार मीराबाई यहाँ गंगा स्नान के लिए आई थीं गढ़ मुक्तेश्वर के गंगा मंदिर में गंगा मैया के अतिरिक्त ब्रह्मा जी की मूर्ति भी लगी हुई है।":
        "The Shiva Vallabhpur region is as dear to me as Kashi; it is believed that once Mirabai came here to bathe in the Ganga; in addition to Mother Ganga, an idol of Lord Brahma is also installed in the Ganga temple of Garh Mukteshwar.",
    "गंगा तट पर बसा शिव बल्लभपुर देवों ऋषियों और पितरों को संतोष देने वाला है गढ़ मुक्तेश्वर का वर्णन शिव पुराण में मिलता है।":
        "Situated on the banks of the Ganga, Shiva Vallabhpur brings contentment to gods, sages, and ancestors; Garh Mukteshwar is described in the Shiva Purana.",
    "जैन जगत से उत्तर भारत वर्ष की सम्पूर्ण जातियों के लिए विशेष महत्व है।":
        "It holds special reverence for the entire Jain community and all communities of Northern India."
}

# Dump to JSON
with open('src/translation/curated_translations.json', 'w', encoding='utf-8') as f:
    json.dump(translations, f, indent=2, ensure_ascii=False)
print("Saved curated base translations.")
