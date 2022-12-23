import '../css/index.css';
import '../img/hero.jpg';
import '../img/OpenDebatesDark.svg';
import VanillaTilt from 'vanilla-tilt';
import Typed from 'typed.js';
import 'vite/modulepreload-polyfill';

const element = document.querySelector(".js-tilt");
// @ts-ignore
VanillaTilt.init(element);

var options = {
    strings: [
        'Semantic Wiki',
        'Semantic Treebanks',
        "Semantic Debates"
    ],
    typeSpeed: 40,
    loop: true
};
new Typed('#semantic-text', options);
