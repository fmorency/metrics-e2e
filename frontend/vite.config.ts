import tailwindcss from '@tailwindcss/vite';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [tailwindcss(), sveltekit()],
	ssr: {
			noExternal: process.env.NODE_ENV === 'production' ? ['@carbon/charts'] : []
	},
	server: {
    proxy: {
      '/rpc': 'http://localhost:3000'
    }
  }
});
