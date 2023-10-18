/** @type {import('tailwindcss').Config} */
module.exports = {
	darkMode: "class",
	content: ["./templates/*.{html,js}", "./templates/*/*.html"],
	theme: {
		extend: {},
	},
	plugins: [require("flowbite/plugin")],
};
