'use strict';
const root=document.documentElement,reduced=matchMedia('(prefers-reduced-motion: reduce)'),darkPreference=matchMedia('(prefers-color-scheme: dark)');
const storeGet=key=>{try{return localStorage.getItem(key)}catch{return null}},storeSet=(key,value)=>{try{localStorage.setItem(key,value)}catch{}};
const motionPaused=()=>reduced.matches||root.dataset.motion==='paused';
function animateIn(element){element.classList.remove('word-enter');void element.offsetWidth;element.classList.add('word-enter')}
const themeButton=document.querySelector('.web-theme'),motionButton=document.querySelector('.web-motion');
function applyTheme(theme){root.dataset.theme=theme;if(themeButton){themeButton.setAttribute('aria-pressed',String(theme==='dark'));themeButton.setAttribute('aria-label',theme==='dark'?'Switch to light theme':'Switch to dark theme');themeButton.querySelector('span').textContent=theme==='dark'?'Light':'Dark'}document.querySelector('meta[name="theme-color"]')?.setAttribute('content',theme==='dark'?'#101d1a':'#123e35')}
applyTheme(storeGet('schoolos-theme')||(darkPreference.matches?'dark':'light'));
themeButton?.addEventListener('click',()=>{const theme=root.dataset.theme==='dark'?'light':'dark';storeSet('schoolos-theme',theme);applyTheme(theme)});
darkPreference.addEventListener('change',e=>{if(!storeGet('schoolos-theme'))applyTheme(e.matches?'dark':'light')});
function applyMotion(){if(motionButton){const paused=motionPaused();motionButton.setAttribute('aria-pressed',String(paused));motionButton.setAttribute('aria-label',paused?'Resume website motion':'Pause website motion');motionButton.innerHTML=paused?'▷ <span>Resume motion</span>':'Ⅱ <span>Pause motion</span>'}if(motionPaused())document.querySelectorAll('.reveal-ready').forEach(el=>el.classList.add('revealed'))}
root.dataset.motion=storeGet('schoolos-motion')||'playing';applyMotion();motionButton?.addEventListener('click',()=>{root.dataset.motion=root.dataset.motion==='paused'?'playing':'paused';storeSet('schoolos-motion',root.dataset.motion);applyMotion()});reduced.addEventListener('change',applyMotion);
const menu=document.querySelector('.menu'),nav=document.querySelector('#webnav');
menu?.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open)});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu?.getAttribute('aria-expanded')==='true'){menu.click();menu.focus()}});
const facts=['Zero is an even number: it is divisible by two with no remainder.','A triangle’s interior angles add to 180° on a flat plane. On a curved surface, the story changes.','Plants use light energy to turn carbon dioxide and water into sugars during photosynthesis.','The number 2 is the only even prime number. Every other even number has 2 as a factor.','Sound needs a medium to travel through. It cannot travel through a vacuum.','A leap year usually has 366 days. Century years must be divisible by 400 to qualify.'];let fact=0;
document.querySelector('#next-fact')?.addEventListener('click',()=>{fact=(fact+1)%facts.length;document.querySelector('#fun-fact').textContent=facts[fact];if(!motionPaused())animateIn(document.querySelector('#fun-fact'))});
const challenges = [
  {
    "id": 0,
    "topic": "Maths",
    "question": "A class plants 3 rows of 8 seedlings. One quarter grows flowers. How many flower?",
    "options": [
      "4",
      "6",
      "8"
    ],
    "correct": "6",
    "explanation": "3 × 8 = 24 seedlings. One quarter of 24 is 6."
  },
  {
    "id": 1,
    "topic": "Maths",
    "question": "What is 15% of 200?",
    "options": [
      "15",
      "30",
      "45"
    ],
    "correct": "30",
    "explanation": "10% of 200 is 20 and 5% is 10. Add them: 30."
  },
  {
    "id": 2,
    "topic": "Maths",
    "question": "A triangle has two angles of 50° and 60°. What is the third?",
    "options": [
      "60°",
      "70°",
      "80°"
    ],
    "correct": "70°",
    "explanation": "On a flat plane, a triangle’s angles total 180°. Subtract 50° and 60° to get 70°."
  },
  {
    "id": 3,
    "topic": "Maths",
    "question": "What is three quarters of 28?",
    "options": [
      "7",
      "14",
      "21"
    ],
    "correct": "21",
    "explanation": "Divide 28 by 4 to get 7, then multiply by 3 to get 21."
  },
  {
    "id": 4,
    "topic": "Maths",
    "question": "Which of these numbers is prime?",
    "options": [
      "21",
      "29",
      "33"
    ],
    "correct": "29",
    "explanation": "29 has exactly two positive factors: 1 and 29. 21 and 33 are divisible by 3."
  },
  {
    "id": 5,
    "topic": "Maths",
    "question": "A square has a perimeter of 36 cm. What is its area?",
    "options": [
      "36 cm²",
      "81 cm²",
      "144 cm²"
    ],
    "correct": "81 cm²",
    "explanation": "Each side is 36 ÷ 4 = 9 cm. Its area is 9 × 9 = 81 cm²."
  },
  {
    "id": 6,
    "topic": "Science",
    "question": "Which gas do plants take in for photosynthesis?",
    "options": [
      "Oxygen",
      "Carbon dioxide",
      "Helium"
    ],
    "correct": "Carbon dioxide",
    "explanation": "Plants use carbon dioxide and water, with light energy, to make sugars during photosynthesis."
  },
  {
    "id": 7,
    "topic": "Science",
    "question": "Which part of a cell contains most of its DNA in a typical animal cell?",
    "options": [
      "Nucleus",
      "Cell membrane",
      "Cytoplasm"
    ],
    "correct": "Nucleus",
    "explanation": "Most DNA is inside the nucleus. Mitochondria also contain a small amount of DNA."
  },
  {
    "id": 8,
    "topic": "Science",
    "question": "Which travels faster in a vacuum: red light or blue light?",
    "options": [
      "Red light",
      "Blue light",
      "Same speed"
    ],
    "correct": "Same speed",
    "explanation": "All visible light travels at the same speed in a vacuum."
  },
  {
    "id": 9,
    "topic": "Science",
    "question": "What force keeps the planets in orbit around the Sun?",
    "options": [
      "Friction",
      "Gravity",
      "Magnetism"
    ],
    "correct": "Gravity",
    "explanation": "Gravity provides the inward force that bends each planet’s path into an orbit."
  },
  {
    "id": 10,
    "topic": "Science",
    "question": "When liquid water becomes water vapour at its surface, what is the process?",
    "options": [
      "Freezing",
      "Evaporation",
      "Condensation"
    ],
    "correct": "Evaporation",
    "explanation": "Evaporation is the change from liquid to gas at the liquid’s surface."
  },
  {
    "id": 11,
    "topic": "Science",
    "question": "Which organ pumps blood around the human body?",
    "options": [
      "Lungs",
      "Heart",
      "Kidneys"
    ],
    "correct": "Heart",
    "explanation": "The heart pumps blood. Lungs exchange gases and kidneys filter the blood."
  },
  {
    "id": 12,
    "topic": "Logic",
    "question": "What comes next: 2, 4, 8, 16, …?",
    "options": [
      "18",
      "24",
      "32"
    ],
    "correct": "32",
    "explanation": "Each number doubles. 16 × 2 = 32."
  },
  {
    "id": 13,
    "topic": "Logic",
    "question": "All robins are birds. Some birds swim. Must all robins swim?",
    "options": [
      "Yes",
      "No",
      "Only in summer"
    ],
    "correct": "No",
    "explanation": "The statements do not tell us whether robins belong to the group of birds that swim."
  },
  {
    "id": 14,
    "topic": "Logic",
    "question": "I have keys but no locks, and space but no room. What am I?",
    "options": [
      "A keyboard",
      "A suitcase",
      "A library"
    ],
    "correct": "A keyboard",
    "explanation": "A keyboard has letter keys and a space bar, but they are not door keys or a physical room."
  },
  {
    "id": 15,
    "topic": "Logic",
    "question": "Which letter comes next: A, C, E, G, …?",
    "options": [
      "H",
      "I",
      "J"
    ],
    "correct": "I",
    "explanation": "Skip one letter each time: A, C, E, G, I."
  },
  {
    "id": 16,
    "topic": "Logic",
    "question": "If today is Tuesday, what day will it be in 10 days?",
    "options": [
      "Thursday",
      "Friday",
      "Saturday"
    ],
    "correct": "Friday",
    "explanation": "Seven days later is Tuesday. Three more days takes you to Friday."
  },
  {
    "id": 17,
    "topic": "Logic",
    "question": "Three children each shake hands with every other child once. How many handshakes?",
    "options": [
      "3",
      "6",
      "9"
    ],
    "correct": "3",
    "explanation": "Label them A, B and C. The pairs are AB, AC and BC: three handshakes."
  },
  {
    "id": 18,
    "topic": "Words",
    "question": "Which word is a synonym of “curious”?",
    "options": [
      "Inquisitive",
      "Sleepy",
      "Silent"
    ],
    "correct": "Inquisitive",
    "explanation": "Inquisitive means eager to ask questions and learn."
  },
  {
    "id": 19,
    "topic": "Words",
    "question": "Which is the correct plural of “child”?",
    "options": [
      "Childs",
      "Children",
      "Childes"
    ],
    "correct": "Children",
    "explanation": "“Children” is an irregular plural. It does not follow the usual add-s rule."
  },
  {
    "id": 20,
    "topic": "Words",
    "question": "Which sentence uses “their” correctly?",
    "options": [
      "Their going home.",
      "Their books are here.",
      "Put it over their."
    ],
    "correct": "Their books are here.",
    "explanation": "“Their” shows possession. “They’re” means they are, and “there” refers to a place."
  },
  {
    "id": 21,
    "topic": "Words",
    "question": "Which word is an adjective in “The bright moon glows”?",
    "options": [
      "Bright",
      "Moon",
      "Glows"
    ],
    "correct": "Bright",
    "explanation": "“Bright” describes the moon, so it is an adjective. “Moon” is a noun and “glows” is a verb."
  },
  {
    "id": 22,
    "topic": "Words",
    "question": "Which word is a palindrome, reading the same forwards and backwards?",
    "options": [
      "Level",
      "Learn",
      "Light"
    ],
    "correct": "Level",
    "explanation": "L-E-V-E-L reads the same in both directions."
  },
  {
    "id": 23,
    "topic": "Words",
    "question": "Which punctuation mark usually ends a direct question?",
    "options": [
      "Comma",
      "Question mark",
      "Semicolon"
    ],
    "correct": "Question mark",
    "explanation": "A direct question ends with a question mark, for example: What did you discover?"
  },
  {
    "id": 24,
    "topic": "Geography",
    "question": "What is the capital of Nigeria?",
    "options": [
      "Lagos",
      "Abuja",
      "Kano"
    ],
    "correct": "Abuja",
    "explanation": "Abuja became Nigeria’s federal capital in 1991."
  },
  {
    "id": 25,
    "topic": "Geography",
    "question": "Which ocean lies along Nigeria’s southern coastline?",
    "options": [
      "Atlantic Ocean",
      "Indian Ocean",
      "Pacific Ocean"
    ],
    "correct": "Atlantic Ocean",
    "explanation": "Nigeria’s coast meets the Gulf of Guinea, which is part of the Atlantic Ocean."
  },
  {
    "id": 26,
    "topic": "Geography",
    "question": "Which direction is opposite north-east?",
    "options": [
      "North-west",
      "South-east",
      "South-west"
    ],
    "correct": "South-west",
    "explanation": "Opposite compass directions are 180° apart. North-east is opposite south-west."
  },
  {
    "id": 27,
    "topic": "Geography",
    "question": "What does the equator divide Earth into?",
    "options": [
      "Eastern and western halves",
      "Northern and southern hemispheres",
      "Land and water"
    ],
    "correct": "Northern and southern hemispheres",
    "explanation": "The equator is the line of latitude at 0°, halfway between the poles."
  },
  {
    "id": 28,
    "topic": "Geography",
    "question": "Which river joins the Niger at Lokoja?",
    "options": [
      "Benue",
      "Thames",
      "Nile"
    ],
    "correct": "Benue",
    "explanation": "Lokoja is known for the confluence of the Niger and Benue rivers."
  },
  {
    "id": 29,
    "topic": "Geography",
    "question": "On a map, 1 cm represents 5 km. How far does 4 cm represent?",
    "options": [
      "9 km",
      "15 km",
      "20 km"
    ],
    "correct": "20 km",
    "explanation": "Multiply the map distance by the scale: 4 × 5 = 20 km."
  },
  {
    "id": 30,
    "topic": "Digital skills",
    "question": "Which password habit is safest?",
    "options": [
      "Reuse one password",
      "Use a unique long password",
      "Share it with friends"
    ],
    "correct": "Use a unique long password",
    "explanation": "Unique long passwords reduce the harm if another service is compromised. A password manager can help."
  },
  {
    "id": 31,
    "topic": "Digital skills",
    "question": "An unexpected message asks for your login code. What should you do?",
    "options": [
      "Send it immediately",
      "Verify through a trusted channel",
      "Post the code publicly"
    ],
    "correct": "Verify through a trusted channel",
    "explanation": "Do not share login codes. Contact the organization independently through a known trusted route."
  },
  {
    "id": 32,
    "topic": "Digital skills",
    "question": "What does a browser’s HTTPS indicator establish?",
    "options": [
      "The website is always honest",
      "The connection is encrypted",
      "Every claim is correct"
    ],
    "correct": "The connection is encrypted",
    "explanation": "HTTPS protects the connection. It does not prove that a website’s content or operator is trustworthy."
  },
  {
    "id": 33,
    "topic": "Digital skills",
    "question": "An offline attendance entry has not synchronized yet. Where might the newest record still be?",
    "options": [
      "Only on the device",
      "On every school account",
      "Nowhere"
    ],
    "correct": "Only on the device",
    "explanation": "Local capture is not proof of a server update. Reconnect, synchronize and review any conflicts."
  },
  {
    "id": 34,
    "topic": "Digital skills",
    "question": "Which file extension commonly identifies a spreadsheet workbook?",
    "options": [
      ".xlsx",
      ".mp3",
      ".jpg"
    ],
    "correct": ".xlsx",
    "explanation": "XLSX is a spreadsheet workbook format. MP3 is audio and JPG is an image format."
  },
  {
    "id": 35,
    "topic": "Digital skills",
    "question": "You see an AI answer that seems wrong. What is the best next step?",
    "options": [
      "Copy it without checking",
      "Check reliable sources and ask a teacher",
      "Assume it is always correct"
    ],
    "correct": "Check reliable sources and ask a teacher",
    "explanation": "AI can make mistakes. Verify claims and calculations with trustworthy sources and a responsible human."
  }
];
Object.freeze(challenges);window.SchoolOSChallenges=challenges;
const topicSelect=document.querySelector('#quiz-topic'),question=document.querySelector('#quiz-question'),answers=document.querySelector('.quiz-answers'),result=document.querySelector('#quiz-result');
let deck=[],active=null,solved=new Set();
function shuffle(list){for(let i=list.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[list[i],list[j]]=[list[j],list[i]]}return list}
function fillDeck(first=false){const topic=topicSelect?.value||'all';deck=challenges.filter(c=>topic==='all'||c.topic===topic).map(c=>c.id);if(first&&topic==='all'){deck=shuffle(deck.slice(1));deck.unshift(0)}else{shuffle(deck);if(deck.length>1&&deck[0]===active?.id)[deck[0],deck[1]]=[deck[1],deck[0]]}}
function showChallenge(){if(!question)return;if(!deck.length)fillDeck();active=challenges[deck.shift()];question.textContent=active.question;document.querySelector('#quiz-topic-label').textContent=active.topic;document.querySelector('#quiz-count').textContent=(topicSelect.value==='all'?36:6)+' discoveries';answers.replaceChildren();active.options.forEach(option=>{const button=document.createElement('button');button.type='button';button.dataset.answer=option;button.textContent=option;button.addEventListener('click',()=>{if(option===active.correct){solved.add(active.id);button.classList.add('correct');answers.querySelectorAll('button').forEach(b=>b.disabled=true);result.textContent='Exactly! '+active.explanation;document.querySelector('#quiz-score').textContent=solved.size+' '+(solved.size===1?'discovery':'discoveries')+' solved';}else{button.classList.add('incorrect');result.textContent='Not quite. Try again! '+(active.id===0?'Start with 3 × 8, then divide by 4.':'Think it through, or try another option.')}});answers.append(button)});result.textContent='Take a guess. A little thinking is always a good thing.';if(!reduced.matches&&!motionPaused())animateIn(question)}
if(question){fillDeck(true);showChallenge();document.querySelector('#next-challenge').addEventListener('click',()=>{showChallenge();question.setAttribute('tabindex','-1');question.focus({preventScroll:true})});topicSelect.addEventListener('change',()=>{fillDeck();showChallenge()})}
const previews={owner:['website-owner.png','School owner overview · Fictional demonstration data.'],onboarding:['website-onboarding.png','School setup checklist · Fictional demonstration data.'],parent:['website-parent.png','Parent mobile dashboard · Fictional demonstration data.']};
document.querySelectorAll('[data-preview]').forEach(b=>b.addEventListener('click',()=>{const data=previews[b.dataset.preview],img=document.querySelector('#dashboard-preview');document.querySelectorAll('[data-preview]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));img.src=data[0];img.alt=data[1];img.classList.toggle('mobile-shot',b.dataset.preview==='parent');document.querySelector('#preview-caption').textContent=data[1]}));

const heroWord=document.querySelector('#hero-word'),words=['flourish.','connect.','shine.','inspire.'];let word=0;
if(heroWord)setInterval(()=>{if(document.hidden||motionPaused())return;word=(word+1)%words.length;heroWord.textContent=words[word];animateIn(heroWord)},4200);
if('IntersectionObserver' in window&&!motionPaused()){const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('revealed');observer.unobserve(entry.target)}}),{threshold:.08});document.querySelectorAll('.cards article,.section-heading,.story>div,.curiosity>div,.steps>h2,.cta').forEach((el,i)=>{el.style.setProperty('--reveal-delay',`${i%3*70}ms`);el.classList.add('reveal-ready');observer.observe(el)})}
if(matchMedia('(hover: hover) and (pointer: fine)').matches){document.querySelectorAll('.cards article').forEach(card=>card.addEventListener('pointermove',event=>{const rect=card.getBoundingClientRect();card.style.setProperty('--spot-x',`${event.clientX-rect.left}px`);card.style.setProperty('--spot-y',`${event.clientY-rect.top}px`)}))}
