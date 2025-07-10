import { format, startOfMonth, endOfMonth } from 'date-fns';

/**
 * Create the calendar grid
 * @returns {Array} rows
 */
export function initRows(): number[][] {
	return [
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0]
	];
}

export function fullMonthYear(month: number, year: number): string {
	// pad the month with a zero if it's less than 10
	const monthStr = month.toString().padStart(2, '0');

	const date = format(new Date(`${year}-${monthStr}-01T12:00:00`), 'MMMM yyyy');

	return date.charAt(0).toUpperCase() + date.slice(1);
}

/**
 * Return an array of days
 * @returns {Array} days
 */
export function arrDays(): string[] {
	return ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'];
}

/**
 * Return an calendary month
 * @returns {Array} months
 */
export function updateRows(month: number, year: number): number[][] {
	const rows = initRows();
	// pad the month with a zero if it's less than 10
	const monthStr = month.toString().padStart(2, '0');

	const firstDayOfCurrentMonth = format(
		startOfMonth(new Date(`${year}-${monthStr}-01T12:00:00`)),
		'EEEEEE'
	);

	const lastDayOfCurrentMonth = +format(
		endOfMonth(new Date(`${year}-${monthStr}-01T12:00:00`)),
		'd'
	);

	let row: number = 0; // week
	let col: number = 0; // day of the week
	let start: boolean = false;
	let i: number = 0;

	for (row = 0; row < 6; row++) {
		arrDays().forEach((daystr: string) => {
			if (i > lastDayOfCurrentMonth) {
				return;
			}

			if (!start && daystr === firstDayOfCurrentMonth) {
				i++;
				start = true;
			}

			rows[row][col] = i;
			col++;

			if (start) {
				i++;
			}
		});
		col = 0;
	}

	return rows;
}
