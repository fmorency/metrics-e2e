// Get the color from CSS variable
// The variable should be formatted as --variable-name. Example: --color-tertiary-500
export function getColorFromCSS(variable: string, fallback?: string) {
  let themeColor = fallback ? fallback : '#E5703D';

  if (typeof window !== 'undefined') {
    const color = getComputedStyle(document.documentElement)
      .getPropertyValue(variable).trim();
    if (color) themeColor = color;
  }

  return themeColor
}