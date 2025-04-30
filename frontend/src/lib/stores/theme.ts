import { writable } from 'svelte/store';

const initial = (typeof window !== 'undefined' && window.localStorage.getItem('mode')) || 'light';
export const mode = writable(initial);

mode.subscribe((value) => {
    if (typeof window !== 'undefined') {
        document.documentElement.setAttribute('data-mode', value);
        window.localStorage.setItem('mode', value);
    }
});