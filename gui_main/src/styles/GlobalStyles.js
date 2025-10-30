import { createGlobalStyle } from 'styled-components';

export const GlobalStyles = createGlobalStyle`
  :root {
    --primary-color: #2563eb;
    --primary-hover: #1d4ed8;
    --secondary-color: #6366f1;
    --accent-color: #22d3ee;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --danger-color: #ef4444;
    
    --bg-primary: #0f172a;
    --bg-secondary: #1e293b;
    --bg-tertiary: #334155;
    --bg-card: #1e293b;
    --bg-modal: rgba(15, 23, 42, 0.9);
    
    --text-primary: #f8fafc;
    --text-secondary: #cbd5e1;
    --text-muted: #64748b;
    --text-inverse: #1e293b;
    
    --border-color: #334155;
    --border-light: #475569;
    --border-focus: #2563eb;
    
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;
    --radius-xl: 16px;
    
    --font-size-xs: 0.75rem;
    --font-size-sm: 0.875rem;
    --font-size-base: 1rem;
    --font-size-lg: 1.125rem;
    --font-size-xl: 1.25rem;
    --font-size-2xl: 1.5rem;
    --font-size-3xl: 1.875rem;
    
    --spacing-1: 0.25rem;
    --spacing-2: 0.5rem;
    --spacing-3: 0.75rem;
    --spacing-4: 1rem;
    --spacing-5: 1.25rem;
    --spacing-6: 1.5rem;
    --spacing-8: 2rem;
    --spacing-10: 2.5rem;
    --spacing-12: 3rem;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  html {
    font-size: 16px;
    scroll-behavior: smooth;
  }

  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    overflow-x: hidden;
  }

  .app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  /* Scrollbar Styles */
  ::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }

  ::-webkit-scrollbar-track {
    background: var(--bg-secondary);
    border-radius: var(--radius-sm);
  }

  ::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: var(--radius-sm);
    
    &:hover {
      background: var(--border-light);
    }
  }

  /* Button Styles */
  button {
    font-family: inherit;
    cursor: pointer;
    border: none;
    outline: none;
    background: none;
    color: inherit;
  }

  /* Input Styles */
  input, textarea {
    font-family: inherit;
    outline: none;
    border: none;
    background: transparent;
    color: inherit;
  }

  /* Link Styles */
  a {
    color: inherit;
    text-decoration: none;
  }

  /* Selection */
  ::selection {
    background: var(--primary-color);
    color: white;
  }

  /* Focus styles */
  *:focus-visible {
    outline: 2px solid var(--border-focus);
    outline-offset: 2px;
  }

  /* Utility Classes */
  .flex {
    display: flex;
  }

  .flex-col {
    flex-direction: column;
  }

  .items-center {
    align-items: center;
  }

  .justify-center {
    justify-content: center;
  }

  .justify-between {
    justify-content: space-between;
  }

  .text-center {
    text-align: center;
  }

  .text-sm {
    font-size: var(--font-size-sm);
  }

  .text-lg {
    font-size: var(--font-size-lg);
  }

  .font-medium {
    font-weight: 500;
  }

  .font-semibold {
    font-weight: 600;
  }

  .font-bold {
    font-weight: 700;
  }

  .opacity-50 {
    opacity: 0.5;
  }

  .opacity-75 {
    opacity: 0.75;
  }

  .cursor-pointer {
    cursor: pointer;
  }

  .select-none {
    user-select: none;
  }

  /* Animation utilities */
  .transition {
    transition: all 0.15s ease-in-out;
  }

  .transition-colors {
    transition: background-color 0.15s ease-in-out, color 0.15s ease-in-out;
  }

  .transition-transform {
    transition: transform 0.15s ease-in-out;
  }

  .hover\\:scale-105:hover {
    transform: scale(1.05);
  }

  .hover\\:opacity-80:hover {
    opacity: 0.8;
  }
`;
