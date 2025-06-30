// Run this in browser console on dashboard page to debug history data
console.log('🔍 DEBUGGING HISTORY DATA');

// Check if history data is available in React DevTools or global scope
if (window.React) {
  console.log('React found, checking for history data...');
}

// Try to find history data in the page
const historyElements = document.querySelectorAll('[data-testid*="history"], [class*="history"]');
console.log('Found history elements:', historyElements.length);

// Check localStorage and sessionStorage
console.log('LocalStorage keys:', Object.keys(localStorage));
console.log('SessionStorage keys:', Object.keys(sessionStorage));

// Check for any global variables that might contain history
Object.keys(window).forEach(key => {
  if (key.toLowerCase().includes('history') || key.toLowerCase().includes('readme')) {
    console.log(`Found potential data in window.${key}:`, window[key]);
  }
});

console.log('🔍 Please click on Full Preview button and check the console logs');
