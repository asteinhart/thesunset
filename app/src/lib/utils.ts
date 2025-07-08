// place files you want to import through the `$lib` alias in this folder.

const s3Prefix = 'https://thesunset.s3.amazonaws.com';

export function getSunsetImage(date: string): string {
	const path = `${s3Prefix}/${date.substring(0, 4)}-${date.substring(5, 7)}-${date.substring(8, 10)}/best_sunset.jpg`;
	return path;
}

export function formatDate(date: Date | string): string {
	// Convert string to Date if necessary
	if (typeof date === 'string') {
		date = new Date(date);
	}
	const year = date.getFullYear();
	const month = (date.getMonth() + 1).toString().padStart(2, '0');
	const day = date.getDate().toString().padStart(2, '0');
	return `${year}-${month}-${day}`;
}
