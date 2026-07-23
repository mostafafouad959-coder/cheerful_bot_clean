import random

THERAPEUTIC_RESPONSES_EN = {

    "sadness": [
        (
            "I hear you, and I want you to know — feeling lost and alone is one of the hardest feelings there is. 💙\n\n"
            "Here are a few things that might help right now:\n"
            "• **Reach out to one person** — even a text saying 'hey' can break the silence.\n"
            "• **Write down 3 things you feel** — getting it out of your head helps.\n"
            "• **Go outside for 10 minutes** — fresh air and movement shift your mood.\n"
            "• **Be kind to yourself** — you don't have to fix everything today.\n\n"
            "You are not alone. I'm here with you. 🌻"
        ),
        (
            "What you're feeling is valid, and it takes real courage to say it out loud. 💙\n\n"
            "Some small steps that can help with sadness:\n"
            "• **Talk to someone you trust** — a friend, family member, or counselor.\n"
            "• **Do one small thing that used to bring you joy** — music, a walk, drawing.\n"
            "• **Remind yourself** — this feeling is temporary, even when it doesn't feel like it.\n"
            "• If things feel overwhelming, please consider **reaching out to a mental health helpline**.\n\n"
            "You matter more than you know. 🌟"
        ),
        (
            "Feeling lost is incredibly hard, especially when you feel like you have no one. 💙\n\n"
            "Here's what I want you to try:\n"
            "• **Ground yourself**: Name 5 things you can see, 4 you can touch, 3 you hear.\n"
            "• **Be gentle with yourself today** — rest is not weakness.\n"
            "• **One message can change everything** — is there anyone, even someone distant, you could reach out to?\n\n"
            "You reached out to me, and that already shows strength. I'm proud of you. 🌸"
        ),
    ],

    "anger": [
        (
            "I can feel the frustration in your words, and those feelings are completely valid. 🔥\n\n"
            "Here's how to process anger in a healthy way:\n"
            "• **Step away** from the situation for 5–10 minutes before reacting.\n"
            "• **Physical release** — go for a brisk walk, do jumping jacks, or squeeze something.\n"
            "• **Write it down** — express everything without filtering, then re-read calmly.\n"
            "• **Ask yourself** — what need of mine is not being met right now?\n\n"
            "Your feelings are real. Let's work through this together. ✨"
        ),
        (
            "Anger is a signal that something important to you is being threatened. That's valid. 💪\n\n"
            "Try these to cool down:\n"
            "• **Breathe** — 4 counts in, hold 4, out 4. Repeat 3 times.\n"
            "• **Name the feeling under the anger** — is it hurt? fear? disappointment?\n"
            "• **Don't make decisions when you're at peak anger** — give it 30 minutes.\n\n"
            "You've got this. I believe in you. 🌟"
        ),
    ],

    "hate": [
        (
            "Carrying feelings of hate is exhausting — for you more than anyone else. 💙\n\n"
            "Here's something to try:\n"
            "• **Identify what's really hurting you** — hate often masks deep pain or fear.\n"
            "• **Talk to someone** — a trusted person or counselor can help you process this.\n"
            "• **Redirect the energy** — exercise, art, or writing can release it safely.\n\n"
            "You deserve peace inside. Let's find it together. 🌈"
        ),
    ],

    "empty": [
        (
            "Feeling empty can be one of the scariest feelings — like you're numb and disconnected. 💙\n\n"
            "Here's what might help:\n"
            "• **Don't isolate** — even sitting near other people (a café, library) helps.\n"
            "• **Do something with your hands** — cook, draw, fold clothes — action breaks numbness.\n"
            "• **Small moments of sensation** — a warm shower, a favourite song, a smell you love.\n"
            "• **Talk to a professional** — emptiness that persists deserves proper support.\n\n"
            "You are not broken. This is temporary. 🌻"
        ),
        (
            "Emptiness is real and it's painful — please don't dismiss what you're feeling. 💙\n\n"
            "Let's try to reconnect:\n"
            "• **One tiny act of self-care** — drink water, eat something, step outside.\n"
            "• **Reach out** — even 'I'm not doing great' to someone who cares.\n"
            "• **Remember a time you felt okay** — what was different? Can any part of that be recreated?\n\n"
            "You are not alone in this. 🌟"
        ),
    ],

    "anxiety": [
        (
            "Anxiety can feel overwhelming, but you CAN get through this. 💙\n\n"
            "Right now, try this:\n"
            "• **Box breathing**: Breathe in 4s → hold 4s → out 4s → hold 4s. Repeat.\n"
            "• **5-4-3-2-1 grounding**: 5 things you see, 4 you touch, 3 you hear, 2 you smell, 1 you taste.\n"
            "• **Remind yourself**: anxiety lies — the worst usually doesn't happen.\n"
            "• **Limit caffeine and screens** — they amplify anxiety significantly.\n\n"
            "You are safe right now. I'm here. 🌸"
        ),
    ],

    "neutral": [
        (
            "Thanks for sharing that with me. 😊\n\n"
            "Even when things feel okay, checking in with yourself is a great habit.\n"
            "• **Is there something on your mind** you haven't fully processed?\n"
            "• **How are you sleeping and eating?** — basics affect mood more than we think.\n"
            "• **Do something kind for yourself today** — even 10 minutes of something you enjoy.\n\n"
            "I'm always here whenever you need to talk. 🌟"
        ),
    ],

    "fun": [
        (
            "Love the positive energy! 🎉\n\n"
            "Keep that joy going:\n"
            "• **Share it** — joy multiplies when shared with others.\n"
            "• **Make a note of what made today fun** — for the harder days ahead.\n"
            "• **Say thank you to someone** who contributed to your good mood.\n\n"
            "You deserve every bit of this happiness! 😄"
        ),
    ],

    "happiness": [
        (
            "That's wonderful to hear! 😊✨\n\n"
            "Here's how to make happiness last longer:\n"
            "• **Savour the moment** — don't rush past it.\n"
            "• **Write down what made you happy** — your future self will thank you.\n"
            "• **Spread it** — a kind word or compliment passes happiness on.\n\n"
            "Keep shining — the world needs your light! 🌟"
        ),
    ],

    "enthusiasm": [
        (
            "That energy is absolutely contagious! 🔥🚀\n\n"
            "Channel that enthusiasm:\n"
            "• **Start that thing you've been putting off** — right now is the perfect time.\n"
            "• **Set a small goal today** and ride this wave to complete it.\n"
            "• **Tell someone about what excites you** — it builds connection.\n\n"
            "Go get it — you've totally got this! 💪"
        ),
    ],

    "love": [
        (
            "That warmth you're feeling is one of life's greatest gifts. 💕\n\n"
            "Nurture it:\n"
            "• **Express it** — tell the people you love that you love them today.\n"
            "• **Also give some of that love to yourself** — self-love is just as important.\n"
            "• **Do something kind** for someone unexpected.\n\n"
            "Love is beautiful — and so are you. 🌸"
        ),
    ],

    "relief": [
        (
            "That feeling of relief is so well-deserved. 😌\n\n"
            "Use this calm moment well:\n"
            "• **Rest** — you've been through something, and rest is earned.\n"
            "• **Reflect** — what helped you get through? Remember it for next time.\n"
            "• **Celebrate** — even small wins deserve acknowledgment.\n\n"
            "You made it through, and that matters. 🌤️"
        ),
    ],

    "surprise": [
        (
            "Life is full of unexpected turns! 🎊\n\n"
            "When things surprise you:\n"
            "• **Give yourself a moment** before reacting — especially if the surprise is difficult.\n"
            "• **Stay curious** — surprises often lead to growth.\n"
            "• **Talk it through** if it's overwhelming.\n\n"
            "Whatever comes next, you can handle it! 💪"
        ),
    ],
}

THERAPEUTIC_RESPONSES_AR = {

    "sadness": [
        (
            "أنا سامعك، وعايزك تعرف إن الإحساس بالضياع والوحدة من أصعب المشاعر اللي ممكن تحس بيها. 💙\n\n"
            "في حاجات ممكن تساعدك دلوقتي:\n"
            "• **تواصل مع شخص واحد** — حتى رسالة بسيطة تكسر الصمت.\n"
            "• **اكتب 3 حاجات بتحس بيها** — إخراجها من دماغك بيساعد.\n"
            "• **اطلع برة 10 دقايق** — الهواء الطلق والحركة بيغيروا المزاج.\n"
            "• **كن لطيف مع نفسك** — مش لازم تحل كل حاجة النهارده.\n\n"
            "مش لوحدك. أنا هنا معاك. 🌻"
        ),
        (
            "اللي بتحس بيه حقيقي، وبيتطلب شجاعة إنك تتكلم عنه. 💙\n\n"
            "خطوات صغيرة ممكن تساعدك:\n"
            "• **اتكلم مع حد بتثق فيه** — صاحب، أحد من أهلك، أو متخصص.\n"
            "• **اعمل حاجة صغيرة كانت بتبهجك** — موسيقى، مشية، رسم.\n"
            "• **فكر** إن الإحساس ده مؤقت، حتى لو مش حاسس بكده دلوقتي.\n\n"
            "أنت أهم مما تتخيل. 🌟"
        ),
        (
            "الإحساس بالضياع صعب جداً، خصوصاً لما حاسس إن محدش موجود. 💙\n\n"
            "جرب ده:\n"
            "• **ركّز في الحاضر**: قول 5 حاجات شايفها، 4 بتلمسها، 3 بتسمعها.\n"
            "• **كن لطيف مع نفسك النهارده** — الراحة مش ضعف.\n"
            "• **رسالة واحدة ممكن تغير كل حاجة** — في حد ولو بعيد تقدر تتواصل معاه؟\n\n"
            "إنك وصلت هنا وتكلمتني ده وحده بيبين قوتك. أنا فخور بيك. 🌸"
        ),
    ],

    "anger": [
        (
            "حاسس بالإحباط في كلامك، ومشاعرك دي حقيقية ومفهومة تماماً. 🔥\n\n"
            "إزاي تتعامل مع الغضب بطريقة صحية:\n"
            "• **ابتعد** عن الموقف 5-10 دقايق قبل ما تتصرف.\n"
            "• **نفّس طاقتك** — امشي بسرعة، أو اعمل أي نشاط جسدي.\n"
            "• **اكتب كل حاجة** — عبّر عن نفسك من غير فلترة، وبعدين اقرأها بهدوء.\n"
            "• **اسأل نفسك** — إيه الاحتياج اللي مش بيتلبى دلوقتي؟\n\n"
            "مشاعرك حقيقية. هنعدي فيها مع بعض. ✨"
        ),
        (
            "الغضب إشارة إن حاجة مهمة ليك بتتهدد. ده مفهوم. 💪\n\n"
            "جرب تهدى:\n"
            "• **خد نفس** — 4 ثواني جوا، احبس 4، برا 4. كرر 3 مرات.\n"
            "• **حدد الإحساس اللي تحت الغضب** — هل هو ألم؟ خوف؟ خيبة أمل؟\n"
            "• **متاخدش قرارات وانت في قمة الغضب** — استنى 30 دقيقة.\n\n"
            "عندك القدرة. أنا مؤمن بيك. 🌟"
        ),
    ],

    "hate": [
        (
            "حمل الكراهية متعب — بالنسبالك أكتر من أي حد تاني. 💙\n\n"
            "جرب ده:\n"
            "• **حدد اللي بيوجعك فعلاً** — الكراهية غالباً بتخبي ألم أو خوف عميق.\n"
            "• **اتكلم مع حد** — شخص بتثق فيه أو متخصص يساعدك تعالج الموضوع ده.\n"
            "• **حوّل الطاقة** — رياضة، فن، أو كتابة تساعد في إطلاقها بأمان.\n\n"
            "تستحق السلام الداخلي. يلا نلاقيه مع بعض. 🌈"
        ),
    ],

    "empty": [
        (
            "الإحساس بالفراغ من أصعب المشاعر — زي ما إنت بايخ ومنفصل عن كل حاجة. 💙\n\n"
            "في حاجات ممكن تساعد:\n"
            "• **متعزلش** — حتى مجرد قعادك جنب ناس (كافيه، مكتبة) بيفرق.\n"
            "• **اعمل حاجة بإيدك** — طبخ، رسم، ترتيب — الحركة بتكسر الخدر.\n"
            "• **لحظات إحساس صغيرة** — دش دافي، أغنية بتحبها، ريحة جميلة.\n"
            "• **اتكلم مع متخصص** — الفراغ المستمر يستحق دعم حقيقي.\n\n"
            "مش مكسور. ده مؤقت. 🌻"
        ),
        (
            "الفراغ حقيقي ومؤلم — متتجاهلش اللي بتحس بيه. 💙\n\n"
            "يلا نحاول نترابط تاني:\n"
            "• **تصرف صغير جداً** — اشرب ميه، كل حاجة، اطلع برة.\n"
            "• **تواصل** — حتى 'مش تمام' لحد بيهتم.\n"
            "• **فكر في وقت كنت تمام** — إيه اللي كان مختلف؟ ممكن ترجعه؟\n\n"
            "مش لوحدك في ده. 🌟"
        ),
    ],

    "anxiety": [
        (
            "القلق ممكن يبقى ساحق، بس أنت تقدر تعدي فيه. 💙\n\n"
            "دلوقتي جرب ده:\n"
            "• **تنفس الصندوق**: جوا 4 ثواني ← احبس 4 ← برا 4 ← احبس 4. كرر.\n"
            "• **تمرين 5-4-3-2-1**: 5 حاجات شايفها، 4 بتلمسها، 3 بتسمعها، 2 بتشمها، 1 بتتذوقها.\n"
            "• **فكّرك**: القلق بيكدب — الأسوأ غالباً بيحصلش.\n"
            "• **قلل الكافيين والشاشات** — بيزودوا القلق بشكل كبير.\n\n"
            "أنت آمن دلوقتي. أنا هنا. 🌸"
        ),
    ],

    "neutral": [
        (
            "شكراً إنك شاركتني. 😊\n\n"
            "حتى لما الأمور ماشية، مراجعة نفسك عادة كويسة.\n"
            "• **في حاجة في بالك** لسه معالجتهاش؟\n"
            "• **بتنام وباكل كويس؟** — الأساسيات بتأثر في المزاج أكتر مما نفتكر.\n"
            "• **اعمل حاجة كويسة لنفسك النهارده** — حتى 10 دقايق بتحبها.\n\n"
            "أنا هنا دايماً وقت ما تحتاج تتكلم. 🌟"
        ),
    ],

    "fun": [
        (
            "أحب الطاقة الإيجابية دي! 🎉\n\n"
            "استمر في الفرح ده:\n"
            "• **شاركه** — الفرح بيتضاعف لما بيتشارك مع الناس.\n"
            "• **دوّن اللي خلى النهارده ممتع** — ليومين التقيلة الجاية.\n"
            "• **قول شكراً لحد** ساهم في مزاجك الحلو.\n\n"
            "تستحق كل لحظة سعادة دي! 😄"
        ),
    ],

    "happiness": [
        (
            "ده كلام جميل أسمعه! 😊✨\n\n"
            "إزاي تخلي السعادة تستمر أطول:\n"
            "• **تلذذ باللحظة** — متستعجلش.\n"
            "• **اكتب اللي عملك سعيد** — نفسك المستقبلي هيشكرك.\n"
            "• **انشره** — كلمة حلوة أو إطراء بينقل السعادة.\n\n"
            "استمر في إضاءتك — العالم محتاجها! 🌟"
        ),
    ],

    "enthusiasm": [
        (
            "الطاقة دي معدية بالفعل! 🔥🚀\n\n"
            "وجّه حماسك:\n"
            "• **ابدأ الحاجة اللي كنت بتأجلها** — دلوقتي هو الوقت المثالي.\n"
            "• **حدد هدف صغير النهارده** واركب موجة الطاقة دي.\n"
            "• **قول لحد عن اللي بيحمسك** — بيبني علاقة أقوى.\n\n"
            "يلا عليها — عندك القدرة! 💪"
        ),
    ],

    "love": [
        (
            "الدفا اللي بتحس بيه ده من أجمل هدايا الحياة. 💕\n\n"
            "غذّيه:\n"
            "• **عبّر عنه** — قول للناس اللي بتحبهم إنك بتحبهم النهارده.\n"
            "• **كمان حب نفسك** — محبة الذات مهمة زي ما تحب غيرك.\n"
            "• **اعمل حاجة كويسة** لحد غير متوقع.\n\n"
            "الحب جميل — وأنت جميل كمان. 🌸"
        ),
    ],

    "relief": [
        (
            "الإحساس بالارتياح ده مستحق جداً. 😌\n\n"
            "استغل اللحظة الهادية دي:\n"
            "• **استرح** — مريت بحاجة، والراحة مستحقة.\n"
            "• **تأمل** — إيه اللي ساعدك تعدي؟ افتكره للمرة الجاية.\n"
            "• **احتفل** — حتى الانجازات الصغيرة تستحق تقدير.\n\n"
            "عديتها، وده بيفرق. 🌤️"
        ),
    ],

    "surprise": [
        (
            "الحياة مليانة مفاجآت! 🎊\n\n"
            "لما حاجة تفاجئك:\n"
            "• **خد لحظة** قبل ما تتفاعل — خصوصاً لو المفاجأة صعبة.\n"
            "• **فضّل فضولي** — المفاجآت غالباً بتؤدي لنمو.\n"
            "• **اتكلم عنها** لو كانت ساحقة.\n\n"
            "مهما جه بعد كده، تقدر تتعامل معاه! 💪"
        ),
    ],
}

THERAPEUTIC_RESPONSES_FR = {

    "sadness": [
        (
            "Je t'entends, et je veux que tu saches — se sentir perdu et seul est l'un des sentiments les plus difficiles. 💙\n\n"
            "Voici quelques choses qui pourraient t'aider maintenant :\n"
            "• **Contacte une personne** — même un simple message peut briser le silence.\n"
            "• **Écris 3 choses que tu ressens** — sortir ça de ta tête aide vraiment.\n"
            "• **Sors 10 minutes** — l'air frais et le mouvement changent l'humeur.\n"
            "• **Sois gentil avec toi-même** — tu n'as pas à tout régler aujourd'hui.\n\n"
            "Tu n'es pas seul. Je suis là avec toi. 🌻"
        ),
        (
            "Ce que tu ressens est valide, et il faut du vrai courage pour en parler. 💙\n\n"
            "Petites étapes pour aider avec la tristesse :\n"
            "• **Parle à quelqu'un de confiance** — un ami, un proche, ou un professionnel.\n"
            "• **Fais une petite chose qui te procurait de la joie** — musique, promenade, dessin.\n"
            "• **Rappelle-toi** — ce sentiment est temporaire, même si ce n'est pas ce que tu ressens.\n\n"
            "Tu comptes plus que tu ne le sais. 🌟"
        ),
        (
            "Se sentir perdu est incroyablement difficile, surtout quand tu sens que tu n'as personne. 💙\n\n"
            "Voici ce que je veux que tu essaies :\n"
            "• **Ancre-toi** : Nomme 5 choses que tu vois, 4 que tu touches, 3 que tu entends.\n"
            "• **Sois doux avec toi-même aujourd'hui** — le repos n'est pas une faiblesse.\n"
            "• **Un message peut tout changer** — y a-t-il quelqu'un que tu pourrais contacter?\n\n"
            "Tu m'as contacté, et ça montre déjà ta force. Je suis fier de toi. 🌸"
        ),
    ],

    "anger": [
        (
            "Je sens la frustration dans tes mots, et ces sentiments sont totalement valides. 🔥\n\n"
            "Voici comment traiter la colère sainement :\n"
            "• **Éloigne-toi** de la situation 5–10 minutes avant de réagir.\n"
            "• **Libération physique** — fais une marche rapide, des jumping jacks, ou serre quelque chose.\n"
            "• **Écris tout** — exprime sans filtre, puis relis calmement.\n"
            "• **Demande-toi** — quel besoin n'est pas satisfait en ce moment?\n\n"
            "Tes sentiments sont réels. Travaillons ça ensemble. ✨"
        ),
        (
            "La colère est un signal que quelque chose d'important pour toi est menacé. C'est valide. 💪\n\n"
            "Essaie ça pour te calmer :\n"
            "• **Respire** — 4 temps en, retiens 4, expire 4. Répète 3 fois.\n"
            "• **Nomme le sentiment sous la colère** — est-ce de la douleur? de la peur? de la déception?\n"
            "• **Ne prends pas de décisions au pic de la colère** — attends 30 minutes.\n\n"
            "Tu peux y arriver. J'ai confiance en toi. 🌟"
        ),
    ],

    "hate": [
        (
            "Porter des sentiments de haine est épuisant — pour toi plus que pour quiconque. 💙\n\n"
            "Voici quelque chose à essayer :\n"
            "• **Identifie ce qui te blesse vraiment** — la haine cache souvent une douleur ou une peur profonde.\n"
            "• **Parle à quelqu'un** — une personne de confiance ou un thérapeute peut t'aider.\n"
            "• **Redirige l'énergie** — le sport, l'art ou l'écriture peuvent la libérer sainement.\n\n"
            "Tu mérites la paix intérieure. Trouvons-la ensemble. 🌈"
        ),
    ],

    "empty": [
        (
            "Se sentir vide peut être l'un des sentiments les plus effrayants — comme être engourdi et déconnecté. 💙\n\n"
            "Voici ce qui peut aider :\n"
            "• **Ne t'isole pas** — même être assis près d'autres personnes (un café, une bibliothèque) aide.\n"
            "• **Fais quelque chose avec tes mains** — cuisiner, dessiner, plier — l'action brise l'engourdissement.\n"
            "• **Petits moments de sensation** — une douche chaude, une chanson préférée, une odeur que tu aimes.\n"
            "• **Parle à un professionnel** — un vide persistant mérite un vrai soutien.\n\n"
            "Tu n'es pas cassé. C'est temporaire. 🌻"
        ),
        (
            "Le vide est réel et douloureux — ne minimise pas ce que tu ressens. 💙\n\n"
            "Essayons de te reconnecter :\n"
            "• **Un tout petit acte de soin** — bois de l'eau, mange quelque chose, sors.\n"
            "• **Contacte quelqu'un** — même 'ça ne va pas très bien' à quelqu'un qui se soucie.\n"
            "• **Souviens-toi d'un moment où tu allais bien** — qu'est-ce qui était différent?\n\n"
            "Tu n'es pas seul dans ça. 🌟"
        ),
    ],

    "anxiety": [
        (
            "L'anxiété peut sembler accablante, mais tu PEUX la traverser. 💙\n\n"
            "Maintenant, essaie ça :\n"
            "• **Respiration en boîte** : Inspire 4s → retiens 4s → expire 4s → retiens 4s. Répète.\n"
            "• **Ancrage 5-4-3-2-1** : 5 choses que tu vois, 4 que tu touches, 3 que tu entends, 2 que tu sens, 1 que tu goûtes.\n"
            "• **Rappelle-toi** : l'anxiété ment — le pire n'arrive généralement pas.\n"
            "• **Limite la caféine et les écrans** — ils amplifient l'anxiété considérablement.\n\n"
            "Tu es en sécurité maintenant. Je suis là. 🌸"
        ),
    ],

    "neutral": [
        (
            "Merci de partager ça avec moi. 😊\n\n"
            "Même quand les choses semblent bien, se vérifier est une excellente habitude.\n"
            "• **Y a-t-il quelque chose dans ton esprit** que tu n'as pas complètement traité?\n"
            "• **Comment tu dors et manges?** — les bases affectent l'humeur plus qu'on ne le pense.\n"
            "• **Fais quelque chose de gentil pour toi aujourd'hui** — même 10 minutes de quelque chose que tu aimes.\n\n"
            "Je suis toujours là quand tu as besoin de parler. 🌟"
        ),
    ],

    "fun": [
        (
            "J'adore cette énergie positive! 🎉\n\n"
            "Garde cette joie vivante :\n"
            "• **Partage-la** — la joie se multiplie quand on la partage avec les autres.\n"
            "• **Note ce qui a rendu ta journée amusante** — pour les jours plus difficiles à venir.\n"
            "• **Dis merci à quelqu'un** qui a contribué à ta bonne humeur.\n\n"
            "Tu mérites chaque instant de ce bonheur! 😄"
        ),
    ],

    "happiness": [
        (
            "C'est merveilleux à entendre! 😊✨\n\n"
            "Voici comment faire durer le bonheur :\n"
            "• **Savoure le moment** — ne te précipite pas.\n"
            "• **Écris ce qui t'a rendu heureux** — ton futur toi te remerciera.\n"
            "• **Propage-le** — un mot gentil ou un compliment transmet le bonheur.\n\n"
            "Continue de briller — le monde a besoin de ta lumière! 🌟"
        ),
    ],

    "enthusiasm": [
        (
            "Cette énergie est absolument contagieuse! 🔥🚀\n\n"
            "Canalise cet enthousiasme :\n"
            "• **Commence ce que tu repoussais** — maintenant c'est le moment parfait.\n"
            "• **Fixe un petit objectif aujourd'hui** et surfe sur cette vague pour l'accomplir.\n"
            "• **Dis à quelqu'un ce qui t'enthousiasme** — ça crée du lien.\n\n"
            "Vas-y — tu peux totalement y arriver! 💪"
        ),
    ],

    "love": [
        (
            "Cette chaleur que tu ressens est l'un des plus grands cadeaux de la vie. 💕\n\n"
            "Nourris-la :\n"
            "• **Exprime-la** — dis aux gens que tu aimes que tu les aimes aujourd'hui.\n"
            "• **Donne aussi de cet amour à toi-même** — l'amour de soi est tout aussi important.\n"
            "• **Fais quelque chose de gentil** pour quelqu'un d'inattendu.\n\n"
            "L'amour est beau — et toi aussi. 🌸"
        ),
    ],

    "relief": [
        (
            "Ce sentiment de soulagement est tellement mérité. 😌\n\n"
            "Profite de ce moment calme :\n"
            "• **Repose-toi** — tu as traversé quelque chose, et le repos est mérité.\n"
            "• **Réfléchis** — qu'est-ce qui t'a aidé à traverser ça? Souviens-t'en pour la prochaine fois.\n"
            "• **Célèbre** — même les petites victoires méritent d'être reconnues.\n\n"
            "Tu t'en es sorti, et ça compte. 🌤️"
        ),
    ],

    "surprise": [
        (
            "La vie est pleine de tournures inattendues! 🎊\n\n"
            "Quand les choses te surprennent :\n"
            "• **Donne-toi un moment** avant de réagir — surtout si la surprise est difficile.\n"
            "• **Reste curieux** — les surprises mènent souvent à la croissance.\n"
            "• **Parles-en** si c'est accablant.\n\n"
            "Quoi qu'il arrive ensuite, tu peux y faire face! 💪"
        ),
    ],
}

RESPONSES_BY_LANG = {
    "en": THERAPEUTIC_RESPONSES_EN,
    "ar": THERAPEUTIC_RESPONSES_AR,
    "fr": THERAPEUTIC_RESPONSES_FR,
}

_DEFAULT = {
    "en": (
        "Thank you for trusting me with how you feel. 💙\n\n"
        "Whatever you're going through, here are some universal tips:\n"
        "• **Talk to someone** — a friend, family member, or professional.\n"
        "• **Take care of your basics** — sleep, water, movement.\n"
        "• **Be patient with yourself** — healing isn't linear.\n\n"
        "I'm here for you, always. 🌟"
    ),
    "ar": (
        "شكراً إنك وثقت فيا بمشاعرك. 💙\n\n"
        "مهما بتمر بيه، في نصايح عامة ممكن تساعد:\n"
        "• **اتكلم مع حد** — صاحب، أهل، أو متخصص.\n"
        "• **اهتم بالأساسيات** — نوم، ميه، حركة.\n"
        "• **كن صبور مع نفسك** — الشفا مش خط مستقيم.\n\n"
        "أنا هنا ليك دايماً. 🌟"
    ),
    "fr": (
        "Merci de me faire confiance avec ce que tu ressens. 💙\n\n"
        "Quoi que tu traverses, voici des conseils universels :\n"
        "• **Parle à quelqu'un** — un ami, un proche, ou un professionnel.\n"
        "• **Prends soin des bases** — sommeil, eau, mouvement.\n"
        "• **Sois patient avec toi-même** — la guérison n'est pas linéaire.\n\n"
        "Je suis là pour toi, toujours. 🌟"
    ),
}

def get_response(emotion: str, lang: str = "en") -> str:
    """
    Return a random therapeutic response for the given emotion and language.
    
    Args:
        emotion: detected emotion label (e.g. 'sadness', 'anger', ...)
        lang: language code — 'en' | 'ar' | 'fr'  (default: 'en')
    
    Returns:
        A therapeutic response string in the requested language.
    """
    lang = lang.strip().lower()
    if lang not in RESPONSES_BY_LANG:
        lang = "en"

    emotion = emotion.strip().lower()
    pool = RESPONSES_BY_LANG[lang].get(emotion)
    if pool:
        return random.choice(pool)
    return _DEFAULT.get(lang, _DEFAULT["en"])
