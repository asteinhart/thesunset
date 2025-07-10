import { writable } from 'svelte/store';

export const currentDate = writable(new Date());

export const scores = writable([]);
