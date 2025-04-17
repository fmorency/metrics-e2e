import { browser } from '$app/environment';
import { readable, writable, derived, type Readable } from 'svelte/store';

type ThemePreference = 'light' | 'dark' | 'system';
type AppliedTheme    = 'light' | 'dark';

// Returns the system theme based on the user's OS/browser settings
const getSystemTheme = (): AppliedTheme =>
  browser && window.matchMedia('(prefers-color-scheme: dark)').matches
    ? 'dark'
    : 'light';

// Emits on every change to the OS/Browser setting:
export const systemTheme: Readable<AppliedTheme> = readable<AppliedTheme>(
  getSystemTheme(),
  (set) => {
    if (!browser) return;
    const mql = window.matchMedia('(prefers-color-scheme: dark)');
    const listener = (e: MediaQueryListEvent) => set(e.matches ? 'dark' : 'light');
    mql.addEventListener('change', listener);
    return () => mql.removeEventListener('change', listener);
  }
);

// The user’s preference
export const themePreference = writable<ThemePreference>(
  (browser && localStorage.getItem('theme') as ThemePreference) || 'system'
);

// The actual theme to apply
export const theme = derived(
  [themePreference, systemTheme],
  ([$preference, $system]) =>
    $preference === 'system' ? $system : $preference
);

if (browser) {
  theme.subscribe((applied) => {
    document.documentElement.classList.toggle('dark', applied === 'dark');
  });

  themePreference.subscribe((pref) => {
    localStorage.setItem('theme', pref);
  });
}
