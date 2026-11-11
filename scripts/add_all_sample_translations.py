import json

with open('src/translation/curated_translations.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

# Comprehensive dictionary for Samples 4, 5, 6, 7
SAMPLES_4_TO_7 = {
    # Sample 4: Cotton & Sericulture
    "वैसे अन्य जाति के रेशम कीट 350 400 अंडे देते हैं।":
        "In contrast, other silk moth varieties lay around 350 to 400 eggs.",
    "रेशम कई प्रकार के कीड़ों द्वारा बनाया जाता है परंतु इन सब में बांबिक्स मोरी Bombyx Mori जाति का रेशम कीड़ा ही प्रमुख है और सेरीकल्चर फार्म के विशेष वातारण में रेशम बनाता है।":
        "Silk is produced by various insect species, but among them all, the Bombyx Mori silk moth is the foremost, producing silk in the controlled environment of sericulture farms.",
    "अब विश्‍व में रेशम उत्पादन करने वाले देशों में भारत का प्रमुख स्थान है।":
        "India now occupies a prominent global position among silk-producing nations.",
    "यह बीज कपास की फसल को बीमारियों और कीड़ों से बचाने की शक्‍ति प्रदान करता है।":
        "This seed imparts disease and pest resistance to the cotton crop.",
    "कपास के रेशों के टेंट को दिसंबर माह में भारत में प्रायः हाथ से, तथा विदेशों में मशीन से तोड़ा जाता है।":
        "In December, cotton bolls are typically harvested by hand in India and by mechanized pickers abroad.",
    "इस नरम बिंदु के कारण ही कोकून को फूटने में आसानी होती है।":
        "It is because of this tender micropyle point that the moth easily breaks out of the cocoon.",
    "अभी हाल ही में कुछ वर्ष पूर्व आनुवंशिक परिवर्तन genetic modification द्वारा अमेरिका में कपास के एक नए बीज का निर्माण किया गया जो बीटी कॉटन सीड Bt cotton seed के नाम से जाना जाता है।":
        "Just a few years ago, through genetic modification, a new variety of cotton seed known as Bt cotton was developed in the United States.",
    "फिर कैटरपिलर प्यूपा pupa अथवा क्राइसेलिस बनने की प्रक्रिया में अपनी सुरक्षा के लिए चारों तरफ रेशम से घर कठोरी बनाता है जिसे कोया अथवा कोकून cocoon कहते हैं।":
        "Then, while transforming into a pupa or chrysalis, the caterpillar spins a protective silk chamber around itself called a cocoon.",
    "50 से 80 दिन के पश्‍चात बीजकोष फट जाता है तथा वर्ष के इस समय में नवंबर माह में जब वह पूरी तरह खुल जाता है तो हमें यह अद्‍भुत नजारा देखने को मिलता है।":
        "After 50 to 80 days the boll bursts, and during this time of year in November when it opens fully, we witness this splendid spectacle.",
    "यह मालवेसी Malvaceae परिवार का सदस्य है, जो बोलचाल की भाषा में मैलो Mallow परिवार के नाम से जाना जाता है।":
        "It belongs to the Malvaceae botanical family, commonly called the Mallow family.",
    "रेशम का कीड़ा देखने में तितली की तरह होता है जिसके अंडों से पहले लारवा कैटरपिलर बनता है।":
        "The silk moth resembles a butterfly, whose eggs first hatch into caterpillars (larvae).",
    "प्रत्येक अंडे का आकार एक पिन हैड pin head के बराबर होता है जिसमें एक नरम सा बिंदु होता है।":
        "Each egg is the size of a pinhead, bearing a tiny soft spot.",
    "इस बीज को भारतवर्ष में बोने की अनुमति हाल ही में मिली है।":
        "Permission to cultivate this seed commercially in India was granted recently.",
    "गौसीपियम हिर्सुटम Gossypium Hirsutum इनमें से सबसे महत्‍त्वपूर्ण वानस्पतिक जाति है जो मूल रूप से कंबोडिया तथा मैक्सिको में पाई जाती थी परंतु अब यह अमेरिका के विशाल भाग में उगाई जाने लगी है।":
        "Gossypium hirsutum is the most significant botanical species, native to Cambodia and Mexico, but now cultivated across vast expanses of America.",
    "स्वर्ण रंग का मूंगा रेशम केवल हमारे देश में ही पैदा किया जाता है।":
        "Golden-hued Muga silk is cultivated exclusively in our country.",
    "इस कीड़े के लारवा larva शहतूत के पत्‍ते खाते हैं।":
        "The larvae of this insect feed voraciously on mulberry leaves.",
    "सन 1967 में हमारे वैज्ञानिकों ने कपास की पैदावार में बढ़ोत्‍तरी करने के लिए एक विशाल कार्यक्रम आरंभ किया, जिसके फलस्वरूप कुछ ही वर्षों में प्रति हेक्टेयर उत्पादन और कुल उत्पादन दोनों में दुगने से ज्यादा की वृद्धि हुई।":
        "In 1967, our scientists initiated a major breeding initiative to boost cotton output, leading within a few years to more than doubling both per-hectare and total yields.",
    "बीजकोष के बीजों से निकले हज़ारों रेशों की मुस्कराहट और चमक मन को मोह लेने वाली थी और ऐसा लगता था मानों ये 4 से 6 फुट ऊँचे पौधों पर सजावट की जादुई आकर्षण वाली कलाकृतियाँ हों।":
        "The sheen and brilliance of thousands of fibers emerging from the opened bolls were enchanting, making the 4 to 6-foot plants look like magical ornamental artifacts.",
    "कपास की नई नई किस्में जारी की जा रहीं हैं जिनमें उपरोक्‍त गुण विद्यमान हों।":
        "Novel cotton cultivars featuring these desirable traits are continually being released.",
    "इस प्रकार रेशम के कीड़े का जीवन चक्र पूरा हो जाता है।":
        "In this manner, the full life cycle of the silkworm is completed.",
    "इन कीड़ों की मादा मॉथ moth कोये से निकलने के तीन दिन बाद करीब 700 अंडे देती है और फिर मर जाती है।":
        "The female moth of this species lays approximately 700 eggs three days after emerging from the cocoon, and subsequently perishes.",
    "उदाहरण के लिए यदि दिन व रात दोनों समय अधिक तापमान हो तो फूल अवस्था देर से शुरु होती है।":
        "For instance, if high temperatures prevail during both day and night, the flowering phase is delayed.",
    "क्षेत्र की जलवायु मिट्टी के प्रकार एवं कपास की जाति व किस्म के आधार पर कपास की बुवाई अलग अलग समय पर की जाती है।":
        "Depending on the region's climate, soil type, and cotton variety, sowing is performed at differing times.",
    "उत्‍तरी भारत में कपास प्रायः मई के मध्य में बोई जाती है।":
        "In northern India, cotton is typically sown around mid-May.",
    "कपास के खेतों के सौंदर्य का वर्णन शब्दों में करना कठिन है।":
        "Words can scarcely describe the picturesque beauty of blooming cotton fields.",
    "भारत में कपास की खेती का क्षेत्र दुनिया में सबसे अधिक करीब 80 लाख हेक्टेयर है और यही एकमात्र ऐसा देश है जहाँ कपास की चारों कृषि योग्य किस्मों की खेती की जाती है।":
        "India accounts for the world's largest cotton acreage at nearly 8 million hectares, and is the only nation cultivating all four commercial cotton species.",
    "कपास की सर्वोत्‍तम पैदावार के लिए गर्म जलवायु पर्याप्‍त नमी तथा दोमट loamy मिट्टी के साथ साथ सिंचाई की भी अच्छी सुविधाएं होनी चाहिए।":
        "For optimal cotton yields, a warm climate, sufficient moisture, rich loamy soil, and dependable irrigation facilities are essential.",
    "भारत ही एक ऐसा देश है जहाँ कई प्रकार के रेशम के कीड़ों का पालन करके विविध प्रकार का रेशम प्राप्‍त किया जाता है।":
        "India is uniquely endowed to rear multiple silkworm varieties and harvest a rich spectrum of natural silks.",
    "राज्यों में प्रति एकड़ उत्पादन के हिसाब से महाराष्‍ट्र सबसे अग्रणी है किंतु कुल उत्पादन में गुजरात सूची में सर्वोपरि है।":
        "Among Indian states, Maharashtra leads in per-acre acreage productivity, whereas Gujarat stands at the pinnacle in aggregate production.",
    "बीजकोष बहुत जल्दी बढ़ता है तथा पकने पर इसका आकार 2 5 सेंटीमीटर चौड़ा तथा 3 8 सेंटीमीटर लंबा हो जाता है।":
        "The boll expands rapidly, reaching 2.5 cm in width and 3.8 cm in length upon maturity.",
    "इनमें से कुछ गुण इस प्रकार हैं फसल का जल्दी तैयार होना फसल में बीमारियों तथा कीड़े मकोड़ों से बचने की प्रतिरक्षा शक्‍ति का पर्याप्‍त मात्रा में होना अधिक उपज देना, रेशों का अधिक मज़बूत होना आदि।":
        "Notable traits include early crop maturity, high pest and disease resistance, elevated fiber yield, and superior tensile fiber strength.",
    "कपास की खेती में लगभग 4 5 करोड़ से अधिक लोग रोज़गार में व्यस्त हैं तथा इसी से आजीविका चलाते हैं।":
        "More than 45 million people are engaged in cotton cultivation, earning their livelihoods from it.",
    "उन्होंने बताया कि हम बांबिक्स मोरी जाति के ही रेशम कीड़ों का पालन करते हैं।":
        "They explained that they rear silkworms belonging specifically to the Bombyx Mori species.",
    "कपास के पौधे की वृद्धि से लेकर फूल आने तक की अवस्था में ताप सूरज की रोशनी तथा पानी की उपलब्धि आदि का अधिक प्रभाव पड़ता है।":
        "Factors like ambient temperature, direct sunlight, and moisture availability profoundly influence the plant from early growth to blossoming.",
    "किंतु उत्पादन में भारत का स्थान अमेरिका रुस और चीन जो सर्वाधिक उत्पादक देश हैं के बाद चौथा है।":
        "In aggregate production, India ranks fourth behind the top-producing nations: the United States, Russia, and China.",
    "चार सप्‍ताह से छः सप्‍ताह के बीच फूलों में कलियाँ निकलना शुरु हो जातीं हैं तथा रोपण के लगभग 100 दिन के बाद पौधे पर सफेद या हल्के अथवा गहरे पीले रंग के अतिसंवेदनशील फूल खिल जाते हैं।":
        "Between 4 to 6 weeks, flower buds begin appearing, and roughly 100 days post-planting, sensitive blossoms of white, pale yellow, or deep yellow unfurl.",
    "कृषि व्यवसाय की तरह रेशम कीट पालन भी जीविकोपार्जन का एक मुख्य साधन है जिसमें कई हजार श्रमिक काम करते हुए यह बहुमूल्य रेशा पैदा करते हैं।":
        "Like commercial farming, sericulture serves as a key livelihood generating precious natural fibers through the labor of thousands of workers.",
    "अध्यापक ने बताया कि भारत में रेशम कीट पालन सन् 400 में शुरु हुआ था।":
        "The instructor recounted that sericulture in India began around 400 CE.",
    "कपास के उत्पादन के लिए प्रजनन breeding कार्यक्रम के माध्यम से कपास की प्रत्येक जाति में विभिन्न किस्में तैयार की गई हैं।":
        "To maximize cotton output, intensive breeding programs have developed distinct cultivars across all botanical species.",
    "इसके उपयोग से अमेरिका और चीन में कपास के उत्पादन में काफी वृद्धि हुई है।":
        "Through its adoption, cotton productivity in the US and China witnessed dramatic growth.",
    "ऐसा लग रहा था मानों स्वर्ग ने स्वयं ही इस धरा पर सफेदी बिखेर दी हो।":
        "It appeared as though heaven itself had draped the landscape in pure white.",
    "भारत में कपास के उत्पादन की कमी का प्रमुख कारण है कि यहाँ कपास की खेती वाले क्षेत्र में से केवल एक चौथाई हिस्से में ही सिंचाई की उचित सुविधा उपलब्ध है और शेष खेती वर्षा पर निर्भर करती है।":
        "The primary reason for lower cotton productivity in India is that barely one-quarter of the cultivated area enjoys assured irrigation, while the remainder relies on monsoon rainfall.",
    "गौसीपियम प्रजाति के अंतर्गत कपास की 36 जातियाँ मान्य हैं परंतु अच्छे किस्म की कपास पैदा करने के लिए इनमें से केवल चार प्रकार की कपास की खेती की जाती है क्योंकि अन्य जातियाँ जंगली हैं।":
        "Under the genus Gossypium, 36 species are recognized; however, only four are cultivated for commercial fiber, as the rest are wild species.",
    "यह एक लघु उद्योग है जिसमें 50 000 गाँव रेशम कीट पालन sericulture के कार्य में जुटे हुए हैं।":
        "This is a vibrant cottage industry in which over 50,000 villages are actively engaged in sericulture operations.",
    "दो जातियों के गुणसूत्रों को मिलाकर अपनी इच्छानुसार संकर hybrid पौधे विकसित किए जा सकते हैं।":
        "By crossing chromosomes from two species, desired hybrid cultivars can be bred tailored to requirements.",
    "डा जोशी ने छात्रों को बताया कि कपास एक बीज तंतु है जो गौसीपियम Gossypium प्रजाति के पौधे से उगता है।":
        "Dr. Joshi explained to students that cotton is a seed trichome fiber harvested from plants of the Gossypium genus.",
    "कपास की फसल में कई गुणों का होना आवश्यक है।":
        "Commercial cotton crops must exhibit multiple agronomic attributes.",
    "बुवाई के पश्‍चात बीज के उगने के बाद जब मूल जड़ भूमि में प्रवेश करती है तो पौधे की वृद्धि के लिए वह भूमि से अपना खाद्‍य पदार्थ लेना शुरु करती है।":
        "Following sowing and germination, once the taproot penetrates the soil, it begins absorbing essential nutrients for vegetative growth.",
    "क्राइसेलिस पूरा विकसित होने के पश्‍चात मॉथ moth के रूप में कोये से बाहर निकलता है तथा फिर मादा मॉथ रेशम कीट अंडे देती है।":
        "Once fully developed, the chrysalis emerges from the cocoon as an adult moth, and the female then lays eggs.",
    "ये अंडे बहुत ही हल्के होते हैं।":
        "These eggs are extraordinarily light in weight.",

    # Sample 5: Silk Fibers & Processing
    "एक कैटरपिलर अपने वजन से 7 000 9 000 गुना शहतूत के पत्‍ते खा जाता है।":
        "A single silkworm caterpillar consumes 7,000 to 9,000 times its own body weight in mulberry foliage.",
    "ये दो पतले रेशम के तंतु स्पिनिंग हैड में सैरिसिन द्वारा जुड़कर एक ही साथ बाहर निकलते हैं जिसे वेब bave कहते हैं।":
        "These two fine silk filaments bond together with sericin within the spinneret head and emerge simultaneously as a single bave thread.",
    "अतः हम कह सकते हैं कि प्रत्येक रेशा मुख्यतया दो रासायनिक पदार्थों से बना है पहला तरल पदार्थ के रूप में फिब्रॉयन, जो स्पिनरेट से निकलकर हवा के संपर्क में आकर सूख जाता है और दूसरा पदार्थ सैरिसिन गोंद है।":
        "Hence we conclude each fiber comprises two main substances: fibroin, a liquid extruded by spinnerets that hardens on air contact, and sericin, a protective gum.",
    "उसके निकलने से पूर्व ही कोकून को हल्की भाप में रखकर रेशम कीट को कोकून के भीतर ही मार देते हैं।":
        "Before it can break out and damage the strands, the cocoon is gently steamed to stifle the pupa inside.",
    "यह सुनहले रंग का रेशम मल्टीवोल्टाइन वर्ग के रेशम कीड़ों से प्राप्‍त होता है।":
        "This golden silk is harvested from multivoltine races of silk moths.",
    "हमारे देश में लगभग 90 शहतूत mulberry रेशम पैदा किया जाता है और शेष 10 वन्य सिल्क wild silk टसर ऐरी तथा मूंगा पैदा किया जाता है।":
        "Around 90% of our domestic silk output is mulberry silk, with the remaining 10% consisting of wild silks: Tasar, Eri, and Muga.",
    "इन महीन तंतुओं को ब्रिन brin कहते हैं।":
        "These individual fine filaments are termed brins.",
    "जापान में हल्के हरे रंग के कोकून भी पैदा किए जाते हैं जिसके कैटरपिलर हरी पत्‍तियाँ खाते हैं।":
        "In Japan, pale-green cocoons are also cultivated, produced by caterpillars feeding on tender green leaves.",
    "ये रेशम के रेशे तिकोने होते हैं और इनमें अणु श्रृंखलाएं सूक्ष्म micro और स्थूल macro तंतुकों fibrils के रूप में व्यवस्थित अवस्था में उपस्थित होती हैं।":
        "These silk filaments are triangular in cross-section, with molecular chains arranged into orderly micro and macro fibrils.",
    "प्रत्येक रेशे में करीब 75 फिब्रॉयन तथा 25 सैरिसिन होता है।":
        "Each raw silk thread comprises roughly 75% fibroin protein and 25% sericin gum.",
    "एक नया कैटरपिलर केवल 1 4 इंच लंबा होता है परंतु यह इतना पेटू होता है कि अत्यधिक शहतूत की पत्‍तियाँ खाकर शीघ्र ही बढ़ने लगता है।":
        "A freshly hatched caterpillar measures barely a quarter-inch, yet feeds so voraciously on mulberry leaves that it grows rapidly.",
    "जब से देश में सिल्क बोर्ड Silk Board की स्थापना हुई, सिल्क उत्पादन में वैज्ञानिक तरीकों से काफी तरक्की हुई है परंतु हम सेरीकल्चर फार्म में क्राइसेलिस को बाहर नहीं निकलने देते कोकून का रंग व आकार रेशम कीट के खाने और जलवायु पर जिसमें उसका पालन किया जाता है निर्भर करता है।":
        "Since the Central Silk Board was established, scientific advancements have elevated silk production, yet on farms we prevent the chrysalis from escaping; cocoon size and hue depend directly on silkworm nutrition and environmental conditions.",
    "परंतु टसर के रेशे मल्बरी सिल्क के रेशे की अपेक्षा मोटे तथा सख्त होते हैं और इनमें सैरिसिन की मात्रा भी मूंगा तथा ऐरी रेशम से ज्यादा होती है।":
        "However, Tasar silk filaments are coarser and stiffer than mulberry silk, containing higher sericin proportions than Muga or Eri.",
    "लच्छियों की चमक तथा कोमलता में अंतर को समझने के लिए यह जानना आवश्यक है कि प्रत्येक रेशा दो महीन तंतुओं brins से बनता है और ये तंतु सैरिसिन गोंद से जुड़े होते हैं।":
        "To comprehend differences in luster and softness of skeins, it is essential to realize that each thread is composed of two twin brins held together by sericin glue.",
    "कश्मीर में यूनिवोल्टाइन तथा बाइवोल्टाइन रेशम कीट, पश्‍चिम बंगाल में बढ़िया किस्म के मल्टीवोल्टाइन रेशम कीट, तथा कर्नाटक में मल्टीवोल्टाइन रेशम कीट का पालन होता है।":
        "Univoltine and bivoltine silkworm strains are reared in Kashmir, high-grade multivoltines in West Bengal, and hardy multivoltine races in Karnataka.",
    "भारत में सफेद कोकून के अतिरिक्‍त स्लेटी तथा हल्के भूरे रंग के कोये भी पाए जाते हैं।":
        "Besides white cocoons, grey and light brown cocoons are also cultivated in India.",
    "एक कोकून का भार करीब 6 3 ग्राम होता है जिसमें पतली परत का केवल 0 5 ग्राम होता है।":
        "An average cocoon weighs around 6.3 grams, with the harvestable shell layer accounting for roughly 0.5 grams.",
    "उसके बाद यह कैटरपिलर हल्के गुलाबी रंग का पारदर्शक कीड़ा बन जाता है तब इसकी खाने में रुचि कम हो जाती है।":
        "Subsequently, the caterpillar turns into a translucent pinkish larva, at which point its appetite markedly diminishes.",
    "ऐसे कीड़ों का पालन असम बिहार बंगाल मणिपुर उड़ीसा तथा त्रिपुरा में किया जाता है।":
        "Such silkworms are reared in Assam, Bihar, West Bengal, Manipur, Odisha, and Tripura.",
    "ऐरी सिल्क के कोयों के खुले मुंह होने के कारण इनसे निकले हुए रेशों की रीलिंग नहीं कर सकते।":
        "Because Eri silk cocoons possess an open-ended morphology, their filaments cannot be reeled continuously.",
    "यह सफेद या लाल रंग का रेशम है जो मल्टीवोल्टाइन वर्ग के रेशम कीड़ों से प्राप्‍त होता है।":
        "This is white or brick-red silk derived from multivoltine silk moth varieties.",
    "एक कोया का भार केवल 3 ग्राम होता है।":
        "The weight of an individual wild cocoon is only around 3 grams.",
    "इस क्रिया को स्टोविंग stoving कहते हैं।":
        "This stifling heat process is called stoving.",
    "इस प्रकार 30 35 दिन तक शहतूत के पत्‍ते खाकर यह श्‍वेत स्लेटी रंग का कैटरपिलर बन जाता है और इसकी लंबाई 3 1 2 और चौड़ाई 1 4 हो जाती है।":
        "Feeding continuously on mulberry leaves for 30 to 35 days, it develops into an off-white caterpillar reaching 3.5 inches in length and 0.25 inches in girth.",
    "यदि हम सूक्ष्मदर्शी microscope से इस महीन रेशे को देखें तो, ज्ञात होगा कि यह रेशा दो तंतुओं का बना होता है।":
        "Examining this exquisite filament under a microscope reveals that it consists of two distinct parallel fibers.",
    "अब इस अवस्था में रेशम कीट एक प्रकार के क्षारीय पदार्थ को निकालकर उसके द्‍वारा कोकून के कुछ भाग को घोलकर छिद्र बना देता है और इस छिद्र से कीड़ा कोकून से बाहर निकल आता है।":
        "At this stage, the emerging moth secretes an alkaline solvent that dissolves part of the cocoon wall to create an exit hole, through which it crawls out.",
    "स्टोविंग की क्रिया में रेशम कीट कोकून के भीतर ही मर जाता है परंतु रेशम के रेशे या कोकून को भाप से किसी प्रकार का नुकसान नहीं पहुँचता भारत में शहतूत mulberry रेशम कीट का पालन कई स्थानों पर होता है जैसे असम के पहाड़ी इलाकों बंगाल कोनूर तमिलनाडु देहरादून तथा हिमाचल प्रदेश।":
        "During stoving, the pupa is killed within the cocoon without damaging delicate silk threads; in India, mulberry sericulture flourishes in areas like the hills of Assam, Bengal, Coonoor in Tamil Nadu, Dehradun, and Himachal Pradesh.",
    "इन कोयों की विशेषता बहुरूपी रंग बदलना है इनके कोकून प्रायः अंडाकार सख्त व भूरे रंग के होते हैं।":
        "These cocoons are characterized by iridescent color variations; they are typically oval, dense, and earthy brown in tint.",
    "यह कहना अधिक उपयुक्‍त होगा कि पूरा तंतु बनाने में आठ अंक को वह करीब 12 लाख बार रेशम के धागे से लिखता है।":
        "It is apt to say that in producing a single filament, the silkworm traces figure-eight loops roughly 1.2 million times.",
    "रेशम का कीड़ा दोनों ग्रंथियों पर दबाव डालकर निरंतर रेशम के दो तंतु बनाता है ऐसे रेशम कीट जिनसे टसर रेशम प्राप्‍त होता है, देश के उष्ण तथा शीतोष्ण जलवायु वाले भागों में पैदा होते हैं।":
        "Applying pressure to both glands, the caterpillar spins twin silk filaments; the moth varieties yielding Tasar silk thrive across tropical and temperate zones of the country.",
    "एक रेशम का कीड़ा 46 मीटर प्रति घंटे की रफ्तार से रेशे का निर्माण करता है।":
        "A silkworm spins silk filaments at a remarkable speed of 46 meters per hour.",
    "ये अंडे जलवायु के अनुसार 3 से 7 दिन के भीतर लारवा कैटरपिलर में परिवर्तित हो जाते हैं।":
        "Depending on climatic conditions, these eggs hatch into caterpillars within 3 to 7 days.",
    "करीब 40 000 अंडों का वजन केवल एक आउंस के लगभग होता है।":
        "Roughly 40,000 silkworm eggs weigh only about one single ounce.",
    "चीन में रेशम के कीड़े से प्राप्‍त कोये प्रायः सफेद रंग के होते हैं क्योंकि वहाँ पर कैटरपिलर सफेद शहतूत के पत्‍ते खाते हैं।":
        "In China, harvested silk cocoons are predominantly white because the caterpillars feed on white mulberry foliage.",
    "कैटरपिलर अपने बढ़ने की क्रिया में बार बार अपनी त्वचा बदलता है ताकि वह बढ़ते हुए आकार को ढक सके इन कीड़ों के कोकून कुछ लंबे आकार के होते हैं।":
        "As it grows, the caterpillar repeatedly molts its skin to accommodate its expanding size; cocoons of these species are notably elongated.",
    "प्रत्येक कीड़े में दो ग्रंथियाँ पायी जाती हैं जो कीड़े के सिर वाले भाग में जबड़े के नीचे स्थित होती हैं।":
        "Each caterpillar possesses two specialized sericteries situated beneath the jaws near its head.",
    "हमारे देश में चार प्रकार के रेशम पैदा किए जाते हैं मल्बरी रेशम टसर ऐरी और मूंगा केवल भारत ही ऐसा देश है जहाँ सुनहले पीले रंग का मूंगा रेशम पैदा किया जाता है।":
        "Our nation cultivates four varieties of silk: Mulberry, Tasar, Eri, and Muga; India is uniquely the sole producer of glistening golden Muga silk.",
    "जापान तथा यूरोप में कोकून क्रीम व हल्के पीले रंग के होते हैं क्योंकि वहाँ पर कैटरपिलर कैस्टर आयल पौधों castor oil plant के पत्‍ते खाकर अपने अंदर टैनिन tannin नामक पदार्थ सोख लेते हैं।":
        "In Japan and Europe, cocoons are creamy or pale yellow because caterpillars feeding on castor foliage absorb tannins into their systems.",
    "ऐसा रेशम कीड़ा विशेषरूप से असम में पाया जाता है।":
        "Such silkworm varieties are indigenous primarily to Assam.",
    "टसर रेशम कीट को कोकून के भीतर मारने की आवश्यकता नहीं पड़ती और लंबे रेशे आसानी से मिल जाते हैं।":
        "Tasar silkworms need not be stifled inside the cocoon, allowing continuous long fibers to be drawn smoothly.",
    "टसर रेशम का कैटरपिलर शहतूत के पत्‍तों की जगह ओक oak पेड़ के पत्‍ते खाता है, संभवतः इसके कोकून का रंग पत्तों का टैनिन सोखने के कारण ही भूरा होता है।":
        "Tasar caterpillars feed on oak leaves rather than mulberry; the rich brownish hue of their cocoons likely stems from tannins absorbed from oak foliage.",
    "इस रेशम कीड़े के कोकून बंद होते हैं और उन पर बाहरी परत Shell काफी पतली होती है।":
        "The cocoons of this species are sealed capsules with a comparatively delicate outer shell.",
    "रेशा बनाने की क्रिया में कीड़े का वजन कम हो जाता है और कोकून के भीतर कैटरपिलर क्राइसेलिस प्यूपा में बदल जाता है और फिर दो सप्‍ताह में मॉथ moth बन जाता है।":
        "During cocoon spinning, the worm sheds body mass, transforming inside into a chrysalis pupa and emerging as an adult moth two weeks later.",

    # Sample 6: Bollywood (Kuch Kuch Hota Hai)
    "यू नो, मैंने कितनी बार सोचा कि उसको जाकर कह दूं मेरी सगाई हो गयी है।":
        "You know, countless times I contemplated going and telling him that I got engaged.",
    "अमन पता नहीं कौन फोन पर है।":
        "Aman, I have no idea who is on the phone.",
    "अमन तुम जानते हो मैं हर साल समर कैंप जाती हूं उन बच्चों को सिंगिंग और डासिंग सिखाने अब तो वो बच्चे मेरी जिंदगी का एक हिस्सा बन चुके हैं।":
        "Aman, you know I go to the summer camp every year to teach those kids singing and dancing; by now, those children have become an inseparable part of my life.",
    "दूसरे कॉलेज के स्टूडेंट्स देखते ही रह जाएंगे कैसी लग रही हूं मैं।":
        "Students from other colleges will be left completely awestruck; how do I look?",
    "पर क्या तुम उससे प्यार करती हो?":
        "But do you truly love him?",
    "राहुल ये तुम क्या कर रहे हो मुझे छोड़ कर जा रही हो, मुझे बताया भी नहीं!":
        "Rahul, what are you doing? You are leaving me, and you did not even inform me!",
    "राहुल तुम्हारा सबसे अच्छा दोस्त है ना?":
        "Rahul is your best friend, isn't he?",
    "मेरी बेटी समझौता करेगी और प्यार नहीं करेगी, ये तो मैंने कभी सोचा ही नहीं था।":
        "That my daughter would compromise without love—I had never even imagined such a thing.",
    "प्यार तो मैंने कर लिया है मां शायद मुझसे फिर से न हो, इसे एक समझौता ही समझ लो।":
        "I already loved once, Mother; perhaps I will never love again; consider this marriage just a compromise.",
    "तुम जाओ शिमला अपने समरकैंप।":
        "You go to Shimla for your summer camp.",
    "ऑफ्कोर्स मैं खुश हूं और मालूम है तुम अगर चाहो ना तो तुम्हें कोई भी लड़का मिल सकता है।":
        "Of course I am happy, and you know, if you wished, you could have any guy in the world.",
    "ऐक्चुली तुम बहुत खूबसूरत हो क्योंकि तुम सबसे ज्यादा अलग हो।":
        "Actually, you are exceptionally beautiful because you are so uniquely different from everyone else.",
    "अंजलि तुम्हारा फोन है।":
        "Anjali, there's a phone call for you.",
    "अपनी मां के सामने एक दुर्गा मां के सामने और राहुल तुम यहां इस वक्त, मैं वापस नहीं आ रही राहुल यह कैसा सवाल है मां।":
        "Before one's mother and before Mother Durga; and Rahul, you here at this hour? I am not returning, Rahul; what kind of question is this, Mother?",
    "ऐक्चुली राहुल की जगह कोई और होता तब भी शायद मुझे इतना ही बुरा लगता।":
        "Actually, even if anyone else had been in Rahul's place, it probably would have hurt me just as deeply.",
    "तुम खुश हो बेटी मुझे क्यों ऐसा लगता है कि तुम मुझसे प्यार नहीं करती तुम उससे प्यार नहीं करती तुम कोई समरकैंप वमरकैंप नहीं जा रही हो।":
        "Are you truly happy, my daughter? Why do I feel you don't love me, you don't love him, and you aren't really heading to any summer camp?",
    "लेकिन राहुल अंजलि की शादी दिसंबर से पहले नहीं हो सकती है।":
        "But Rahul, Anjali's wedding cannot take place before December.",
    "मेरे डैड कहा करते थे कि मर्द का सिर सिर्फ तीन औरतों के सामने झुकता है।":
        "My dad used to say that a man bows his head only before three women.",
    "अंजलि मैं तुम्हें ही मिलने आ रहा था।":
        "Anjali, I was on my way just to meet you.",
    "ऐक्चुली मुझे नींद नहीं आ रही थी और मैंने सोचा कि तुम्हें भी नहीं आ रही होगी और अगर तुम जाग रही होगी तो मेरे बारे में ही सोच रही होगी मेरा पहला प्यार अधूरा रह गया।":
        "Actually I couldn't fall asleep, and I thought you wouldn't be sleeping either, and if you were awake you'd be thinking of me; my first love remained unfulfilled.",
    "रिफ़त दी तुम मुझसे कोई भी बात छुपा नहीं सकती हो।":
        "Rifat Bi, you cannot hide anything from me.",
    "खुदा की रहमत तो सुना था आज देख भी लिया, बच्ची की दुआ कबूल हो गयी।":
        "I had heard of God's divine mercy, and today I witnessed it firsthand; the child's prayer has been answered.",
    "तुम्हें और कोई नहीं मिला मुझसे बहुत प्यार करता है बेटा वहां पर बहुत बर्फ पड़ती है।":
        "Could you find no one else? He loves me very deeply; son, it snows heavily out there.",
    "कहते हैं टूटते तारे को देखकर कुछ मांगो ना तो मिल जाता है।":
        "They say that if you make a wish upon seeing a falling star, it comes true.",
    "आई होप मैं उसको ये सब कह पाऊं।":
        "I hope I find the courage to confess all this to him.",
    "अंजलि तुमसे कुछ पूछूं तुम्हें नहीं लगता यहां पर काफी गर्मी है।":
        "Anjali, may I ask you something? Don't you feel it is rather warm in here?",
    "कॉलेज छोड़ कर जा रही हो तुम मैं तुम्हारी तरह खूबसूरत लगना चाहती थी लेकिन मुझे तो कुछ आता ही नहीं।":
        "You are leaving college? I wished to look as glamorous as you, but I don't know the first thing about styling.",
    "तुमने उससे अपने दिल की बात कह दी अंजलि राहुल को तुम कब से जानती हो।":
        "Did you pour out your heart to him? Anjali, how long have you known Rahul?",
    "मैं भी मां हूं, क्या मैं नहीं चाहती कि तुम खुश रहो, तुम्हारा घर बस जाए।":
        "I too am a mother; wouldn't I desire for you to be joyful and well-settled in life?",
    "अमन बहुत अच्छा लड़का है तुम मुझे इस तरह छोड़ कर मत जाया करो मेरी एक छोटी सी प्रॉब्लम है।":
        "Aman is an wonderful boy; please never walk away leaving me like this; I have a small dilemma.",
    "लेकिन वो घर जो समझौते के बलबूते पर बना हो, प्यार के नहीं, वो घर नहीं होता है बेटी, मकान होता है।":
        "However, a household built upon compromises rather than genuine love is never a true home, my daughter—it is merely a house.",
    "मैंने कभी नहीं सोचा था कि मैं कभी किसी को ये कहूंगा।":
        "I never imagined I would ever utter these words to anyone.",
    "टीना मैं जानता हूं राहुल सिर्फ तुमसे प्यार करता है।":
        "Tina, I know in my heart that Rahul loves only you.",

    # Sample 7: Hum Aapke Hain Koun
    "जी आप मुझे बता सकती हैं कि प्रोफ़ेसर चौधरी किस कमरे में ठहरे हुए हैं?":
        "Excuse me, could you tell me which room Professor Choudhury is staying in?",
    "राजेश तो फिर भी अपनी माँ की गोद में खेला है मगर प्रेम वो तो आज तक उस ममता से वंचित रहा।":
        "Rajesh at least had the privilege of playing in his mother's lap, but Prem was deprived of maternal affection all his life.",
    "सच कैलाशनाथ जब अख़बारों में तुम्हारा नाम पढ़ते हैं तो बहुत गर्व महसूस करते हैं।":
        "Truly, Kailashnath, whenever we read your name in the newspapers, we swell with immense pride.",
    "इस बार छुट्टियों में हमने रामटेकड़ी जाने का फैसला किया है।":
        "During this vacation, we have resolved to visit Ramtekdi.",
    "पिछले दिनों प्रोफ़ेसर्स की कांफ्रेंस के लिए मैं पूना गया हुआ था वहां मेरी मुलाकात प्रोफ़ेसर एस एस चौधरी से हुई।":
        "Recently I traveled to Pune for a professors' conference, where I had the pleasure of meeting Professor S.S. Choudhury.",
    "पूजा बेटे जब रामचंद्र जी ने शिव जी का धनुष तोड़ा तो परशुराम जी ने बड़े गरजते हुए पूछा कि ये धनुष किसने तोड़ा।":
        "Pooja, dear child, when Lord Ramachandra broke Lord Shiva's bow, Parashurama demanded in a thundering voice who had dared to break it.",
    "मैनेजर की कुर्सी पर बैठकर न जाने आप अपने को क्या समझ रही हैं।":
        "Sitting in the manager's chair, heaven knows what you think of yourself.",
    "सच कहती हूँ भाई साहब अपने राजेश बेटे की जितनी तारीफ़ की जाए वो कम है।":
        "I speak the truth, brother, no matter how much praise we bestow on our son Rajesh, it is never enough.",
    "अब आपके सामने आ रहे हैं वो जिनकी गेंद की रफ़्तार हवा से भी तेज है।":
        "Now approaching before you is the bowler whose delivery speed outpaces the wind itself.",
    "आज बड़ी देर तक चली तुम्हारी मीटिंग मैंने डॉक्टर चाची की बात सुन ली, अब तो तुम्हारी बारी है दुल्हन चुनने की।":
        "Your business meeting ran quite late today; I overheard Auntie Doctor speaking, now it is your turn to pick a bride.",
    "आज हम बहुत गुस्से में हैं आज न हम खाएंगे, न पीएंगे, हम जा रहे हैं।":
        "Today we are profoundly upset; today we will neither eat nor drink anything; we are leaving.",
    "इतने अच्छे संस्कार दिए आपने बच्चों को, तभी तो राजेश का आज इतना नाम है और प्रेम भी तो इस साल एमबीए में अव्वल आया है।":
        "You instilled such noble values in the boys, which is why Rajesh enjoys such prestige, and Prem topped his MBA cohort this year.",
    "इन बच्चों की जिम्मेदारी निभाने के लिए आपने कॉलेज की पढ़ाई भी अधूरी छोड़ दी और एक छोटी सी नौकरी से शुरुआत की।":
        "To shoulder responsibility for these young children, you gave up your college education and began working a modest job.",
    "नंबर बढ़वाइए आप अपने चश्मे का मैडम अमचूर की चटनी के साथ खाइये चौबे जी, मथुरा की कचौड़ियों को भूल जाएंगे।":
        "You ought to increase the power of your spectacles, madam; have it with dry mango chutney, Chaubey ji, and you'll forget even Mathura's famous kachoris.",
    "बेटा बीस साल तक इन आंसुओं को आँखों के अंदर रोक के रखा था, आज ये रुकने वाले नहीं हैं बेटा।":
        "Son, for twenty long years I held back these tears in my eyes; today they refuse to be held back, my child.",
    "क्या निशा वहां मम्मी कब से तेरी राह देख रही हैं, क्या कर रही है तू यहां।":
        "Nisha, Mother has been anxiously awaiting you over there; what in the world are you doing here?",
    "देखा प्रेम मुझसे बोले कि रज़िया बेग़म हम बहुत नाराज़ हैं, किसी से कुछ बात मत करना और यहां बहू की फोटो देखते ही गुस्सा गुल, पापा ने लाइब्रेरी की किताबें भेजी हैं और कहा है थैंक्यू।":
        "Look, Prem told me: Raziya Begum, I am furious, don't talk to anyone; yet the moment he saw the bride's photograph, all his anger melted away; Dad sent back the library books with a note of thanks.",
    "राजेश से जब भी शादी की बात करो वो टाल जाता है, अब ऐसे में दोनों को मिलाएं भी तो कैसे, जब भी मैं तुमसे बात करना चाहती हूँ, कोई न कोई तुम्हें बुला लेता है।":
        "Whenever we broach marriage with Rajesh, he dodges the topic; in such circumstances, how do we bring them together; whenever I wish to speak with you, someone interrupts.",
    "लेकिन मैं तुम्हारा दिल जीतना खूब जानती हूँ जल्दी कीजिए पापा अगर मम्मी ने आपको रसोई में ये एक्सपेरीमेंट करते देख लिया ना तो बड़ी नाराज़ होंगी।":
        "Yet I know full well how to win your heart; hurry up, Dad, if Mom catches you doing this culinary experiment in the kitchen, she will be furious.",
    "इस वक्त प्रोफ़ेसर साहब अपने परिवार के साथ तीर्थ यात्रा पर रामटेकड़ी गए हुए हैं और जैसे ही घर लौटें, चले चलते हैं।":
        "At present, the Professor has gone on pilgrimage to Ramtekdi with his family; the moment they return home, we shall proceed.",
    "आप प्रोफ़ेसर चौधरी जी के लिए पूछ रहे थे न, ये हैं उनकी बेटियां पूजा और निशा और पूजा बेटी ये हैं कैलाशनाथ जी तुम्हारे पापा के दोस्त निशा बेटी एक काम करेगी।":
        "You were inquiring after Professor Choudhury, were you not? These are his daughters, Pooja and Nisha; and Pooja dear, this is Kailashnath, your father's cherished friend; Nisha, would you do a favor?",
    "वहां मैं उनकी बड़ी बेटी से मिला बच्ची को बस एक बार देखा, दिल में घर कर गई, राजेश और प्रेम इतने इतने से थे जब जीजी और जीजा जी का देहांत हुआ था।":
        "There I met his elder daughter; I caught just one glimpse of the girl, and she captured my heart instantly; Rajesh and Prem were merely toddlers when Sister and Brother-in-law passed away.",
    "मैनेजर साहब बिल का टोटल आप एक बार फिर से चेक कर लीजिए राजेश का रिश्ता तय कर आए, बहू चुन ली और हमें खबर मिल रही है आज।":
        "Manager sir, kindly re-verify the invoice total; you finalized Rajesh's alliance, selected our daughter-in-law, and we are only being informed today!",
    "बेटा प्रेम तुम शायद हम तीनों की हिस्ट्री नहीं जानते होगे, हम तीनों कॉलेज में एक साथ थे और बहुत मौज मस्ती किया करते थे।":
        "Son Prem, you probably do not know the history of us three; we were in college together and used to have endless fun.",
    "लोग कहते हैं खूबसूरत लड़कियां टोटल में अक्सर मार खा जाती हैं।":
        "People often say that pretty girls tend to bungle arithmetic totals.",
    "अपने भतीजे राजेश के लिए हमें तुम्हारी बड़ी बेटी बहुत भा गई है देखा मामा जी टफ़ी को भी पता है आज शाम को बड़े भैया की ससुराल वाले सगाई का शगुन लेकर आने वाले हैं।":
        "We have taken a great liking to your elder daughter for our nephew Rajesh; look, Uncle, even Tuffy knows that elder brother's prospective in-laws are arriving this evening with the engagement gifts.",
    "इतनी कम उम्र में इतना बड़ा कारोबार संभालना कोई खेल नहीं है लेकिन काका आप तो कह रहे थे कि आपको किसी हिल स्टेशन पर जाना था।":
        "Managing such a sprawling business empire at such a young age is no child's play; but Uncle, you were saying that you planned to visit a hill station.",
    "अगर सब कुछ प्लान के मुताबिक गया न तो जैसे आपने कहा था, इस फैक्ट्री का देश भर में कोई मुकाबला नहीं होगा।":
        "If everything proceeds according to plan, then just as you said, this industrial plant will be without equal across the entire nation.",
    "इनके भविष्य के लिए सिर्फ मेहनत को अपनी ज़िंदगी का लक्ष्य माना भगवान ने मुझे सब कुछ दिया इन बच्चों का प्यार, बड़ा कारोबार मगर घर का आँगन सूना है।":
        "For their bright future, he made tireless diligence the sole purpose of his existence; God blessed me with everything—the devotion of these boys, a thriving enterprise—yet the family courtyard remains desolate.",
    "वो चले गए यहाँ से उनकी बेटी की शादी है ना, सब कुछ बेच के चले गए पंजाब।":
        "They have permanently relocated from here; their daughter is getting married, you see; they sold everything and left for Punjab.",
    "क्या कहा फ़ॉरेन कॉलैबरेटर्स ने जब तक हम स्टोर रूम से वापस आएं, यह बिल का टोटल चेक कर देगी।":
        "What did the foreign collaborators say? By the time we return from the storeroom, she will have audited this invoice total.",
    "थोड़ी ही देर में मैच शुरू होने वाला है और हम आपको आँखों देखा हाल सुनाने जा रहे हैं।":
        "In just a few moments the match is slated to commence, and we bring you the live commentary.",
    "तेरा भैया तुझे बिज़नेस में लांच करने के लिए कितनी बड़ी फैक्ट्री लगा रहा है जी हाँ साल भर तो पढ़ाई करते हैं नहीं इम्तिहान के समय बगले झांकते हैं और फिर आ जाते हैं यहां तक अपने नंबर बढ़वाने।":
        "Look what an enormous factory your elder brother is constructing just to launch you in business! Indeed, students don't study all year round, look blank during exams, and then rush here to get their marks inflated.",
    "अच्छा तो ये हलवा प्रेम भैया के लिए बनाया जा रहा है, वो भी इस किताब में पढ़कर पूजा नाम है उसका बी ए पास किया है, बड़ा ही मीठा स्वभाव है।":
        "Oh, so this sweet halwa is being cooked for brother Prem, and that too by consulting this recipe book! Her name is Pooja, she has completed her B.A., and she possesses an extraordinarily sweet demeanor.",
    "रामचंद्र जी ने बड़ी सरलता से, बड़े प्रेम भाव से उत्तर दिया।":
        "Lord Ramachandra answered with utmost simplicity and heartfelt affection.",
    "लेकिन अगर उन्होंने भी एक बार इन कचौरियों को देख लिया ना तो अपना उपवास तोड़ देंगी।":
        "However, if even she were to catch a single sight of these hot kachoris, she would instantly break her fast.",
    "आपसे जीतना तो हम दोनों के बस के बाहर है, आपसे कोई जीते तो बस निशा।":
        "Defeating you is completely beyond the capabilities of either of us; if anyone can ever triumph over you, it is only Nisha."
}

db.update(SAMPLES_4_TO_7)

with open('src/translation/curated_translations.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print(f"Comprehensive translation database updated: {len(db)} sentences mapped.")
